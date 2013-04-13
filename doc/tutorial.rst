Tutorial
========

Please refer to `RFC 6901 <http://tools.ietf.org/html/rfc6901>`_ for the exact
pointer syntax. ``jsonpointer`` has two interfaces. The ``resolve_pointer``
method is basically a deep ``get``.

.. code-block:: python

    >>> import jsonpointer
    >>> obj = {"foo": {"anArray": [ {"prop": 44}], "another prop": {"baz": "A string" }}}

    >>> resolve_pointer(obj, '') == obj
    True

    >>> resolve_pointer(obj, '/foo') == obj['foo']
    True

    >>> resolve_pointer(obj, '/foo/another%20prop') == obj['foo']['another prop']
    True

    >>> resolve_pointer(obj, '/foo/another%20prop/baz') == obj['foo']['another prop']['baz']
    True

    >>> resolve_pointer(obj, '/foo/anArray/0') == obj['foo']['anArray'][0]
    True

    >>> resolve_pointer(obj, '/some/path', None) == None
    True


The ``JsonPointer`` class wraps a (string) path and can be used to access the
same path on several objects.

.. code-block:: python

    >>> import jsonpointer

    >>> pointer = jsonpointer.JsonPointer('/foo/1')

    >>> obj1 = {'foo': ['a', 'b', 'c']}
    >>> pointer.resolve(obj1)
    'b'

    >>> obj2 = {'foo': {'0': 1, '1': 10, '2': 100}}
    >>> pointer.resolve(obj2)
    10
