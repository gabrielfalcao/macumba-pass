# -*- coding: utf-8 -*-
import os
from macumba_pass.clients import get_aws_client


class PasswordKeyStore(object):
    def __init__(self, s3_client=None):
        self.s3 = s3_client or get_aws_client('s3')
        self.bucket_name = os.getenv('MACUMBA_BUCKET_NAME')

    def list_buckets(self):
        response = self.s3.list_buckets()
        buckets = response['Buckets']
        return buckets

    def get_bucket(self):
        for bucket in self.list_buckets():
            if bucket['Name'] == self.bucket_name:
                return bucket

    def create_bucket(self):
        bucket = self.get_bucket()
        if not bucket:
            bucket = self.s3.create_bucket(Bucket=self.bucket_name)

        return bucket
