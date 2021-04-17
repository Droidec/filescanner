# filescanner

`filescanner` is a scanning tool that operates on files.  
It allows you to apply various operations on a set of files.

# Dependencies

Python dependencies:

None

# Usage

Simply call the python script by a specifying a source directory and an operation.

Available options:
- Display help (-h, --help)
- Restrict the set to a file format list (MKV, MP3, JPG, ...) (-f, --format)

Available operations:
- Prefix the set of files (--prefix)
- Suffix the set of files (--suffix)
- Rename the set of files according to a nameset file (--nameset)

You can also import the module in another project:

```python
import filescanner
fileset = FileSet(path)

# Apply operation by calling its corresponding method
# You can restrict by format (fmt) or preview operation changes
fileset.prefix(value, [fmt=], [preview=])
fileset.suffix(value, [fmt=], [preview=])
fileset.rename_by_file(namefile, [fmt=], [preview=])
```

# Author(s)

Droidec (Marc G.) <https://github.com/Droidec>

# Licence

`filescanner` is released under BSD-3 clause licence. See the LICENCE file in this source distribution for more information.
