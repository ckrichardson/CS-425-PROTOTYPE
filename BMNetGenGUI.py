##############################################################################
# Name: Justin A. Haghighi
# Date: 2020-04-08
# Course: CS 426.1001
# Instructors: Devrin Lee, MS, and Sergiu Dascalu, PhD
# Team: 30
##############################################################################

import BMNetGen

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generateNetworkBody():
    body = """
    <br>
        <button id="emailButton" data-xdh-onevent="emailNetGraph" {}>
            Generate graph
        </button>
        </button>
        <button id="networkStartButton" data-xdh-onevent="networkStart" {}>
            Fuzz network
        </button>
        </button>
        
        <form>
            <br>
            <label> Enter email and click "Generate graph": <label>
            <br>
            <input type="text" id="tput_email_field">
        </form>
            <br>
        
    <br>
    """
    return body
    
def acNetworkStart(dom):    
    dom.disableElement("networkStartButton")
    dom.disableElement("emailButton")
    dom.disableElement("tput_email_field")

    try:
        BMNetGen.generateTopo()
        dom.alert("Network is up. Click the Fuzzer button to begin testing.")

    except:
        dom.alert("Error: The network is running. Please terminate terminal and relaunch.")
        
def acSendGraphEmail(dom):
    dom.disableElement("emailButton")
    dom.disableElement("tput_email_field")

    try:
        BMNetGen.plotNet()
        print("*** Tput graph successfully saved")
   
        tput_email = dom.getContent("tput_email_field")
        print("*** Email address captured")
    
        subject = "SDN Topology Throughput Graph"
        body = "The attached image presents the result of the throughput test."
        sender_email = "resiliencedonotreply+bmnet@gmail.com"
        receiver_email = "jhaghighi@nevada.unr.edu"
        password = "tubesock1"

        # create and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = tput_email
        message["Subject"] = subject

        # add body to email
        message.attach(MIMEText(body, "plain"))

        filename = "tput_graph.png" # located in /root/CS-425-PROTOTYPE

        # open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # bytestream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # encode file to send by email    
        encoders.encode_base64(part)

        # add header to attachment
        part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                        )

        # add attachment to message 
        message.attach(part)
        text = message.as_string()
        print("*** Tput graph attached")


        try:
            # log in to server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, tput_email, text)
            print("*** Email sent")
            dom.alert("Email sent!")
        except:
            dom.alert("Error: Email not sent! Please check the spelling.")
            dom.enableElement("emailButton")
            dom.enableElement("tput_email_field")
    except:
        dom.alert("Error: The network is running. Please terminate terminal and relaunch.")

networkCallbacks = {
    "networkStart": acNetworkStart,
    "emailNetGraph": acSendGraphEmail,
}
