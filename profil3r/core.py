import sys
from itertools import chain, combinations, permutations
import json
from profil3r.modules.email import email
from profil3r.modules.social import facebook, twitter, tiktok, instagram
from profil3r.modules.porn import onlyfans
from profil3r.colors import Colors
import threading
import json
import os

result = {}

class Core:

    def __init__(self, config_path, items):
        with open(config_path, 'r') as f:
            self.CONFIG = json.load(f)
        # Items passed from the command line
        self.items = items
        self.permutations_list = []
        self.modules = [
            {"name": "email"    , "method" : self.email},
            {"name": "facebook" , "method" : self.facebook},
            {"name": "twitter"  , "method" : self.twitter},
            {"name": "tiktok"   , "method" : self.tiktok},
            {"name": "instagram", "method" : self.instagram},
            {"name": "onlyfans" , "method" : self.onlyfans}
        ]

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
    def email(self):
        result["email"] = email.Email(self.CONFIG, self.permutations_list).search()
        # print results
        self.print_results("email")

    # Facebook
    def facebook(self):
        result["facebook"] = facebook.Facebook(self.CONFIG, self.permutations_list).search()
        # print results
        self.print_results("facebook")
    
    # Twitter
    def twitter(self):
        result["twitter"] = twitter.Twitter(self.CONFIG, self.permutations_list).search()
        # print results
        self.print_results("twitter")

    # TikTok
    def tiktok(self):
        result["tiktok"] = tiktok.TikTok(self.CONFIG, self.permutations_list).search()
        # print results
        self.print_results("tiktok")

    # Instagram
    def instagram(self):
        result["instagram"] = instagram.Instagram(self.CONFIG, self.permutations_list).search()
        # print results
        self.print_results("instagram")

    # Onlyfans
    def onlyfans(self):
        result["onlyfans"] = onlyfans.Onlyfans(self.CONFIG, self.permutations_list).search()
        # print results
        self.print_results("onlyfans")

    def print_results(self, element):
        if element in result:
            element_results = result[element]
            
            # Section title

            # No results
            if not element_results["accounts"]:
                print("\n" + Colors.BOLD + "└──" + Colors.ENDC + Colors.OKGREEN + " {} ✔️".format(element.upper()) + Colors.ENDC + Colors.FAIL + " (No results)" + Colors.ENDC)
                return 
            # Results
            else: 
                print("\n" + Colors.BOLD + "└──" + Colors.ENDC + Colors.OKGREEN + " {} ✔️".format(element.upper()) + Colors.ENDC)

            # General case
            if element != "email":
        
                for account in element_results["accounts"]:
                    print(Colors.BOLD + "   ├──" + Colors.ENDC + Colors.HEADER + account["value"] + Colors.ENDC)
            
            # Emails case
            else:
                possible_emails_list = [account["value"] for account in element_results["accounts"]]
                
                for account in element_results["accounts"]:
                     # We pad the emails with spaces for better visibility
                    longest_email_length = len(max(possible_emails_list))
                    email = account["value"].ljust(longest_email_length + 5)

                    # Breached account
                    if account["breached"]:
                        print(Colors.BOLD + "   ├──" + Colors.ENDC + Colors.HEADER + email + Colors.FAIL + "[BREACHED]" + Colors.ENDC)
                    # Safe account
                    else:
                        print(Colors.BOLD + "   ├──" + Colors.ENDC + Colors.HEADER + email + Colors.OKGREEN + "[SAFE]" + Colors.ENDC)

    # Generate a report in JSON format containing the collected data
    # Report will be in "./reports/"
    # You can modify th path in the config.json file
    def generate_report(self):
        # Create ./reports directory if not exists
        if not os.path.exists('reports'):
            os.makedirs('reports')

        file_name = self.CONFIG["report_path"].format("_".join(self.items[:-1]))
        try:
            with open(file_name, 'w') as fp:
                json.dump(result, fp)
        except Exception as e:
            print(e)

    def run(self):
        for module in self.modules:
            thread = threading.Thread(target=module["method"])
            thread.start()
            thread.join()
        self.generate_report()