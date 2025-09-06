import csv
import os
from Laptime import Laptime

class LaptimeData:
    def __init__(self, laptimes_filename='Naascar_v2/Laptimes.csv'):
        self.laptimes_filename = laptimes_filename
        self.ensure_file_exists()


    def ensure_file_exists(self):
        """
        Check if CSV files exist, creating them if not with headers.
        """
        self.create_file_if_not_exists(self.laptimes_filename, ['track_id', 'time'])


    def create_file_if_not_exists(self, filename, fieldnames):
        '''
        Creates file with given fieldnames if it doesnt exist.
        '''
        if not os.path.exists(filename):
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

    
    def add_laptime(self, **kwargs):
        '''
        Adds a new laptime to the certain track_id.
        name is optional

        :param track_id: int = [0, 8]
        :param time: MM:SS:MsMs
        :param kwargs: Attributes of the laptime. (name='name',ssn='ssn'...etc)

        :raises ValueError: If required fields are missing or empty.
        Add a new laptime to the CSV file.
        '''


        required_fields = ['track_id', 'time']
        for field in required_fields:
            if kwargs.get(field) is None or kwargs.get(field) == '':
                raise ValueError("Required fields cannot be empty.")

        # add general laptime information after going through all checks
        laptime = Laptime(**kwargs)

        try:
            with open(self.laptimes_filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(
                    file, fieldnames=laptime.__dict__.keys())
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(laptime.__dict__)
        except Exception as e:
            raise Exception(f"An error occurred while writing to the file: {e}")
        

    def get_best_track_laptime(self, track_id):
        return "00:00:00"    

    
    def object_list_to_dict_list(self, object_list):
        '''
        Takes a list of objects and returns a list of dictionaries.
        '''
        dict_list = []
        for obj in object_list:
            dict_list.append(obj.__dict__)

        return dict_list