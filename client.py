#!/usr/bin/env python

import requests
import datetime
import json
import os
import sys
import pyperclip

jheaders = {'Content-type': 'application/json', 'Client-ID': '22581'}
serverUrl = 'http://127.0.0.1:5000/airclip'


def getConf():
    # get client ID
    global jheaders
    global serverUrl

    fileConf = os.environ['HOME'] + '/.airclip/client.conf'
    with open(fileConf, 'r') as confReader:
        strClientConf = confReader.read()
        jConf = json.loads(strClientConf)
        jheaders['Client-ID'] = jConf['Client-ID']
        serverUrl = jConf['Server-URL']

def main():

    # TODO check for correct statuses being returned

    if sys.argv[1] == 'copy':
        selText = os.popen('xsel').read()
        jData = {'data': selText, 'action': 'copy'}
        reqP = requests.post(
            serverUrl, data=json.dumps(jData), headers=jheaders)
        if reqP.status_code == 201:
            print 'Copied:', selText
        else:
            print 'Server returned code %s: %s' % (reqP.status_code, reqP.text)
            return

    elif sys.argv[1] == 'paste':
        reqG = requests.get(serverUrl, headers=jheaders)
        if reqG.status_code == 200:
            print 'Ready to paste'
        else:
            print 'Server returned code %s: %s' % (reqG.status_code, reqG.text)
            return

        strPaste = json.loads(reqG.text)['data']
        pyperclip.copy(strPaste)
        pyperclip.paste()

    elif sys.argv[1] == 'append':
        selText = os.popen('xsel').read()
        jData = {'data': selText, 'action': 'append'}
        reqA = requests.post(
            serverUrl, data=json.dumps(jData), headers=jheaders)

        if reqA.status_code == 202:
            print 'Appended', selText
        else:
            print 'Server returned code %s: %s' % (reqA.status_code, reqA.text)


if __name__ == '__main__':
    getConf()
    main()
