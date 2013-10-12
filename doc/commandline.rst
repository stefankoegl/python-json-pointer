The ``jsonpointer`` commandline utility
=======================================

The JSON pointer package also installs a ``jsonpointer`` commandline utility
that can be used to resolve a JSON pointers on JSON files.

The program has the following usage ::

    usage: jsonpointer [-h] [--indent INDENT] [-v] POINTER FILE [FILE ...]

    Resolve a JSON pointer on JSON files

    positional arguments:
      POINTER          File containing a JSON pointer expression
      FILE             Files for which the pointer should be resolved

    optional arguments:
      -h, --help       show this help message and exit
      --indent INDENT  Indent output by n spaces
      -v, --version    show program's version number and exit


The following shows example usage ::

    $ cat a.json
    { "a": [1, 2, 3] }
    $ cat b.json
    { "a": {"b": [1, 3, 4]}, "b": 1 }
    $ cat ptr.json
    "/a"
    $ jsonpointer ptr.json a.json b.json
    [1, 2, 3]
    {"b": [1, 3, 4]}
