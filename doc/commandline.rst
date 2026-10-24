The ``jsonpointer`` commandline utility
=======================================

The JSON pointer package also installs a ``jsonpointer`` commandline utility
that can be used to resolve a JSON pointers on JSON files.

The program has the following usage ::

    usage: jsonpointer [-h] [-f POINTER_FILE | -p POINTER] [--indent INDENT]
                       [--continue-on-error] [-v]
                       [POINTER] FILE [FILE ...]

    Resolve a JSON pointer on JSON files

    positional arguments:
      POINTER               A JSON pointer expression (if neither -f nor -p is
                            given)
      FILE                  Files for which the pointer should be resolved

    options:
      -h, --help            show this help message and exit
      -f POINTER_FILE, --pointer-file POINTER_FILE
                            File containing a JSON pointer expression
      -p POINTER, --pointer POINTER
                            A JSON pointer expression
      --indent INDENT       Indent output by n spaces
      --continue-on-error   Continue with remaining files after JSON or text
                            decoding errors
      -v, --version         show program's version number and exit

The pointer can be passed as the first positional argument, with ``-p``, or
read from a file with ``-f``.

JSON input files and pointer files are read as UTF-8.

The exit status is 0 if the pointer could be resolved on all files, 1 if it
could not be resolved on at least one file (the remaining files are still
processed) and 2 on usage errors, such as an invalid pointer or a missing
file.

By default, invalid JSON or a text decoding error stops processing. With
``--continue-on-error``, these errors are reported on standard error with
the file name and decoder details, and the remaining files are processed.
The exit status is 1 if any file has such an error, even if later files
succeed. Missing files and other usage errors still stop processing with
status 2.

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
