# -*- coding: utf-8 -*-
import json
from macumba_pass.clients import MacumbaPassAPIClient


PROD_BASE_URL = 'https://kxjxyfnwo5.execute-api.us-east-1.amazonaws.com/Prod/'
STAGE_BASE_URL = 'https://kxjxyfnwo5.execute-api.us-east-1.amazonaws.com/Stage/'

prod = MacumbaPassAPIClient(PROD_BASE_URL)
stage = MacumbaPassAPIClient(STAGE_BASE_URL)
local = MacumbaPassAPIClient()


for client in [prod]:
    index = client.get('/', json=True)
    stored = client.post('/api/v1/secret', json=True, body={
        'label': 'my-secret',
        'password': '1234',
    })
    retrieved = client.get('/api/v1/secret?label=my-secret', json=True)

    for response in (index, stored, retrieved):
        status = response.pop('status_code', None)
        url = response.pop('url')
        method = response.pop('method')
        body = response.pop('body')
        data = None
        try:
            response['body'] = json.loads(body)
        except ValueError:
            response['body'] = body

        print("\033[1;33m<{}>\033[0m".format(" ".join([method.upper(), url, str(status)])))
        if status != 200:
            print("\033[1;31m{}\033[0m".format(json.dumps(response, indent=2)))
        else:
            print("\033[1;32m{}\033[0m".format(json.dumps(response, indent=2)))
        print("\033[1;33m</{}>\033[0m".format(" ".join([method.upper(), url, str(status)])))
