allow_k8s_contexts("minikube")

docker_build(ref="buildrlabs/dac-operator", context="./python", dockerfile="./python/Dockerfile")

k8s_yaml(encode_yaml({
    "apiVersion": "v1",
    "kind": "Namespace",
    "metadata": {
        "name": "dac-system"
    }
}))

k8s_yaml(
    helm(
        './chart',
        values=["./chart/values.yaml"],
        namespace="dac-system",
    )
)