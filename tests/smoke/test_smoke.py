import requests


response = requests.get('http://localhost:3000')
response.json().should.equal({
    'message': 'hello world'
})
