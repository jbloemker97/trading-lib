import os
import csv

class WriteCSV:

    def __init__(self, filename, pubdir=None):
        self.filename = filename
        self.pubdir = pubdir
    
    def file_path(self):
        if self.pubdir is not None:
            os.chdir(self.pubdir)
            return os.path.join(os.getcwd(), self.filename)
        return os.path.join(os.getcwd(), self.filename)

    def write_list(self, header_row, data):
        is_file = os.path.isfile(self.file_path())

        with open(self.file_path(), "a") as file:
            writer = csv.writer(file)

            # Write header if file (or headers) don't exist
            if not is_file:
                writer.writerow(header_row)
            
            writer.writerow(data)

    def write_dict(self, data):
        is_file = os.path.isfile(self.file_path())

        with open(self.file_path(), "a") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys(), lineterminator = '\n')
            
            # Write header if file (or headers) don't exist
            if not is_file:
                writer.writeheader()

            writer.writerow(data)