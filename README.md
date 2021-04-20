# filescanner

`filescanner` is a scanning tool that operates on files.  
It allows you to apply various operations on a set of files to increase your productivity.  
*Unix/OS-X hidden files are ignored.*

# Dependencies

None

# Usage

Simply call the python script `filescanner.py` by specifying a source directory and an operation.  
Before any changes, the script will preview the operation and ask you if you're agree.  
Operations are mutually exclusive. Simply re-call the script to perform multiple operations.

Available options:
- Display help (-h, --help)
- Restrict the set to a file format list (MKV, MP3, JPG, ...) (-f, --format)

Available operations (See full description below):
- Prefix (--prefix)
- Suffix (--suffix)
- Replace (--replace)
- Nameset (--nameset)
- Plexify (--plexify)

## Prefix

Prefix the set of files (--prefix)

For example, if you want to prefix your *FLAC* files in *Download* directory with `0`:

```text
> python3 filescanner.py ~/Downloads --format flac --prefix 0

Will rename [1 - Track 1.flac] to [01 - Track 1.flac]
Will rename [2 - Track 2.flac] to [02 - Track 2.flac]
Will rename [3 - Track 3.flac] to [03 - Track 3.flac]

Is this ok ? [Y/n]
```

## Suffix

Suffix the set of files (--suffix)

For example, if you want to suffix your *FLAC* files in *Download* directory with `[To remove]`:

```text
> python3 filescanner.py ~/Downloads --format flac --suffix ' [To remove]'

Will rename [1 - Track 1.flac] to [1 - Track 1 [To remove].flac]
Will rename [2 - Track 2.flac] to [2 - Track 2 [To remove].flac]
Will rename [3 - Track 3.flac] to [3 - Track 3 [To remove].flac]

Is this ok ? [Y/n]
```

## Replace

Replace substring by another one in the set of files (--replace)

For example, if you want to replace `Track` by `Song` in your *MP3* files in *Download* directory:

```text
> python3 filescanner.py ~/Downloads --format mp3 --replace 'Track' 'Song'

Will rename [Track 1.mp3] to [Song 1.mp3]
Will rename [Track 2.mp3] to [Song 2.mp3]
Will rename [Track 3.mp3] to [Song 3.mp3]

Is this ok ? [Y/n]
```

## Nameset

Rename the set of files according to a nameset file (--nameset)

The nameset file consists of a UTF-8 file where each line corresponds to a name (Ignore empty/blank lines).  
The operation proceed until it reaches the end of the nameset file or if there is no more files in the set.  
It is greatly inspired by the [FileBot](https://www.filebot.net) naming convention, but this script will do it for free...

For example, consider a `name.txt` file containing:

```text
121045
131045
181045
```

The command would be:

```text
> python3 filescanner.py ~/Downloads --nameset name.txt

Will rename [Episode 1.mkv] to [121045.mkv]
Will rename [Episode 2.mkv] to [131045.mkv]
Will rename [Episode 3.mkv] to [181045.mkv]

Is this ok ? [Y/n]
```

## Plexify

Rename the set of files in a format recommended by streaming services such as [PleX](https://www.plex.tv/).  
Made for people who massively download OST on the Internet and are too lazy to modify one by one the format of each file.  
This operation attempts to recognize the pattern used in the set of files and transform it to:  
`DiskNumber-TrackNumber - TrackName.ext`.

Recognize patterns with `whitespace characters`, `dots`, `dashes` and `underscores`.

For example, if you want to plexify your *FLAC* files in *Download* directory:

```text
> python3 filescanner.py ~/Downloads --format flac --plexify

Will rename [01.Track 1.flac] to [01 - Track 1.flac]
Will rename [02-Track 2.flac] to [02 - Track 2.flac]
Will rename [03_Track 3.flac] to [03 - Track 3.flac]
Will rename [04 Track 4.flac] to [04 - Track 4.flac]
Will rename [05 - Track 5.flac] to [05 - Track 5.flac]
Will rename [1.01.Track 1.flac] to [1-01 - Track 1.flac]
Will rename [1.02-Track 2.flac] to [1-02 - Track 2.flac]
Will rename [1.03_Track 3.flac] to [1-03 - Track 3.flac]
Will rename [1.04 Track 4.flac] to [1-04 - Track 4.flac]
Will rename [1.05 - Track 5.flac] to [1-05 - Track 5.flac]

Is this ok ? [Y/n]
```

# Import

You can import the module in another project like so:

```python
import filescanner
fileset = FileSet(path)

# Apply operation by calling its corresponding method
# Each method accept format restriction and let you preview changes
fileset.prefix(affix, [fmt=], [preview=])
fileset.suffix(affix, [fmt=], [preview=])
fileset.replace(oldval, newval, [fmt=], [preview=])
fileset.nameset(nmfile, [fmt=], [preview=])
fileset.plexify([fmt=], [preview=])
```

# Author(s)

Droidec (Marc G.) <https://github.com/Droidec>

# Licence

`filescanner` is released under BSD-3 clause licence. See the LICENCE file in this source distribution for more information.
