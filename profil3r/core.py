import sys
from itertools import chain, combinations, permutations
import json
from profil3r.modules.email import email
from profil3r.modules.social import facebook, twitter, tiktok

class Core:

    def __init__(self, config_path, items):
        with open(config_path, 'r') as f:
            self.CONFIG = json.load(f)
        # Items passed from the command line
        self.items = items
        self.permutations_list = []

    def config():
        return self.CONFIG

    # return all possible permutation for a username
    # exemple : ["john", "doe"] -> ("john", "doe", "johndoe", "doejohn", "john.doe", "doe.john") 
    def get_permutations(self):
        self.items.append('.')
        combinations_list = list(chain(*map(lambda x: combinations(self.items, x), range(1, len(self.items) + 1))))   
        for combination in combinations_list:
            # Remove combinations that start or end by a dot
            for perm in list(permutations(combination)):
                if not perm[0] == "." and not perm[-1] == ".":
                    self.permutations_list.append("".join(perm))
    
    # Emails
    def search_emails(self):
        email.Email(self.CONFIG, self.permutations_list).search()

    # Facebook
    def search_facebook(self):
        facebook.Facebook(self.CONFIG, self.permutations_list).search()

    # Twitter
    def search_twitter(self):
        twitter.Twitter(self.CONFIG, self.permutations_list).search()

    # TikTok
    def search_tiktok(self):
        tiktok.TikTok(self.CONFIG, self.permutations_list).search()