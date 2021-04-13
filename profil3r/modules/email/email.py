import time
import pwnedpasswords
from profil3r.colors import Colors

class Email:

    def __init__(self, config, permutations_list):
        # Have I been pwned API rate limit ( 1500 ms)
        self.delay = DELAY = 1500 / 1000
        # The 20 most common email domains, you can add more if you wish (in the config.jon file)
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
        print(Colors.BOLD + Colors.OKGREEN + "\n----- EMAILS -----\n" + Colors.ENDC)

        possible_emails_list = self.possible_emails()

        for possible_email in possible_emails_list:
            pwned = pwnedpasswords.check(possible_email)
            
            # We pad the emails with spaces for better visibility
            longest_email_length = len(max(possible_emails_list))
            email = possible_email.ljust(longest_email_length + 5)
            
            # Not breached email
            if not pwned:
               print(Colors.BOLD + "[+] " + Colors.ENDC + Colors.HEADER  + email + Colors.ENDC)
            # Breached emails
            else:
               print(Colors.BOLD + "[+] " + Colors.ENDC + Colors.HEADER  + email + Colors.ENDC + Colors.FAIL + Colors.BOLD + "[BREACHED]" + Colors.ENDC)

            time.sleep(self.delay)