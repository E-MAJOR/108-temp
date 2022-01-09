# instead of npm (node project manager) in js, use pip for py python -m pip --version, need put on top of python a framework (flask or **django)
# using flask to use with API, but need force into the folder instead the operating system, requiring shield around folder (virtual environment) python -m pip install venv
# mac:sudo python3 -m pip install virtualenv
# win:python -m pip install virtualenv
# python server.py to run

from flask import Flask, request, abort #class with upper case F, add request to access to request, abort to return error in bad request
from mock_data import catalog
import json
import random #to import random id

#magic functions/variables __name__
app = Flask(__name__) #to create new application in Flask, with name of "Main", don't need word new Flask()

me = {
        "name": "Mark",
        "last": "Courtright",
        "age": 56,
        "hobbies": [],
        "address": {
            "street": "Jimray",
            "number": 123,
            "city": "Mishawaka"
        }
    }

@app.route("/") #a decorator, defining end points in route
#127.001 local host, not on net
#this part is python, everything else is flask
def home():  
    return "Hello from Python"

@app.route("/test") #also a get request, by default
def test_function():
    return "I'm a test function"

#return full name getting value from dictionary
@app.route("/about")  #url is /about, catch url code and return something
def about():
    return me["name"] + " " + me["last"] #dictionary exists global

#--------------------------------------------------------
#------------------API ENDPOINTS------------------------
#--------------------------------------------------------

@app.route("/api/catalog") #flask desides if get here, or post below, depending on guest request, using JSON for the format
def get_catalog():
    return json.dumps(catalog)  #later to be done from database, now mock_data, need to put into .JSON, not plain data, wont work without import json 

@app.route("/api/catalog", methods=["post"]) #casing on post not important
def save_product():
    product = request.get_json() #will give payload of the request, whatever the user sends
    print(product) #not able to do with browser url, which is for GET, therefore use "POSTMAN", we download extension "THUNDER CLIENT", click on thunder bolt on left to access
    #data validation
    #if product does not contain a title, return error, title is at least 5 chars long 
    if not 'title' in product or len(product["title"]) < 5:
        return abort(400, "Title (5 character minimum) is required")

    #needs price
    if not 'price' in product:
        return abort(400, "Product must include price")
    #validate price is float or integer, not a string, etc, before comparing with a number, or will crash
    if isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should be a number")
    #needs price > 0
    if product["price"] <= 0:
        return abort(400, "Product price must be greater than $0")
    


    #assign uniques _id
    product["_id"] = random.randint(1000, 100000)

    #save in catalog
    catalog.append(product)

    return json.dumps(product) #always need return something, even if only printing, otherwise error



@app.route("/api/cheapest")
#catalog is a global list of dictionaries
def get_cheapest():
    cheapest = catalog[0]
    for product in catalog:
        print(product["price"])
        if cheapest["price"] > product["price"]:
            cheapest = product
    return json.dumps(cheapest)

@app.route("/api/product/<id>") #<id> is a variable, that you fill in with the _id number from the catalog, it will find the product and return it
def get_product(id):
    for product in catalog:
        if product["_id"] == id:
            return json.dumps(product)

    return "DNE"

@app.route("/api/catalog/<category>")
def get_by_category(category):
    list_products = []
    category = category.lower()  #command to parse into lower only once, vs doing everytime below
    for product in catalog:
        if product["category"].lower() == category:
            list_products.append(product)
    return json.dumps(list_products)

@app.route("/api/categories")
def get_category_list():
    #list_categories = []
    #exists = False
    #for product in catalog:
    #    for in_list in list_categories:
    #        if product["category"] == in_list:
    #            exists = True
    #    if exists == False:
    #        list_categories.append(product["category"])
    #    exists = False
    list_categories = []
    for product in catalog:
        cat = product["category"]
        if cat not in list_categories:
            list_categories.append(cat)
    return json.dumps(list_categories)



app.run(debug=True) # to run app


#Rest API = "API", intermediary allows connect 2 systems, present easy to read interface, establish rules, Application Programming Interface, across the web = web api's = web services, with robo-waiters serving data to apps or websites with menu of data available, to add "+" source code, served as .JSON {} or .XML <>file
# {"video":{"id": "xxx","published":"xxx", "title":"xxx"}}
# <video> <id>xxx <published>xxx <title>xxx </video>
#google company huge with free/open API's call URL in their site, get served data back, but cannot access to change their code, with restrictions, before serving data, secret google indo protected, "the gate keeper"
#rest api's to post, delete, get 90% use .JSON strings, but.XML is more secure, by default api's = GET
#speed of processor 3.2 GHz million/sec operations