# Class for Truck Objects
from Package import Package


class Truck:

    def __init__(self, truck_num):
        self.truck_num = truck_num
        self.truck_package_weight = 0
        self.truck_package_list = []
        self.truck_miles = 0
        self.current_location = 0
        self.released = False
        self.first_trip = True
        self.distance_to_next_delivery = 0

    def load_package(self, package: Package):
        if len(self.truck_package_list) < 16:
            package.status = 'Loaded on Truck #' + str(self.truck_num)
            self.truck_package_list.append(package)
            return 'Loaded\n'
        else:
            return 'Truck full\n'

    def view_truck_status(self):
        package: Package
        s = ''
        for package in self.truck_package_list:
            s += 'ID: %s, Address: %s, City: %s, State: %s, Zip: %s, Weight: %s, Status: %s Deadline: %s\n' % (package.id,
                                                                                                              package.address,
                                                                                                              package.city,
                                                                                                              package.state,
                                                                                                              package.zipcode,
                                                                                                              package.weight,
                                                                                                              package.status,
                                                                                                              package.get_deadline())
        return s
