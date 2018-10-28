import os
import re
import hashlib

##---------------------------------
def _getexeregkey(reg):
    regdata = os.popen('reg query '+reg+' -s ').read()
    r = re.findall(r'REG_SZ    (.*?.exe)',regdata)
    exepath = []
    for i in r:
        s = i.replace('"','')
        exepath.append(s)
    return exepath

reg = ['HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\ ', 'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run '] 
##---------------------------------
exe = []
for i in reg:
    ex = _getexeregkey(i)
    exe = exe + ex


print(exe)

def file_hash(file):
    h = hashlib.sha256()
    try :
        with open(file, 'rb', buffering=0) as f:
            for b in iter(lambda : f.read(128*1024), b''):
                    h.update(b)
    except Exception:
        return 'not found'
    return h.hexdigest()

listhash = []

for i in exe:
    huh = file_hash(i)
    listhash.append(huh)
##    print( i + ' -- ' + huh)
print(listhash)
##----------------------------------
f = open("testreg.csv", "w")
for i in range(len(exe)):
    if i == (len(exe)-1):
        f.write("{}".format(exe[i]))
    if i != (len(exe)-1):
        f.write("{},".format(exe[i]))
    
f.write("\n")
for i in range(len(listhash)):
    if i == (len(listhash)-1):
        f.write("{}".format(listhash[i]))
    if i != (len(listhash)-1):
        f.write("{},".format(listhash[i]))
    
f.close()
