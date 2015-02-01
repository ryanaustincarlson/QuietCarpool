
import pdb
import pickle

from flask import Flask, request, redirect, render_template
app = Flask(__name__)

from Person import Person
from Event import Event
from Reservation import Reservation
from ReservationManager import ReservationManager

PICKLE_FNAME = 'reservation-manager.pickle'

# try:
#     with open(PICKLE_FNAME, 'r') as f:
#         manager = pickle.load(f)
# except:
manager = ReservationManager()
manager.reservation_map['1'] = Reservation(Event('partytime', Person('Roberto', 'a@a.com')))


@app.route('/')
def index():
    return open('create_event.html', 'r').read()


@app.route('/event/', methods=['POST'])
@app.route('/event/<event_id>/', methods=['GET'])
def event(event_id=None):
    print('event_id:', event_id)
    if event_id is None:
        organizer_name = request.form['org_name']
        organizer_email = request.form['org_email']
        organizer = Person(name=organizer_name,
                           email=organizer_email)

        # create an event
        event_name = request.form['event_name']
        event = Event(event_name, organizer)

        location = request.form['location']
        event.location = location if len(location) > 0 else None

        event_id = manager.register_event(event)
        # serialize_manager()
        # print(url_for('event/{}'.format(event_id)))
        return redirect('/event/{}'.format(event_id))
    else:
        reservation = manager.reservation_map[event_id]
        return render_template('event.html',
                               event_name=reservation.event.name,
                               org_name=reservation.event.organizer.name)


@app.route('/event/<event_id>/need_a_ride', methods=['POST'])
def need_a_ride(event_id=None):
    return 'You Need A Ride'

@app.route('/event/<event_id>/have_a_ride', methods=['POST'])
def have_a_ride(event_id=None):
    return 'You can offer rides'

def serialize_manager():
    with open(PICKLE_FNAME, 'w') as f:
        pickle.dump(f)

if __name__ == '__main__':
    app.run(debug=True)