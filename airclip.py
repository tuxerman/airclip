from flask import Flask, request, Response
import datetime
import json
import pymongo

# APP INIT
app = Flask(__name__)

# APP CONFIG
app.config['DEBUG'] = True

# DATABASE INIT
mongoDbName = 'defaultDB'
mongoConn = pymongo.MongoClient()
db = mongoConn[mongoDbName]

# HOME DOC


@app.route('/')
def api_root():
    return 'Welcome'


# MAIN API
@app.route('/airclip', methods=['GET', 'POST'])
def api_airclip():
    if request.headers['Content-Type'] != 'application/json':
        pass

    if request.method == 'GET':
        jId = request.headers['Client-ID']
        mongoColl = db[jId]
        
        # GET LATEST THINGY
        latestEntry = mongoColl.find().sort( [['_id', -1]] ).limit(1).next()

        # CREATE JSON RESPONSE
        jResponse = {"timestamp": latestEntry['timestamp'],
                        "data": latestEntry['data']}

        strResponse = json.dumps(jResponse, encoding='utf-8')

        # TODO: VALIDATE
        # 

        resp = Response(strResponse, status=200, mimetype='application/json')

    elif request.method == 'POST':
        jData = request.json['data']
        jId = request.headers['Client-ID']
        jAction = request.json['action']
        jTimestamp = str(datetime.datetime.now())

        if jAction == 'copy':

            writeDoc = { "Client-ID": jId, "timestamp" : jTimestamp, "data": jData }

            # write to db
            # TODO: Handle errors
            mongoColl = db[jId]
            mongoColl.insert(writeDoc)

            if True:
                strResponse = json.dumps({"statusmsg": "Copied to clipboard"}, encoding='utf-8')
                resp = Response(strResponse, status=201, mimetype='application/json')
            else:
                strResponse = json.dumps({"statusmsg": "Copying failed"}, encoding='utf-8')
                resp = Response(strResponse, status=401, mimetype='application/json')

        elif jAction == 'append':
            # find latest
            mongoColl = db[jId]
            latestEntry = mongoColl.find().sort( [['_id', -1]] ).limit(1).next()
            latestId = latestEntry['_id']
            latestData = latestEntry['data']
            newData = '%s %s' %(latestData, jData)

            # update record
            writeDoc = { "Client-ID": jId, "timestamp" : jTimestamp, "data": newData }
            updateStatus = mongoColl.update({"_id": latestId}, writeDoc)

            if updateStatus['err'] is None:
                strResponse = json.dumps({"statusmsg": "Clipboard appended"}, encoding='utf-8')
                resp = Response(strResponse, status=202, mimetype='application/json')
            else:                
                strResponse = json.dumps({"statusmsg": "Appending failed"}, encoding='utf-8')
                resp = Response(strResponse, status=402, mimetype='application/json')
  
    return resp


# OLDER API
@app.route('/airclipold', methods=['GET', 'POST'])
def api_airclip_old():
    if request.headers['Content-Type'] != 'application/json':
        pass

    if request.method == 'GET':
        with open('/tmp/jsonDump.txt', 'r') as jReader:
            rawData = jReader.read()

        rawData = rawData.replace('\n', '\\n')
        rawData = rawData.replace('\r', '\\r')

        jData = json.loads(rawData, encoding='utf-8')
        jResponse = json.dumps(jData)
        resp = Response(jResponse, status=201, mimetype='application/json')

    elif request.method == 'POST':
        jsonDataField = request.json['data']
        writeData = '{ "timestamp" : "%s", "data": "%s" }' % (
            str(datetime.datetime.now()), jsonDataField)
        with open('/tmp/jsonDump.txt', 'w') as jWriter:
            jWriter.write(writeData)

        jResponse = json.dumps({"status": "done"})
        resp = Response(jResponse, status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run()
