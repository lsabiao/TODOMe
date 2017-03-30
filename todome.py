#!/usr/bin/env python3

import shutil
import sys
import os
import random


#custom settings
MAX_FILES = 100
MAX_SIZE = (1024)*1024 #in kb

#terminal settings
width = shutil.get_terminal_size()[0]-2	

#string constants
nDone = u"\u25A1"
done  = u"\u25A3"

#color
ansiRed = "\033[31m"
ansiGreen = "\033[32m"
ansiYellow = "\033[33m"
ansiBlue = "\033[34m"
ansiMagenta = "\033[35m"
ansiCyan = "\033[36m"
ansiDefault = "\033[39m"

ansiNow = ""
#config constants
recursive = False
countOnly = False


#formatColors
def aR(txt):
	return ansiRed+str(txt)+ansiDefault

def aG(txt):
	return ansiGreen+str(txt)+ansiDefault

def aY(txt):
	return ansiYellow+str(txt)+ansiDefault

def aB(txt):
	return ansiBlue+str(txt)+ansiDefault

def aM(txt):
	return ansiBlue+str(txt)+ansiDefault

def aC(txt):
	return ansiCyan+str(txt)+ansiDefault

def aW(txt):
        p= ansiNow+txt+ansiDefault
        return p

def randomizeColor():
    global ansiNow
    pos = [ansiRed,ansiGreen,ansiYellow,ansiBlue,ansiMagenta,ansiCyan]
    ansiNow = pos[random.randint(0,(len(pos)-1))]

def isBinary(p):
    #linux only
    i =  os.system("file -b " + p + " | grep text > /dev/null")
    if(i == 0):
        return False
    else:
        return True

def getTodo(f):
    stat = os.stat(f)
    if(stat.st_size > MAX_SIZE):
        return False
    try:
        p = open(f,'r')
        todos = []
        aux = 0
        for linha in p:
            aux+=1
            linha = linha.strip()
            if (linha.startswith("#TODO")):
                todos.append(str(aux)+":  "+linha.strip("#TODO").strip())
            elif(linha.startswith("//TODO")):
                todos.append(str(aux)+":  "+linha.strip("//TODO").strip())
    except:
        return False
    if(todos == []):
        return False
    else:
        todos.append(f)
        return todos


def makeBox():
    print ("\n"+aR("+")+aW("-"*width)+aR("+"))

def endBox():
    print ("\n"+aR("+")+aW("-"*width)+aR("+")+"\n")
    randomizeColor()

def makeRow(msg):
    indent = 2

    div = msg.split(" ",1)
    #div[0] rown number
    #div[1] the msg
    final = (" "*indent)+aB(div[0])+div[1]

    return final

def makeHeader(msg):
    p = int((width/2)-len(msg)/2)

    #that's an ugly code :(
    if((len(msg) % 2) == 0):
        return ((" "*(p))+aY(msg)+(" "*(p+1)))
    else:
        return ((" "*(p))+aY(msg)+(" "*(p+2)))
        
def getFiles():
    filesToCheck = []
    if(recursive):
        f = os.walk(os.getcwd())
        for b in f:        
            #b[0] full path
            #b[1] folders
            #b[2] files
            for files in b[2]:
                if(isBinary(os.path.join(b[0],files))== False):
                    if(files.startswith(".") == False):
                        filesToCheck.append(os.path.join(b[0],files))
    else:
        f = os.listdir(os.getcwd())
        if(len(f) >= MAX_FILES):
            sys.exit(0)
        for b in f:
            if(os.path.isdir(b) == False):
                if(isBinary(b) == False):
                    if(b.startswith(".") == False):
                        filesToCheck.append(os.path.join(os.getcwd(),b))

    return filesToCheck

if __name__ == "__main__":
    #parsing the line arguments
    if("-i" in sys.argv):
        countOnly = True
    if("-r" in sys.argv):
        recursive = True

    randomizeColor()
    #prepare the files
    pre = [] #every index is a file
    for f in getFiles():
        p = getTodo(f)
        if(p):
            pre.append(p)
    #if -i
    if(countOnly):
        total = 0
        for t in pre:
            total+=len(t[:-1])
        if(total >= 1):
            sys.exit(total)
        sys.exit(0)

    #make the UI
    else:
        for t in pre:
            makeBox()
            print(makeHeader(t[-1]))
            for f in t[:-1]:
                print(makeRow(f))
            endBox()
    sys.exit(0)
