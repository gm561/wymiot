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

    def __init__(self, exec_path, exec_name, test_path):
        self.exec_name = exec_name
        self.exec_path = exec_path
        self.test_path = test_path

    def list_input_files(self):
        ins = [f for f in os.listdir(self.test_path) if re.search('[.]*.in', f) ]
        ous = [(fin, fin.replace('.in', '.out')) for fin in ins]
        return ous

    def run_program(self, end_listener):
        output = subprocess.check_output(to_path(self.exec_path, self.exec_name), stderr=subprocess.STDOUT)
        decoded_output = output.decode()
        end_listener(decoded_output)


def to_path(dir_path_0, dir_path_1):
    return "%s/%s" % (dir_path_0, dir_path_1)


def main():
    arguments = docopt(__doc__, version="0.0.1")
    prog_path = "." if arguments['--exec-path'] is None else arguments['--exec-path']
    prog_name = os.path.basename(os.getcwd()) if arguments['--exec-name'] is None else arguments.get('--exec-name')
    test_dir = 'tests' if arguments['--test_dir'] is None else arguments.get('--test_dir')

    if not os.path.isfile(to_path(prog_path, prog_name)):
        print("The program %s does not exists" % (prog_path + "/" + prog_name))
        return

    wymiot = Wymiot(prog_path, prog_name, test_dir)
    wymiot.run_program(print)

if __name__ == '__main__':
    main()

