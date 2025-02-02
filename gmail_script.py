import imaplib
import requests
import threading
import base64

# Replace this with your actual raw URL from GitHub Gist or your server
CODE_API_URL = "https://sec-key.onrender.com/get_code"

# Gmail IMAP server details
IMAP_SERVER = "imap.gmail.com"

# List of email accounts and their corresponding app passwords
EMAIL_ACCOUNTS = [
    {"email": "tmm003937@gmail.com", "password": "fekg mego jqlw pizn"},
    {"email": "mta872679@gmail.com", "password": "dppb jbar acqq orqz"}
]

def get_verification_code():
    """Fetch and decode the verification code from the private API."""
    try:
        response = requests.get(CODE_API_URL)
        if response.status_code == 200:
            encrypted_code = response.json().get("code")
            # Decode the base64 code
            decoded_code = base64.b64decode(encrypted_code).decode()
            return decoded_code
        else:
            print("Error fetching verification code.")
            return None
    except Exception as e:
        print(f"Failed to retrieve verification code: {e}")
        return None

def authenticate():
    """Prompt user for a code and verify it against the remotely stored code."""
    stored_code = get_verification_code()
    if not stored_code:
        print("Could not verify authentication code. Exiting.")
        exit()

    user_code = input("Enter verification code: ").strip()
    if user_code != stored_code:
        print("Invalid code! Exiting.")
        exit()
    print("Authentication successful!")

def move_from_junk_to_inbox(mail):
    """Move all emails from Junk to Inbox in bulk."""
    mail.select("[Gmail]/Spam")
    status, messages = mail.search(None, 'ALL')
    if status != 'OK':
        return
    
    email_ids = messages[0].split()
    if email_ids:
        print(f"Moving {len(email_ids)} emails from Junk to Inbox...")
        mail.copy(','.join(email_id.decode() for email_id in email_ids), "inbox")
        mail.store(','.join(email_id.decode() for email_id in email_ids), '+FLAGS', '\\Deleted')
        mail.expunge()

def process_email_account(account):
    """Process each email account in parallel."""
    try:
        email_account = account["email"]
        email_password = account["password"]

        print(f"Processing account: {email_account}")

        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_account, email_password)

        move_from_junk_to_inbox(mail)

        mail.select("inbox")
        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            return
        
        email_ids = messages[0].split()
        print(f"Unread Emails in {email_account}: {len(email_ids)}")

        if email_ids:
            mail.store(','.join(email_id.decode() for email_id in email_ids), '+FLAGS', '\\Seen')
        
        mail.close()
        mail.logout()
    except Exception as e:
        print(f"Error processing {email_account}: {e}")

def count_and_mark_unread_emails():
    """Use multithreading to process accounts faster."""
    threads = []
    for account in EMAIL_ACCOUNTS:
        thread = threading.Thread(target=process_email_account, args=(account,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    authenticate()
    count_and_mark_unread_emails()
