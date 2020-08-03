import json
from typing import Any, Dict, Iterable, Mapping, Optional, Union

from caches.types import Serializable
from caches.core import CacheURL
from caches.backends.base import BaseBackend

from aioaerospike.client import AerospikeClient


class AeroSpikeBackend(BaseBackend):

    def __init__(self, cache_url: Union[CacheURL, str], **options: Any) -> None:
        self._cache_url = CacheURL(cache_url)
        self._options = options
        self._pool = None
        self.namespace = 'default'
        self.set_name = 'default'


    async def connect(self):
        # pylint: disable=attribute-defined-outside-init
        assert self._pool is None, "Cache backend is already running"

        self._pool = AerospikeClient(self._cache_url.hostname, self._cache_url.components.username, self._cache_url.components.password, port=self._cache_url.port)
        if self._cache_url.database:
            self.namespace = self._cache_url.database
        if 'set_name' in self._cache_url.options.keys():
            self.set_name = self._cache_url.options['set_name']
        await self._pool.connect()

    async def disconnect(self):
        assert self._pool is not None, "Cache backend is not running"
        self._pool._writer.close()
        await self._pool._writer.wait_closed()

    async def get(self, key: str, default: Any = None) -> Any:
        value = await self._pool.get_key(self.namespace, self.set_name, key)
        return value if value not in [None, {}] else default

    async def set(self, key: str, value: Serializable, *, ttl: Optional[int] = None) -> Any:
        if type(value) != dict:
            value = {'data': value}
        if ttl is None:
            await self._pool.put_key(self.namespace, self.set_name, key, value)
        elif ttl:
            await self._pool.put_key(self.namespace, self.set_name, key, value, ttl=ttl)


    async def add(self, key: str, value: Serializable, *, ttl: Optional[int]):
        return await self.set(key, value, ttl=ttl)

    async def delete(self, key: str):
        await self._pool.delete_key(self.namespace, self.set_name, key)

    async def touch(self, key: str, ttl: Optional[int] = None) -> bool:
            return await self._pool.key_exists(self.namespace, self.set_name, key)

    async def get_or_set(self, key: str, default: Serializable, *, ttl: Optional[int]) -> Any:
        value = await self.get(key, None)
        if value in [{}, None]:
            await self.set(key, default, ttl=ttl)
            return default
        return value

    async def get_many(self, keys: Iterable[str]) -> Dict[str, Any]:
        result_dict = dict()
        for key in keys:
            result_dict[key] = await self.get(key)
        return result_dict

    async def set_many(
        self, mapping: Mapping[str, Serializable], *, ttl: Optional[int]
    ):
        if ttl is None or ttl:
            for key, value in mapping.items():
                await self.set(key, value, ttl=ttl)

    async def delete_many(self, keys: Iterable[str]):
        for key in keys:
            if await self.touch(key):
                await self.delete(key)

    async def clear(self):
        NotImplemented('Pleese Implemented method clear')

    async def incr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        if not await self.touch(key):
            raise ValueError(f"'{key}' is not set in the cache")

        value = await self.get(key)
        if 'data' not in value.keys():
            raise ValueError("Not send initial 'data' from value")

        if type(delta) in [int, float]:
            res  = value['data'] + delta
            await self.set(key, res)
            return res
        raise ValueError("incr value must be int or float")

    async def decr(self, key: str, delta: Union[float, int]) -> Union[float, int]:
        if not await self.touch(key):
            raise ValueError(f"'{key}' is not set in the cache")

        value = await self.get(key)
        if 'data' not in value.keys():
            raise ValueError("Not send initial 'data' from value")

        if type(delta) in [int, float]:
            res  = value['data'] - delta
            await self.set(key, res)
            return res
        raise ValueError("incr value must be int or float")
