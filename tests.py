#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import doctest
import unittest
import sys
from jsonpointer import resolve_pointer

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




modules = ['jsonpointer']
coverage_modules = []

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(SpecificationTests))

for module in modules:
    m = __import__(module, fromlist=[module])
    coverage_modules.append(m)
    suite.addTest(doctest.DocTestSuite(m))

runner = unittest.TextTestRunner(verbosity=2)

try:
    import coverage
except ImportError:
    coverage = None

if coverage is not None:
    coverage.erase()
    coverage.start()

result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)

if coverage is not None:
    coverage.stop()
    coverage.report(coverage_modules)
    coverage.erase()

if coverage is None:
    print("""
    No coverage reporting done (Python module "coverage" is missing)
    Please install the python-coverage package to get coverage reporting.
    """, file=sys.stderr)
