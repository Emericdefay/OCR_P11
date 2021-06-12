# Std Libs:
import datetime
# Locals Libs:
import server


def substract_clubs_points(club_points: int, places_bought: int):
    """Substract the club points by places bought.
    Need to have more points than places bought
    Plus, cannot buy more than 12 places.

    Args:
        - clubs_points (int)  : Points owned by a club
        - places_bought (int) : Places bought by a club
    """
    if int(places_bought) > 12:
        return False
    if int(places_bought) < 0:
        return False
    if int(club_points) < 0:
        return False
    if int(club_points) < int(places_bought):
        return False
    return int(club_points) - int(places_bought)


def substract_comp_places(comp_places: int, places_bought: int):
    """Substract the competitions places by places bought.
    Need to have more places available than places bought
    Plus, cannot buy more than 12 places.

    Args:
        - comp_places (int)  : Places availables for a competition
        - places_bought (int) : Places bought by a club
    """
    if int(places_bought) > 12:
        return False
    if int(places_bought) < 0:
        return False
    if int(comp_places) < 0:
        return False
    if int(comp_places) < int(places_bought):
        return False
    return int(comp_places) - int(places_bought)


def check_books_places(
    clubs: list,
    competitions: list,
    competition_name: str,
    club_name: str,
    places_wanted: int
    ):
    """Check if places reserved aren't higher than 12.
    
    Args:
        - competition_name (str) : Name of the competition
        - club_name (str) : Name of the club
        - places_wanted (int) : Number of places wanted
    """
    if int(places_wanted) > 12:
        return False
    
    if int(places_wanted) < 0:
        return False

    club = [c for c in clubs if c['name'] == club_name]
    comp = [c for c in competitions if c['name'] == competition_name]

    if (not club) or (not comp):
        return False

    reserved = club[0]['competitionsReserved']
    print(reserved)
    places_booked = [int(c) for c in reserved if c['name'] == competition_name]
    places_booked = 0 if not places_booked else int(places_booked)
    places_available = comp[0]['numberOfPlaces']

    if int(places_available) <= 0:
        return False
    if int(places_booked) >= 12:
        return False
    if int(places_booked) + int(places_wanted) > 12:
        return False
    print(reserved)
    return True


def futur_competition(date_to_check):
    """Check if competition is still in future.

    Args:
        - date_to_check (str) : Date of competition
    """
    try:
        date = datetime.datetime.strptime(date_to_check,
                                          '%Y-%m-%d %H:%M:%S')
    except Exception:
        return False
    date_today = datetime.datetime.today()

    if date < date_today:
        return False
    return True
