import columnar_transposition as ct
import playfair
import affine
import AES

import time
from prettytable import PrettyTable

print()
def run(opt, message, key):
    t1 = time.time()
    message2 = opt(message,key)
    t2 = time.time()
    total_time = round(t2-t1,5)
    return message2, total_time

def display(name,enc, dec, plain_text, key):
    cipher, t1 = run(enc,plain_text, key)
    text, t2 = run(dec,cipher, key)

    if len(plain_text) > 20:
        text = str(len(text))+" chars"
        cipher = str(len(cipher))+" chars"

    print(name+" : Encryption")
    print("Cipher =",cipher,"\nTime =",t1)
    print(name+" : Decryption")
    print("Plain text =",text,"\nTime =",t2)
    print()
    return [name, cipher, text, t1, t2]

all_result = PrettyTable()
all_result.field_names = ["Name", "Plain text", "Cipher", "Decrypted text", "Encryption time", "Decryption time"]

file_path = "plain_text.txt"
plain_text_file = open(file_path, "r")
plain_texts = []
for i in plain_text_file:
    plain_texts.append(i.strip('\n'))
#print(len(plain_texts))
#plain_texts = plain_texts[:1]
#print(plain_text)

'''
ctkey = input("Columnar Transposition key >>> ")
pfkey = input("Playfair key >>> ")
afkey = input("Affine key >>> ")
afkey = list(map(int, afkey.split(',')))
'''
ctkey = 'hack'
pfkey = 'hack'
afkey = '17,20'
afkey = list(map(int, afkey.split(',')))
aekey = 'hack'
for plain_text in plain_texts:

    tmp = [plain_text if len(plain_text)<20 else str(len(plain_text))+' char'][0]

    key = ctkey
    result = display("Columnar Transposition",ct.encrypt,ct.decrypt,plain_text,key)
    result.insert(1,tmp)
    all_result.add_row(result)

    key = pfkey
    result = display("Playfair",playfair.encrypt,playfair.decrypt,plain_text,key)
    result.insert(1,tmp)
    all_result.add_row(result)

    key = afkey
    result = display("Affine",affine.encrypt,affine.decrypt,plain_text,key)
    result.insert(1,tmp)
    all_result.add_row(result)

    key = aekey
    result = display("AES",AES.encrypt, AES.decrypt,plain_text,key)
    result.insert(1,tmp)
    all_result.add_row(result)

print("[NOTE] Plain text that is too long will be shown as its length")
print(all_result)