import unittest
import os
import sys
from StringIO import StringIO
from main import to_one_line

TEST_DIRECTORY = 'tests'

class TestOneLine(unittest.TestCase):
    def runTest(self):
        pass

def make_test(filename):
    def new_test(self):
        with open(filename, 'r') as fi:
            self.longMessage = True
            original = fi.read().strip()
            onelined = to_one_line(original)
            self.assertEqual(capture_exec(original),
                             capture_exec(onelined),
                             msg="Onelined: "+onelined)
    return new_test

class FakeStdin(object):
    def __init__(self):
        self.counter = 0
    def readline(self):
        self.counter += 1
        return str(self.counter)

def capture_exec(code_string):
    new_stdout = StringIO()
    old_stdout = sys.stdout
    old_stdin = sys.stdin
    sys.stdout = new_stdout
    sys.stdin = FakeStdin()
    namespace = {}
    try:
        exec code_string in namespace
    except Exception as e:
        import traceback
        exc = traceback.format_exc()
        raise type(e)(code_string + '\n\n' + exc)
    sys.stdout = old_stdout
    sys.stdin = old_stdin
    return new_stdout.getvalue()

for subdir, dirs, files in os.walk(TEST_DIRECTORY):
    for filename in files:
        if not 'unimplemented' in subdir:
            setattr(TestOneLine,
                    'test_%s' % filename.split('.')[0],
                    make_test(os.path.join(subdir, filename)))

if __name__ == '__main__':
    unittest.main()
