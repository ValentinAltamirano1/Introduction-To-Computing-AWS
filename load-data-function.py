import boto3
import csv
import pymysql


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket_name = 'my-bank-fraud-bucket-nwoncowocmic'
    key = 'fraudTest-CSV.csv'
    s3.Bucket(bucket_name).download_file(key, '/tmp/my-file')
    
    host = 'fraud-bank-db.cg3alcmwp2sx.us-east-1.rds.amazonaws.com'
    port = 3306
    user = 'admin'
    password = 'Valealta28'
    database = 'fraudbank'
    
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    cursor=conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
        id INT PRIMARY KEY,
        trans_date_trans_time TIMESTAMP,
        cc_num BIGINT,
        merchant VARCHAR(255),
        category VARCHAR(255),
        amt DECIMAL(10,2),
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        gender CHAR(1),
        street VARCHAR(255),
        city VARCHAR(255),
        state CHAR(2),
        zip INT,
        latitude DECIMAL(9,6),
        longitude DECIMAL(9,6),
        city_pop INT,
        job VARCHAR(255),
        dob DATE,
        trans_num VARCHAR(255),
        unix_time BIGINT,
        merch_lat DECIMAL(9,6),
        merch_long DECIMAL(9,6),
        is_fraud TINYINT
    )""")
    
   
    with open('/tmp/my-file', newline='') as csvfile:#abre el csv con nombre guardado en filename
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        i=0
        j=0
        for row in reader:
            i = i + 1
            sql = "INSERT INTO transactions (id,trans_date_trans_time,cc_num,merchant,category,amt,first_name,last_name,gender,street,city,state,zip,latitude,longitude,city_pop,job,dob,trans_num,unix_time,merch_lat,merch_long,is_fraud) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22]))
            if i==10000:
                conn.commit()
                i=0

    
    conn.commit()
    cursor.close()