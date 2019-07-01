from __future__ import print_function

import subprocess
import sys

from safety.cli import check


def main(argv):
    '''
    - Pass files with 'requirement' in the filename as args to safety
    - Build each file into virtualenv (to pin versions) and call safety on venv
    '''

    try:
        # Check *requirement* files
        check.main(['--full-report'] + sum((['-r', f] for f in argv), []))
    except SystemExit as error:
        if error.code != 0:
            return 1

    for file in argv:
        try:
            # Build virtual environments to force pinning of versions
            subprocess.run(["pip", "install", "-r", str(file)])
            check.main(['--full-report'])
            subprocess.run(["pip", "uninstall", "-ry", str(file)])
        except SystemExit as error:
            if error.code != 0:
                return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
