# -*- coding: utf-8 -*-
import os
import re

from macumba_pass.clients import get_aws_client
from macumba_pass.web.framework.serializers import json


def slugify(string, repchar='-'):
    return re.sub(r'[^\w_/-]+', repchar, string)


class S3Helper(object):
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

    def put_object(self, name, data, acl='private'):
        self.create_bucket()
        response = self.s3.put_object(
            Key=name,
            Bucket=self.bucket_name,
            Body=data,
            ACL=acl,
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code is 200:
            return self.get_object(name)

        return {}

    def get_object(self, name):
        response = self.s3.get_object(
            Key=name,
            Bucket=self.bucket_name,
        )

        return response


class PasswordKeyStore(object):
    def __init__(self, s3_client=None):
        self.s3 = S3Helper(s3_client)

    def persist_secret(self, label, value):
        label = slugify(label)
        self.s3.put_object(label, json.dumps(value))
        return self.retrieve_secret(label)

    def retrieve_secret(self, label):
        label = slugify(label)
        obj = self.s3.get_object(label)
        body = obj['Body']
        value = body.read()
        result = {
            'label': label,
            'value': json.loads(value),
        }
        return result
