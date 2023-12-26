### TO FIX ###
# 1. TypeError: 'ImmutableMultiDict' object is not callable -> on expense_record dict
# --> Might be better just to wait for an available network and setup DB in Azure or Mongo Atlas


from flask import Flask, render_template, request
# from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from pip._vendor import requests
from wtforms import StringField, DecimalField, SelectField, DateField
import csv

app = Flask(__name__)
# app.config.from_object('config')
# app.config.from_pyfile('config.py')
app.config["SECRET_KEY"]="include_a_strong_secret_key"

## DB CONN FOR LATER - NoSQL(Mongo) or SQL (Azure based)??? ##
# app.config["SECRET_KEY"] = "Include_a_strong_secret_key"
# app.config["MONGO_URI"] = "..."
# mongo = PyMongo(app)
# myDB - mongo.db

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
    cost = DecimalField("Cost")
    currency = SelectField('Currency', choices=[("JPN","Japanese Yen"),
                                                ("USD", "US Dollar")])
    date = DateField(label="Date", format = '%m/%d/%Y')

def saveRecord(expRecord):
    with open('storage/expDB.csv', 'a', newline='') as csv_file:
        record_struct = [
            'Description', 'Location', 'Category', 'Cost', 'Currency', 'Date'
        ]
        new_row = expRecord
        #print("1. Creating new record dictionary")
        print("...")
        print("...")
        # new_record = dict(zip(record_struct, expRecord))
        #print("Done! Dictionary record created!!")
        #print("2. Saving dictionary record to expDB.csv")
        print("...")
        print("...")
        dbWriter = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        dbWriter.writerow(new_row)
    return ("Done! new record saved in expDB.csv!")

#### Currency Conversion Function ####
#
#
#
#

##### Total Expenses Function #####
#
#
#
#

###### APP ROUTES ######
@app.route('/')
## Index page will display total expenditure and expense by category ##
def index():
    ## Check if DB exist (LATER) ##
    # my_expenses = ...
    total_cost = 0
    # for i in my_expenses:
    #     total_cost += float(i["cost"])
    expensesByCategory = [        
                            ("snacks", 1500.0),
                            ("restaurant", 25000.0),
                            ("services", 950.0),
                            ("clothes", 8000.0),
                            ("souvenirs", 3000.0),
                            ("hobbies", 8850.68),
                            ("transportation", 3251.37),
                            ("entertainment", 2750.0),
                            ("ATM", 30000.0),
                            ("miscellaneous", 5427.45)
                        ]
    for i in expensesByCategory:
        total_cost += i[1]

    ## Validate expense category structure ##
    print("Showing expense category structure")
    print(expensesByCategory)
    print("Showing total expensditure")
    print(total_cost)
    return render_template("index.html", expenses=total_cost, expCat=expensesByCategory)

@app.route('/addExpenses', methods=["GET", "POST"])
def addExpenses():
    print("Opening Add Expense page")
    # Create a new Expense instant from defined class. Instant will be passed to addExpense.html
    expenseForm = Expense(request.form)
    print("Creating new expense record. Please wait...")
    print("...")
    # Capture input from addExpense into the expense_record list (OR vars below is dict doesn't work ;~; )
    if request.method == "POST":
        print("New expense request created")
        expRecord = [
            request.form.get('description'),
            request.form.get('location'),
            request.form.get('category'),
            request.form.get('cost'),
            request.form.get('currency'),
            request.form.get('date')
        ]
        saveRecord(expRecord)
        # Once input are captured, pass them to expensesAdded.html to display new record
        ## Optional: Save record in .txt file or in a .CSV (.CSV manip might be handy later)
        return render_template("expensesAdded.html")
    return render_template("addExpenses.html", form=expenseForm)

app.run()