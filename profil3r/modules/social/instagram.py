import requests
from profil3r.colors import Colors
import time

class Instagram:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['instagram']['rate_limit'] / 1000
        # https://instagram.com/{username}
        self.format = config['plateform']['instagram']['format']
        self.permutations_list = permutations_list

    # Generate all potential instagram usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        instagram_usernames = {
            "accounts" : []
        }

        bibliogram_URL = "https://bibliogram.art/u/{}"

        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                bibliogram_formatted_URL = bibliogram_URL.format(username.replace("https://instagram.com/", ""))
                r = requests.get(bibliogram_formatted_URL)
            except requests.ConnectionError:
                print("failed to connect to instagram")
            
            # If the account exists
            if r.status_code == 200:
                instagram_usernames["accounts"].append({"value": username})

            time.sleep(self.delay)
        
        return instagram_usernames