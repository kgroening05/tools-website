import pytest
from tools.pdf_tools.logic import parse_range_spec


# --- Happy path: single ranges ---

@pytest.mark.parametrize("spec,total,expected", [
    ("1-5",         10, [(1, 5)]),
    ("1",           10, [(1, 1)]),
    ("5-5",         10, [(5, 5)]),
    ("1-10",        10, [(1, 10)]),
])
def test_single_range(spec, total, expected):
    assert parse_range_spec(spec, total) == expected


# --- Happy path: multiple ranges ---

@pytest.mark.parametrize("spec,total,expected", [
    ("1-5, 6-12",       20, [(1, 5), (6, 12)]),
    ("1-5,6-12",        20, [(1, 5), (6, 12)]),      # no whitespace
    ("1-5; 6-12",       20, [(1, 5), (6, 12)]),      # semicolon
    ("1-3, 7, 10-15",   20, [(1, 3), (7, 7), (10, 15)]),
])
def test_multiple_ranges(spec, total, expected):
    assert parse_range_spec(spec, total) == expected
    
    
# --- Semicolon delimiter ---
@pytest.mark.parametrize("spec,total,expected", [
    ("1-5;6-10",           20, [(1, 5), (6, 10)]),      # semicolon, no spaces
    ("1-5; 6-10",          20, [(1, 5), (6, 10)]),      # semicolon with space
    ("1-5 ; 6-10",         20, [(1, 5), (6, 10)]),      # spaces around semicolon
    ("1-5, 6-10; 11-15",   20, [(1, 5), (6, 10), (11, 15)]),  # mixed
    ("1-5; begin-3",       20, [(1, 5), (1, 3)]),       # semicolon + keyword
])
def test_semicolon_delimiter(spec, total, expected):
    assert parse_range_spec(spec, total) == expected


@pytest.mark.parametrize("spec,total", [
    (",;",         20),   # only delimiters
    ("1-5;;6-10",  20),   # double semicolon (empty piece)
    ("1-5,;6-10",  20),   # mixed empty piece
    (";1-5",       20),   # leading semicolon
    ("1-5;",       20),   # trailing semicolon
])
def test_invalid_delimiter_specs(spec, total):
    result = parse_range_spec(spec, total)
    assert isinstance(result, str)
    assert result


# --- Keywords ---

@pytest.mark.parametrize("spec,total,expected", [
    ("begin-5",         20, [(1, 5)]),
    ("start-5",         20, [(1, 5)]),
    ("first-5",         20, [(1, 5)]),
    ("15-end",          20, [(15, 20)]),
    ("15-last",         20, [(15, 20)]),
    ("begin-end",       20, [(1, 20)]),
    ("1-5, remaining",  20, [(1, 5), (6, 20)]),
    ("1-5, rest",       20, [(1, 5), (6, 20)]),
    ("remaining",       20, [(1, 20)]),               # remaining at start = everything
    ("begin-3, remaining",      10, [(1, 3), (4, 10)]),      # keyword + remaining
    ("1-3, remaining, 8-10",    10, [(1,3), (4, 10), (8, 10)]), # something after remaining
])
def test_keywords(spec, total, expected):
    assert parse_range_spec(spec, total) == expected


# --- Case and whitespace insensitivity ---

@pytest.mark.parametrize("spec", [
    "BEGIN-5",
    "Begin-5",
    "  begin  -  5  ",
    "BeGiN-5,ReMaInInG",
])
def test_case_and_whitespace_insensitive(spec):
    result = parse_range_spec(spec, 20)
    assert isinstance(result, list), f"expected list, got error: {result!r}"
    assert result[0] == (1, 5)


# --- Errors ---

@pytest.mark.parametrize("spec,total", [
    ("",            20),   # empty
    ("   ",         20),   # whitespace only
    ("abc",         20),   # non-numeric
    ("1-abc",       20),   # partial non-numeric
    ("1-middle",    20),   # unknown keyword
    ("10-5",        20),   # reversed range
    ("0-5",         20),   # zero page
    ("-1-5",        20),   # negative
    ("1-999",       20),   # exceeds total pages
    ("999",         20),   # single page exceeds total
    (",1-5",        20),   # leading delimiter
    ("1-5,",        20),   # trailing delimiter
    ("1-5,,6-10",   20),   # empty range in middle
])
def test_invalid_specs_return_error(spec, total):
    result = parse_range_spec(spec, total)
    assert isinstance(result, str), f"expected error string, got {result!r}"
    assert result  # non-empty error message


@pytest.mark.parametrize("spec,total", [
    # ... your existing cases ...
    ("1--5",        20),   # double dash
    ("1-5-7",       20),   # chained range
    ("-5",          20),   # missing start
    ("5-",          20),   # missing end
    ("-",           20),   # just a dash
    ("---",         20),   # nonsense
])
def test_invalid_specs_return_error(spec, total):
    result = parse_range_spec(spec, total)
    assert isinstance(result, str), f"expected error string, got {result!r}"
    assert result

def test_remaining_after_end_returns_empty_or_error():
    # begin-end, remaining — "remaining" after "end" is nothing.
    # Design decision: this should be an error.
    result = parse_range_spec("begin-end, remaining", 20)
    assert isinstance(result, str)


def test_overlapping_ranges_are_allowed():
    # user asked for it, they get it
    assert parse_range_spec("1-10, 5-15", 20) == [(1, 10), (5, 15)]


def test_out_of_order_ranges_are_allowed():
    assert parse_range_spec("10-15, 1-5", 20) == [(10, 15), (1, 5)]
    
def test_zero_pages_document():
    result = parse_range_spec("1", 0)
    assert isinstance(result, str)
    
