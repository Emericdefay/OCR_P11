# Std Libs:
import sys
sys.path.append('.')
# External Libs:
import pytest
# Locals Libs:
import server


class Client:
    """"""
    @pytest.fixture
    def client(self):
        """"""
        server.app.config['TESTING'] = True
        server.app.config['SERVER_NAME'] = 'TEST'

        with server.app.test_client() as client:
            with server.app.app_context():
                pass
            server.app.app_context().push()
            yield client


class TestBook(Client):
    """"""
    def test_get_books_from_own_mail(self, client):
        """"""
        # Connect with
        form = {'email': 'not@authorized.secretary'}
        # Get competitions
        competitions = server.loadCompetitions()
        clubs = server.loadClubs()
        for club in clubs:
            for competition in competitions:
                rv = client.get(
                    path=f'/book/{competition["name"]}/{club["name"]}'
                    )
                if club['email'] == form['email']:
                    assert rv.status_code == 200
                    assert b'Places availables' in rv.data
                else:
                    assert rv.status_code == 405
