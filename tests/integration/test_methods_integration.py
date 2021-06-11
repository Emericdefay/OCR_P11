# Std Libs:
import datetime
import sys
sys.path.append('.')
# External Libs:
import pytest
# Locals Libs:
import server
from server import (
    substract_clubs_points as sub_club,
    substract_comp_places as sub_comp,
    check_books_places as chk_book,
    futur_competition as futur_comp,
)


class Client:
    """Client app class"""
    @pytest.fixture
    def client(self):
        """Set a client test"""
        server.app.config['TESTING'] = True
        server.app.config['SERVER_NAME'] = 'TEST'

        with server.app.test_client() as client:
            with server.app.app_context():
                pass
            server.app.app_context().push()
            yield client


class TestShowSummary(Client):
    """List of booking tests"""
    def test_book_places_on_next_competitions_only(self, client):
        """Link for booking only appear on next competition."""
        competitions = server.loadCompetitions()
        form = {'email': 'john@simplylift.co'}
        rv = client.post(path='/showSummary', data=form, follow_redirects=True)
        club = "Simply%20Lift"
        for competition in competitions:
            comp_date = datetime.datetime.strptime(competition["date"],
                                                   '%Y-%m-%d %H:%M:%S')
            comp = competition['name'].replace(" ", "%20")
            strg = bytes(f'/{comp}/{club}">Book Places</a>', 'utf-8')
            if comp_date < datetime.datetime.today():
                assert rv.status_code == 200
                assert strg in rv.data
            else:
                assert rv.status_code == 200
                assert strg not in rv.data


class TestPurchasePlaces(Client):
    """Purchase places tests"""
    def test_purchase_places(self, client):
        """Purchase places
        Check if competition is in futur
        Check if enough places in competition
        Check if enough points from club"""
        clubs = server.loadClubs()
        competitions = server.loadCompetitions()

        for club in clubs:
            for comp in competitions:
                form = {
                    'competition': f'{comp["name"]}',
                    'club': f'{club["name"]}',
                    'places': '1',
                    }
                rv = client.post(
                    path='/purchasePlaces', data=form, follow_redirects=True
                    )
                
                kwargs = {
                'club_name': '',
                'competition_name': '',
                'places_booked': club['competitionsReserved'][comp['name']],
                'places_wanted': form['places']
                }

                still_book = chk_book(**kwargs)

                time_comp = comp['date']
                time_now = datetime.datetime.today()

                still_comp = futur_comp(time_comp, time_now)

                if still_book and still_comp:
                    available_places = sub_comp(
                        comp['numberOfPlaces'],
                        form['places'])
                    
                    available_points = sub_club(
                        club['points'],
                        form['places'])
                    
                    if available_points and available_places:
                        update_places = bytes(
                            f"Number of Places: {available_places}", 'utf-8')
                        update_points = bytes(
                            f"available: {available_points}", 'utf-8')
            
                        assert rv.status_code == 200
                        assert update_points in rv.data
                        assert update_places in rv.data
                    else:
                        assert rv.status_code == 200
                        assert b'Something went wrong' in rv.data
                else:
                    assert rv.status_code == 200
                    assert b'Something went wrong' in rv.data
