# -*- coding: utf-8 -*-
from macumba_pass.clients import get_aws_client
from .scenarios import with_localstack


@with_localstack('s3')
def test_create_password(context):
    ("S3 service should work")

    s3 = get_aws_client('s3')

    s3.create_bucket(Bucket='test')
    response = s3.list_buckets()

    buckets = response['Buckets']
    bucket = buckets[0]
    bucket.should.have.key('Name').being.equal('macumba-secrets')


    objects = s3.list_objects(Bucket='macumba-secrets')['Contents']
    [s3.delete_object(Key=o['Key'], Bucket='macumba-secrets') for o in objects]
    s3.delete_bucket(Bucket=bucket['Name'])
