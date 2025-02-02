import imaplib

# Gmail IMAP server details
IMAP_SERVER = "imap.gmail.com"

# List of email accounts and their corresponding app passwords
EMAIL_ACCOUNTS = [
    {"email": "tmm003937@gmail.com", "password": "fekg mego jqlw pizn"},
    {"email": "mta872679@gmail.com", "password": "dppb jbar acqq orqz"}
]

def move_from_junk_to_inbox(mail):
    # Select the Junk (Spam) folder
    mail.select("[Gmail]/Spam")

    # Search for all emails in the Junk folder
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()

    if len(email_ids) > 0:
        print(f"Moving {len(email_ids)} emails from Junk to Inbox...")
        for email_id in email_ids:
            # Move each email from Junk to Inbox
            mail.copy(email_id, "inbox")
            mail.store(email_id, '+FLAGS', '\\Deleted')  # Mark as deleted from Spam folder
        mail.expunge()  # Remove deleted emails

def count_and_mark_unread_emails():
    for account in EMAIL_ACCOUNTS:
        try:
            email_account = account["email"]
            email_password = account["password"]

            print(f"Processing account: {email_account}")

            # Connect to Gmail's IMAP server
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(email_account, email_password)

            # Move emails from Junk (Spam) to Inbox
            move_from_junk_to_inbox(mail)

            # Select the inbox
            mail.select("inbox")

            # Search for all unread emails
            status, messages = mail.search(None, 'UNSEEN')
            email_ids = messages[0].split()

            print(f"Unread Emails in {email_account}: {len(email_ids)}")

            # Mark each unread email as read
            for email_id in email_ids:
                mail.store(email_id, '+FLAGS', '\\Seen')

            # Close and logout
            mail.close()
            mail.logout()

        except Exception as e:
            print(f"Error processing {email_account}: {e}")

if __name__ == "__main__":
    count_and_mark_unread_emails()
