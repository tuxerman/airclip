import requests
import datetime
import json
import os
import sys
import pyperclip

jheaders = {'Content-type': 'application/json', 'Client-ID': '22580'}

# for i in range(10):
# 	jData = {'data': 'Current iteration: %s' %str(i)}
# 	reqP = requests.post('http://127.0.0.1:8080/airclip', data = jData, headers=jheaders)
# 	reqG = requests.get('http://127.0.0.1:8080/airclip', headers=jheaders)
# 	print reqG.text


def main():
    if sys.argv[1] == '1':  # copy from clipboard
        selText = os.popen('xsel').read()
        print 'Copied:', selText
        jData = {'data': selText}
        reqP = requests.post(
            'http://127.0.0.1:5000/airclip', data=json.dumps(jData), headers=jheaders)
        print reqP

    elif sys.argv[1] == '2':
        reqG = requests.get('http://127.0.0.1:5000/airclip', headers=jheaders)
        print reqG.text
        strPaste = json.loads(reqG.text)['data']
        pyperclip.copy(strPaste)
        pyperclip.paste()

if __name__ == '__main__':
    main()
