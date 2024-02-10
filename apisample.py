import pymysql

# Database connection details
host = 'mysql.clarksonmsda.org'
port = 3306
user = 'ia626'
password = 'ia626clarkson'
database = 'ia626'

# Create a connection and cursor
conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database, autocommit=True)
cur = conn.cursor()

# Get the feature names
polygon_wkt = 'POLYGON((-74 42,-75 39,-74 41,-74 42))'  # Corrected polygon definition
sql = 'SELECT * FROM `conlontj_datapoints` WHERE ST_Within(geo_point, ST_GeomFromText(%s, 4326));'
cur.execute(sql, (polygon_wkt,))
feature_names = [column_info[0] for column_info in cur.description]

# Print the feature names
print(feature_names)

# Close the cursor and connection
cur.close()
conn.close()

