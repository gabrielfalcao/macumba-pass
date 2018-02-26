# -*- coding: utf-8 -*-
import os
import json
import boto3
import requests
import urllib
import json as json_module
from botocore.utils import fix_s3_host
from localstack.constants import DEFAULT_SERVICE_PORTS


def get_localstack_endpoint_url_for_service(service_name):
    port = DEFAULT_SERVICE_PORTS.get(service_name)
    if not port:
        raise RuntimeError('cannot localstack port mapped to service: {}'.format(service_name))

    return 'http://localhost:{}/'.format(port)


def get_boto_session():
    PROFILE_NAME = os.getenv('profile_name', 'personal')
    session = boto3.Session(profile_name=PROFILE_NAME)
    return session


def is_running_local():
    enabled = os.getenv('LOCALSTACK_ENABLED')  # must equal `true` (lowercase)
    return enabled and json.loads(enabled) is True


def get_aws_client(service_name, session=None):
    session = session or get_boto_session()
    params = {}

    if is_running_local():
        params['use_ssl'] = False
        params['endpoint_url'] = get_localstack_endpoint_url_for_service(service_name)

    service = session.client(
        service_name,
        **params
    )
    service.meta.events.unregister('before-sign.s3', fix_s3_host)

    return service


class MacumbaPassAPIClient(object):
    """A python-client for MacumbaPass RESTful API"""

    PROD_BASE_URL = 'https://kxjxyfnwo5.execute-api.us-east-1.amazonaws.com/Prod/'
    LOCAL_BASE_URL = 'http://localhost:3000/'

    def __init__(self, base_url=None):
        self.base_url = base_url or self.default_base_url
        self.http = requests.Session()

    @property
    def default_base_url(self):
        if is_running_local():
            return self.LOCAL_BASE_URL
        else:
            return self.PROD_BASE_URL

    def build_full_url(self, path):
        return urllib.parse.urljoin(self.base_url.rstrip('/'), path)

    def request(self, method, path, body=None, headers=(), json=False):
        headers = headers and dict(headers) or {}
        if json:
            headers['Content-Type'] = 'application/json'
            if body is not None:
                body = json_module.dumps(body)

        return self.http.request(method, self.build_full_url(path), data=body, headers=headers).json()

    def __getattr__(self, attr):
        if attr.upper() in ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'):
            return lambda *args, **kw: self.request(attr.lower(), *args, **kw)
        return object.__getattribute__(self, attr)
