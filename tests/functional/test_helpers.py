# -*- coding: utf-8 -*-
from macumba_pass.web.helpers import PasswordKeyStore


def test_list_buckets():
    ("PasswordKeyStore().list_buckets() should list my buckets")

    store = PasswordKeyStore()
    b1 = store.get_or_create_bucket('macumba-secrets')
    b2 = store.get_or_create_bucket('test')

    store.list_buckets().should.equal([b1, b2])
