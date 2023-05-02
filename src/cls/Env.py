import os
import json
from dotenv import load_dotenv

class Env:
    def __init__(self):
        load_dotenv()

    def get_var(self, varname):
        return os.getenv(varname)

    def get_bot_config(self):
        output_folder = self.get_var('OUTPUT_FOLDER').strip()
        descriptive_mode = (self.get_var('DESCRIPTIVE_MODE').strip()) == 'YES'

        return output_folder, descriptive_mode

    def get_searches(self):
        searches_file = self.get_var('SEARCHES_FILE').strip()

        f = open(searches_file)
        searches = json.load(open(searches_file))
        f.close()

        return searches