# Hash table for the package information
from Package import Package


class HashTable:

    # Constructor
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Defining the hash function
    def hash(self, key):
        return int(key) % 40

    # Insert new item into table
    def hash_insert(self, key, value):
        bucket = self.hash(key)
        self.table[bucket].append(value)

    # Search hash table for item
    def hash_search(self, key):
        bucket = self.hash(key)
        package: Package

        for package in self.table[bucket]:
            if int(package.id) == int(key):
                return package
            else:
                return None

    # Removes an item based on key
    def hash_remove(self, key):
        bucket = self.hash(key)
        bucket_list = self.table[bucket]

        # Remove if item is present in bucket
        if key in bucket_list:
            bucket_list.remove(key)

    def hash_update(self, package: Package):
        key = int(package.id)
        bucket = self.hash(key)
        package: Package
        for package in self.table[bucket]:
            if int(package.id) == int(key):
                package_update = package
                return package_update
            else:
                return None
