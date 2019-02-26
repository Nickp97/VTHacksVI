import sys
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode


inputFile = open("encryptedOut.txt", "r")

if inputFile.mode == 'r': #checks to make sure the file is actually open
    contents = inputFile.read()
    #print(contents)
    inputFile.close()

password = "password"
encoded_cipher = contents #sys.argv[1]

cipher = b64decode(encoded_cipher)
plaintext = decrypt(password, cipher)
#print(plaintext)
writeFile = open("decrypted_file.txt","w+")
writeFile.write(plaintext)
writeFile.close()