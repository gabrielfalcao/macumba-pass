# -*- coding: utf-8 -*-
from sure import scenario
from localstack.services import infra

from macumba_pass.web import application


def create_test_client(context):
    context.http = application.test_client()


def with_localstack(*apis, **kw):
    auto_stop = kw.get('auto_stop', False)

    def start_localstack(context):
        context.infra = infra
        infra.start_infra(async=True, apis=apis)

    def stop_localstack(context):
        if auto_stop:
            context.infra.stop_infra()

    return scenario([start_localstack, create_test_client], stop_localstack)


with_chalice_client = scenario(create_test_client)
