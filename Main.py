import sys
import requests
import json
import pickle
import cognitive_face as CF
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

subscription_key = None
SUBSCRIPTION_KEY = '23ce81d1545b4f018781e3bdfefd4e46'
BASE_URL = 'https://clases2021.cognitiveservices.azure.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

"""
This is the parent class, that inherits its characteristics to the others classes.

Arguments:
This gets the identification, personid, name, age, gender and picture from a person

Returns:
Return a created class Person
"""
class Person():
    def __init__(self, identification, personid, name, age , gender, picture):
        self.identification = identification
        self.personid = personid
        self.name = name
        self.age = age
        self.gender = gender
        self.picture = picture

"""
This is the class that has the specific characteristics of the Cashiers, and
inherits the rest from the person class

Arguments:
This gets the identification, personid, name, age, gender and picture, workday and salary from a person and have any characteristics inherits from the class person

Returns:
Return a created class Cashier
"""
class Cashier(Person):
    def __init__(self, identification, personid, name, age , gender, picture, workday , salary ):
        Person.__init__(self,identification, personid, name, age, gender, picture)
        self.workday = workday
        self.salary = salary
    def __str__(self):
        return "Identification {}, Personid {}, Name {}, Age {}, Gender {}, Picture {}, Workday {}, Salary {}".format(self.identification, self.personid, self.name, self.age, self.gender,self.picture, self.workday, self.salary)

'''
This is the class tha has the specific characteristics of the Client, and
inherits the rest from the Person class

Arguments:
This gets the identification, personid, name, age, gender and picture, profession and phonenumber from a person and have any characteristics inherits from the class person

Returns:
Return a created class Client
'''

class Client(Person):
    def __init__(self, identification, personid, name, age, gender, picture, profession, phonenumber ):
        Person.__init__(self, identification, personid, name, age, gender, picture)
        self.profession = profession
        self.phonenumber = phonenumber
    def __str__(self):
        return "Identification {}, Personid {}, Name {}, Age {}, Gender {}, Picture {}, Profession {}, Phonenumber {}".format(self.identification, self.personid, self.name, self.age, self.gender,self.picture,  self.profession, self.phonenumber)

"""
This is the class that has the specific characteristics of the Bosses, and
and inherits the rest from the person class

Arguments:
This gets the identification, personid, name, age, gender and picture, office and laboralyears from a person and have some characteristics inherits from the class person

Returns:
Return a created class Client
"""

class Boss(Person):
    def __init__(self, identification, personid, name, age, gender, picture, office, laboralyears  ):
        Person.__init__(self, identification, personid, name, age, gender, picture)
        self.office = office
        self.laboralyears = laboralyears
    def __str__(self):
        return "Identification {}, Personid {}, Name {}, Age {}, Gender {}, Picture{}, Office {}, Laboralyears {}".format(self.identification, self.personid, self.name, self.age, self.gender,self.picture, self.office, self.laboralyears)

"""
This is the class that contains the specific characteristics of the products.

Arguments:
This gets the identification, description and price to create a Product

Returns:
Returns a created class Product
"""

class Product():
    def __init__(self, identification, description, price):
        self.identification = identification
        self.description = description
        self.price = price
    def __str__(self):
        return "id {}, Description {}, Price {}".format(self.identification, self.description, self.price)

"""
This is the class that contains the specific characteristics to sell a product.

Arguments:
gets the date, cashier_id, client_id, bill_id, mount, path_photo_cashier, path_photo_client, products_id and price

Returns:
This returns a class Sale
"""

class Sales():
    def __init__(self, date, cashier_id, client_id, bill_id, mount, path_photo_cashier, path_photo_client, products_id, price ):
        self.date = date
        self.cashier_id = cashier_id
        self.client_id = client_id
        self.bill_id = bill_id
        self.mount = mount
        self.path_photo_cashier = path_photo_cashier
        self.path_photo_client = path_photo_client
        self.products_id = products_id
        self.price = price
    def __str__(self):
        return "Date {}, Cashier_id {}, Client_id {}, Bill_id {}, Mount {}, Path_photo_cashier {}, Path_photo_client {}, Products_id {}, Price {} ".format(self.date, self.cashier_id, self.client_id, self.bill_id, self.mount, self.path_photo_cashier, self.path_photo_client, self.products_id, self.price)

'''
This function gets the age based on the actual calendar

Arguments:
This function check your calendar and store it on a variable

Returns:
Returns the actual date
'''

def date():
    date = str(datetime.now())
    date = date.split()
    date = date[0]
    return date

'''
This function creates a group on Microsoft Azure database

Arguments:
This function gets the group_id and a group_name and create a group

Returns:
Return a created group in Microfoft Azure database
'''

def create_group(group_id, group_name): 
    CF.person_group.create(group_id, group_name)
    print("Created group")

'''
This function shows the existing groups on microsoft azure

Arguments:
This function check the microsoft azure database to find the created groups

Returns:
Return all the created groups
'''

def print_groups():
    f = CF.person_group.lists()
    for x in f:
        print (x)
'''

This function prints all the people on a microsoft azure group

Arguments:
This function receives a group ID and check the Microsoft azure database to find people in that group

Returns:
Return all the people on a specific group

'''
def print_people(group_id):
    f = CF.person.lists(group_id)
    for x in f:
        print (x)

"""
This function obtains from an image, the faceAttributes, to get the age, and the gender to use them in other functions.

Arguments: 
This function gets an image to analyze and gets its faceAttributes for obtains the age and gender

Returns:
This function returns a list with the picture, age and gender of a face
"""

def data():
    picture = input('Enter the image path: ')

    image_path = picture
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    'Content-Type': 'application/octet-stream'}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
    response = requests.post(
                                BASE_URL + "detect/", headers=headers, params=params, data=image_data)
    analysis = response.json()
    dic = analysis[0]
    faceattributes = dic['faceAttributes']
    age = faceattributes['age']
    gender = faceattributes['gender']
    return [picture, age, gender]  

'''
This function receives a image and group_id, then gets the faceRectangle to print the image with a rectangle and name in the face

Arguments:
Receives a image and group_id to gets the faceRectangle with the respective angles

Returns:
This function returns the picture with a rectangle and name in the face
'''

def showimage(picture, group_id):

    response = CF.face.detect(picture)
    dic = response[0]
    faceRectangle = dic['faceRectangle']
    width = faceRectangle['width']
    top = faceRectangle['top']
    height = faceRectangle['height']
    left = faceRectangle['left']
    image=Image.open(picture)
    draw = ImageDraw.Draw(image)
    draw.rectangle((left,top,left + width,top+height), outline='red')
    image.show()

"""
Reads the respectively file of the Cashier, Client and Boss classes, and prints the content with his characteristics and image
with the rectangle and name in the face.

Arguments: 
This function gets a option to see what file read and then gets the picture and characteristics for all people 
in the respective file

Returns:
Returns the characteristics for each person and the picture with a rectangle and name in the face
"""
def read():
    print ("1) Read Cashier group file")
    print ("2) Read Client group file")
    print ("3) Read Boss group file")
    o = int(input())
    if o == 1:
        with (open("Cashier.bin", "rb")) as f:
            while True:
                try:
                    e = (pickle.load(f))
                    print (e)
                    picture = (e.picture)
                    group_id = 1
                    showimage(picture, group_id)
                except EOFError:
                    break
        
    if o == 2:
        with (open("Client.bin", "rb")) as f:
            while True:
                try:
                    e = (pickle.load(f))
                    print (e)
                    picture = (e.picture)
                    group_id = 2
                    showimage(picture, group_id)
                except EOFError:
                    break

    if o == 3:
        with (open("Bosses.bin", "rb")) as f:
            while True:
                try:
                    e = (pickle.load(f))
                    print ('\n',e)
                    picture = (e.picture)
                    group_id = 3
                    showimage(picture, group_id)
                except EOFError:
                    break

'''
This function gets data for create a product and put in on the file

Arguments:
Gets the identification, description and price to make a product

Returns:
Return a product with the characteristics from the class Product and put in on a file
'''

def createproduct():
    identification = input('Enter its identification: ')
    description = input('Enter the product name: ')
    price = input('Enter the price: ')
      
    p1 = Product(identification, description, price)

    with open ("Product.bin", "ab") as f:
        pickle.dump(p1, f) 

'''
Reads the respectively file of the products and print all the products with his characteristics

Arguments:
This function read the file of the products and gets the data

Returns:
This function returns all the products with the characteristics in the file
'''
def readproduct():
      with (open("Product.bin", "rb")) as f:
        while True:
          try:
            print(pickle.load(f))
          except EOFError:
            break

'''
This function performs a sale with a selected client and cashier.

Arguments:
This gets the client_id, cashier_id, date of the sale, bill_id, mount, path_photo_cashier, path_photo_client, products_id, price

Returns:
If the money is enought it returns a sale and save it on a file
if the money is not enought, prints 'it's not enough money'
'''

def doasale(date):

    print ("which Client did you are? \n") 
    with (open("Client.bin", "rb")) as f: #This shows all the clients registered
        while True:
            try:
                e = pickle.load(f)
                print(e.identification, 'to use', e.name)
            except EOFError:
                break

        print ('\nInser the identification to the person that you are: ')
        cid = input("Insert option: ")
    with (open("Client.bin", "rb")) as f: #This is for select a client and get the respective id
        while True:
            try:
                e = pickle.load(f)
                if e.identification == cid:
                    client_id = e.personid
            except EOFError:
                break

    print ("which cashier would you like to use to make the purchase: \n")
    with (open("Cashier.bin", "rb")) as f: #This shows all the cashiers registered
        while True:
            try:
                e = pickle.load(f) 
                print(e.identification, 'to use', e.name) 
            except EOFError:
                break
        print ('\nInsert the identification to the person that want to use: ')
        cid = input("Insert option: ")

    with (open("Cashier.bin", "rb")) as f: #This is for select a cashier and get the respective id
        while True:
            try:
                e = pickle.load(f)
                if e.identification == cid:
                    cashier_id = e.personid
            except EOFError:
                break

    print("The products that we offer are: \n")
    readproduct()                                                    #This reads all the products
    products_id = input("\nType the id of the product you want: ") #This select a product

    with (open("Product.bin", "rb")) as f:
            while True:
                try:
                    e = (pickle.load(f))
                    if e.identification == products_id:  #Gets the price of the selected product
                        price = int(e.price)
                except EOFError:
                    break
    mount = int(input("How much money will you pay with?"))
    path_photo_client = input("Insert an image path of the client: ")
    path_photo_cashier = input("Insert an image path of the cashier: ")
    if mount > price:
        bill_id = mount - price
        s = Sales(date, cashier_id, client_id, bill_id, mount, path_photo_cashier, path_photo_client, products_id, price)

        with open("Sales.bin", "ab") as f: #This save the sale
            pickle.dump(s, f)

        print("Sale succesfully")
    else:
        print("It's not enough money")   

'''
This function reads all the sales of a cashier and shows the characteristics, emotions, and picture during the sale

Argument:
gets the cashier data, also gets the picture, emotion and characteristics of the cashier and client during a sale

Returns:
Shows the cashier and also shows the characteristics, emotions, and picture during the sale of the cashier and client
'''
def readsales():
    print ("which cashier would you like to see the sales: \n")
    with (open("Cashier.bin", "rb")) as f: #Select a cashier to see all the sales
        while True:
            try:
                e = pickle.load(f)
                print(e.name, 'to see his image and sales')
            except EOFError:
                break
        name = input("Insert option: ") 

    with (open("Cashier.bin", "rb")) as f:
        while True:
            try:
                e = pickle.load(f)
                if e.name == name:
                    cid = e.personid
            except EOFError:
                break

    with (open("Sales.bin", "rb")) as f:
        c = 0
        c1 = 1
        while True:
            try:
                e = pickle.load(f)
                if e.cashier_id == cid:
                    picture = (e.path_photo_cashier)
                    group_id = 1
                    showimage(picture, group_id)
                    if c < 1:
                        with (open("Cashier.bin", "rb")) as p:
                            while True:
                                try:
                                    r = pickle.load(p)
                                    if name == r.name:
                                        print("**************************Cashier**************************")
                                        print(r,'\n')
                                except EOFError:
                                    c += 1
                                    break                    

                    image_data = open(picture, "rb").read()
                    headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
                    'Content-Type': 'application/octet-stream'}
                    params = {
                        'returnFaceId': 'true',
                        'returnFaceLandmarks': 'false',
                        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
                    }
                    response = requests.post(
                                                BASE_URL + "detect/", headers=headers, params=params, data=image_data)
                    analysis = response.json()
                    dic = analysis[0]
                    faceattributes = dic['faceAttributes']
                    emotions = faceattributes['emotion']
                    print('The emotions for the sale',c1,'of the cashier were: ')
                    print(emotions,'\n')
                    print (e,'\n')
                    c1 += 1


            except EOFError:
                break


    with (open("Sales.bin", "rb")) as f:
        c = 0
        ci = 1
        ci2 = 1
        while True:
            try:
                e = pickle.load(f)
                if cid == e.cashier_id:
                        client = e.client_id
                else:
                    client = 0
                if e.client_id == client:
                    picture = (e.path_photo_client)
                    group_id = 2
                    showimage(picture, group_id)

                    print("**************************Clients**************************")
                    with (open("Client.bin", "rb")) as p:
                        c = 0
                        while True:
                                try:
                                    r = pickle.load(p)
                                    if client == r.personid:
                                        print ("The characteristics of the client", ci2, 'were:')
                                        print(r,'\n')
                                        ci2 += 1
                                        c += 1
                                except EOFError:
                                    break


                    image_data = open(picture, "rb").read()
                    headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
                    'Content-Type': 'application/octet-stream'}
                    params = {
                        'returnFaceId': 'true',
                        'returnFaceLandmarks': 'false',
                        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
                    }
                    response = requests.post(
                                                BASE_URL + "detect/", headers=headers, params=params, data=image_data)
                    analysis = response.json()
                    dic = analysis[0]
                    faceattributes = dic['faceAttributes']
                    emotions = faceattributes['emotion']
                    print('The emotions while the sale of the client', ci ,'were:')
                    print(emotions,'\n')
                    ci += 1

            except EOFError:
                break

'''
This is the general menú to create and consult about people, groups, products and files.

Argument:
gets the input

Return:
Returns the correspondent action 
'''

if __name__ == "__main__":
    print("      Menú      ")
    print("Enter 1 -> Make a group")
    print("Enter 2 -> Show all the existing groups")
    print("Enter 3 -> Consult all persons in a group")
    print("Enter 4 -> To make a cashier")
    print("Enter 5 -> To make a client")
    print("Enter 6 -> To make a boss")
    print("Enter 7 -> To read the group files")
    print("Enter 8 -> To read all product")
    print("Enter 9 -> To make a product")
    print("Enter 10 -> To make a sale")
    print("Enter 11 -> To show sales from a cashier")
    case = int(input())

    if case == 1 :
        group_id = int(input("Enter the group ID: "))
        group_name = input("Enter the group name: ")
        create_group(group_id, group_name)

    if case == 2:
        print_groups()
        
    elif case == 3 :
        group_id = int(input("Enter the group ID: "))
        print_people(group_id)

    elif case == 4:
        data = data()
        picture = data[0]
        age = data[1]
        gender = data[2]

        group_id = 1
        Identification = input('Enter its identification: ')
        name = input('Enter the person name: ')
        workday = input('Enter the workday: ')
        salary = input('Enter the salary: ')
        response = CF.person.create(group_id,name, Identification)
        person_id = response['personId']
        CF.person.add_face(picture, group_id, person_id)

        CF.person_group.train(group_id)

        response = CF.person_group.get_status(group_id)

        status = response['status']
        print(status)
        p1 = Cashier(Identification, person_id, name, age,gender, picture , workday, salary)

        with open ("Cashier.bin", "ab") as f:
            pickle.dump(p1, f) 


    elif case == 5:
        data = data()
        picture = data[0]
        age = data[1]
        gender = data[2]

        group_id = 2
        Identification = input('Enter its identification: ')
        name = input('Enter the person name: ')
        profession = input('Enter the profession: ')
        phonenumber = input('Enther the phonenumber: ')
        response = CF.person.create(group_id,name, Identification)
        person_id = response['personId']
        CF.person.add_face(picture, group_id, person_id)

        CF.person_group.train(group_id)

        response = CF.person_group.get_status(group_id)

        status = response['status']
        print(status)
        p1 = Client(Identification, person_id, name, age,gender,picture,profession, phonenumber)

        with open ("Client.bin", "ab") as f:
            pickle.dump(p1, f) 

    elif case == 6:
        data = data()
        picture = data[0]
        age = data[1]
        gender = data[2]

        group_id = 3

        Identification = input('Enter its identification: ')
        name = input('Enter the persons name: ')
        office = input('Enter its office: ')
        laboralyears = input('Enter its worked years: ')
        response = CF.person.create(group_id,name, Identification)
        person_id = response['personId']
        CF.person.add_face(picture, group_id, person_id)

        CF.person_group.train(group_id)

        response = CF.person_group.get_status(group_id)

        status = response['status']
        print(status)
        p1 = Boss(Identification, person_id, name, age,gender,picture,office, laboralyears)
        with open ("Bosses.bin", "ab") as f:
            pickle.dump(p1, f) 
            
    elif case == 7:
        read()
    
    elif case == 8:
        readproduct()

    elif case == 9:
        createproduct()
    
    elif case == 10:
        date = date()
        doasale(date)

    elif case == 11:
        readsales()

#Cr7 cashier
#Edgar cashier

#Brenda client
#Pedrito Client