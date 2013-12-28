
import unittest
from wymiot import Wymiot


class DoesDoSth(unittest.TestCase):

    def test_nothing(self):
        path_to_nothing = '../examples/nothing/'
        wymiot = Wymiot("nothing", path_to_nothing, path_to_nothing)
        wymiot.run_program(lambda result: self.assertEquals(result, 'nothing\n'))

    def test_read_files(self):
        path_to_test_dir = '../examples/fib/tests/'
        path_to_exec_dir = '../examples/fib'
        fib_exec = "fib"
        wymiot = Wymiot(fib_exec, path_to_exec_dir, path_to_test_dir)
        result = wymiot.list_input_files()

        self.assertListEqual(result, [('test01.in', 'test01.out')])

    def ignore_test_do_sth0(self):
        path_to_exec_dir = '../examples/fib/'
        fib_exec = 'fib'
        test_instance = 'tests/test01.in'
        wymiot = Wymiot(fib_exec, path_to_exec_dir, test_instance)

        expected = '1 13 233'
        wymiot.run_program(lambda result: self.assertEquals(result, expected))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
