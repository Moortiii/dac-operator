from typing import Type, TypeVar

import kubernetes.client
import kubernetes.client.exceptions
from loguru import logger as default_loguru_logger
from pydantic import TypeAdapter, ValidationError

from dac_operator.ext import kubernetes_exceptions, kubernetes_models

T = TypeVar("T")


class KubernetesClient:
    """
    Simple wrapper around the native Kubernetes python-bindings to perform common tasks
    such as result conversion and error handling. Provides a simpler interface for
    developers since only a fraction of the functionality offered by the kubernetes
    package is ever used or needed.
    """

    def __init__(
        self,
        custom_objects_api: kubernetes.client.CustomObjectsApi,
        core_api: kubernetes.client.CoreV1Api,
        logger=default_loguru_logger,
    ):
        self._custom_objects_api = custom_objects_api
        self._core_api = core_api
        self._logger = logger

    def get_secret(self, name: str, namespace: str) -> dict:
        try:
            secret = self._core_api.read_namespaced_secret(name=name, namespace=namespace)
        except kubernetes.client.exceptions.ApiException:
            self._logger.error(
                f"Secret '{name}' does not exist in namespace '{namespace}'."
            )
            raise kubernetes_exceptions.ResourceNotFoundException
        
        return secret.data

    def get_config_map(self, name: str, namespace: str) -> kubernetes_models.ConfigMap:
        try:
            configmap = self._core_api.read_namespaced_config_map(
                name=name, namespace=namespace
            )
        except kubernetes.client.exceptions.ApiException:
            self._logger.error(
                f"Config map '{name}' does not exist for namespace '{namespace}'."
            )
            raise kubernetes_exceptions.ResourceNotFoundException

        configmap = kubernetes_models.ConfigMap.model_validate(
            configmap, from_attributes=True
        )

        return configmap

    def get_namespaced_custom_object(
        self,
        name: str,
        group: str,
        version: str,
        plural: str,
        namespace: str,
        return_type: Type[T],
    ) -> T:
        """
        Get a namespaced custom object and coerce the result to the chosen return type.

        Args:
            name: The name of the object to read

            group(str): The Kubernetes group, e.g. buildrlabs.io

            version(str): The API version for the resource, e.g. v1

            plural(str): The name of the CRD, e.g. microsoftsentinelanalyticrules

            namespace(str): The namespace the object belongs to

            return_type(Type[T]): The type to coerce the result to, typically a Pydantic
                model, but primitives are also supported. Raises a ResourceValidationError
                if the type conversion is not possible.

        Raises:
            ResourceValidationError: If it is not possible to convert the result
                to the requested type.
        """  # noqa: E501
        try:
            result = self._custom_objects_api.get_namespaced_custom_object(
                group=group,
                version=version,
                namespace=namespace,
                plural=plural,
                name=name,
            )
        except kubernetes.client.exceptions.ApiException as err:
            self._logger.exception(err)
            self._logger.error(f"Config map '{name}' does not exist!")
            raise kubernetes_exceptions.ResourceNotFoundException

        try:
            return TypeAdapter(return_type).validate_python(
                result, from_attributes=True
            )
        except ValidationError as err:
            self._logger.exception(err)
            self._logger.error(
                f"Unable to convert result for '{group}.{plural}.{version}.{name}' "
                f"into an object of type {return_type}: {err}"
            )
            raise kubernetes_exceptions.ResourceValidationError
