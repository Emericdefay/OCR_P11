# Std Libs:
import datetime
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
            if comp_date > datetime.datetime.today():
                assert rv.status_code == 200
                assert strg in rv.data
            else:
                assert rv.status_code == 200
                assert strg not in rv.data


class TestBook(Client):
    """Integration Book tests"""
    def test_maximum_buy(self, client):
        """Test maximum amount of place able to buy"""
        club = 'Simply Lift'
        competitition = 'Spring Festival'
        path = f'book/{competitition}/{club}'
        coeff = server.coeff
        rv = client.get(path=path, follow_redirects=True)
        assert rv.status_code == 200
        max_first_check = bytes(f'max="{12//coeff}"/>', "utf-8")
        assert max_first_check in rv.data

        form = {
            'competition': competitition,
            'club': club,
            'places': 1,
            }
        client.post(path='/purchasePlaces', data=form, follow_redirects=True)

        rv = client.get(path=path, follow_redirects=True)
        assert rv.status_code == 200
        max_second_check = bytes(f'max="{(12-(1*coeff))//coeff}"/>', "utf-8")
        assert max_second_check in rv.data


class TestPurchasePlaces(Client):
    """Purchase places tests"""
    def test_purchase_places_correct_club_and_comp_and_places(self, client):
        """Purchase places
        Correct execution"""
        coeff = server.coeff
        club = 'Simply Lift'
        # Available points : 13
        competition = 'Spring Festival'
        # Available places : 25
        nb_places = 12//coeff
        awaited_places = 25 - (nb_places)
        awaited_points = 1

        clubs = server.loadClubs()
        competitions = server.loadCompetitions()
        comp = [c for c in competitions if c['name'] == competition]
        club = [c for c in clubs if c['name'] == club]

        form = {'email': 'john@simplylift.co'}
        client.post(path='/showSummary', data=form, follow_redirects=True)

        form = {
            'competition': f'{comp[0]["name"]}',
            'club': f'{club[0]["name"]}',
            'places': nb_places,

            }
        rv = client.post(
            path='/purchasePlaces', data=form, follow_redirects=True
            )

        update_places = bytes(f"Number of Places: {awaited_places}", 'utf-8')
        update_points = bytes(f"available: {awaited_points}", 'utf-8')

        assert rv.status_code == 200
        assert update_points in rv.data
        assert update_places in rv.data
        assert b'Confirmation:' in rv.data

    def test_purchase_places_too_many_places_reserved(self, client):
        """Purchase places
        Too many places reserved."""
        club = 'Simply Lift'
        # Available points : 13
        competition = 'Spring Festival'
        # Available places : 25
        nb_places = 13
        awaited_places = 25
        awaited_points = 13

        clubs = server.loadClubs()
        competitions = server.loadCompetitions()
        comp = [c for c in competitions if c['name'] == competition]
        club = [c for c in clubs if c['name'] == club]

        form = {'email': 'john@simplylift.co'}
        client.post(path='/showSummary', data=form, follow_redirects=True)
        form = {
            'competition': f'{comp[0]["name"]}',
            'club': f'{club[0]["name"]}',
            'places': nb_places,

            }
        rv = client.post(
            path='/purchasePlaces', data=form, follow_redirects=True
            )

        update_places = bytes(f"Number of Places: {awaited_places}", 'utf-8')
        update_points = bytes(f"available: {awaited_points}", 'utf-8')

        assert rv.status_code == 200
        assert update_points in rv.data
        assert update_places in rv.data
        assert b'Something went wrong' in rv.data


class TestDisplayBoardUpdate(Client):
    """Display properly working tests"""
    def test_update_points_then_check_board_too_much_reserved(self, client):
        """Check display board when update points from club"""
        club = 'Simply Lift'
        # Available points : 13
        competition = 'Spring Festival'
        # Available places : 25
        nb_places = 13
        awaited_points = 13

        comp = [c for c in server.competitions if c['name'] == competition][0]
        club = [c for c in server.clubs if c['name'] == club][0]

        form = {'email': 'john@simplylift.co'}
        client.post(path='/showSummary', data=form, follow_redirects=True)
        form = {
            'competition': f'{comp["name"]}',
            'club': f'{club["name"]}',
            'places': nb_places,

            }
        client.post(
            path='/purchasePlaces', data=form, follow_redirects=True
            )

        rv = client.get(
            path='/displayBoard', follow_redirects=True
        )

        update_points = bytes(f"{club['name']} : {awaited_points}", 'utf-8')

        assert update_points in rv.data

    def test_update_points_then_check_board_12_places_reserved(self, client):
        """Check display board when update points from club"""
        club = 'Simply Lift'
        # Available points : 13
        competition = 'Spring Festival'
        # Available places : 25
        nb_places = 12
        awaited_points = 1

        comp = [c for c in server.competitions if c['name'] == competition][0]
        club = [c for c in server.clubs if c['name'] == club][0]

        form = {'email': 'john@simplylift.co'}
        client.post(path='/showSummary', data=form, follow_redirects=True)
        form = {
            'competition': f'{comp["name"]}',
            'club': f'{club["name"]}',
            'places': nb_places,

            }
        client.post(
            path='/purchasePlaces', data=form, follow_redirects=True
            )

        rv = client.get(
            path='/displayBoard', follow_redirects=True
        )

        update_points = bytes(f"{club['name']} : {awaited_points}", 'utf-8')
        assert update_points in rv.data


class TestLoginLogout(Client):
    """Login then Logout test"""
    def test_login_logout(self, client):
        """Check login/logout"""
        form = {'email': 'john@simplylift.co'}
        client.post(path='/', data=form, follow_redirects=True)
        rv = client.get(path='/logout', follow_redirects=True)
        assert rv.status_code == 200
        assert b'Welcome to the GUDLFT Registration Portal!' in rv.data
