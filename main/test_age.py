import unittest
import age

url = 'https://www.inondations.lu/basins/sauer?station=14&show-details'

class TestAGE(unittest.TestCase):
    def test_fetch_data_value_now(self):        
        result = age.fetch_data(4, url)
        result_int = int(result)
        self.assertGreaterEqual(result_int, 0) 
    
    def test_fetch_data_value_past(self):        
        result = age.fetch_data(3, url)
        result_int = int(result)
        self.assertGreaterEqual(result_int, 0) 

if __name__ == '__main__':
    unittest.main()