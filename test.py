total_cost = 0
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
        ("miscellaneous", 5427.45),
    ]

for i in expensesByCategory:
    total_cost += i[1]

print("Showing expense category structure")
print(expensesByCategory)
print("Showing total expensditure")
print(total_cost)

