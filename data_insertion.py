import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="intern"
)

data = pd.read_csv("D:\\search-app\\products.csv")

query = "INSERT INTO product (id,name,description,category,location) VALUES (%s, %s, %s, %s, %s)"

for index, row in data.iterrows():
    values = (row['id'], row['name'], row['description'], row['category'], row['location'])
    cursor = mydb.cursor()
    cursor.execute(query, values)
mydb.commit()
cursor.close()
mydb.close()

