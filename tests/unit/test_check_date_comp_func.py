# Std Libs:
import datetime
import sys
sys.path.append('.')
# External libs:
import pytest
# Locals Libs:
import server


class TestCheckDate:
    """Test futur_competition func"""
    def test_check_date_(self):
        """Check if futur competition
        With a next date."""
        date_after = datetime.datetime.strptime('2022-10-22 13:30:00',
                                                '%Y-%m-%d %H:%M:%S')
        date_today = datetime.datetime.today()
        assert server.futur_competition(date_after, date_today) == True

    def test_check_date_(self):
        """Check if futur competition
        With a past date."""
        date_before =datetime.datetime.strptime('2020-10-22 13:30:00',
                                                '%Y-%m-%d %H:%M:%S')
        date_today = datetime.datetime.today()
        assert server.futur_competition(date_before, date_today) == False
     