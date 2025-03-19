import imaplib
import email
import os
from email.header import decode_header

# Gmail credentials
EMAIL = "22054081@kiit.ac.in"  # Replace with your Gmail
PASSWORD = "tswl jlat gqwy hzdb"  # Use an App Password if 2FA is enabled

# IMAP server settings for Gmail
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Folder to save PDFs
DOWNLOAD_FOLDER = "gmail_pdfs"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def clean_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (" ", ".", "_")).rstrip()


def download_pdfs():
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # Search for emails with attachments
    status, messages = mail.search(None, 'ALL')  # You can use 'UNSEEN' to filter unread emails
    email_ids = messages[0].split()

    print(f"Found {len(email_ids)} emails. Scanning for PDFs...")

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Decode email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                # Check for attachments
                for part in msg.walk():
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            filename = clean_filename(filename)
                            if filename.lower().endswith(".pdf"):
                                filepath = os.path.join(DOWNLOAD_FOLDER, filename)

                                # Save the PDF
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))

                                print(f"Downloaded: {filename} (From Email: {subject})")

    # Logout and close connection
    mail.logout()
    print("Finished downloading all PDFs.")


# Run the script
download_pdfs()
