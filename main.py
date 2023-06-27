import unittest
import tests_tdd

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(tests_tdd)
    unittest.TextTestRunner(verbosity=1).run(suite)