# Std Libs:
import sys
sys.path.append('.')
# External Libs:
import pytest  # noqa: F401, E402
# Locals Libs:
import functions  # noqa: E402


class TestSubstractionsClubPoints:
    """Substract club's points tests"""
    def test_substraction_clubs_points_with_enough_points_to_buy_places(self):
        """Substraction of club's points
        With correct amount of points and correct places reserved."""
        kwargs = {
            'club_points': 13,
            'places_bought': 12
        }
        assert functions.substract_clubs_points(**kwargs) == 1

    def test_substraction_clubs_points_enough_points_but_to_many_places(self):
        """Substraction of club's points
        But to much places bought"""
        kwargs = {
            'club_points': 13,
            'places_bought': 13
        }
        assert functions.substract_clubs_points(**kwargs) is False

    def test_substraction_clubs_points_not_enough_points_to_buy_places(self):
        """Substraction of club's points
        But not enought points from club."""
        kwargs = {
            'club_points': 10,
            'places_bought': 12
        }
        assert functions.substract_clubs_points(**kwargs) is False

    def test_substraction_clubs_points_not_enough_points_to_many_places(self):
        """Substraction of club's points
        But to many places bought with not enough points from club."""
        kwargs = {
            'club_points': 10,
            'places_bought': 13
        }
        assert functions.substract_clubs_points(**kwargs) is False


class TestSubstractionCompPlaces:
    """Substract Competition places tests"""
    def test_substraction_enough_places_correct_reserve(self):
        """Substraction of competition places
        With correct places bought with enough comp places."""
        kwargs = {
            'comp_places': 13,
            'places_bought': 12
        }
        assert functions.substract_comp_places(**kwargs) == 1

    def test_substraction_enough_place_to_much_reserve(self):
        """Substraction of competition places
        But to many reservations."""
        kwargs = {
            'comp_places': 13,
            'places_bought': 13
        }
        assert functions.substract_comp_places(**kwargs) is False

    def test_substraction_not_enough_places_correct_reserve(self):
        """Substraction of competition places
        But not enough place at competition for this reservation."""
        kwargs = {
            'comp_places': 11,
            'places_bought': 12
        }
        assert functions.substract_comp_places(**kwargs) is False

    def test_substraction_not_place_to_reserve(self):
        """Substraction of competition places
        But no place to reserve."""
        kwargs = {
            'comp_places': 0,
            'places_bought': 1
        }
        assert functions.substract_comp_places(**kwargs) is False
