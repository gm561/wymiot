"""
Usage:
   wymiot [-e <name>] [-p <path>] [-t <path>]

-e --exec-name Set name of the program.
-p --exec-path Set path to the program.
-h --help Show help.
-t --test_dir Set test directory.
--version Show version.
"""

import os
import re
import subprocess

from docopt import docopt


class Wymiot(object):

    @staticmethod
    def list_input_files(tests_dir):
        ins = [f for f in os.listdir(tests_dir) if re.search('[.]*.in', f) ]
        ous = [(fin, fin.replace('.in', '.out')) for fin in ins]
        return ous

    @staticmethod
    def run_program(path, name, tests_dir):
        output = subprocess.check_output(path + name, stderr=subprocess.STDOUT)
        return output.decode()


def main():
    arguments = docopt(__doc__, version="0.0.1")
    prog_path = arguments.get('--program', ".")
    prog_name = arguments.get('--exec-name', os.path.basename(os.getcwd()))
    test_dir = arguments.get('--test_dir', 'tests')

    if not os.path.isfile(prog_name):
        print("The program %s does not exists" % (prog_path + "/" + prog_name))
        return

    result = Wymiot.run_program(prog_path, prog_name, test_dir)
    print(result)

if __name__ == '__main__':
    main()

