# -*- coding: utf-8 -*-
import os
import json
import boto3

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
