from processors.base.writers.location import normalize_location


@pytest.mark.parametrize("test_input,expected", [
    ("c.h.i.n.a", "China"),
    ("china", "China"),
    ("China", "China"),
    ("US","United States"),
    ("u.s.a","United States"),
    ("Chnia","China"),
    ("United Stated","United States"),
    ("Beijing","China"),
    ("Global trial(North America)","Global trial(North America)"),
    ("Henan","China"),
    ("South America","South America")])
def test_simple_case(test_input, expected):
	assert normalize_location(test_input) == expected

