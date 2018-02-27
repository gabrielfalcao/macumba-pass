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
        print(json.dumps(response, indent=2))
