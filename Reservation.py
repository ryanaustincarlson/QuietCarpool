
import random


class Reservation:
    def __init__(self, event, db=None):
        self.event = event
        self.rideshares = {}
        self.rideshare_requests = {}

        self.possible_matches = set()

        self._id = None
        if db:
            self._id = db.reservations.insert(
                {'event_id': event._id,
                 'rideshares': [],
                 'requests': []
                 })

    def get_open_rideshares(self, seats_needed):
        open_rideshares = set()
        for rideshare_id in self.rideshares:
            rideshare = self.rideshares[rideshare_id]
            if rideshare.seats_available() >= seats_needed:
                open_rideshares.add((rideshare, rideshare_id))
        return open_rideshares

    def get_rideshare_request_matches(self, rideshare):
        matches = set()
        for request_id in self.rideshare_requests:
            rideshare_request = self.rideshare_requests[request_id]

            if rideshare_request.requester in rideshare.riders:
                continue

            if rideshare in rideshare_request.acceptable_rideshares:
                matches.add((rideshare_request, request_id))

        return matches

    def make_reservation(self, rideshare, reserver):
        rideshare.reserve_seat(reserver)

    def register_rideshare(self, rideshare):
        rideshare_id = Reservation.generate_uuid()
        self.rideshares[rideshare_id] = rideshare
        return rideshare_id

    def register_rideshare_request(self, rideshare_request):
        request_id = Reservation.generate_uuid()
        self.rideshare_requests[request_id] = rideshare_request
        return request_id

    def people(self):  # TODO: test that this works..
        people = set()
        for rideshare in self.rideshares:
            people.add(rideshare.ride_sharer)
            for rider in rideshare.riders:
                people.add(rider)
        return people

    @staticmethod
    def generate_uuid():
        return str(random.randint(10, 10000))
