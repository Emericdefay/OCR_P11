# Std Libs:
import sys
sys.path.append('.')
# External Libs:
import pytest
# Locals Libs:
import server


class TestCheckReservedPlaces:
    """Check already booked and wanted places to reserve tests."""
    def test_correct_comp_correct_booked_correct_wanted(self):
        """Check already booked and wanted places to reserve
        With correct competition, correct booked & correct wanted places."""
        kwargs = {
            'competitionName': 'Spring Festival',
            'places_booked': 11,
            'places_wanted': 1
        }
        assert server.check_books_places(**kwargs) == 1
        
    def test_correct_comp_full_booked_and_too_many_wanted(self):
        """Check already booked and wanted places to reserve
        With correct competition, full booked and too many places wanted."""
        kwargs = {
            'competitionName': 'Spring Festival',
            'places_booked': 12,
            'places_wanted': 13
        }
        assert server.check_books_places(**kwargs) == False

    def test_correct_comp_too_many_places_wanted(self):
        """Check already booked and wanted places to reserve
        With correct competition, no booked but too many places wanted."""
        kwargs = {
            'competitionName': 'Spring Festival',
            'places_booked': 0,
            'places_wanted': 13
        }
        assert server.check_books_places(**kwargs) == False

    def test_correct_comp_places_booked_already_full(self):
        """Check already booked and wanted places to reserve
        With correct competition but full booked and one place wanted."""
        kwargs = {
            'competitionName': 'Spring Festival',
            'places_booked': 12,
            'places_wanted': 1
        }
        assert server.check_books_places(**kwargs) == False
    def test_incorrect_comp_correct_booked_correct_wanted(self):
        """Check already booked and wanted places to reserve
        Incorrect competition, correct booked and correct wanted places."""
        kwargs = {
            'competitionName': 'Bad Comp',
            'places_booked': 11,
            'places_wanted': 1
        }
        assert server.check_books_places(**kwargs) == False
        
    def test_incorrect_comp_full_booked_and_too_many_wanted(self):
        """Check already booked and wanted places to reserve
        Incorrect competition, full booked and too many places wanted."""
        kwargs = {
            'competitionName': 'Bad Comp',
            'places_booked': 12,
            'places_wanted': 13
        }
        assert server.check_books_places(**kwargs) == False

    def test_incorrect_comp_too_many_places_wanted(self):
        """Check already booked and wanted places to reserve
        Incorrect competition, no booked and too many wanted places."""
        kwargs = {
            'competitionName': 'Bad Comp',
            'places_booked': 0,
            'places_wanted': 13
        }
        assert server.check_books_places(**kwargs) == False

    def test_incorrect_comp_places_booked_already_full(self):
        """Check already booked and wanted places to reserve
        Incorrect competition, full booked and one place wanted."""
        kwargs = {
            'competitionName': 'Bad Comp',
            'places_booked': 12,
            'places_wanted': 1
        }
        assert server.check_books_places(**kwargs) == False
