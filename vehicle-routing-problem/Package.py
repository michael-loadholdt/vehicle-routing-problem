# Class for packages
import datetime


class Package:

    def __init__(self, id, address, city, state, zipcode, deadline, weight, note=None, status='AT HUB'):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status
        self.location_id = -1
        self.truck2_only = False
        self.is_late = False
        self.has_early_deadline = False
        self.is_grouped = False
        self.wrong_addr = False
        self.no_note = True

    def set_location_id(self, id):
        self.location_id = id

    def special_notes(self):
        if self.note == 'Can only be on truck 2':
            self.truck2_only = True
            self.no_note = False
        if self.note == 'Delayed on flight---will not arrive to depot until 9:05 am':
            self.is_late = True
            self.no_note = False
        if self.note == 'Wrong address listed':
            self.wrong_addr = True
            self.no_note = False
        if self.id in ['13', '14', '15', '16', '19', '20']:
            self.is_grouped = True
            self.no_note = False
        if self.deadline != 'EOD':
            self.has_early_deadline = True
            self.no_note = False

    def get_deadline(self):
        if self.deadline == 'EOD':
            return datetime.datetime.strptime('5:00 PM', '%I:%M %p')
        else:
            return datetime.datetime.strptime(self.deadline, '%I:%M %p')

    def package_string(self):
        return 'ID: %s, ' \
               'Address: %s, ' \
               'City: %s, ' \
               'ZipCode: %s, ' \
               'Weight: %s, ' \
               'Deadline: %s, ' \
               'Status: %s, ' % (self.id,
                                 self.address,
                                 self.city,
                                 self.zipcode,
                                 self.weight,
                                 self.deadline,
                                 self.status)
