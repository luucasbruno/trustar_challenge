from challenge import JsonDeserializer
import pytest


json = """
{
    "value": "foo",
    "list": [1, 2, 3],
    "dict": {
        "a": 1,
        "b": ["a", "b", "c"],
        "c": {
            "nested_list": [4, 5],
            "nested_dict": {
                "key": "value"
            },
            "list_of_dicts": [
                {"key": "abc"},
                {"foo": "bar"}
            ]
        }
    }
}
"""

params = [
    # path to field, exists, value,  type
    ('value', True, 'foo'),
    ('list', True, [1, 2, 3]),
    ('bar', False, ''),
    ('dict.a', True, 1),
    ('dict.b', True, ['a', 'b', 'c']),
    ('dict.c.nested_list', True, [4, 5]),
    ('dict.c.nested_dict.key', True, 'value'),
    ('dict.c.nested_dict.foo', False, ''),
    ('dict.c.list_of_dicts[0].key', True, 'abc'),
    ('dict.c.list_of_dicts[1].foo', True, 'bar'),
    ('dict.c.list_of_dicts[0].bar', False, ''),
    ('dict.c.list_of_dicts[14]', False, ''),
]


@pytest.mark.parametrize('path,exists,assert_value', params)
def test_json_deserializer(path, exists, assert_value):
    data = JsonDeserializer(json)
    if not exists:
        assert data.get_field_or_none(path) is None
    else:
        value = data.get_field_or_none(path)
        assert value == assert_value
