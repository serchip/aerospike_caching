"""
utils.py
====================================
Файл с доп. функциями
"""

import hashlib
from urllib.parse import quote

from .settings import TEMPLATE_MAKE_KEY


async def make_key(fragment_name, *args, **kwargs):
    vary_on = []
    if args or kwargs:
        vary_on.extend(args)
        vary_on.extend(tuple([(k, hash(v)) for k, v in kwargs.items()]))
    key = ':'.join(quote(str(var)) for var in vary_on)
    args = hashlib.md5(key.encode())
    return TEMPLATE_MAKE_KEY.format(fragment_name, args.hexdigest())
