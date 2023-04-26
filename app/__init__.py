


import os
import json


DATA_DIRPATH = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIRPATH = os.path.join(os.path.dirname(__file__), "..", "results")




def download_json(data, json_filepath):
    with open(json_filepath, "w") as json_file:
        json.dump(data, json_file)


#class FileSaver:
#
#    @staticmethod
#    def download_json(data, json_filepath):
#        with open(json_filepath, "w") as json_file:
#            json.dump(data, json_file)
#
