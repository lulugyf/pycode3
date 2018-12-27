#coding=utf-8

import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from PyQt5 import QtWidgets

import subprocess as sp

def warn(msg, title="Warning", parent=None):
    QtWidgets.QMessageBox.information(parent, title, msg)

def __exec(cmd, cwd):
    p = sp.Popen(cmd, cwd=cwd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    s_out = p.stdout.read().decode("gbk")
    s_err = p.stderr.read().decode("gbk")
    msg = "[STDOUT]%s\n[STDERR]%s\n" % (s_out, s_err)
    p.terminate()
    return msg

# q12202 git 文档同步
def git_pull(wdir, parent=None):
    msg = __exec(["git", "pull"], wdir)
    warn(msg, "Pull output", parent)
    return msg

def git_push(wdir, comment="[comment]", parent=None):
    comment, ok = QtWidgets.QInputDialog.getText(parent, "Comment",
            "Comment:", QtWidgets.QLineEdit.Normal, "")
    if not ok:
        return ""
    msg = __exec(["git", "add", "."], wdir)
    msg2 = __exec(["git", "commit", "-m", comment], wdir)
    msg3 = __exec(["git", "push"], wdir)
    warn(msg3, "Push return", parent)

def git_status(wdir, parent=None):
    msg = __exec(["git", "status"], cwd=wdir)
    warn(msg, "Pull output", parent)

# q12201
def inputPassword(parent, prompt="password"):
    text, ok = QtWidgets.QInputDialog.getText(parent, "Input encryption password:",
               prompt+":", QtWidgets.QLineEdit.Password, "")
    if not ok:
        return ""
    return text


def encryptToFile(content, key, filename):
    chunksize = 64 * 1024
    outputFile = filename
    content_b = content.encode("utf8")
    filesize = len(content_b)
    IV = Random.new().read(16)

    encryptor = AES.new(getKey(key), AES.MODE_CBC, IV)

    pos = 0
    with open(outputFile, "wb") as outfile:
        outfile.write(str(filesize).zfill(16).encode("ISO8859-1"))
        outfile.write(IV)
        while pos < filesize:
            chunk = content_b[pos: pos+chunksize]

            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - (len(chunk) % 16))
            outfile.write(encryptor.encrypt(chunk))
            pos += chunksize


def decryptFromFile(key, filename):
    chunksize = 64 * 1024
    output = []

    with open(filename, "rb") as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(getKey(key), AES.MODE_CBC, IV)
        # print("--filesize", filesize)

        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            plain = decryptor.decrypt(chunk)
            # print("---plain", plain)
            output.append(plain)
    # print("---out.len", len(output), filesize)
    content_b = b"".join(output)
    text = content_b[:filesize].decode("utf8")
    # print("---text", text)
    return text

#Encryption of files
def encrypt(key, filename):
    chunksize =64 * 1024
    outputFile = "(encrypted)" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)
    
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    with open(filename, "rb") as infile:
        with open(outputFile, "wb") as outfile:
            outfile.write(filesize.encode("UTF-8"))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk +=b' ' * (16 - (len(chunk) % 16))
                outfile.write(encryptor.encrypt(chunk))

#Decryption of files
def decrypt(key, filename):
    chunksize =64 * 1024
    outputFile = filename[11:]
    
    with open(filename, "rb") as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
    
        decryptor = AES.new(key, AES.MODE_CBC, IV)
    
        with open(outputFile, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
    
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)
    
def getKey(password):
    hasher = SHA256.new(password.encode("utf-8"))
    return hasher.digest()
    
def Main():
    choice = input("Would you like to (E)ncrypt or (D)ecrypt?: ")
    if choice == 'E' or choice == 'e':
        filename = input("File to encrypt: ")
        password = input("Password: ")
        encrypt(getKey(password), filename)
        print("Done.")
    elif choice == 'D' or choice == 'd':
        filename = input("File to decrypt: ")
        password = input("Password: ")
        decrypt(getKey(password), filename)
        print("Done.")
    else:
        print("No Option selected, closing…")

if __name__ == '__main__':
    key = ""
    filename = r"E:\worksrc\pycode3\seditor\docs\work\TODO.writer"
    content = decryptFromFile(key, filename)