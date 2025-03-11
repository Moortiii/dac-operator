# Splunk

This document contains (temporary) information about how to use the Splunk REST API to upload content

## Create an app using the REST API:

bash curl -k -u admin:ThisIsAPassword \ -X POST https://localhost:8089/services/apps/local \ --data "name=my_custom_app" \ --data "label=My Custom App" \ --data "template=barebones" \ --data "visible=true"

## Creating a saved search using the API:

bash curl https://localhost:8089/services/saved/searches -k -u admin:ThisIsAPassword -d name="My first search" --data-urlencode description="This is the description" --data-urlencode search="index=devtutorial | top limit=20 REPLACEMENT_COST"

## Create a macro using the API:

bash curl -k -u admin:ThisIsAPassword -X POST https://localhost:8089/servicesNS/admin/search/admin/macros --data "name=my_macro(1)" --data "definition=source=\* | stats count" --data "args=count"

## Edit permissions for a macro using the API:

bash curl -k -u admin:ThisIsAPassword -X POST "https://localhost:8089/servicesNS/admin/search/admin/macros/my_macro(1)/acl" --data "sharing=global" --data "perms.read=\*" --data "perms.write=admin" --data "output_mode=json" --data "owner=admin"

## Create a lookup using the API:

bash curl -k -u admin:ThisIsAPassword \ -X POST https://localhost:8089/servicesNS/admin/search/storage/collections/config/my_kv_lookup \ --header "Content-Type: application/json" \ --data '{ "field1": "string", "field2": "number", "field3": "boolean" }'

## Insert data into a lookup using the API:

bash curl -k -u admin:ThisIsAPassword \ -X POST https://localhost:8089/servicesNS/admin/search/storage/collections/data/my_kv_lookup \ --header "Content-Type: application/json" \ --data '{ "field1": "example_value", "field2": 123, "field3": true }'
