# Decrypt Chromium Passwords
#
# Original script from: https://github.com/ohyicong/decrypt-chrome-passwords
# Credits: @ohyicong
#
# Usage: python3 ./dcp.py -S='XXXXXXX' -P='<user_data_path>'
#
# Ex.: python3 ./dcp.py -S 'SECRET_KEY' -P 'X:\Cases\SIR0149979\Exports\Google\Chrome\User Data\Default\Login Data'
#

# Import List
import argparse
import base64
import os
import re
import shutil
import sqlite3
import sys
from Cryptodome.Cipher import AES

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    
def get_db_connection(chromium_path_login_db):
    try:
        shutil.copy2(chromium_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome database cannot be found")
        return None

# Main Function
def main():
    parser = argparse.ArgumentParser(
            prog='Decrypt Chrome Browser Passwords - 0.1',
            description='This program was adapted from decrypt_chrome_passwords.py script developed by @ohyicong -> https://github.com/ohyicong/decrypt-chrome-passwords',
            epilog='Please check for newer version on https://github.com/palmenas/dcp')
    parser.add_argument('-S', '--secret', dest='secret', help='Secret key extracted from \'Local State\' and decrypted with DPAPI masterkey', type=str, required=True)
    parser.add_argument('-P', '--ld-path', dest='path', help='Full path to \'Login Data\' file', type=str, required=True)
    args = parser.parse_args()
    chromium_path = os.path.normpath(args.path)
    secret_key = bytes.fromhex(args.secret)

    try:
        chromium_path_login_db = os.path.normpath(chromium_path)
        conn = get_db_connection(chromium_path_login_db)
        if(secret_key and conn):
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for index,login in enumerate(cursor.fetchall()):
                url = login[0]
                username = login[1]
                ciphertext = login[2]
                decrypted_password = decrypt_password(ciphertext, secret_key)
                if (decrypted_password != ""):
                    print("Sequence: %d"%(index))
                    print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                    print("*"*50)
            # Close database connection
            cursor.close()
            conn.close()
            # Delete temp login db
            os.remove("Loginvault.db")
    except Exception as e:
        print("[ERR] %s"%str(e))
 
if __name__ == '__main__':
    main()
