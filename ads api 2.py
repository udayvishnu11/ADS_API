from flask import Flask, request, jsonify
import json
import pymysql

app = Flask(__name__)

# Define the API key.
API_KEY = "123"

def check_api_key():
    key = request.args.get('key')
    if key != API_KEY:
        response = {
            'code': 401,
            'msg': 'Unauthorized - Invalid API key',
        }
        return jsonify(response), 401
    return None

@app.route("/getData", methods=['GET', 'POST'])
def getData():
    api_key_check = check_api_key()
    if api_key_check:
        return api_key_check

    res = {}
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    start_datef = None
    end_datef = None
    res['req'] = '/searchdate'

    try:
        start_datef = start_date
        end_datef = end_date
    except Exception as e:
        print(str(e))
        pass

    if start_datef is not None and end_datef is not None:
        conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626', passwd='ia626clarkson',
                               db='ia626', autocommit=True)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM `conlontj_datapoints` WHERE `date_time` BETWEEN %s AND %s ORDER BY `date_time` LIMIT 0, 500;'
        cur.execute(sql, (start_datef, end_datef))

        res['code'] = 0
        res['msg'] = 'ok'
        items = []

        for row in cur:
            item = {}
            item['dpid'] = row['dpid']
            item['date_time'] = row['date_time'].strftime('%Y-%m-%d %H:%M:%S')
            item['flight_num'] = row['flight_num']
            items.append(item)

        res['results'] = items
        res['num_results'] = len(items)

        cur.close()
        conn.close()

        return json.dumps(res, indent=4)

    else:
        res['msg'] = 'startdate and enddate must be entered'
    return json.dumps(res, indent=4)

@app.route("/countInPolygon", methods=['GET', 'POST'])
def countInPolygon():
    api_key_check = check_api_key()
    if api_key_check:
        return api_key_check

    res = {}
    latlong = request.args.get('polygon')
    latlongf = None
    res['req'] = '/countInPolygon'

    try:
        latlongf = latlong
    except Exception as e:
        print(str(e))
        pass

    if latlongf is not None:
        conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626', passwd='ia626clarkson',
                               db='ia626', autocommit=True)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        polygon_wkt = f'POLYGON(({latlongf}))'
        sql = 'SELECT * FROM `conlontj_datapoints` WHERE ST_Within(geo_point, ST_GeomFromText(%s, 4326));'
        cur.execute(sql, (polygon_wkt,))
        data = cur.fetchall()
        res['code'] = 0
        res['msg'] = 'ok'
        items = []
        c = 0
        for row in data:
            c += 1

        res['Count'] = c

        cur.close()
        conn.close()

        return json.dumps(res, indent=4)
    else:
        res['msg'] = 'Please provide the latlong in the correct format'
        return json.dumps(res, indent=4)

@app.route("/getAvgSpeedByFlight", methods=['GET', 'POST'])
def getAvgSpeedByFlight():
    api_key_check = check_api_key()
    if api_key_check:
        return api_key_check

    res = {}
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    start_datef = None
    end_datef = None
    res['req'] = '/getAvgSpeedByFlight'

    try:
        start_datef = start_date
        end_datef = end_date
    except Exception as e:
        print(str(e))
        pass

    if start_datef is not None and end_datef is not None:
        conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626', passwd='ia626clarkson',
                               db='ia626', autocommit=True)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT AVG(gs),`flight_num` FROM `conlontj_datapoints` WHERE `date_time` BETWEEN %s AND %s GROUP BY `flight_num` ORDER BY `flight_num` LIMIT 0,500;'
        cur.execute(sql, (start_datef, end_datef))

        res['code'] = 0
        res['msg'] = 'ok'
        items = []

        for row in cur:
            item = {}
            # Convert the Decimal to float before serialization
            item['AVG(gs)'] = float(row['AVG(gs)'])
            item['flight_num'] = row['flight_num']
            items.append(item)

        res['results'] = items
        res['num_results'] = len(items)

        cur.close()
        conn.close()

        return json.dumps(res, indent=4)

    else:
        res['msg'] = 'startdate and enddate must be entered'
    return json.dumps(res, indent=4)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
