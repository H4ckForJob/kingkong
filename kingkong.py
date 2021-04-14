import base64
from Crypto.Cipher import AES
from Crypto import Random
import os
import urllib
import json
from hashlib import md5

def padding_key(text):
    while len(text) % 16 != 0:
        text += '\0'
    return (text)

def padding_base64(data):
    missing_padding = 4-len(data)%4
    if missing_padding:
        data += b'='*missing_padding
    return (data)

def decode_req(key,password,filename,isbase64):
    if isbase64:
        mode = "r"
    else:
        mode = "rb"
    with open(filename,'r') as raw_file:
        message = raw_file.read()
        message = message.replace(password,'')
        message = urllib.unquote(message)
    key = padding_key(key) 

    encrypt_data = message
    if isbase64 == True:
        encrypt_data = padding_base64(encrypt_data)

    #print(encrypt_data)

    cipher = AES.new(key,AES.MODE_ECB)
    result2 = encrypt_data
    if isbase64 == True:
        result2 = base64.b64decode(encrypt_data)
    a = cipher.decrypt(result2)

    a = a.decode('utf-8','ignore')
    a = a.rstrip('\n')
    a = a.rstrip('\t')
    a = a.rstrip('\r')
    a = a.replace('\x06','')
    #print('\n','data:',a)

    key_list = a.split("&")
    for key in key_list:
        raw = key.split("=")
        every_key = raw.pop(0)
        #print("raw=",raw)
        for i in range(len(raw)):
            #print('i={}'.format(i))
            if raw[i] == '':
                raw[i] = '='
        s = ''.join(raw)
        #print(s)
        try:            
            print('request data:{}={}'.format(every_key,base64.b64decode(s)))
        except Exception as e:
            pass

def decode_rep(key,password,filename,isbase64):
    if isbase64:
        mode = "r"
    else:
        mode = "rb"
    with open(filename,mode) as raw_file:
        message = raw_file.read()
        md5_hash = md5(password+key).hexdigest().upper()
        prefix = md5_hash[0:16]
        suffix = md5_hash[16:32]
        #print(md5_hash,prefix,suffix)
        message = message.replace(prefix,'')
        message = message.replace(suffix,'')
        message = urllib.unquote(message)
        #print(message)
    key = padding_key(key)

    encrypt_data = message
    if isbase64 == True:
        encrypt_data = padding_base64(encrypt_data)
    cipher = AES.new(key,AES.MODE_ECB)
    result2 = encrypt_data
    if isbase64 == True:
        result2 = base64.b64decode(encrypt_data)
    a = cipher.decrypt(result2)

    a = a.decode('utf-8','ignore')
    a = a.rstrip('\n')
    a = a.rstrip('\t')
    a = a.rstrip('\r')
    a = a.replace('\x06','')
    print('reponse data:{}'.format(a))

#config
#webshell aes key
key = 'd8ea7326e6ec5916'
key = '3c6e0b8a9c15224a'
#webshell password
password = 'pass123'
password = 'pass'
#where is your file?
filepath = '.'
#is base64 mode?
isbase64 = False

for filename in os.listdir(filepath):
    try:
        decode_req(key = key,password = password, filename=filename, isbase64=isbase64)
    except Exception as e:
        print(e)

    try:
        decode_rep(key = key,password = password, filename=filename, isbase64=isbase64)
    except Exception as e:
        print(e)
