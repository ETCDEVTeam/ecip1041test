#!/usr/bin/env python

# pip install kubernetes

import json
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint

all_nodes = ["g1", "g2", "gm1"]

def rpc_payload(method, params):
    payload = {
        "jsonrpc":"2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    #s = json.dumps(payload)
    #print("Json: %s" % s)
    return payload

def get_height(node_id):
    return rpc_call(node_id, "eth_blockNumber", [])

def get_hash(node_id, height):
    return rpc_call(node_id, "eth_getBlockByNumber", [height, False])

def rpc_call(pod_id, method, params):
    config.load_kube_config()
    api = client.CoreV1Api()
    resource_path = '/api/v1/namespaces/{namespace}/pods/{name}/proxy'.replace('{format}', 'json')
    collection_formats = {}
    path_params = {}
    path_params['name'] = pod_id
    path_params['namespace'] = "default"
    query_params = {}
    query_params['path'] = ":8545"
    header_params = {}
    header_params['Accept'] = api.api_client.select_header_accept(['*/*'])
    header_params['Content-Type'] = api.api_client.select_header_content_type(['*/*'])
    body_params = rpc_payload(method, params)
    auth_settings = ['BearerToken']
    form_params = []
    local_var_files = {}
    try:
        api_response = api.api_client.call_api(resource_path, 'POST',
                                 path_params,
                                 query_params,
                                 header_params,
                                 body=body_params,
                                 post_params=form_params,
                                 files=local_var_files,
                                 response_type="object",
                                 auth_settings=auth_settings,
                                 collection_formats=collection_formats)
        x = api_response[0]
        #pprint(x)
        return x["result"]
    except ApiException as e:
        print("Exception when calling CoreV1Api: %s\n" % e)

def list():
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Nodes status")
    print("%s\t\t\t%s\t%s" % ("ID", "HEIGHT", "HASH"))
    ret = v1.list_namespaced_pod("default", watch=False)
    for i in ret.items:
        pod_id = i.metadata.name
        height = get_height(pod_id)
        hash = get_hash(pod_id, height)["hash"]
        print("%s\t%s\t%s" % (pod_id, int(height, 16), hash))


if __name__ == "__main__":
    list()
