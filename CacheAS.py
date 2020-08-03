from typing import Any, Dict, Iterable, Mapping, Optional, Type, Union

from caches import Cache
from caches.types import Serializable, Version


class CacheAS(Cache):
     def __init__(
            self,
            url: Union[str, "CacheURL"],
            *,
            ttl: Optional[int] = None,
            version: Optional[Version] = None,
            key_prefix: str = "",
            **options: Any
        ):
         self.SUPPORTED_BACKENDS["aerospike"] = "offerBuilderGrpc.caching.backends.aerospike:AeroSpikeBackend"
         return super(CacheAS, self).__init__(url, ttl=ttl, version=version, key_prefix=key_prefix, **options)
