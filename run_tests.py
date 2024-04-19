
import time
import unittest

if __name__ == '__main__':
    start_time = time.time()
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')  # Discover test files starting with 'test_'
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    end_time = time.time()

    print(f"Tests executed in {end_time - start_time} seconds")