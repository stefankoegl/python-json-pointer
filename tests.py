#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import doctest
import unittest
import sys
import os
import copy
import subprocess
from jsonpointer import resolve_pointer, EndOfList, JsonPointerException, \
         JsonPointer, set_pointer


class SpecificationTests(unittest.TestCase):
    """ Tests all examples from the JSON Pointer specification """

    def test_example(self):
        doc =   {
            "foo": ["bar", "baz"],
            "": 0,
            "a/b": 1,
            "c%d": 2,
            "e^f": 3,
            "g|h": 4,
            "i\\j": 5,
            "k\"l": 6,
            " ": 7,
            "m~n": 8
        }

        self.assertEqual(resolve_pointer(doc, ""), doc)
        self.assertEqual(resolve_pointer(doc, "/foo"), ["bar", "baz"])
        self.assertEqual(resolve_pointer(doc, "/foo/0"), "bar")
        self.assertEqual(resolve_pointer(doc, "/"), 0)
        self.assertEqual(resolve_pointer(doc, "/a~1b"), 1)
        self.assertEqual(resolve_pointer(doc, "/c%d"), 2)
        self.assertEqual(resolve_pointer(doc, "/e^f"), 3)
        self.assertEqual(resolve_pointer(doc, "/g|h"), 4)
        self.assertEqual(resolve_pointer(doc, "/i\\j"), 5)
        self.assertEqual(resolve_pointer(doc, "/k\"l"), 6)
        self.assertEqual(resolve_pointer(doc, "/ "), 7)
        self.assertEqual(resolve_pointer(doc, "/m~0n"), 8)


    def test_eol(self):
        doc = {
            "foo": ["bar", "baz"]
        }

        self.assertTrue(isinstance(resolve_pointer(doc, "/foo/-"), EndOfList))
        self.assertRaises(JsonPointerException, resolve_pointer, doc, "/foo/-/1")

    def test_round_trip(self):
        paths = [
            "",
            "/foo",
            "/foo/0",
            "/",
            "/a~1b",
            "/c%d",
            "/e^f",
            "/g|h",
            "/i\\j",
            "/k\"l",
            "/ ",
            "/m~0n",
            '/\xee',
        ]
        for path in paths:
            ptr = JsonPointer(path)
            self.assertEqual(path, ptr.path)

            parts = ptr.parts
            new_ptr = JsonPointer.from_parts(parts)
            self.assertEqual(ptr, new_ptr)


class ComparisonTests(unittest.TestCase):

    def setUp(self):
        self.ptr1 = JsonPointer("/a/b/c")
        self.ptr2 = JsonPointer("/a/b")
        self.ptr3 = JsonPointer("/b/c")

    def test_eq_hash(self):
        p1 = JsonPointer("/something/1/b")
        p2 = JsonPointer("/something/1/b")
        p3 = JsonPointer("/something/1.0/b")

        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        self.assertNotEqual(p2, p3)

        self.assertEqual(hash(p1), hash(p2))
        self.assertNotEqual(hash(p1), hash(p3))
        self.assertNotEqual(hash(p2), hash(p3))

        # a pointer compares not-equal to objects of other types
        self.assertFalse(p1 == "/something/1/b")

    def test_contains(self):

        self.assertTrue(self.ptr1.contains(self.ptr2))
        self.assertTrue(self.ptr1.contains(self.ptr1))
        self.assertFalse(self.ptr1.contains(self.ptr3))

    def test_contains_magic(self):

        self.assertTrue(self.ptr2 in self.ptr1)
        self.assertTrue(self.ptr1 in self.ptr1)
        self.assertFalse(self.ptr3 in self.ptr1)

class WrongInputTests(unittest.TestCase):

    def test_no_start_slash(self):
        # an exception is raised when the pointer string does not start with /
        self.assertRaises(JsonPointerException, JsonPointer, 'some/thing')

    def test_invalid_index(self):
        # 'a' is not a valid list index
        doc = [0, 1, 2]
        self.assertRaises(JsonPointerException, resolve_pointer, doc, '/a')

    def test_oob(self):
        # this list does not have 10 members
        doc = [0, 1, 2]
        self.assertRaises(JsonPointerException, resolve_pointer, doc, '/10')

    def test_trailing_escape(self):
        self.assertRaises(JsonPointerException, JsonPointer, '/foo/bar~')

    def test_invalid_escape(self):
        self.assertRaises(JsonPointerException, JsonPointer, '/foo/bar~2')


class ToLastTests(unittest.TestCase):

    def test_empty_path(self):
        doc = {'a': [1, 2, 3]}
        ptr = JsonPointer('')
        last, nxt = ptr.to_last(doc)
        self.assertEqual(doc, last)
        self.assertTrue(nxt is None)


    def test_path(self):
        doc = {'a': [{'b': 1, 'c': 2}, 5]}
        ptr = JsonPointer('/a/0/b')
        last, nxt = ptr.to_last(doc)
        self.assertEqual(last, {'b': 1, 'c': 2})
        self.assertEqual(nxt, 'b')


class SetTests(unittest.TestCase):

    def test_set(self):
        doc =   {
            "foo": ["bar", "baz"],
            "": 0,
            "a/b": 1,
            "c%d": 2,
            "e^f": 3,
            "g|h": 4,
            "i\\j": 5,
            "k\"l": 6,
            " ": 7,
            "m~n": 8
        }
        origdoc = copy.deepcopy(doc)

        # inplace=False
        newdoc = set_pointer(doc, "/foo/1", "cod", inplace=False)
        self.assertEqual(resolve_pointer(newdoc, "/foo/1"), "cod")

        newdoc = set_pointer(doc, "/", 9, inplace=False)
        self.assertEqual(resolve_pointer(newdoc, "/"), 9)

        newdoc = set_pointer(doc, "/fud", {}, inplace=False)
        newdoc = set_pointer(newdoc, "/fud/gaw", [1, 2, 3], inplace=False)
        self.assertEqual(resolve_pointer(newdoc, "/fud"), {'gaw' : [1, 2, 3]})

        newdoc = set_pointer(doc, "", 9, inplace=False)
        self.assertEqual(newdoc, 9)

        self.assertEqual(doc, origdoc)

        # inplace=True
        set_pointer(doc, "/foo/1", "cod")
        self.assertEqual(resolve_pointer(doc, "/foo/1"), "cod")

        set_pointer(doc, "/", 9)
        self.assertEqual(resolve_pointer(doc, "/"), 9)

        self.assertRaises(JsonPointerException, set_pointer, doc, "/fud/gaw", 9)

        set_pointer(doc, "/fud", {})
        set_pointer(doc, "/fud/gaw", [1, 2, 3] )
        self.assertEqual(resolve_pointer(doc, "/fud"), {'gaw' : [1, 2, 3]})

        self.assertRaises(JsonPointerException, set_pointer, doc, "", 9)


class AltTypesTests(unittest.TestCase):

    class Node(object):
        def __init__(self, name, parent=None):
            self.name = name
            self.parent = parent
            self.left = None
            self.right = None

        def set_left(self, node):
            node.parent = self
            self.left = node

        def set_right(self, node):
            node.parent = self
            self.right = node

        def __getitem__(self, key):
            if key == 'left':
                return self.left
            if key == 'right':
                return self.right

            raise KeyError("Only left and right supported")

        def __setitem__(self, key, val):
            if key == 'left':
                return self.set_left(val)
            if key == 'right':
                return self.set_right(val)

            raise KeyError("Only left and right supported: %s" % key)

    class mdict(object):
        def __init__(self, d):
            self._d = d
        def __getitem__(self, item):
            return self._d[item]

    mdict = mdict({'root': {'1': {'2': '3'}}})
    Node = Node


    def test_alttypes(self):
        Node = self.Node

        root = Node('root')
        root.set_left(Node('a'))
        root.left.set_left(Node('aa'))
        root.left.set_right(Node('ab'))
        root.set_right(Node('b'))
        root.right.set_left(Node('ba'))
        root.right.set_right(Node('bb'))

        self.assertEqual(resolve_pointer(root, '/left').name, 'a')
        self.assertEqual(resolve_pointer(root, '/left/right').name, 'ab')
        self.assertEqual(resolve_pointer(root, '/right').name, 'b')
        self.assertEqual(resolve_pointer(root, '/right/left').name, 'ba')

        newroot = set_pointer(root, '/left/right', Node('AB'), inplace=False)
        self.assertEqual(resolve_pointer(root, '/left/right').name, 'ab')
        self.assertEqual(resolve_pointer(newroot, '/left/right').name, 'AB')

        set_pointer(root, '/left/right', Node('AB'))
        self.assertEqual(resolve_pointer(root, '/left/right').name, 'AB')

    def test_mock_dict_sanity(self):
        doc = self.mdict
        default = None

        # TODO: Generate this automatically for any given object
        path_to_expected_value = {
            '/root/1': {'2': '3'},
            '/root': {'1': {'2': '3'}},
            '/root/1/2': '3',
        }

        for path, expected_value in iter(path_to_expected_value.items()):
            self.assertEqual(resolve_pointer(doc, path, default), expected_value)

    def test_mock_dict_returns_default(self):
        doc = self.mdict
        default = None

        path_to_expected_value = {
            '/foo': default,
            '/x/y/z/d': default
        }

        for path, expected_value in iter(path_to_expected_value.items()):
            self.assertEqual(resolve_pointer(doc, path, default), expected_value)

    def test_mock_dict_raises_key_error(self):
        doc = self.mdict
        self.assertRaises(JsonPointerException, resolve_pointer, doc, '/foo')
        self.assertRaises(JsonPointerException, resolve_pointer, doc, '/root/1/2/3/4')


class CommandLineTests(unittest.TestCase):
    """ Tests the command line """

    def test_file(self):
        output = subprocess.check_output(
            ["bin/jsonpointer", "-f", "test/ptr.json", "test/a.json", "test/b.json"],
            env={"PYTHONPATH": os.getcwd()},
        )
        self.assertEqual(output, b'[1, 2, 3]\n{"b": [1, 3, 4]}\n')

    def test_pointerarg(self):
        output = subprocess.check_output(
            ["bin/jsonpointer", "-p", "/a", "test/a.json", "test/b.json"],
            env={"PYTHONPATH": os.getcwd()},
        )
        self.assertEqual(output, b'[1, 2, 3]\n{"b": [1, 3, 4]}\n')



suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(SpecificationTests))
suite.addTest(unittest.makeSuite(ComparisonTests))
suite.addTest(unittest.makeSuite(WrongInputTests))
suite.addTest(unittest.makeSuite(ToLastTests))
suite.addTest(unittest.makeSuite(SetTests))
suite.addTest(unittest.makeSuite(AltTypesTests))
suite.addTest(unittest.makeSuite(CommandLineTests))

modules = ['jsonpointer']

for module in modules:
    m = __import__(module, fromlist=[module])
    suite.addTest(doctest.DocTestSuite(m))

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)
