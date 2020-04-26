import atlastk as Atlas
import execnet

try:
    import log_integrity
except ImportError:
    print("Abs import fail")

try:
    from . import log_integrity
except ModuleNotFoundError:
    print("Relative import fail")

from time import sleep
import smtplib
import os
from email.mime.text import MIMEText

"""
This is a way of calling Python2 methods from Python3 using the execnet module.
Otherwise, there would have to be an effort in ICSREF to futureproof the entire 
codebase which is written in Python2.
"""
def call_python_version(Version, Module, Function, ArgumentList):
    gw = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec("""
        try:
            from %s import %s as the_function
        except ImportError:
            print("Abs import fail")

        from binaryAnalysis.analysis import binary_analysis as the_function
        #print("Relative import fail")
        channel.send(the_function(*channel.receive()))
    """ % (Module, Function))
    channel.send(ArgumentList)
    return channel.receive()


# This is the HTML body of the page that will be hosted thru Atlas.
# It is without any sort of javascript - all dynamic page elements are handled through 
# The backend using python
def generateIDAttrBody():
    body = """
        <div align="center">
            <div align="center">
                <div align="left" style="display: inline-block">
                    <form>
                        <label for="filepath">Enter File Path (ABS)</label><br>
                        <input type="text" id="filepath" name="filepath" style="width:300px">
                    </form>
                    <br>
                </div>
            </div>
            <form>
            <div align="left" style="display: inline-block">
                <label for="integrity">Perform Hashing?</label>
              <fieldset id="integrity">
                    <input type="radio" id="integrity1" name="yes1" value="yes1">
                    <label for="yes1">Yes, with integrity check
                    <br>
                    <input type="radio" id="integrity2" name="yes1" value="yes2">
                    <label for="yes2">Yes, without integrity check
                      <br>
                    <input type="radio" id="integrity3" name="yes1" value="yes3">
                    <label for="yes3">No
                <br>
                </fieldset>
            </div>
            <div>
              <br>
              <br>
                <form>
                </fieldset>
                  <label> Would you like a graphical output? 
                    <br>
                            <input type="radio" id="graphics1" name="graph_radio_1" value="yes1">
                    <label for="yes1">Yes
                    <br>
                    <input type="radio" id="graphics2" name="graph_radio_1" value="yes2">
                    <label for="yes2">No
                      <br>
                </form>
                <br>
            </div>
            <button id="analyzeStartButton" data-xdh-onevent="startAnalysis" {}>
            Begin
            </button>
            <button id="analyzeCancelButton" data-xdh-onevent="endAnalysis" {}>
                Cancel
            </button>
            <br>
            <br>
             <br>
                    <label id="status"> STATUS: </label>
                            <p id="analysisStatus"></p>
        </div>
    """
    return body

# This is used to load the HTML body upon the user connecting
def acConnect(dom):
    dom.setLayout("", generateIDAttrBody())
    print(os.getcwd())

# This runs the entire automation process for analyzing PLC's, any integrity checks, as well as 
# graphical outputs.
def acStartAnalysis(dom):
    # Integrity radio button bools
    integrity_1_bool = dom.getContent("integrity1")
    integrity_2_bool = dom.getContent("integrity2")
    integrity_3_bool = dom.getContent("integrity3")
    
    # Graphical output radio button bools
    graphics_1_bool = dom.getContent("graphics1")
    graphics_2_bool = dom.getContent("graphics2")

    contents = None

    print(integrity_1_bool, integrity_2_bool, integrity_3_bool)

    path = dom.getContent("filepath")
    if path==None:
        dom.setContent("status", "Please enter a file path.")

    if not integrity_1_bool and integrity_2_bool and integrity_3_bool:
        dom.setContent("status", "Please select a hashing option.")

    if not graphics_1_bool and graphics_2_bool:
        dom.setContent("status", "Please select a graph option.") 

    #try:
    print("doing binary analysis")
    result = call_python_version("2.7", "analysis", "binary_analysis", [path, True])
    #except:
    #    dom.setContent("status", "Binary analysis failed.")
    #    return

    if integrity_1_bool == "true":
        print(integrity_1_bool, "has triggered!")
        input()
        gmail_user = "resiliencedonotreply@gmail.com"
        gmail_pass = "tubesock1"

        dest_addr = "clifford_richardson@nevada.unr.edu"

        hash_path = os.getcwd()

        log_integrity.hash_dirs(has_path)
        hash_check = log_integrity.check_hash_dirs(hash_path, verbose=True)
        print("HASH CHECK RESULT", hash_check)

        # If check_hash_dirs returns something, that means that a file is corrupt.
        # Here, we send an email with the files that were corrupted, as well as 
        # suggestions to find out how it may have been corrupted.
        if len(hash_check):
            email_str = "Hello.   \nThe following items have been flagged as corrupted or illegitimately modified in the last automated file integrity scan.\n" + \
                        str(hash_check) + "\nPATH:   " + path + "\n\n" + "Please rehash this file and compare its hash with your stored has to verify.\n" + \
                        "If there are discrepancies, check the file modification dates or any logs that record file actvity." + "\nAdditionally, please check your IDS " + \
                        "for any alerts regarding suspicious behavior."

            msg = MIMEText(email_str)
            msg["Subject"] = "File Integrity Scan Alert"
            msg["From"] = gmail_user
            msg["To"] = dest_addr

            server = smtplib.SMTP("smtp.gmail.com:587")
            server.starttls()
            server.ehlo()
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, dest_addr, msg.as_string())
            server.quit()

    if integrity_2_bool == "true":
        gmail_user = "resiliencedonotreply@gmail.com"
        gmail_pass = "tubesock1"
        dest_addr = "clifford_richardson@nevada.unr.edu"
        hash_path = os.getcwd()
        log_integrity.hash_dirs(path)

    dom.setContent("status", "Loading...")

    fields = path.split("/")
    length_fields = len(fields)
    filename = fields[length_fields-1].split(".")[0]
    results_dir = None
    if __name__ == "__main__":
        results_dir = "/home/nope/Documents/project/CS-425-PROTOTYPE/binaryAnalysis/results/"
    else:
        results_dir = "/root/CS-425-PROTOTYPE/binaryAnalysis/results"
    with open(results_dir+filename + "/" + filename + ".analytics", "r") as inputfile:
        analytics = inputfile.read()
   
    print(analytics)
    dom.setContent("filepath", "")
    dom.setContent("status", analytics)
    
    print("Analysis complete, ready for new task...")
    
    return

def acEndAnalysis(dom):
    return

IDAttrCallbacks= {
        "startAnalysis": acStartAnalysis,
        "endAnalysis": acConnect
        }

if __name__ == "__main__":
    IDAttrCallbacks = {
            "": acConnect,
            "startAnalysis": acStartAnalysis,
            "endAnalysis": acConnect
            }

    Atlas.launch(IDAttrCallbacks)
