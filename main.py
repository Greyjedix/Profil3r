import sys
from itertools import chain, combinations
from profil3r import core
from profil3r.colors import Colors

CONFIG = './config.json'

print(Colors.OKGREEN + Colors.BOLD + ''' ___            ___  _  _  ____     
| . \ _ _  ___ | | '<_>| |<__ / _ _ 
|  _/| '_>/ . \| |- | || | <_ \| '_>
|_|  |_|  \___/|_|  |_||_|<___/|_|  

''' + Colors.ENDC)

print("v1.0.0\n")

# Use command line arguments
arguments = sys.argv[1:]

# No argument
if not len(arguments):
    print('''Profil3r is an OSINT tool that allows you to find potential profiles of a person on social networks, as well as their email addresses. This program also alerts you to the presence of a data leak for the found emails.

Usage : ./main.py <arguments>
for exemple : ./main.py john doe
              ./main.py john doe 67''')

else:
    profil3r = core.Core(CONFIG, sys.argv[1:])
    profil3r.get_permutations()

    # TikTok
    profil3r.search_tiktok()
    # Emails
    profil3r.search_emails()
    # Facebook
    profil3r.search_facebook()
    # Twitter 
    profil3r.search_twitter()