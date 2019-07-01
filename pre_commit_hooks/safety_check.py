from __future__ import print_function

import logging
import subprocess
import sys

from safety.cli import check


def main(argv=None):
    '''
    - Pass files with 'requirement' in the filename as args to safety
    - Build each file into virtualenv (to pin versions) and call safety on venv
    '''

    logging.info('Preparing argv...')
    if not argv:
        argv = sys.argv[1:]
    logging.info(argv)

    logging.info('Checking requirements files...')
    try:
        # Check *requirement* files
        check.main(['--full-report'] + sum((['-r', f] for f in argv), []))
    except SystemExit as error:
        if error.code != 0:
            logging.info('...failed!')
            return 1
        logging.info('...passed')

    _precommit_venv = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE)

    for file in argv:
        logging.info('Building virtualenv for %s and checking...', file)
        try:
            # Build virtual environments to force pinning of versions
            subprocess.run(["pip", "install", "-r", str(file)])
            check.main(['--full-report'])
        except SystemExit as error:
            subprocess.run(["pip", "uninstall", "-y", "-r", str(file)])
            _current_venv = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE)
            for pkg in _precommit_venv.stdout.decode().split('\n'):
                if pkg and pkg not in _current_venv.stdout.decode().split('\n'):
                    subprocess.run(["pip", "install", pkg])
            if error.code != 0:
                logging.info('...failed!')
                return 1
            logging.info('...passed')

    return 0


if __name__ == '__main__':
    sys.exit(main())
