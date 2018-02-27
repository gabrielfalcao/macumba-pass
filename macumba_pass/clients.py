# -*- coding: utf-8 -*-
import os
import sys
import json
import boto3
import requests
import logging
import json as json_module

from botocore.utils import fix_s3_host
from localstack.constants import DEFAULT_SERVICE_PORTS


logger = logging.getLogger('macumba_pass')


def get_localstack_endpoint_url_for_service(service_name):
    port = DEFAULT_SERVICE_PORTS.get(service_name)
    if not port:
        raise RuntimeError('cannot localstack port mapped to service: {}'.format(service_name))

    return 'http://localhost:{}/'.format(port)


def get_boto_session():
    session = boto3.Session()
    return session


def is_running_local():
    enabled = os.getenv('LOCALSTACK_ENABLED')  # must equal `true` (lowercase)
    return enabled and (json.loads(enabled) is True or sys.platform in ('darwin', ))


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

    LOCAL_BASE_URL = 'http://localhost:3000/'

    def __init__(self, base_url=None):
        self.base_url = base_url or self.default_base_url
        self.http = requests.Session()

    @property
    def default_base_url(self):
        return self.LOCAL_BASE_URL

    def build_full_url(self, path):
        return '/'.join([self.base_url.strip('/'), path.strip('/')])

    def request(self, method, path, body=None, headers=(), json=False):
        headers = headers and dict(headers) or {}
        if json:
            headers['Content-Type'] = 'application/json'
            if body is not None:
                body = json_module.dumps(body)

        url = self.build_full_url(path)
        try:
            response = self.http.request(method, url, data=body, headers=headers)
        except Exception:
            logger.exception('MacumbaPassAPIClient failed to request {method} {ur}'.format(**locals()))
            return {}

        if json:
            return {'headers': dict(response.headers), 'status_code': response.status_code, 'body': response.text, 'url': url, 'method': method.upper()}

        return response

    def __getattr__(self, attr):
        if attr.upper() in ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'):
            return lambda *args, **kw: self.request(attr.lower(), *args, **kw)
        return object.__getattribute__(self, attr)
