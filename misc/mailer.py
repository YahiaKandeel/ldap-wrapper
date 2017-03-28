#!/usr/bin/python
#################################################################
# Mailer
# Sends Emails that support attachements - Text & Zipped.
#################################################################
import smtplib
import datetime
import zipfile
import argparse
import sys
import os
from conf import server, From
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#################################################################
# Support Function ...
#################################################################

# create & read Zip File


def zip(attachment):
    try:
        # Compressed File:
        compressed_file = os.path.basename(attachment).split('.')[0] + '.zip'
        # create compressed file
        output = zipfile.ZipFile(compressed_file, 'w')
        # Add attachment to it
        output.write(attachment, compress_type=zipfile.ZIP_DEFLATED)
        # Close compressed file
        output.close()
        # read Zip file
        data = open(compressed_file).read()
        # return data
        return compressed_file, data

    except:
        print "Can't create compressed file"
        return False, False


# Construct Message
def message(From, To, Subject, Body, Attachment_Data=False, Attachment_Filename=False, Attachment_Type='text'):

    # Construct Message
    msg = MIMEMultipart()
    msg["From"] = From
    msg["To"] = To
    msg["Subject"] = Subject

    # Prepare Attachement ..
    if Attachment_Filename and Attachment_Data:
        # Set Type
        attachment = MIMEBase('application', Attachment_Type)
        # Add Payload
        attachment.set_payload(Attachment_Data)
        # Encode it
        encoders.encode_base64(attachment)
        # Add Header
        attachment.add_header("Content-Disposition",
                              "attachment", filename=Attachment_Filename)
        # Attach it to the message
        msg.attach(attachment)

    # Attach Body
    body = MIMEText(Body, 'html')
    msg.attach(body)

    return msg


def send(Server, From, To, Message):
    try:
        # Send Message
        server = smtplib.SMTP(Server)
        # Helo
        server.ehlo()
        # Send
        server.sendmail(From, To.split(','), Message.as_string())
        # Close
        server.quit()

    except:
        print "Error in Seding Message!"


# Send Zipped
def notify(Attachement, To, Subject, Zipped=True):
    if Zipped:
        attachment_name, data = zip(Attachement)
        Attachment_Type = 'zip'

    else:
        data = open(Attachement).read()
        attachment_name = Attachement
        Attachment_Type = 'text'

    # Create Message
    msg = message(
        From,  # From
        To,  # To
        Subject,  # Subject
        '<br /><br /><br /><p>Best Regards,</p>',  # Body
        Attachment_Data=data,
        Attachment_Filename=attachment_name,
        Attachment_Type=Attachment_Type
    )

    # Send The Message
    send(server, From, To, msg)
