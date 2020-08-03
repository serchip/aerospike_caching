#!/usr/bin/python

import pytest


@pytest.mark.asyncio
async def test_make_key():
    from ..utils import make_key
    key = await make_key('buildImg', [1,'test', 4], {'k1': 5, 'k2': {'t': 't3'}, 'k3': [6,4], 'k4': 'string'})
    assert key == "cache.buildImg.c69519c733a3bffc42e3ecbc8481f031"
