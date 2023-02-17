from flask import Flask,render_template,request,redirect
import requests,datetime,pymysql,json
today = str(datetime.date.today().year-1911)+"."+datetime.date.today().strftime("%m.%d")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/storeData",methods=["GET","POST"])
def storeData():
    db = pymysql.connect(host='localhost', port=3309, user='root', password='root', db='productsinfo')
    url='https://data.coa.gov.tw/api/v1/AgriProductsTransType/'
    response = requests.get(url)
    data = response.json()['Data']
    str="Already Exists"
    for i in data:
        cursor = db.cursor()
        # Check if data already exists
        sql = "SELECT COUNT(*) FROM products WHERE date = %s AND `name`= %s AND market = %s"
        value = (i['TransDate'], i['CropName'], i['MarketName'])
        cursor.execute(sql, value)
        result = cursor.fetchone()
        if result[0] <= 0:
            # Insert new data
            sql = "INSERT INTO products (date, number, name, upper, lower, avg, volume, market) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            value = (i['TransDate'], i['CropCode'], i['CropName'], i['Upper_Price'], i['Lower_Price'], i['Avg_Price'], i['Trans_Quantity'],i['MarketName'])
            cursor.execute(sql, value)
            db.commit()
            # Delete old data
            sql = "DELETE FROM products WHERE date <> %s"
            value = (i['TransDate'])
            cursor.execute(sql, value)
            db.commit()
        cursor.close()
    db.close()
    return str
    

@app.route("/getData",methods=["GET","POST"])
def getData():
    db = pymysql.connect(host='localhost', port=3309, user='root', password='root', db='productsinfo')
    cursor = db.cursor()
    sql = "SELECT * FROM products"
    cursor.execute(sql)
    result=cursor.fetchall()
    dataList=[]
    for i in result:
        dataList.append(i)
    db.close()
    return json.dumps(dataList)
    
@app.route("/sortData",methods=["POST"])
def sortData():
    db = pymysql.connect(host='localhost', port=3309, user='root', password='root', db='productsinfo')
    data=int(request.get_data().decode())
    orderList=['date','number','name','upper','lower','avg','volume','market']
    if data==4:
        sql="SELECT * FROM `products` ORDER BY "+orderList[data]
    else:
        sql="SELECT * FROM `products` ORDER BY "+orderList[data]+" DESC"        
    cursor = db.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    dataList=[]
    for i in result:
        dataList.append(i)
    db.close()
    return json.dumps(dataList)

@app.route("/searchData",methods=["POST"])
def searchData():
    db = pymysql.connect(host='localhost', port=3309, user='root', password='root', db='productsinfo')
    data=request.get_data().decode()
    cursor = db.cursor()
    sql="SELECT * FROM products WHERE name LIKE %s"
    cursor.execute(sql,("%"+data+"%",))
    result=cursor.fetchall()
    dataList=[]
    for i in result:
        dataList.append(i)
    db.close()
    return json.dumps(dataList)

@app.route("/getContact",methods=["GET","POST"])
def getContact():
    data=request.get_json()
    db = pymysql.connect(host='localhost', port=3309, user='root', password='root', db='productsinfo')
    cursor = db.cursor()
    sql = "INSERT INTO `contact` (`name`, `phone`, `email`, `message`) VALUES (%s, %s, %s, %s)"
    value=(data['name'], data['phone'], data['email'], data['message'])
    cursor.execute(sql,value)
    db.commit()
    db.close()
    return data

if __name__ == '__main__':
    #app.debug = True
    app.run()
