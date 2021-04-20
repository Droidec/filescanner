# -*- coding: utf-8 -*-
#
# Copyright (c) 2019-2021, Droidec (Marc G.)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  - Neither the name of Thomas J Bradley nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import re
import sys
import argparse

def query_yes_no(question, default='yes'):
    """Prompt user for a boolean choice

    Parameters
        question (str) : Question to ask to user
        default (str) : Default answer (Default is 'yes') [optional]

    Return
        A boolean representing user choice

    Raise
        ValueError if the default answer is invalid
    """

    valid = {
        'yes': True,
        'ye': True,
        'y': True,
        'no': False,
        'n': False
    }
    if default is None:
        prompt = " [y/n] "
    elif default == 'yes':
        prompt = " [Y/n] "
    elif default == 'no':
        prompt = " [y/N] "
    else:
        raise ValueError(f"Invalid default value: '{default}'")

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        if choice in valid:
            return valid[choice]

class File():
    """File describe a file on the filesystem

    Attributes
        name (str) : File name
        ext (str) : File extension (Default is '')
    """

    def __init__(self, name, ext=''):
        """File init

        Raise
            ValueError if extension is not valid
        """
        # Check consistency
        if ext and not ext.startswith('.'):
            raise ValueError(f"'{ext}' is not a valid extension")

        self.name = name
        self.ext = ext

    def namext(self):
        """Get file name with its extension

        Return
            The file name with its extension as a string
        """
        return self.name + self.ext

class FileSet():
    """FileSet describe utilities methods appliable on a set of files

    Attributes
        path (str) : Path to file set
    """

    def __init__(self, path):
        """FileSet init

        Raise
            ValueError if path is not a directory
        """
        # Check consistency
        if not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a valid directory")

        self.path = path

    def __get_fileset(self, fmt=None):
        """Get file set

        NOTE : Ignore hidden files

        Parameters
            fmt (list) : File format(s) restriction

        Return
            The file set as a list of File object
        """
        fileset = []

        for file in sorted(os.listdir(self.path)):
            # Ignore hidden files
            if file.startswith('.'):
                continue

            # Ignore everything that is not a file
            if not os.path.isfile(os.path.join(self.path, file)):
                continue

            # Format restriction
            if fmt is not None and not os.path.splitext(file)[1][1:] in fmt:
                continue

            name, ext = os.path.splitext(file)
            fileset.append(File(name, ext))

        return fileset

    def prefix(self, affix, fmt=None, preview=False):
        """Prefix the file set with given affix

        Parameters
            affix (str) : The affix to be applied as a prefix
            fmt (list) : Only operate on specified format(s) (Default is 'None') [optional]
            preview (boolean) : Only preview changes (Default is 'False') [optional]

        Return
            Number of files (that would be) processed
        """
        fileset = self.__get_fileset(fmt)
        index = -1

        for index, file in enumerate(fileset):
            if preview:
                print(f"Will rename [{file.namext()}] to [{affix + file.namext()}]")
            else:
                os.rename(os.path.join(self.path, file.namext()), os.path.join(self.path, affix + file.namext()))

        return index+1

    def suffix(self, affix, fmt=None, preview=False):
        """Suffix the file set with given affix

        Parameters
            affix (str) : The affix to be applied as a suffix
            fmt (list) : Only operate on specified format(s) (Default is 'None') [optional]
            preview (boolean) : Only preview changes (Default is 'False') [optional]

        Return
            Number of files (that would be) processed
        """
        fileset = self.__get_fileset(fmt)
        index = -1

        for index, file in enumerate(fileset):
            if preview:
                print(f"Will rename [{file.namext()}] to [{file.name + affix + file.ext}]")
            else:
                os.rename(os.path.join(self.path, file.namext()), os.path.join(self.path, file.name + affix + file.ext))

        return index+1

    def replace(self, oldval, newval, fmt=None, preview=False):
        """Replace substring by another one in the set of files

        Parameters
            oldval (str) : The old substring to look for
            newval (str) : The new substring to be applied
            fmt (list) : Only operate on specified format(s) (Default is 'None') [optional]
            preview (boolean) : Only preview changes (Default is 'False') [optional]
        """
        fileset = self.__get_fileset(fmt)
        index = -1

        for index, file in enumerate(fileset):
            if preview:
                print(f"Will rename [{file.namext()}] to [{file.name.replace(oldval, newval) + file.ext}]")
            else:
                os.rename(os.path.join(self.path, file.namext()), os.path.join(self.path, file.name.replace(oldval, newval) + file.ext))

        return index+1

    def nameset(self, nmfile, fmt=None, preview=False):
        """Rename the file set according to a nameset file (Filebot methodology)

        NOTE : Ignore empty/blank lines

        Parameters
            nmfile (str) : Path to nameset file (File encoding is supposed to be in UTF-8)
            fmt (list) : Only operate on specified format(s) (Default is 'None') [optional]
            preview (boolean) : Only preview changes (Default is 'False') [optional]

        Return
            Number of files (that would be) processed

        Raise
            ValueError if nmfile is not a file
        """
        # Check consistency
        if not os.path.isfile(nmfile):
            raise ValueError(f"'{nmfile}' is not a valid file")

        nameset = [line.strip() for line in open(nmfile, encoding='utf-8').readlines() if line.strip()]
        fileset = self.__get_fileset(fmt)
        index = -1

        for index, (name, file) in enumerate(zip(nameset, fileset)):
            if preview:
                print(f"Will rename [{file.namext()}] to [{name + file.ext}]")
            else:
                os.rename(os.path.join(self.path, file.namext()), os.path.join(self.path, name + file.ext))

        return index+1

    def plexify(self, fmt=None, preview=False):
        """Apply PleX OST naming convention to the set of files

        Parameters
            fmt (list) : Only operate on specified format(s) (Default is 'None') [optional]
            preview (boolean) : Only preview changes (Default is 'False') [optional]

        Return
            Number of files (that would be) processed
        """
        fileset = self.__get_fileset(fmt)
        index = -1

        for index, file in enumerate(fileset):
            if re.search(r'^\d+[-.]\d+[\s._-]*\w*', file.name):
                # Pattern with Disk Number
                newname = re.sub(r'^(\d+)[-.](\d+)[\s._-]*', r'\1-\2 - ', file.name, count=1)
            else:
                # Simple pattern
                newname = re.sub(r'^(\d+)[\s._-]*', r'\1 - ', file.name, count=1)

            if preview:
                print(f"Will rename [{file.namext()}] to [{newname + file.ext}]")
            else:
                os.rename(os.path.join(self.path, file.namext()), os.path.join(self.path, newname + file.ext))

        return index+1

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="A file scanner that operates on a set of files")
    parser.add_argument('-f', '--format', default=None, nargs='+', help="Restrict the set to a file format list (Default is None)")
    parser.add_argument('dir', help="Source directory")

    # Possible operations
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prefix', help="Prefix the set of files")
    group.add_argument('--suffix', help="Suffix the set of files")
    group.add_argument('--replace', nargs=2, help="Replace substring by another one in the set of files")
    group.add_argument('--nameset', help="Rename files according to a nameset file")
    group.add_argument('--plexify', help="Rename the set of files in a format recommended by streaming services such as PleX", action='store_true')

    args = parser.parse_args()
    fileset = FileSet(args.dir)

    # Various transformations
    if args.format is not None:
        args.format = [fmt.lower() for fmt in args.format]

    # Apply chosen operation
    if args.prefix is not None:
        num = fileset.prefix(args.prefix, args.format, True)
        if num == 0:
            raise ValueError("Empty set of files. Nothing to do")
        if not query_yes_no("\nIs this ok ?", 'yes'):
            sys.exit(1)
        num = fileset.prefix(args.prefix, args.format, False)

    if args.suffix is not None:
        num = fileset.suffix(args.suffix, args.format, True)
        if num == 0:
            raise ValueError("Empty set of files. Nothing to do")
        if not query_yes_no("\nIs this ok ?", 'yes'):
            sys.exit(1)
        num = fileset.suffix(args.suffix, args.format, False)

    if args.replace is not None:
        num = fileset.replace(args.replace[0], args.replace[1], args.format, True)
        if num == 0:
            raise ValueError("Empty set of files. Nothing to do")
        if not query_yes_no("\nIs this ok ?", 'yes'):
            sys.exit(1)
        num = fileset.replace(args.replace[0], args.replace[1], args.format, False)

    if args.nameset is not None:
        num = fileset.nameset(args.nameset, args.format, True)
        if num == 0:
            raise ValueError("Empty set of files. Nothing to do")
        if not query_yes_no("\nIs this ok ?", 'yes'):
            sys.exit(1)
        num = fileset.nameset(args.nameset, args.format, False)

    if args.plexify is True:
        num = fileset.plexify(args.format, True)
        if num == 0:
            raise ValueError("Empty set of files. Nothing to do")
        if not query_yes_no("\nIs this ok ?", 'yes'):
            sys.exit(1)
        num = fileset.plexify(args.format, False)

    print(f"Processed {num} files")
