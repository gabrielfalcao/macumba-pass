# -*- coding: utf-8 -*-
from macumba_pass.web.helpers import PasswordKeyStore

from .scenarios import with_localstack


@with_localstack('s3')
def test_persist_secret(context):
    ("PasswordKeyStore().persist_secret() should list my buckets")

    store = PasswordKeyStore()
    created = store.persist_secret('some secret', {'password': 'some password'})

    store.retrieve_secret('some-secret').should.equal(created)
