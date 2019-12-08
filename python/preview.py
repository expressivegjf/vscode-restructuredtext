#!/usr/bin/env python3
from __future__ import print_function
import codecs
import os.path
import sys

from docutils import core
from contextlib import contextmanager
import rst2html5_

rst2html5_.register_directives()

# If Python 3, get a binary STDOUT
if sys.version_info >= (3,):
    sys.stdout = sys.stdout.detach()

# Make STDOUT utf-8
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def main(argv=None):
    # Some sanity checks on if the path exists.
    filepath = argv[1] if argv is not None else sys.argv[1]
    filepath = os.path.abspath(filepath)
    if not os.path.exists(filepath):
        return 'File Not Found'

    # open in binary, decode utf-8, and live in unicode
    with codecs.open(filepath, 'r', 'utf8') as f:
        page_string = f.read()

    overrides = {
        'initial_header_level': 1,
        'halt_level': 5,
        'strip_comments': 'true',
    }

    # change directory to the directory containing the file
    # to pick up stylesheets etc having relative paths
    with cd(os.path.dirname(filepath)):

        parts = core.publish_parts(
            source=page_string,
            source_path=filepath,
            writer_name='html5',
            writer=rst2html5_.HTML5Writer(),
            settings_overrides=overrides,
        )

        html_document = parts['whole']
        html_document = html_document.replace('\ufeff', '')

        # the REAL print function in python 2, now... see top of file
        print(html_document)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
