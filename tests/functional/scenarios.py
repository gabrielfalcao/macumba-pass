# -*- coding: utf-8 -*-
from sure import scenario
from localstack.services import infra
from macumba_pass.clients import get_aws_client

from macumba_pass.web import application


def cleanup_s3():
    s3 = get_aws_client('s3')
    response = s3.list_buckets()
    buckets = response['Buckets']

    list_objects_from_bucket = lambda b: s3.list_objects(Bucket=b['Name']).get('Contents', [])
    delete_objects_from_bucket = lambda b: [s3.delete_object(Key=o['Key'], Bucket=b['Name']) for o in list_objects_from_bucket(b)]
    [delete_objects_from_bucket(b) for b in buckets]
    [s3.delete_bucket(Bucket=b['Name']) for b in buckets]


def create_test_client(context):
    context.http = application.test_client()


def with_localstack(*apis, **kw):
    auto_start = kw.get('auto_start', False)
    auto_stop = kw.get('auto_stop', False)

    def start_localstack(context):
        cleanup_s3()
        context.infra = infra
        if auto_start:
            infra.start_infra(async=True, apis=apis)

    def stop_localstack(context):
        cleanup_s3()
        if auto_stop:
            context.infra.stop_infra()

    return scenario([start_localstack, create_test_client], stop_localstack)


with_chalice_client = scenario(create_test_client)
