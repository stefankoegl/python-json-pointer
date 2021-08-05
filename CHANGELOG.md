# Change Log

## x.y (unreleased)

### Breaking Changes

The `jsonpointer` commandline utility accepts either a file containing a JSON pointer expression (example: `jsonpointer -f ptr.json a.json b.json`) or
the expression as a commandline argument (example: `jsonpointer -p "/a" a.json b.json`).
