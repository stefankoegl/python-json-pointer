The ``jsonpointer`` commandline utility
=======================================

The JSON pointer package also installs a ``jsonpointer`` commandline utility
that can be used to resolve a JSON pointers on JSON files.

The program has the following usage ::

    usage: jsonpointer [-h] [-f [POINTER_FILE] | -p POINTER] [--indent INDENT]
                       [-v]
                       [POINTER] FILE [FILE ...]

    Resolve a JSON pointer on JSON files

    positional arguments:
      POINTER               A JSON pointer expression (if neither -f nor -p is
                            given)
      FILE                  Files for which the pointer should be resolved

    options:
      -h, --help            show this help message and exit
      -f [POINTER_FILE], --pointer-file [POINTER_FILE]
                            File containing a JSON pointer expression
      -p POINTER, --pointer POINTER
                            A JSON pointer expression
      --indent INDENT       Indent output by n spaces
      -v, --version         show program's version number and exit

The pointer can be passed as the first positional argument, with ``-p``, or
read from a file with ``-f``.

Example
^^^^^^^

.. code-block:: bash

    # inspect JSON files
    $ cat a.json
    { "a": [1, 2, 3] }

    $ cat b.json
    { "a": {"b": [1, 3, 4]}, "b": 1 }

    # resolve JSON pointer
    $ jsonpointer /a a.json b.json
    [1, 2, 3]
    {"b": [1, 3, 4]}

    # same, using the -p option
    $ jsonpointer -p /a a.json b.json
    [1, 2, 3]
    {"b": [1, 3, 4]}

    # same, reading the pointer from a file
    $ cat ptr.txt
    /a

    $ jsonpointer -f ptr.txt a.json b.json
    [1, 2, 3]
    {"b": [1, 3, 4]}
