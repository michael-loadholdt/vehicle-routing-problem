# Michael Loadholdt - Student ID# 001035593
import csv
import math

from Graph import Graph, Vertex
from HashTable import HashTable
from Package import Package
from Truck import Truck

package_table = HashTable()
location_list = []
distance_matrix = []
package_list = []
visited = [0]
city_map = Graph()
truck2 = Truck(2)
time = [8, 0]
HUB = 0


def get_location_id(package: Package):
    address_str = '%s' % package.address
    package.location_id = location_list.index(address_str)
    return package.location_id


with open('AddressList.csv', 'r', encoding='utf-8-sig') as address_file:
    csv_reader = csv.DictReader(address_file)

    for row in csv_reader:
        location_list.append(row['Location'])
        city_map.add_vertex(Vertex(location_list.index(row['Location'])))

with open('DistanceTable.csv', 'r', encoding='utf-8-sig') as distance_file:
    csv_reader = csv.reader(distance_file)

    for row in csv_reader:
        distance_matrix.append(row)

    for i in range(len(distance_matrix[0])):
        for j in range(len(distance_matrix[0])):
            city_map.add_edge(city_map.get_vertex(i), city_map.get_vertex(j), distance_matrix[i][j])

with open('WGUPS Package File.csv', 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        package = Package(row['Package ID'],
                          row['Address'],
                          row['City'],
                          row['State'],
                          row['Zip'],
                          row['Delivery Deadline'],
                          row['Weight'],
                          row['Special Notes'])
        package_table.hash_insert(package.id, package)
        package.set_location_id(get_location_id(package))
        package.special_notes()
        package_list.append(package)

early_delivery = []
for package in package_list:
    if package.has_early_deadline and not package.is_late:
        early_delivery.append(package)
    if package.is_grouped and package not in early_delivery:
        early_delivery.append(package)

late_arrivals_early_deadline = []
late_arrivals = []
for package in package_list:
    if package.is_late and package.has_early_deadline:
        late_arrivals_early_deadline.append(package)
    if package.is_late:
        if package not in late_arrivals_early_deadline:
            late_arrivals.append(package)

no_notes = []
for package in package_list:
    if package.no_note or package.truck2_only or package.wrong_addr:
        no_notes.append(package)

def package_sort(unsorted_pkg_list):
    sorted_list = []
    current_location = HUB
    while len(unsorted_pkg_list) > 0:
        shortest = math.inf
        for package in unsorted_pkg_list:
            if float(distance_matrix[current_location][get_location_id(package)]) < shortest:
                shortest = float(distance_matrix[current_location][get_location_id(package)])
                if shortest.is_integer():
                    shortest = int(shortest)
                closest_package = package

        sorted_list.append(closest_package)
        current_location = distance_matrix[current_location].index(str(shortest))
        unsorted_pkg_list.remove(closest_package)
    return sorted_list


early_delivery = package_sort(early_delivery)
no_notes = package_sort(no_notes)
late_arrivals.extend(no_notes)
remaining_packages = package_sort(late_arrivals)
sorted_package_list = []
sorted_package_list.extend(early_delivery)
sorted_package_list.extend(late_arrivals_early_deadline)
sorted_package_list.extend(late_arrivals)
sorted_package_list.extend(remaining_packages)

load1 = [sorted_package_list[i] for i in range(16)]
load2 = [sorted_package_list[i] for i in range(14, 30)]
load3 = [sorted_package_list[i] for i in range(30, 40)]

# for package in load1:
#     print(package.package_string())
# print()
# for package in load2:
#     print(package.package_string())
# print()
# for package in load3:
#     print(package.package_string())
# print()


# Delivers packages.
def run_truck(truck, timeparam=None):

    miles_per_minute = 0.3  # Distance a truck drives in one minute.

    # Handles actual delivery of the packages.  Begins by updating the package delivery status to delivered.
    # Then checks if there are any packages still on the truck.  If no, the truck is returned to Hub and the
    # loop is broken.  Else, the next package in the list is checked and it's Location ID is returned.  We
    # get the distance between our current location and the location that was just returned.  If this distance
    # is 0 the while loop executes again.  Else the loop is broken.
    def multiple_packages_at_address():

        all_packages = False
        while not all_packages:
            update_delivery_status()
            package_table.hash_update(truck.truck_package_list[0])
            current_delivery = truck.truck_package_list.pop(0).location_id

            if len(truck.truck_package_list) == 0:
                all_packages = True
                return_to_hub()
            else:
                next_delivery = truck.truck_package_list[0].location_id
                truck.distance_to_next_delivery = city_map.get_distance_by_address(current_delivery, next_delivery)
                if float(truck.distance_to_next_delivery) > 0 and all_packages is False:
                    truck.distance_to_next_delivery = float(truck.distance_to_next_delivery) + miles_over_destination
                    all_packages = True
        return 0

    # Updates package status to Delivered and notes the time of delivery.
    def update_delivery_status():
        if len(truck.truck_package_list) > 0:
            truck.truck_package_list[0].status = 'Delivered at ' + str(current_time)

    # Returns truck to the Hub once all packages are delivered.
    def return_to_hub():
        truck.current_location = HUB
        update_delivery_status()
        if len(truck.truck_package_list) > 0:
            package_table.hash_update(truck.truck_package_list[0])
            truck.distance_to_next_delivery = city_map.get_distance_by_address(
                truck.truck_package_list.pop(0).location_id, 0)

    def run_print_time():
        # Takes time from time array and converts it to normal time format.
        clock_increment()
        current_time = "%02d:%02d" % (time[0], time[1])
        return current_time

    # Updates package status to in route.
    for package in truck.truck_package_list:
        package.status = 'In Route on Truck %d' % truck.truck_num

    # Tracks time and distance driven.  This while loop is how the truck moves from one location to the next.
    # For each iteration the clock it incremented one minute, 0.3 miles is added to the truck mileage total.
    # 0.3 miles is also deducted from the distance to the next delivery until that distance is less than or equal
    # to zero.
    while True:
        current_time = run_print_time()
        update = 'Truck #%s: ' % truck.truck_num
        truck.truck_miles += miles_per_minute
        if (float(truck.distance_to_next_delivery) - miles_per_minute) <= 0:
            miles_over_destination = float(truck.distance_to_next_delivery) - miles_per_minute
            if len(truck.truck_package_list) == 1:
                return_to_hub()
            elif len(truck.truck_package_list) == 0:
                truck_location = 'At Hub'
                print(update + truck_location)
                return 0
            else:
                multiple_packages_at_address()
        elif len(truck.truck_package_list) != 0:
            truck.distance_to_next_delivery = float(truck.distance_to_next_delivery) - miles_per_minute

        else:
            truck.distance_to_next_delivery = float(truck.distance_to_next_delivery) - miles_per_minute

        # Update for package 9 to satisfy constraint from requirements.
        if time[0] == 10 and time[1] == 20:
            package = package_table.hash_search(9)
            update_address(20, package)

        # Checks to see if the clock has reached the time the user requested. If yes, the time is returned
        # and the loop breaks.
        if timeparam is None:
            pass
        elif time[0] == timeparam[0] and time[1] == timeparam[1]:
            return time

        # Breaks the loop onces all packages for that load are delivered.
        if len(truck.truck_package_list) == 0:
            break


# Increments the clock by one minute.  A simple array is used to implement the time.
def clock_increment():
    time[1] += 1

    if time[1] >= 60:
        time[1] -= 60
        time[0] += 1

    return 0


# Converts user input string to a time array.
def process_time_input(input):
    time_input = input.split(':')
    time_input_hr = int(time_input[0])
    time_input_min = int(time_input[1])
    return [time_input_hr, time_input_min]


# Returns package from hash table based on Package ID.
def get_package():
    package_num = input('Enter Package ID: \n')
    package = package_table.hash_search(package_num)
    print(package.package_string())


# Iterates over Hashtable and prints package information for each package.
def show_all_packages():
    current_time = '%02d:%02d' % (time[0], time[1])
    print('\n\nPACKAGE STATUS AS OF: %s' % current_time)
    for bucket in package_table.table:
        for package in bucket:
            print(package.package_string())

    return 0


# Returns the address as a string.
def get_address(location_id):
    return location_list[int(location_id)]


# Takes Location ID and the package to update as input.  Assigns the package a new Location ID.
# Gets the address for that Location ID.  Assigns the new address to the package.  Updates
# the Hash Table.
def update_address(location_id, package: Package):
    package.location_id = int(location_id)
    new_address = get_address(location_id)
    package.address = new_address
    package_table.hash_update(package)

    return 0


# Resets time, package status, and distance driven by the truck.
def clock_truck_reset():
    time[0] = 8
    time[1] = 0
    update_address(12, package_table.hash_search(9))
    for i in range(1, 40):
        package = package_table.hash_search(i)
        package.status = 'AT HUB'
    truck2.truck_miles = 0


# Main Interface for user interaction.
def menu():
    while True:
        welcome_text = 'WGUPS DELIVERY SYSTEM\n' \
                       'Select an Option:\n' \
                       '1: Load Trucks and Run Delivery\n' \
                       '2: Lookup Package\n' \
                       '3: Show All Packages at Specified Time\n' \
                       '0: Exit\n'
        user_input = int(input(welcome_text))
        if user_input == 0:  # Ends execution when selected.
            break
        elif user_input == 3:  # Reset, Get Time input, Execute code until that time is reached.
            clock_truck_reset()
            time_input = input('Please Enter a Time to View Package Status (HH:MM - 24 hour clock)')
            user_time = process_time_input(time_input)
            truck2.truck_package_list.extend(load1)
            load1_time = run_truck(truck2, user_time)
            if load1_time != user_time:
                truck2.truck_package_list.extend(load2)
                load2_time = run_truck(truck2, user_time)
                if load2_time != user_time:
                    truck2.truck_package_list.extend(load3)
                    run_truck(truck2, user_time)
            show_all_packages()
        elif user_input == 1:  # Runs Initial delivery of all packages.
            clock_truck_reset()
            truck2.truck_package_list.extend(load1)
            run_truck(truck2)
            truck2.truck_package_list.extend(load2)
            run_truck(truck2)
            truck2.truck_package_list.extend(load3)
            run_truck(truck2)
            show_all_packages()
            print('\n\nTOTAL MILEAGE: %f\n\n' % truck2.truck_miles)
        elif user_input == 2: # Searches and returns an individual package based on package ID
            get_package()
        else:
            print('Invalid Selection')


menu()
