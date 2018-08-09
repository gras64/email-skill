import sys
import imaplib
import getpass
import email
import email.header


def list_new_email(account, folder, password, port, address):
    M = imaplib.IMAP4_SSL(str(address), port=int(port))
    M.login(str(account), str(password))
    M.select(str(folder))
    #TODO: PROCESS INBOX
    rv, data = M.search(None, "(UNSEEN)")
    message_num = 1
    new_emails = []
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        sender = email.header.make_header(email.header.decode_header(msg['From']))
        M.store(num, "-FLAGS", '\\SEEN')
        subject = str(hdr)
        sender = str(sender)
        mail = {"message_num": message_num, "sender": sender, "subject": subject}
        new_emails.append(mail)
        message_num += 1
    
    M.close()
    M.logout()

    return new_emails

