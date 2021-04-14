import requests
from profil3r.colors import Colors
import time

class Facebook:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['facebook']['rate_limit'] / 1000
        # https://facebook.com/{username}
        self.format = config['plateform']['facebook']['format']
        # facebook usernames are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]

    # Generate all potential facebook usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        facebook_usernames = {
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to facebook")
            
            # If the account exists
            if r.status_code == 200:
                facebook_usernames["accounts"].append({"value": username})
            time.sleep(self.delay)
        
        return facebook_usernames