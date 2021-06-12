# Std Libs:
import datetime
import sys
sys.path.append('.')
# External Libs:
import pytest
# Locals Libs:
import server
from functions import (
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
                'places_wanted': form['places']
                }

                still_book = chk_book(**kwargs)

                time_comp = comp['date']

                still_comp = futur_comp(time_comp)

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
