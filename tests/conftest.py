import pytest

from ..CacheAS import CacheAS
from ..settings import CACHE_CONNECT


@pytest.fixture()
async def resource():
    client = CacheAS(CACHE_CONNECT)
    await client.connect()
    yield client
    await client.delete_many(['all_build_3', 'not_int_value_key'])
    await client.disconnect()
