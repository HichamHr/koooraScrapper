#!/usr/bin/env python

"""MailBox class for processing IMAP email.
(To use with Gmail: enable IMAP access in your Google account settings)
usage with GMail:
    import mailbox
    with mailbox.MailBox(gmail_username, gmail_password) as mbox:
        print mbox.get_count()
        print mbox.print_msgs()
for other IMAP servers, adjust settings as necessary.
"""

import imaplib
import email
import email.header


class EmailScraper:
    def __init__(self, username, password, imap_url="imap.gmail.com"):
        self.imap_username = username
        self.imap_password = password
        self.imap_url = imap_url
        self.my_mail = imaplib.IMAP4_SSL(self.imap_url)

    def login(self):
        self.my_mail.login(self.imap_username, self.imap_password)

    @staticmethod
    def decode_subject(message):
        text, encoding = email.header.decode_header(message)[0]
        return text

    def get_email(self, inbox, search_key, search_value):
        # For other keys (criteria): https://gist.github.com/martinrusev/6121028#file-imap-search
        self.my_mail.select(inbox)
        # Search for emails with specific key and value
        _, search_data = self.my_mail.search(None, search_key, search_value)
        mail_id_list = search_data[0].split()  # IDs of all emails that we want to fetch
        msgs = []  # empty list to capture all messages
        # Iterate through messages and extract data into the msgs list
        for num in mail_id_list:
            # RFC822 returns whole message (BODY fetches just body)
            typ, data = self.my_mail.fetch(num, '(RFC822)')
            msgs.append(data)

        for msg in msgs[::-1]:
            for response_part in msg:
                if type(response_part) is tuple:
                    my_msg = email.message_from_bytes((response_part[1]))
                    print("_________________________________________")
                    print("subj:", self.decode_subject(my_msg['subject']))
                    print("from:", my_msg['from'])
                    print("body:")
                    for part in my_msg.walk():
                        # print(part.get_content_type())
                        if part.get_content_type() == 'text/plain':
                            print(part.get_payload(decode=True))


if __name__ == '__main__':
    emailScraper = EmailScraper('rachid.ahmed.bls@gmail.com', 'emyuamjnduexgkar')
    # from credentials.yml import user name and password
    emailScraper.login()
    emailScraper.get_email("Inbox", "FROM", "no-reply@accounts.google.com")
