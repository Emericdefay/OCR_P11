# Std Libs:
import datetime
import sys
sys.path.append('.')
# External Libs:
import pytest
# Locals Libs:
import server


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


class TestIndex(Client):
    """Show index test"""

    def test_get_index(self, client):
        """Show index"""
        rv = client.get(path='/')
        assert rv.status_code == 200
        assert b'Welcome to the GUDLFT Registration Portal!' in rv.data


class TestShowSummary(Client):
    """Show summary tests"""
    def test_post_index_correct(self, client):
        """Show summary
        Correct email form."""
        form = {'email': 'john@simplylift.co'}
        rv = client.post(path='/showSummary', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Welcome, john@simplylift.co' in rv.data

    def test_post_index_fail(self, client):
        """Show summary
        Incorrect email form."""
        form = {'email': 'not@authorized.secretary'}
        rv = client.post(path='/showSummary', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b"Sorry, that email wasn't found." not in rv.data


class TestBook(Client):
    """"""
    def test_get_books_from_own_mail(self, client):
        """"""
        # Get competitions
        competitions = server.loadCompetitions()
        clubs = server.loadClubs()
        for club in clubs:
            for competition in competitions:
                rv = client.get(
                    path=f'/book/{competition["name"]}/{club["name"]}'
                )
                comp_date = datetime.datetime.strptime(competition["date"],
                                                       '%Y-%m-%d %H:%M:%S')
                if comp_date < datetime.datetime.today:
                    assert rv.status_code == 200
                    assert b'Places availables' in rv.data
                else:
                    assert rv.status_code == 302
                    # assert b'Something went wrong' in rv.data



class TestPurchasePlaces(Client):
    """Purchase Places tests"""
    def test_correct_comp_correct_reserve_correct_club(self, client):
        """Purchase Places
        Correct competition, correct reserve and correct club."""
        form = {
            'competition': 'Spring Festival',
            # Place available : 25
            # Competition status : In preparation
            'club': 'Simply Lift',
            # Points available : 13
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(path='/purchasePlaces', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Confirmation:' in rv.data

    def test_correct_club_incorrect_reserve_incorrect_club(self, client):
        """Purchase Places
        Correct competition, incorrect reserve and incorrect club."""
        form = {
            'competition': 'Spring Festival',
            # Place available : 25
            # Competition status : In preparation
            'club': 'Bad Club',
            # Points available : x
            'places': '13'
            # Points bought : 13
               }
        rv = client.post(path='/purchasePlaces', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

    def test_correct_comp_correct_reserve_incorrect_club(self, client):
        """Purchase Places
        Correct competition, correct reserve and incorrect club."""
        form = {
            'competition': 'Spring Festival',
            # Place available : 25
            # Competition status : In preparation
            'club': 'Bad Club',
            # Points available : x
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(path='/purchasePlaces', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Something went wrong' in rv.data

    def test_correct_comp_incorrect_reserve_correct_club(self, client):
        """Purchase Places
        Correct competition, incorrect reserve and correct club."""
        form = {
            'competition': 'Spring Festival',
            # Place available : 25
            # Competition status : In preparation
            'club': 'Simply Lift',
            # Points available : 13
            'places': '13'
            # Points bought : 13
               }
        rv = client.post(path='/purchasePlaces', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

    def test_incorrect_comp_correct_reserve_from_correct_club(self, client):
        """Purchase Places
        Incorrect competition, correct reserve and correct club."""
        form = {
            'competition': 'Fall Classic',
            # Place available : 13
            # Competition status : already done
            'club': 'Simply Lift',
            # Points available : 13
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(path='/purchasePlaces', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

    def test_incorrect_comp_incorrect_reserve_from_incorrect_club(self, client):
        """Purchase Places
        Incorrect competition, incorrect reserve and incorrect club."""
        form = {
            'competition': 'Fall Classic',
            # Place available : 13
            # Competition status : already done
            'club': 'Bad Club',
            # Points available : x
            'places': '13'
            # Points bought : 13
               }
        rv = client.post(path='/purchasePlaces', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Something went wrong' in rv.data

    def test_incorrect_comp_correct_reserve_incorrect_club(self, client):
        """Purchase Places
        Incorrect competition, correct reserve and incorrect club."""
        form = {
            'competition': 'Bad Comp',
            # Place available : x
            # Competition status : x
            'club': 'Bad Club',
            # Points available : x
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(path='/purchasePlaces', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Something went wrong' in rv.data

    def test_incorrect_comp_incorrect_reserve_correct_club(self, client):
        """Purchase Places
        Incorrect competition, incorrect reserve and correct club."""
        form = {
            'competition': 'Bad Comp',
            # Place available : x
            # Competition status : x
            'club': 'Iron Temple',
            # Points available : 4
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(path='/purchasePlaces', data=form, follow_redirects=True)
        assert rv.status_code == 200
        assert b'Something went wrong' in rv.data


class TestDisplayBoard(Client):
    """Display Board unit test"""
    def test_display_board(self, client):
        """Display Board without login"""
        rv = client.get(path='/displayBoard')
        assert rv.status_code == 200
        assert b'List of clubs' in rv.data


class TestLogout(Client):
    """Logout feature unit test"""
    def test_logout_without_login(self, client):
        """Logout without login."""
        rv = client.get(path='/logout', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Welcome to the GUDLFT Registration Portal!' in rv.data
