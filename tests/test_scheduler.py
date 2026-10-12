from datetime import datetime
from zoneinfo import ZoneInfo
from app.scheduler import tomorrow_dd_mm

def test_tomorrow_date_timezone():
    now = datetime(2026, 10, 12, 21, 59, tzinfo=ZoneInfo("Asia/Kolkata"))
    assert tomorrow_dd_mm(now, "Asia/Kolkata") == "13-10"

def test_month_boundary():
    now = datetime(2026, 12, 31, 22, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
    assert tomorrow_dd_mm(now, "Asia/Kolkata") == "01-01"
