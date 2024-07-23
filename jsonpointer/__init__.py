# -*- coding: utf-8 -*-
#
# python-json-pointer - An implementation of the JSON Pointer syntax
# https://github.com/stefankoegl/python-json-pointer
#
# Copyright (c) 2011 Stefan Kögl <stefan@skoegl.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

""" Identify specific nodes in a JSON document (RFC 6901) """
from .jsonpointer import JsonPointerException, JsonPointer, resolve_pointer, set_pointer, EndOfList

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore

# Will be parsed by setup.py to determine package metadata
jsonpointer_metadata = metadata.metadata("jsonpointer")
__author__ = jsonpointer_metadata["Author"]
__version__ = metadata.version("jsonpointer")
__website__ = jsonpointer_metadata["Home-page"]
__license__ = jsonpointer_metadata["License"]

__all__ = [
    "resolve_pointer",
    "set_pointer",
    "JsonPointerException",
    "JsonPointer",
    "EndOfList",
    "__author__",
    "__version__",
    "__website__",
    "__license__",
]
