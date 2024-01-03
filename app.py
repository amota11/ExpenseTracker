### TO DO -OR- FIX ###
# 1. Review and add more comments
# 2. Azure connection and deployment

import bson
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import csv
#from pip._vendor import requests

## Access for MongoDB Atlas cluster ##
load_dotenv()
connection_string: str = os.environ.get("CONNECTION_STRING")
mongo_client: MongoClient = MongoClient(connection_string)

## Adding Atlas DB and collection  ##
database: Database = mongo_client.get_database("expenses")
collection: Collection = database.get_collection("records")
# Create a new client and connect to the server


## Test for DB connection - SUCCESS 01/03/2023 ##
# record = { "description" : "Ninja Pocket WiFi", "location" : "Terminal 1, Narita Intl. Airport, Narita",
#           "category" : "services", "cost" : "5000", "currency" : "JPN", "date" : "2023-11-20"}
# collection.insert_one(record) 

app = Flask(__name__)
app.config["SECRET_KEY"]="include_a_strong_secret_key"


### Expense Class ###
class Expense(FlaskForm):
    description = StringField('Description')
    location = StringField('Location')
    category = SelectField('Category', choices = [("snacks", "Snacks"),
                                                  ("restaurant","Restaurant"),
                                                  ("services","Services"),
                                                  ("clothes","Clothes"),
                                                  ("souvenirs","Souvenirs"),
                                                  ("hobbies","Hobbies"),
                                                  ("transportation","Transportation"),
                                                  ("entertainment","Entertaimnet"),
                                                  ("ATM", "ATM"),
                                                  ("miscellaneous","Miscellaneous"),])
    cost = DecimalField('Cost')
    currency = SelectField('Currency', choices=[("JPN","Japanese Yen"),
                                                ("USD", "US Dollar")])
    date = DateField(label="Date", format = '%m/%d/%Y')

#### Currency Conversion Function (?) ####

##### Expenses Total By Category #####
def get_total_expenses(cat):
    query = {"category" : cat}
    expense_category = collection.find(query)
    total_by_category = 0
    for i in expense_category:
        total_by_category += float(i["cost"])
    return total_by_category

###### APP ROUTES ######
@app.route('/')
## Index page will display total expenditure and expense by category ##
def index():
    # Got overall total from all records
    all_expenses = collection.find()
    print(all_expenses)
    total_cost = 0
    for i in all_expenses:
        print(i)
        total_cost += float(i["cost"])
    # Expense by category structure
    print("Querying DB to create Expense by category structure before routing")
    expensesByCategory = [        
                            ("snacks", get_total_expenses("snacks")),
                            ("restaurant", get_total_expenses("restaurant")),
                            ("services", get_total_expenses("services")),
                            ("clothes", get_total_expenses("clothes")),
                            ("souvenirs", get_total_expenses("souvenirs")),
                            ("hobbies", get_total_expenses("hobbies")),
                            ("transportation", get_total_expenses("transportation")),
                            ("entertainment", get_total_expenses("entertainment")),
                            ("ATM", get_total_expenses("ATM")),
                            ("miscellaneous", get_total_expenses("miscellaneous"))
                        ]
    # Validate expense category structure and total cost
    print(" ... ")
    print("Showing expense category structure")
    print(expensesByCategory)
    print(" ... ")
    print("Showing total expensditure")
    print(total_cost)
    print(" ... ")
    return render_template("index.html", allExpenses=total_cost, expByCat=expensesByCategory)

@app.route('/addExpenses', methods=["GET", "POST"])
def addExpenses():
    print("Opening Add Expense page")
    # Create a new Expense instant from defined class. Instant will be passed to addExpense.html
    print("Creating new expense record. Please wait...")
    print("...")
    expenseForm = Expense(request.form)
    # Capture input from addExpense into the expense_record list (OR vars below is dict doesn't work ;~; )
    if request.method == "POST":
        print("Creating expense record dictionary")
        print(" ... ")
        expDesc = request.form.get('description')
        expLoc = request.form.get('location')
        expCat = request.form.get('category')
        expCost = request.form.get('cost')
        expCurr = request.form.get('currency')
        expDate = request.form.get('date')
        newExp = {
            'description' : expDesc,
            'location' : expLoc,
            'category' : expCat,
            'cost' : expCost,
            'expCurr' : expCurr,
            'date' : expDate 
        }
        print("Adding expense to database")
        print(" ... ")
        collection.insert_one(newExp)
        print(" ... ")
        print("New record successfully added to database!!!")
        # Once input are captured, pass them to expensesAdded.html to display new record
        ## Optional: Save record in .txt file or in a .CSV (.CSV manip might be handy later)
        return render_template("expensesAdded.html")
    return render_template("addExpenses.html", form=expenseForm)

app.run()