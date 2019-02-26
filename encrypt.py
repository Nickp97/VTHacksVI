import sys
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode

inputString = sys.argv[1]
inputFile = open(inputString, "r")

password = "password"
message = inputFile.read()
inputFile.close()

cipher = encrypt(password, message)
encoded_cipher = b64encode(cipher)
#print(encoded_cipher)
writeFile = open("encryptedOut.txt","w+") #create a read text file
writeFile.write(encoded_cipher)
writeFile.close()