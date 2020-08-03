"""
settings.py
====================================
Файл настроики для кеширования результатов
"""

import os

CACHE_CONNECT = "aerospike://{}:{}/{}?set_name={}".format(os.environ.get('AEROSPIKE_HOST', 'aerospike'),
                                                         os.environ.get('AEROSPIKE_PORT', 3000),
                                                         os.environ.get('AEROSPIKE_NAMESPACE', 'test'),
                                                         os.environ.get('AEROSPIKE_SET', 'demo')
                                                         )
TEMPLATE_MAKE_KEY = 'cache.{!s}.{!s}'
