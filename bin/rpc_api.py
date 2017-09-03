from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint


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

class RpcApi:

    def __init__(self):
        config.load_kube_config()

    def get_height(self, node_id):
        return self.rpc_call(node_id, "eth_blockNumber", [])

    def get_peers(self, node_id):
        return self.rpc_call(node_id, "net_peerCount", [])

    def get_block(self, node_id, num):
        if type(num) is int:
            num=hex(num)
        return self.rpc_call(node_id, "eth_getBlockByNumber", [num, False])

    def get_uncles(self, node_id, block):
        uncles = range(0, len(block["uncles"]))
        num = block["number"]
        return [(num, self.rpc_call(node_id, "eth_getUncleByBlockNumberAndIndex", [num, hex(i)])) for i in uncles]

    def rpc_call(self, pod_id, method, params):
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
            if not x.has_key("result"):
                pprint(x)
            return x["result"]
        except ApiException as e:
            print("Exception when calling CoreV1Api: %s\n" % e)

    def get_nodes(self):
        api = client.CoreV1Api()
        ret = api.list_namespaced_pod("default", watch=False)
        return [i.metadata.name for i in ret.items]