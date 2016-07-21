from processors.base.writers.location import normalize_location

def test_simple_case(self):
	#"""Testing the simple and easy normal case of normalization"""
	case1 = normalize_locations("c.h.i.n.a")
	case2 = normalize_locations("china")
	case3 = normalize_locations("China")
	expected = "China"
	assert case1 == expect
	assert case2 == expect
	assert case3 == expect

def testAlphaCase(self):
	#"""Testing the alpha name case of normalization"""
	case1 = normalize_locations("US")
	case2 = normalize_locations("usa")
	case3 = normalize_locations("u.s.a")
	expected = "United States"
	assert case1 == expect
	assert case2 == expect
	assert case3 == expect
	
def testTypingErrors(self):
	#"""Testing the typing errors case of normalization"""
	case1 = normalize_locations("Chnia")
	case2 = normalize_locations("United Stated")
	case3 = normalize_locations("Thailland")
	expected1 = "China"
	expected2 = "United States"
	expected3 = "Thailand"
	assert case1 == expect1
	assert case2 == expect2
	assert case3 == expect3

def testCapitalErrors(self):
	#"""Testing the capital errors case of normalization"""
	case = normalize_locations("Beijing")	
	expected = "China"
	assert case == expect

def testCornerErrors(self):
	#"""Testing the corner case of normalization, based on the database of open trials"""
	case = normalize_locations("Global trial(North America)")	
	expected = "Global trial(North America)"
	assert case == expect

def testCityErrors(self):
	#"""Testing the city names case of normalization, in this case the code receive a name of city/provincy and normalize for the country"""
	case = normalize_locations("Henan")	
	expected = "China"
	assert case == expect
	
def testContinentErrors(self):
	#"""Testing the continent names case of normalization, in this case the code receive a name of a continent and dont normalize it"""
	case = normalize_locations("South America")	
	expected = "South America"
	assert case == expect