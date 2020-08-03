#!/usr/bin/python

import pytest


@pytest.mark.asyncio
async def test_set_get(resource):
    client = resource
    await client.set("all_build", {"test_bin_name": "test_value"})
    result = await client.get("all_build")
    assert result['test_bin_name'] == "test_value"

    await client.set("key_str_value", "test_string_value")
    result = await client.get("key_str_value")
    assert result['data'] == "test_string_value"

    result = await client.get("not_key", {})
    assert result == {}


@pytest.mark.asyncio
async def test_add(resource):
    client = resource
    await client.add("all_build_add", {"test_bin_name": "test_value"})
    result = await client.get("all_build_add")
    assert result['test_bin_name'] == "test_value"


@pytest.mark.asyncio
async def test_delete_and_touch(resource):
    client = resource
    await client.set("all_build", {"test_bin_name": "test_value"})
    await client.set("key_str_value", "test_string_value")

    result = await client.touch("all_build")
    assert result == True
    result = await client.touch("key_str_value")
    assert result == True
    #------delete------
    await client.delete("all_build_add")
    await client.delete("all_build")
    result = await client.touch("all_build")
    assert result == False
    result = await client.touch("key_str_value")
    assert result == True

@pytest.mark.asyncio
async def test_get_or_set(resource):
    client = resource
    result = await client.get("all_build_3")
    assert result == None
    result = await client.get_or_set("all_build_3", {"test_bin_name": "test_value"})
    assert result == {"test_bin_name": "test_value"}

    await client.get_or_set("all_build_3", {"new_test_key": "new_test_value"})
    assert result == {"test_bin_name": "test_value"}

@pytest.mark.asyncio
async def test_get_many_set_many_delete_many(resource):
    client = resource
    await client.set_many({"key_1": {"test_key_1": "test_value_1"},
                                    "key_2": 'string_value_2',
                                    "Key_3": {"test_key_3": "test_value_3"}
                                    })
    result = await client.get_many(["key_1", "key_2"])
    assert result['key_1'] == {"test_key_1": "test_value_1"}
    assert result['key_2'] == {"data": "string_value_2"}
    assert result.get('key_3') == None

    await client.delete_many(["key_1", "key_3"])
    result = await client.get_many(["key_1", "key_2", "key_3"])
    assert result.get('key_1') == None
    assert result.get('key_2') == {"data": "string_value_2"}
    assert result.get('key_3') == None

@pytest.mark.asyncio
async def test_incr_decr(resource):
    client = resource
    try:
        result = await client.incr('dos_not_key')
    except ValueError as e:
        assert str(e) == "'::dos_not_key' is not set in the cache"
    try:
        await client.set('not_int_or_float_value_key', {'test_key': 'test_value'})
        result = await client.incr('not_int_or_float_value_key')
    except ValueError as e:
        assert str(e) == "Not send initial 'data' from value"

    await client.set('inc_key', 1)
    result = await client.incr('inc_key')
    assert result == 2
    result = await client.incr('inc_key', 0.5)
    assert result == 2.5
    result = await client.get('inc_key')
    assert result['data'] == 2.5
    #------decr------
    try:
        result = await client.decr('dos_not_key')
    except ValueError as e:
        assert str(e) == "'::dos_not_key' is not set in the cache"
    try:
        await client.set('not_int_or_float_value_key', {'test_key': 'test_value'})
        result = await client.decr('not_int_or_float_value_key')
    except ValueError as e:
        assert str(e) == "Not send initial 'data' from value"

    result = await client.decr('inc_key', 0.5)
    assert result == 2.0
    result = await client.decr('inc_key', 3)
    assert result == -1.0
    result = await client.get('inc_key')
    assert result['data'] == -1
