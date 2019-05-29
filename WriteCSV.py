import os
import csv

class WriteCSV:

    def __init__(self, filename, pubdir=None):
        self.filename = filename
        self.pubdir = pubdir

    def clean_path(self):
        # Is directory doesn't end with / and filename doesn't start with a /
        if self.pubdir[-1] is not "/" and self.filename[0] is not "/":
            self.pubdir = self.pubdir + "/"
    
    def file_path(self):
        if self.pubdir is not None:
            self.clean_path()
            try:
                os.makedirs(os.path.join(os.getcwd(), self.pubdir))
            except OSError as error:
                if os.path.isdir(self.pubdir):
                    pass
                else: raise

            return os.path.join(os.getcwd(), self.pubdir + self.filename)
        return os.path.join(os.getcwd(), self.filename)

    def write_list(self, header_row, data):
        is_file = os.path.isfile(self.file_path())

        with open(self.file_path(), "a") as file:
            writer = csv.writer(file)

            # Write header if file (or headers) don't exist
            if not is_file:
                writer.writerow(header_row)
            
            writer.writerow(data)

    def write_dict(self, data, permission = "a"):
        is_file = os.path.isfile(self.file_path())

        
        # if self.pubdir is not None:

        with open(self.file_path(), permission) as file:
            writer = csv.DictWriter(file, fieldnames=data.keys(), lineterminator = '\n')
            
            # Write header if file (or headers) don't exist
            if not is_file:
                writer.writeheader()

            writer.writerow(data)