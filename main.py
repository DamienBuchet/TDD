import unittest
import tests_tdd
import sys

try:
    x = sys.argv[1]
    vbs = 2
except:
    vbs = 1

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(tests_tdd)
    unittest.TextTestRunner(verbosity=vbs).run(suite)