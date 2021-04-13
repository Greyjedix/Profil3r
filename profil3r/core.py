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
        self.result = {}

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
    def emails(self):
        self.result["emails"] = email.Email(self.CONFIG, self.permutations_list).search()

    # Facebook
    def facebook(self):
        self.result["facebook"] = facebook.Facebook(self.CONFIG, self.permutations_list).search()
    
    # Twitter
    def twitter(self):
        self.result["twitter"] = twitter.Twitter(self.CONFIG, self.permutations_list).search()

    # TikTok
    def tiktok(self):
        self.result["tiktok"] = tiktok.TikTok(self.CONFIG, self.permutations_list).search()

