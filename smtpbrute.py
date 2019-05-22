#!/usr/bin/python
import argparse
import socket
import time
import sys
import re

def serverConnect(target, port, wordlist):
    #create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #create a connection to the server
    connect = s.connect((target,int(port)))
    #recieve the banner
    banner = s.recv(1024)
    print('Connected to: ' + banner).rstrip()
    #open wordlist
    file = open(wordlist,'r').read()
    line = 1 
    #verify username
    for x in file.split('\n'):
        s.send('VRFY ' + x + '\r\n')
        result = s.recv(1024)
        if re.search('252 ', result):
            print('Username: ' + x + ' VALID ') ; time.sleep(1)
            sys.stdout.flush()
        elif re.search('550 ', result):
            sys.stdout.write("[%s] Testing: %s\r" %  (line,x) )
            sys.stdout.flush()
        elif re.search('421 ', result):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect = s.connect((target,int(port)))
        else:
            print(result)
        line += 1
    #close connection
    s.close()

def main():
    example = 'usage: smtpbrute.py -t 127.0.0.1 -w rockyou.txt'
    parser = argparse.ArgumentParser(prog='smtpbrute.py',
                                     description='smtp username brute scanner',
                                     epilog=example,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-t','--target',action="store",dest='target')
    parser.add_argument('-w','--wordlist',action="store",dest='wordlist')
    parser.add_argument('-p','--port',action="store",dest='port',default=25)
    args = parser.parse_args()
    if (args.target == None) | (args.wordlist == None):
        print(parser.epilog)
        sys.exit(1)
    else:
        target = args.target
        wordlist = args.wordlist
        port = args.port
    s = serverConnect(target, port, wordlist)



if __name__ == '__main__':
    main()
