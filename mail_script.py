#!/usr/bin/env python3
import os
import base64
import mimetypes
import json
from Mails import MAILS
from Google import Create_Service
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

CLIENT_SECRET_FILE = 'credentials_oauth2.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# with open("thumbnail_image.jpg", "rb") as image_file:
#     image = base64.b64encode(image_file.read())

# image = f'{image}'
# image = image[2:]
# image = f'data:image/png;base64,{image}'
# print(image)

for i in range(len(MAILS)):
    file_name = 'attachments/XX Škola Nefrologije 2023 - ' + MAILS[i][0] + '.pdf'
    recipient_name = MAILS[i][0]
    attachment = file_name
    emailMsg = open("email.html", "r", encoding="utf8").read().format(recipient_name=recipient_name)

    # create email message
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = MAILS[i][1]
    mimeMessage['subject'] = 'NefroBiH Certifikat'
    mimeMessage.attach(MIMEText(emailMsg, 'html'))

    # Attach files
    content_type, encoding = mimetypes.guess_type(attachment)
    main_type, sub_type = content_type.split('/', 1)
    file_name = os.path.basename(attachment)

    if os.path.isfile(attachment): 
        f = open(attachment, 'rb')
        myFile = MIMEBase(main_type, sub_type)
        myFile.set_payload(f.read())
        myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
        encoders.encode_base64(myFile)
        f.close()

        mimeMessage.attach(myFile)
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(recipient_name)
    else:
        print("File for " + recipient_name + " doesn't exits.")

print("Emails have been successfully sent.")