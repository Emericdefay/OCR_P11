# Std Libs:
import sys
sys.path.append('.')
# External Libs:
import pytest
# Locals Libs:
import functions
import server


class TestCheckReservedPlaces:
    """Check already booked and wanted places to reserve tests."""
    def test_correct_comp_correct_booked_correct_wanted(self):
        """Check already booked and wanted places to reserve
        With correct competition, correct booked & correct wanted places."""
        kwargs = {
            'clubs': server.loadClubs(),
            'competitions': server.loadCompetitions(),
            'club_name': 'Simply Lift',
            'competition_name': 'Spring Festival',
            'places_wanted': 1
        }
        assert functions.check_books_places(**kwargs) == 1
        
    def test_correct_comp_full_booked_and_too_many_wanted(self):
        """Check already booked and wanted places to reserve
        With correct competition, full booked and too many places wanted."""
        kwargs = {
            'clubs': server.loadClubs(),
            'competitions': server.loadCompetitions(),
            'club_name': 'Simply Lift',
            'competition_name': 'Spring Festival',
            'places_wanted': 13
        }
        assert functions.check_books_places(**kwargs) == False

    def test_correct_comp_too_many_places_wanted(self):
        """Check already booked and wanted places to reserve
        With correct competition, no booked but too many places wanted."""
        kwargs = {
            'clubs': server.loadClubs(),
            'competitions': server.loadCompetitions(),
            'club_name': 'Simply Lift',
            'competition_name': 'Spring Festival',
            'places_wanted': 13
        }
        assert functions.check_books_places(**kwargs) == False

    def test_correct_comp_places_booked_already_full(self):
        """Check already booked and wanted places to reserve
        With correct competition but full booked and one place wanted."""
        kwargs = {
            'clubs': server.loadClubs(),
            'competitions': server.loadCompetitions(),
            'club_name': 'Simply Lift',
            'competition_name': 'Spring Festival',
            'places_wanted': 1
        }
        assert functions.check_books_places(**kwargs) == True
    def test_incorrect_comp_correct_booked_correct_wanted(self):
        """Check already booked and wanted places to reserve
        Incorrect competition, correct booked and correct wanted places."""
        kwargs = {
            'clubs': server.loadClubs(),
            'competitions': server.loadCompetitions(),
            'club_name': 'Simply Lift',
            'competition_name': 'Bad Comp',
            'places_wanted': 1
        }
        assert functions.check_books_places(**kwargs) == False
        
    def test_incorrect_comp_full_booked_and_too_many_wanted(self):
        """Check already booked and wanted places to reserve
        Incorrect competition, full booked and too many places wanted."""
        kwargs = {
            'clubs': server.loadClubs(),
            'competitions': server.loadCompetitions(),
            'club_name': 'Simply Lift',
            'competition_name': 'Bad Comp',
            'places_wanted': 13
        }
        assert functions.check_books_places(**kwargs) == False

    def test_incorrect_comp_too_many_places_wanted(self):
        """Check already booked and wanted places to reserve
        Incorrect competition, no booked and too many wanted places."""
        kwargs = {
            'clubs': server.loadClubs(),
            'competitions': server.loadCompetitions(),
            'club_name': 'Simply Lift',
            'competition_name': 'Bad Comp',
            'places_wanted': 13
        }
        assert functions.check_books_places(**kwargs) == False

    def test_incorrect_comp_places_booked_already_full(self):
        """Check already booked and wanted places to reserve
        Incorrect competition, full booked and one place wanted."""
        kwargs = {
            'clubs': server.loadClubs(),
            'competitions': server.loadCompetitions(),
            'club_name': 'Simply Lift',
            'competition_name': 'Bad Comp',
            'places_wanted': 1
        }
        assert functions.check_books_places(**kwargs) == False
