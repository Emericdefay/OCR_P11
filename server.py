import json
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   flash,
                   url_for)
from functions import (substract_clubs_points as sub_club,
                       substract_comp_places as sub_comp,
                       check_books_places as chk_book,
                       futur_competition as next_comp)


def loadClubs():
    """"""
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    """"""
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    """"""
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """Show the summary if email is registered.
    If not, redirect to '/' 
    """
    try:
        email = request.form['email']
        club = [club for club in clubs if club['email'] == email][0]
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions)
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return redirect('/', 302)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """"""
    try:
        found_club = [c for c in clubs if c['name'] == club][0]
        found_comp = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)
    points_available = int(found_club['points'])
    return render_template('booking.html',
                            club=found_club,
                            competition=found_comp,
                            max=min(points_available, 12))


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    """"""
    try:
        form_comp = request.form['competition']
        form_club = request.form['club']
        competition = [c for c in competitions if c['name'] == form_comp][0]
        club = [c for c in clubs if c['name'] == form_club][0]
    except IndexError:
        flash('Error: try to access unknown path.')
        return redirect('/', 302)
    
    comp_name = competition['name']
    club_name = club['name']
    
    places_required = int(request.form['places'])

    able_to_buy = chk_book(clubs,
                           competitions,
                           comp_name,
                           club_name,
                           places_required)
    
    if able_to_buy:
        comp_places = int(competition['numberOfPlaces'])
        places_still_av = sub_comp(comp_places, places_required)
        points_club = sub_club(club['points'], places_required)
        print(places_still_av, points_club)
        if places_still_av and points_club:
            competition['numberOfPlaces'] = places_still_av
            if comp_name in club['competitionsReserved']:
                club['competitionsReserved'][comp_name] += places_required
                print(club['competitionsReserved'])
            else:
                club['competitionsReserved'][comp_name] = 0

            flash(f'Confirmation: {places_required} places reserved.')
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions)
        else:
            flash('Something went wrong-please try again')
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions)
    else:
        flash('Something went wrong-please try again')
        return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    """"""
    return redirect(url_for('index'))
