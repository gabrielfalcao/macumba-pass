# -*- coding: utf-8 -*-

from macumba_pass.clients import MacumbaPassAPIClient


prod = MacumbaPassAPIClient(MacumbaPassAPIClient.PROD_BASE_URL)
local = MacumbaPassAPIClient(MacumbaPassAPIClient.LOCAL_BASE_URL)


for client in [prod, local]:
    index = client.get('/', json=True)
    stored = client.post('/api/v1/secret', json=True, body={
        'label': 'my-secret',
        'password': '1234',
    })
    retrieved = client.get('/api/v1/secret/my-secret', json=True)

    index.should.equal({
        'message': 'hello world'
    })
    retrieved.should.equal({
        'label': 'my-secret',
        'value': {
            'password': '1234',
        }
    })
    stored.should.equal({
        'label': 'my-secret',
        'value': {
            'password': '1234',
        }
    })
