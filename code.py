import requests
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="jadi_password",
  db= "maktab_khooneh"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE bama (price VARCHAR(100), karkard VARCHAR(100))")

brand = input('what brand do you looking for? ')

model = input('what model do you seek? ')

def get_ingfo(adress) :

    price_list = []
    far_list = []
    mixed_list = []

    page = requests.get(address)

    soup = BeautifulSoup(page.text,'html.parser')

    container = soup.find_all("p", {"class": "price hidden-xs"})

    container2 = soup.find_all("p", {"class": "cost"})


    for name in container:
        car_name = name.contents

        far_list.extend(car_name)

    for name in container2:

        a =name.find_all("span", {"itemprop": "price"})

        if a == []:

            a = ['توافقی']

        else:
            a = a[0].contents

        price_list.extend(a)

    for a in range(0,len(far_list)):

        mixed_list.append((far_list[a],price_list[a]))

    sql = "INSERT INTO bama (karkard, price) VALUES (%s, %s)"

    val = mixed_list

    mycursor.executemany(sql, val)

    mydb.commit()

address = 'https://bama.ir/car/'+brand+'/'+model
get_ingfo(address)

address = 'https://bama.ir/car/'+brand+'/'+model+'/all-trims?page=2'
print(address)
get_ingfo(address)
