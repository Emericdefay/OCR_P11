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
        server.clubs =  server.loadClubs()
        server.competitions = server.loadCompetitions()

        with server.app.test_client() as client:
            with server.app.app_context():
                pass
            server.app.app_context().push()
            yield client


class TestFunctionnal(Client):
    """Purchase places tests"""
    def test_connect_and_purchase_correct(self, client):
        """
        1. login
        2. Book place on Spring Festival
        3. Reserve 12 places
        4. Check cannot click on Book place one more time
        5. Check Display Board
        6. Logout
        """
        pass