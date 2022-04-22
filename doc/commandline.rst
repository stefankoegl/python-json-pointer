The ``jsonpointer`` commandline utility
=======================================

The JSON pointer package also installs a ``jsonpointer`` commandline utility
that can be used to resolve a JSON pointers on JSON files.

The program has the following usage ::

    usage: jsonpointer [-h] (-f [POINTER_FILE] | -p [POINTER]) [--indent INDENT] [-v] FILE [FILE ...]

    Resolve a JSON pointer on JSON files

    positional arguments:
      FILE             Files for which the pointer should be resolved

    optional arguments:
      -h, --help       show this help message and exit
      -f [POINTER_FILE], --pointer-file [POINTER_FILE]
                       File containing a JSON pointer expression
      -p [POINTER], --pointer [POINTER]
                       A JSON pointer expression
      --indent INDENT  Indent output by n spaces
      -v, --version    show program's version number and exit


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
    /a

    # resolve JSON pointer
    $ jsonpointer -f ptr.json a.json b.json
    [1, 2, 3]
    {"b": [1, 3, 4]}
