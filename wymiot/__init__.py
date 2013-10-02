"""
Usage: wymiot ARG

ARG name of the program to test
-h --help shows help
-p --program path to the program
-t --test_dir test directory
"""

import os
import subprocess

from docopt import docopt


class Wymiot:

    @staticmethod
    def run_program(path, name, tests_dir):
        output = subprocess.check_output(path + name, stderr=subprocess.STDOUT)
        return output.decode()


def main():
    arguments = docopt(__doc__, version="0.0.1")
    prog_name = arguments['ARG']
    prog_path = arguments.get('program', '.')
    test_dir = arguments.get('test_dir', 'tests')

    if not os.path.isfile(prog_name):
        print("The program does not exists")

    result = Wymiot.run_program(prog_path, prog_name, test_dir)
    print(result)

if __name__ == '__main__':
    main()


