# -*- coding: utf-8 -*-
from macumba_pass.clients import get_aws_client


def test_create_password():
    ("S3 service should work")

    s3 = get_aws_client('s3')

    s3.list_buckets().should.have.key('Buckets').being.a(list)
