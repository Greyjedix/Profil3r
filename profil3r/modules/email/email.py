import time
import pwnedpasswords
from profil3r.colors import Colors

class Email:

    def __init__(self, config, permutations_list):
        # Have I been pwned API rate limit ( 1500 ms)
        self.delay = DELAY = config['plateform']['email']['rate_limit'] / 1000
        # The 20 most common email domains, you can add more if you wish (in the config.jon file)
        # The more domains you add, the longer it gets of course
        self.domains = config['plateform']['email']['domains']
        # {username}@{domain}
        self.format = config['plateform']['email']['format']
        # email adresses are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]

    # Generate all potential adresses
    def possible_emails(self):
        possible_emails = []

        for domain in self.domains:
            for permutation in self.permutations_list:
                possible_emails.append(self.format.format(
                    permutation = permutation,
                    domain      = domain
                ))
        return possible_emails

    # We use the Have I Been Pwned API to search for breached emails
    def search(self):
        emails_usernames = {
            "accounts": []
        }
        possible_emails_list = self.possible_emails()

        for possible_email in possible_emails_list:
            pwned = pwnedpasswords.check(possible_email)
            
            # Not breached email
            if not pwned:
                emails_usernames["accounts"].append({"value": possible_email, "breached": False})
            # Breached emails
            else:
                emails_usernames["accounts"].append({"value": possible_email, "breached": True})

            time.sleep(self.delay)

        return emails_usernames