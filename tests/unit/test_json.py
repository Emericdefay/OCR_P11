# Std Libs:
import sys
# External libs:
import pytest  # noqa: F401
# Locals Libs:
from server import loadClubs, loadCompetitions
sys.path.append('.')


class TestJSON:
    """Test if json functions are correct."""
    def test_json_clubs(self):
        """Test if loadClubs() returns correct JSON."""
        clubs = [
            {
                'name': 'Simply Lift',
                'email': 'john@simplylift.co',
                'points': '13',
                'competitionsReserved': {}
            },
            {
                'name': 'Iron Temple',
                'email': 'admin@irontemple.com',
                'points': '4',
                'competitionsReserved': {}
            },
            {
                'name': 'She Lifts',
                'email': 'kate@shelifts.co.uk',
                'points': '12',
                'competitionsReserved': {}
            }
        ]
        assert loadClubs() == clubs

    def test_json_competitions(self):
        """Test if loadCompetitions() returns correct JSON."""
        competitions = [
            {
                'name': 'Spring Festival',
                'date': '2022-03-27 10:00:00',
                'numberOfPlaces': '25'
            },
            {
                'name': 'Fall Classic',
                'date': '2020-10-22 13:30:00',
                'numberOfPlaces': '13'
            }
        ]
        assert loadCompetitions() == competitions
