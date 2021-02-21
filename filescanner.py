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
import sys
import argparse

def query_yes_no(question, default='yes'):
    """Prompt user for a boolean choice

    Parameters
        question (str) : Question to ask to user
        default (str) : Default answer (Default is 'yes') [optional]

    Return
        A boolean representing user choice
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

class FileSet():
    """FileSet describe a set of files to be renamed

    Attributes
        nameset (str) : File containing the name list to be applied
        path (str) : Path containing files to be renamed
    """

    def __init__(self, nameset, path):
        """FileSet init

        Raise
            ValueError :
                - If file does not exist
                - If path does not exist
        """
        # Check consistency
        if not os.path.isfile(nameset):
            raise ValueError(f"'{nameset}' is not a valid file")

        if not os.path.isdir(path):
            raise ValueError(f"'{path}' is not a valid directory")

        self.nameset = nameset
        self.path = path

    def print(self):
        """Print how files will be renamed

        Parameters
            None

        Return
            None
        """
        nameset = open(self.nameset, encoding='utf-8').readlines()
        files = [file for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file))]

        for index, (name, file) in enumerate(zip(nameset, files)):
            ext = os.path.splitext(file)[1]
            print(f"'{file}' will be renamed '{name.strip() + ext}'")

    def rename(self):
        """Rename files in path according to nameset

        Parameters
            None

        Return
            None
        """
        nameset = open(self.nameset, encoding='utf-8').readlines()
        files = [file for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file))]

        for index, (name, file) in enumerate(zip(nameset, files)):
            ext = os.path.splitext(file)[1]
            os.rename(os.path.join(self.path, file), os.path.join(self.path, name.strip() + ext))

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="A file scanner that renames... files")
    parser.add_argument('-f', '--file', help="File containing the name list to be applied", required=True)
    parser.add_argument('-d', '--dir', help="Directory containing files to be renamed", required=True)

    args = parser.parse_args()
    fileset = FileSet(args.file, args.dir)

    fileset.print()

    if not query_yes_no("\nIs this ok ?", 'yes'):
        sys.exit(1)

    fileset.rename()
