# Std Libs:
import sys
sys.path.append('.')
# External Libs:
import pytest  # noqa: F401, E402
# Locals Libs:
import server  # noqa: E402


class Client:
    """Client app class"""
    @pytest.fixture
    def client(self):
        """Set a client test"""
        server.app.config['TESTING'] = True
        server.app.config['SERVER_NAME'] = 'TEST'
        server.clubs = server.loadClubs()
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
        # 1. Login
        form = {'email': 'john@simplylift.co'}
        rv = client.post(path='/showSummary', data=form, follow_redirects=True)
        assert b'simplylift.co' in rv.data
        assert rv.status_code == 200

        # 2. Book places on Spring Festival
        competition = "Spring Festival"
        club = "Simply Lift"

        rv = client.get(
            path=f'book/{competition}/{club}',
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'How many places?' in rv.data

        # 3. Reserve 12 places
        form = {
            "competition": competition,
            "club": club,
            "places": 12,
        }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)

        assert rv.status_code == 200
        assert b'Confirmation' in rv.data

        # 4. Check cannot click on Book Place button
        strg = bytes(f'/{competition}/{club}">Book Places</a>', 'utf-8')
        assert rv.status_code == 200
        assert strg not in rv.data

        # 5. Check display board to see updates
        awaited_points = 1
        rv = client.get(path='/displayBoard', follow_redirects=True)
        strg = bytes(f'{club} : {awaited_points}', 'utf-8')
        assert rv.status_code == 200
        assert strg in rv.data

        # 6. Logout
        rv = client.get(path='/logout', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Welcome to the GUDLFT Registration Portal!' in rv.data
