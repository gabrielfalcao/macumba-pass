# -*- coding: utf-8 -*-
from macumba_pass.clients import get_aws_client


class PasswordKeyStore(object):
    def __init__(self, s3_client=None):
        self.s3 = s3_client or get_aws_client('s3')

    def list_buckets(self):
        response = self.s3.list_buckets()
        buckets = response['Buckets']
        return buckets

    def get_bucket(self, name):
        for bucket in self.list_buckets():
            if bucket['Name'] == name:
                return bucket

    def get_or_create_bucket(self, name):
        bucket = self.get_bucket(name)
        if not bucket:
            bucket = self.s3.create_bucket(Bucket=name)

        return bucket
