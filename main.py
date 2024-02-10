import json,pymysql,time
from flask import Flask
from flask import request,redirect


app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def root():
    res = {} 
    res['code'] = 2
    res['msg'] = 'ok'
    res['req'] = '/'
    return json.dumps(res,indent=4)


@app.route("/searchdate", methods=['GET','POST'])
def searchCountry():
    
    res = {} 
    res['req'] = '/searchdate'
    sart_date = request.args.get('date1')
    end_date = request.args.get('date2')
    if end_date is None:
        res['code'] = 1
        res['msg'] = 'enddate and start date needs to be provided.'
        return json.dumps(res,indent=4)
    conn = pymysql.connect(host='mysql.clarksonmsda.org', port=3306, user='ia626',passwd='ia626clarkson', db='ia626', autocommit=True) #setup our credentials
    cur = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM conlontj_airlines WHERE `date_time` between %s and %s ORDER BY `date_time` limit 0,500;'
    st = f'%{}%'
    cur.execute(sql,(st))
    res['code'] = 0
    res['msg'] = 'ok'
    items = []
    for row in cur:
        item = {}
        item['icao'] = row['icao']
        item['country'] = row['country']
        item['airline'] = row['airline']
        items.append(item)

    res['results'] = items
    res['num_results'] = len(items)
    return json.dumps(res,indent=4)

if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)