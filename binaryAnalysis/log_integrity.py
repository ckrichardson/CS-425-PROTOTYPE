import hashlib, os

"""
This function hashes all the files in a referenced dictory and then creates
combo lists of the file and its hash.   It also outputs a final hash of the
entire directory at the end.
"""
def hash_dirs(path, verbose=False):

    md5hashDir = hashlib.md5()
    if not os.path.exists(path):
        return 0

    for root, dirs, files in os.walk(path):
        output_file = open(path + "/integrity.hash", 'w+')
        for element in files:
            if verbose:
                print("Hashing ", element)
            filepath = os.path.join(root, element)

            input_file = open(filepath, 'rb')
            md5hashFile = hashlib.md5()
            while True:
                input_buffer = input_file.read(4096)
                # print(input_buffer)
                if not input_buffer:
                    output_file.write(element + ':' + md5hashFile.hexdigest() + "\n")
                    break
                md5hashFile.update(hashlib.md5(input_buffer).hexdigest().encode())
                md5hashDir.update(hashlib.md5(input_buffer).hexdigest().encode())
            
            input_file.close()
        
        output_file.close()

    return md5hashDir.hexdigest()

"""
This rehashes all the files in the referenced directory.   It reads past hashes from a combo list
that is saved locally.   If there is a difference in the hashes, then it will return a list of 
filenames that it has determined has changed illegitimately.   
"""

def check_hash_dirs(path, verbose=False):
    md5hashDir = hashlib.md5()
    if not os.path.exists(path):
        return 0

    list_of_mismatch = []

    input_file = open(path + "/integrity.hash", 'r')
    combos = input_file.read()
    input_file.close()

    input_file = open(path + "/integrity.hash", 'r')

    for root, dirs, files in os.walk(path):
        for element in files:
            filepath = os.path.join(root, element)

            input_file = open(filepath, 'rb')
            md5hashFile = hashlib.md5()
            while True:
                input_buffer = input_file.read(4096)
                if not input_buffer:
                    combo = element + ':' + md5hashFile.hexdigest() + "\n"
                    if combo in combos:
                        print("match!")
                    elif element != "integrity.hash":
                        list_of_mismatch.append(element)
                    break
                # print(input_buffer)
                md5hashFile.update(hashlib.md5(input_buffer).hexdigest().encode())
                md5hashDir.update(hashlib.md5(input_buffer).hexdigest().encode())
            input_file.close()

    return list_of_mismatch

if __name__ == "__main__":
    import smtplib
    from email.mime.text import MIMEText
    gmail_user = "resiliencedonotreply@gmail.com"
    gmail_pass = "tubesock1"

    dest_addr = "clifford_richardson@nevada.unr.edu"

    path = input("Please enter path")
    
    hash_dirs(path)
    hash_check = check_hash_dirs(path, verbose=True)
    print("HASH CHECK RESULT", hash_check)

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
        
