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

        resp = Response(strResponse, status=201, mimetype='application/json')

    elif request.method == 'POST':
        jData = request.json['data']
        jId = request.headers['Client-ID']
        jTimestamp = str(datetime.datetime.now())

        writeDoc = { "Client-ID": jId, "timestamp" : jTimestamp, "data": jData }

        # write to db
        mongoColl = db[jId]
        mongoColl.insert(writeDoc)

        # get latest
        # mongoColl.find().sort( [['_id', -1]] ).limit(1).next()

        strResponse = json.dumps({"status": "done"}, encoding='utf-8')
        resp = Response(strResponse, status=200, mimetype='application/json')

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
