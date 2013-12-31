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


def to_path(dir_path_0, dir_path_1):
    return "%s/%s" % (dir_path_0, dir_path_1)


class EndListener:
    def __init__(self):
        self.expected_output_dic = None

    def failure(self, text):
        pass

    def success(self, filename, output):
        if self.exected_output_dic[filename] == output:
            print("Test %s correct" % filename)
        else:
            print("Test %s incorrect" % filename)

    def register_output(self, read_output):
        self.expected_output_dic = read_output()

    @staticmethod
    def __compare_output(given, expected):
        return given == expected


class Wymiot(object):
    def __init__(self, exec_path, exec_name, test_path, timeout=None):
        self.exec_name = exec_name
        self.exec_path = exec_path
        self.test_path = test_path
        self.timeout = timeout
        self.ins = self.outs = None

    def __list_input_files(self):
        if self.ins is None:
            self.ins = [f for f in os.listdir(self.test_path) if re.search('[.]*.in', f)]
        return self.ins

    def __output_files(self):
        if self.outs is None:
            ins = self.__list_input_files()
            self.outs = [(fin, fin.replace('.in', '.out')) for fin in ins]
        return self.outs

    def run_test_set(self, end_listener):
        ins = self.__list_input_files()

        def expected_output():
            output_files = self.__output_files()
            output = {}
            for filename in output_files:
                with open(filename, "r") as file:
                    content = file.read()
                output[filename] = content
            return output

        end_listener.register_output(expected_output)

        for testfile in ins:
            self.run_program(testfile, end_listener)

    def run_program(self, testfile, end_listener):
        try:
            output = subprocess.check_output(to_path(self.exec_path, self.exec_name) + " < " + testfile,
                                             timeout=self.timeout,
                                             stderr=subprocess.STDOUT)
            decoded_output = output.decode()
            end_listener.success(decoded_output)
        except subprocess.CalledProcessError as exp:
            end_listener.failure(exp.output)


def main():
    arguments = docopt(__doc__, version="0.0.1")
    prog_path = "." if arguments['--exec-path'] is None else arguments['--exec-path']
    prog_name = os.path.basename(os.getcwd()) if arguments['--exec-name'] is None else arguments.get('--exec-name')
    test_dir = 'tests' if arguments['--test_dir'] is None else arguments.get('--test_dir')

    if not os.path.isfile(to_path(prog_path, prog_name)):
        print("The program %s does not exists" % (prog_path + "/" + prog_name))
        return

    wymiot = Wymiot(prog_path, prog_name, test_dir)


if __name__ == '__main__':
    main()

