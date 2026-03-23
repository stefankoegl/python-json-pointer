The ``jsonpointer`` commandline utility
=======================================

The JSON pointer package also installs a ``jsonpointer`` commandline utility
that can be used to resolve a JSON pointers on JSON files.

The program has the following usage ::

    usage: jsonpointer [-h] (-e EXPRESSION | -f POINTER_FILE) [--indent INDENT]
                       [-v]
                       FILE [FILE ...]

    Resolve a JSON pointer on JSON files

    positional arguments:
      FILE                  Files for which the pointer should be resolved

    options:
      -h, --help            show this help message and exit
      -e EXPRESSION, --expression EXPRESSION
                            A JSON pointer expression (e.g. "/foo/bar")
      -f POINTER_FILE, --pointer-file POINTER_FILE
                            File containing a JSON pointer expression
      --indent INDENT       Indent output by n spaces
      -v, --version         show program's version number and exit

For backward compatibility, if the first argument is a file path, it is treated as
if `-f` was specified, allowing the command to be used as in previous versions.


Example
^^^^^^^

.. code-block:: bash

    # inspect JSON files
    $ cat a.json
    { "a": [1, 2, 3] }

    $ cat b.json
    { "a": {"b": [1, 3, 4]}, "b": 1 }

    # inspect JSON pointer
    $ cat ptr.json
    "/a"

    # resolve JSON pointer (version 1 compatible syntax)
    $ jsonpointer ptr.json a.json b.json
    [1, 2, 3]
    {"b": [1, 3, 4]}

    # resolve with -f option
    $ jsonpointer -f ptr.json a.json b.json
    [1, 2, 3]
    {"b": [1, 3, 4]}

    # resolve with -e option for direct expression
    $ jsonpointer -e "/a" a.json b.json
    [1, 2, 3]
    {"b": [1, 3, 4]}
