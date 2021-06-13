# Std Libs:
import datetime
import sys
sys.path.append('.')
# External Libs:
import pytest
import flask
# Locals Libs:
import server


class Client:
    """Client app class"""
    @pytest.fixture(scope='function')
    def client(self):
        """Set a client test"""
        server.app.testing = True
        server.clubs =  server.loadClubs()
        server.competitions = server.loadCompetitions()

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
        assert b"Sorry, that email wasn&#39;t found." in rv.data
        assert flask.request.path == '/'


class TestBook(Client):
    """Book tests"""
    def test_book_on_every_comp(self, client):
        """Book on every competitions
        Verifying Book Place button doesn't appear on past comp"""
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
                if comp_date > datetime.datetime.today():
                    assert rv.status_code == 200
                    assert b'How many places?' in rv.data
                else:
                    assert rv.status_code == 302
                    # assert b'Something went wrong' in rv.data

    def test_past_competition(self, client):
        """Past competition try book"""
        club = 'Simply Lift'
        competition = 'Fall Classic'

        rv = client.get(
            path=f"/book/{competition}/{club}",
            follow_redirects=True
        )
        assert rv.status_code == 200
        assert b'Something went wrong' in rv.data

    def test_next_competition(self, client):
        """Next competition"""
        club = 'Simply Lift'
        competition = 'Spring Festival'
        rv = client.get(
            path=f"/book/{competition}/{club}",
            follow_redirects=True
        )
        assert rv.status_code == 200
        assert b'How many places?' in rv.data

    def test_incorrect_competition(self, client):
        """Wrong path with wrong competition"""
        clubs = server.loadClubs()
        competition = 'Bad Competition'
        for club in clubs:
            rv = client.get(
                path=f"/book/{competition}/{club['name']}",
                follow_redirects=True
            )

            assert rv.status_code == 200
            assert b'Something went wrong' in rv.data

    def test_incorrect_club(self, client):
        """Wrong path with wrong club"""
        club = 'Bad Club'
        competitions = server.loadCompetitions()
        for competition in competitions:
            rv = client.get(
                path=f"/book/{competition['name']}/{club}",
                follow_redirects=True
            )
            assert rv.status_code == 200
            assert b'Something went wrong' in rv.data


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
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)

        cp_name = form['competition']
        competition = [c for c in server.competitions if c['name']==cp_name][0]
        assert int(competition['numberOfPlaces']) == 13

        cl_name = form['club']
        club = [c for c in server.clubs if c['name']==cl_name][0]
        assert int(club['points']) == 1
        print(club['competitionsReserved'])
        assert int(club['competitionsReserved']['Spring Festival']) == 12

        assert rv.status_code == 200
        assert b"<li>Confirmation:" in rv.data

    def test_multiple_correct_purchase(self, client):
        """Multiple purchase Places
        Correct competition, correct reserve and correct club."""

        form = {
            'competition': 'Spring Festival',
            # Place available : 25
            # Competition status : In preparation
            'club': 'Simply Lift',
            # Points available : 13
            'places': '1'
            # Points bought : 1
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)

        cp_name = form['competition']
        competition = [c for c in server.competitions if c['name']==cp_name][0]
        assert int(competition['numberOfPlaces']) == 24

        cl_name = form['club']
        club = [c for c in server.clubs if c['name']==cl_name][0]
        assert int(club['points']) == 12
        print(club['competitionsReserved'])
        assert int(club['competitionsReserved']['Spring Festival']) == 1

        assert rv.status_code == 200
        assert b"<li>Confirmation:" in rv.data

        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)

        cp_name = form['competition']
        competition = [c for c in server.competitions if c['name']==cp_name][0]
        assert int(competition['numberOfPlaces']) == 23

        cl_name = form['club']
        club = [c for c in server.clubs if c['name']==cl_name][0]
        assert int(club['points']) == 11
        print(club['competitionsReserved'])
        assert int(club['competitionsReserved']['Spring Festival']) == 2

        assert rv.status_code == 200
        assert b"<li>Confirmation:" in rv.data

    def test_multiple_purchase_but_not_enough_points(self, client):
        """Purchase Places but not enough points
        Correct competition, incorrect reserve and correct club."""

        form = {
            'competition': 'Spring Festival',
            # Place available : 25
            # Competition status : In preparation
            'club': 'Iron Temple',
            # Points available : 4
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)

        cp_name = form['competition']
        competition = [c for c in server.competitions if c['name']==cp_name][0]
        assert int(competition['numberOfPlaces']) == 25

        cl_name = form['club']
        club = [c for c in server.clubs if c['name']==cl_name][0]
        assert int(club['points']) == 4

        assert rv.status_code == 200
        assert b"Something went wrong" in rv.data


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
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
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
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

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
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Something went wrong' in rv.data

    def test_old_comp_correct_reserve_from_correct_club(self, client):
        """Purchase Places
        old competition, correct reserve and correct club."""
        form = {
            'competition': 'Fall Classic',
            # Place available : 13
            # Competition status : already done
            'club': 'Simply Lift',
            # Points available : 13
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Something went wrong' in rv.data

    def test_old_comp_incorrect_reserve_from_incorrect_club(self, client):
        """Purchase Places
        old competition, incorrect reserve and incorrect club."""
        form = {
            'competition': 'Fall Classic',
            # Place available : 13
            # Competition status : already done
            'club': 'Bad Club',
            # Points available : x
            'places': '13'
            # Points bought : 13
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

    def test_old_comp_correct_reserve_incorrect_club(self, client):
        """Purchase Places
        old competition, correct reserve and incorrect club."""
        form = {
            'competition': 'Fall Classic',
            # Place available : 13
            # Competition status : already done
            'club': 'Bad Club',
            # Points available : x
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

    def test_old_comp_incorrect_reserve_correct_club(self, client):
        """Purchase Places
        old competition, incorrect reserve and correct club."""
        form = {
            'competition': 'Fall Classic',
            # Place available : 13
            # Competition status : already done
            'club': 'Iron Temple',
            # Points available : 4
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Something went wrong' in rv.data

    def test_incorrect_comp_correct_reserve_from_correct_club(self, client):
        """Purchase Places
        incorrect competition, correct reserve and correct club."""
        form = {
            'competition': 'Bad Comp',
            # Place available : 13
            # Competition status : already done
            'club': 'Simply Lift',
            # Points available : 13
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

    def test_incorrect_comp_incorrect_reserve_incorrect_club(self, client):
        """Purchase Places
        incorrect competition, incorrect reserve and incorrect club."""
        form = {
            'competition': 'Bad Comp',
            # Place available : 13
            # Competition status : already done
            'club': 'Bad Club',
            # Points available : x
            'places': '13'
            # Points bought : 13
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

    def test_incorrect_comp_correct_reserve_incorrect_club(self, client):
        """Purchase Places
        incorrect competition, correct reserve and incorrect club."""
        form = {
            'competition': 'Bad Comp',
            # Place available : x
            # Competition status : x
            'club': 'Bad Club',
            # Points available : x
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data

    def test_incorrect_comp_incorrect_reserve_correct_club(self, client):
        """Purchase Places
        incorrect competition, incorrect reserve and correct club."""
        form = {
            'competition': 'Bad Comp',
            # Place available : x
            # Competition status : x
            'club': 'Iron Temple',
            # Points available : 4
            'places': '12'
            # Points bought : 12
               }
        rv = client.post(
            path='/purchasePlaces',
            data=form,
            follow_redirects=True)
        assert rv.status_code == 200
        assert b'Error:' in rv.data


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
