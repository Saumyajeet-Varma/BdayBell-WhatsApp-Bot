from app.birthdays import validate_dd_mm, parse_add_command, format_birthdays, names_for_reminder

def test_valid_dates():
    assert validate_dd_mm("10-08")
    assert validate_dd_mm("29-02")
    assert not validate_dd_mm("31-02")
    assert not validate_dd_mm("00-01")
    assert not validate_dd_mm("1-1")
    assert not validate_dd_mm("12-13")

def test_parse_add_command():
    assert parse_add_command("!add Saumyajeet-Varma 10-08") == ("Saumyajeet-Varma", "10-08")
    assert parse_add_command("!add Saumyajeet Varma 10-08") == ("Saumyajeet Varma", "10-08")
    assert parse_add_command("!add 10-08") is None
    assert parse_add_command("!list") is None
    assert parse_add_command("!add Saumyajeet 31-02") is None

def test_format_birthdays():
    assert format_birthdays([]) == "No birthdays saved yet."
    assert "- Samm: 10-08" in format_birthdays([{"name": "Samm", "date": "10-08"}])

def test_names_for_reminder():
    assert names_for_reminder([{"name": "A"}]) == "A"
    assert names_for_reminder([{"name": "A"}, {"name": "B"}]) == "A and B"
    assert names_for_reminder([{"name": "A"}, {"name": "B"}, {"name": "C"}]) == "A, B and C"
