#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doctest
import unittest
import sys
import copy
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


class ComparisonTests(unittest.TestCase):

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
        p1 = JsonPointer("/a/b/c")
        p2 = JsonPointer("/a/b")
        p3 = JsonPointer("/b/c")

        self.assertTrue(p1.contains(p2))
        self.assertFalse(p1.contains(p3))



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

    def test_alttypes(self):
        JsonPointer.alttypes = True

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
            
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(SpecificationTests))
suite.addTest(unittest.makeSuite(ComparisonTests))
suite.addTest(unittest.makeSuite(WrongInputTests))
suite.addTest(unittest.makeSuite(ToLastTests))
suite.addTest(unittest.makeSuite(SetTests))
suite.addTest(unittest.makeSuite(AltTypesTests))

modules = ['jsonpointer']

for module in modules:
    m = __import__(module, fromlist=[module])
    suite.addTest(doctest.DocTestSuite(m))

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)
