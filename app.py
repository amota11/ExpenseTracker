### TO FIX ###
# 1. TypeError: 'ImmutableMultiDict' object is not callable -> on expense_record dict
# --> Might be better just to wait for an available network and setup DB in Azure or Mongo Atlas


from flask import Flask, render_template, request
# from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from pip._vendor import requests
from wtforms import StringField, DecimalField, SelectField, DateField

app = Flask(__name__)

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
    expensesByCategory = [        ("snacks", 1500.0),        ("restaurant", 25000.0),        ("services", 950.0),        
                          ("clothes", 8000.0),        ("souvenirs", 3000.0),        ("hobbies", 8850.68),
                          ("transportation", 3251.37),        ("entertainment", 2750.0),        ("ATM", 30000.0),        ("miscellaneous", 5427.45)  ]
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
        expDesc = request.form.get("Description")
        print("Displaying expense description: ")
        print(expDesc)
        # print(request.form('Location'))
        # print(request.form('Category'))
        # print(request.form('Cost'))
        # print(request.form('Currency'))
        # print(request.form('Date'))

        # Once input are captured, pass them to expensesAdded.html to display new record
        ## Optional: Save record in .txt file or in a .CSV (.CSV manip might be handy later)
        return render_template("expensesAdded.html")
    return render_template("addExpenses.html", form=expenseForm)

app.run()