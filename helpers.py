import unittest

def convertSalaryRange(string):
    changeToAnnual = 1
    if "a month" in string:
        changeToAnnual = 12
    
    lower_range, upper_range = None, None


    try:
        if "-" in string:
            # split string into lower and upper range using "-"
            lower_range, upper_range = string.split("-")

            # remove all non-numeric characters
            lower_range = int("".join(filter(str.isdigit, lower_range))) * changeToAnnual
            upper_range = int("".join(filter(str.isdigit, upper_range))) * changeToAnnual
            
            return (lower_range, upper_range)
        else:
            lower_range = int("".join(filter(str.isdigit, string))) * changeToAnnual
            return lower_range, upper_range
    except:
        return lower_range, upper_range


class TestConversion(unittest.TestCase):
    def test_valid_range(self):
        self.assertEqual(convertSalaryRange("$2,000 - $3,000 a month"), (24000, 36000))
        self.assertEqual(convertSalaryRange("$2,000 a month"), (24000, None))
        self.assertEqual(convertSalaryRange("$60,000 - $84,000 a year"), (60000, 84000))
        # Test nonsense input
        self.assertEqual(convertSalaryRange("aaksjdlkasd"), (None, None))

if __name__ == "__main__":
    unittest.main()