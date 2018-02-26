# -*- coding: utf-8 -*-
from macumba_pass.web.helpers import PasswordKeyStore

from .scenarios import with_localstack


@with_localstack('s3')
def test_list_buckets(context):
    ("PasswordKeyStore().list_buckets() should list my buckets")

    store = PasswordKeyStore()
    b1 = store.get_bucket()

    store.list_buckets().should.equal([b1])
