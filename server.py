from datetime import datetime
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


@app.route('/showSummary', methods=['POST', 'GET'])
def showSummary():
    """Show the summary if email is registered.
    If not, redirect to '/' 
    """
    try:
        email = request.form['email']
        club = [club for club in clubs if club['email'] == email][0]
        next_comps = [c for c in competitions if next_comp(c['date'])]
        reservations = club['competitionsReserved']
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions,
            next_competitions=next_comps,
            reservations=reservations)
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return redirect('/', 302)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """"""
    try:
        found_club = [c for c in clubs if c['name'] == club][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return redirect("/")
    try:
        found_comp = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        next_comps = [c for c in competitions if next_comp(c['date'])]
        print(found_club['competitionsReserved'])
        reservations = found_club['competitionsReserved']
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                            club=club,
                            competitions=competitions,
                            next_competitions=next_comps,
                            reservations=reservations)

    competition_not_happened = next_comp(found_comp['date'])
    if competition_not_happened:
        points_available = int(found_club['points'])
        return render_template('booking.html',
                                club=found_club,
                                competition=found_comp,
                                max=min(points_available, 12))
    else:
        flash("Something went wrong-please try again")
        return redirect('/')


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    """Purchase places from competition with club's points.
    Check if club is able to buy those places.
    Check if competition not happened yet."""
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
    
    competition_not_happened = next_comp(competition['date'])

    if able_to_buy and competition_not_happened:
        comp_places = int(competition['numberOfPlaces'])
        places_still_av = sub_comp(comp_places, places_required)
        points_club = sub_club(club['points'], places_required)
        if places_still_av and points_club:
            competition['numberOfPlaces'] = places_still_av
            club['points'] = points_club
            if comp_name in club['competitionsReserved']:
                club['competitionsReserved'][comp_name] += places_required
            else:
                club['competitionsReserved'][comp_name] = places_required
            
            next_comps = [c for c in competitions if next_comp(c['date'])]
            reservations = club['competitionsReserved']
            flash(f'Confirmation: {places_required} places reserved.')
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions,
                                   next_competitions=next_comps,
                                   reservations=reservations)
        else:
                
            next_comps = [c for c in competitions if next_comp(c['date'])]
            reservations = club['competitionsReserved']
            
            flash('Something went wrong-please try again')
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions,
                                   next_competitions=next_comps,
                                   reservations=reservations)
    else:
        next_comps = [c for c in competitions if next_comp(c['date'])]
        reservations = club['competitionsReserved']
        flash('Something went wrong-please try again')
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               next_competitions=next_comps,
                               reservations=reservations)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    """"""
    return redirect(url_for('index'))
