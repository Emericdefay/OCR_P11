# Std Libs:
import sys
sys.path.append('.')
# External libs:
import pytest  # noqa: F401, E402
# Locals Libs:
from functions import futur_competition  # noqa: E402


class TestCheckDate:
    """Test futur_competition func"""
    def test_check_date_next(self):
        """Check if futur competition
        With a next date."""
        date_after = '2022-10-22 13:30:00'
        assert futur_competition(date_after) is True

    def test_check_date_past(self):
        """Check if futur competition
        With a past date."""
        date_before = '2020-10-22 13:30:00'
        assert futur_competition(date_before) is False

    def test_check_date_wrong(self):
        """Check if futur competition
        With a past date."""
        wrong_date = "wrong date"
        assert futur_competition(wrong_date) is False
