import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, value, PULP_CBC_CMD

# Set the default goal
diet_goal = None

# Set the default total macro restrictions
min_cals = 0
max_cals = 2000
min_prot = 140
max_prot = 175
min_fats = 50
max_fats = 9999
min_carbs = 0
max_carbs = 9999

# Define the new maximum and minimum macro values
set_custom_macros = input("The default macro values are: kcal[0,2000], prot[140,175], fat[50,Inf], carbs[0,Inf].\nDo you want to set your own macro values? (Y/N): ").strip().lower() == 'y'
if set_custom_macros:
    min_cals = float(input("Enter the minimum calories value: ").strip())
    max_cals = float(input("Enter the maximum calories value: ").strip())
    min_prot = float(input("Enter the minimum protein value: ").strip())
    max_prot = float(input("Enter the maximum protein value: ").strip())
    min_fats = float(input("Enter the minimum fats value: ").strip())
    max_fats = float(input("Enter the maximum fats value: ").strip())
    min_carbs = float(input("Enter the minimum carbs value: ").strip())
    max_carbs = float(input("Enter the maximum carbs value: ").strip())

# Define the diet goal
diet_goal = input("Diet Goals: \n  0. Don't care \n  1. Low calories \n  2. High calories \n  3. Low protein \n  4. High protein \n  5. Low fat \n  6. High fat \n  7. Low carbs \n  8. High carbs \n  9. Astrology-based \nChoose a diet goal (0-9): ").strip()

# Leer datos del CSV
df = pd.read_csv('food.csv')
# print(df)

# Definir el problema
model = LpProblem(name="dieta", sense=LpMaximize)

# Crear variables
variables = {
    row['name']: LpVariable(
        name=row['name'],
        lowBound=0,
        upBound=row['max'],
        cat='Continuous' if row['unit'] == '100g' else 'Integer'
    )
    for idx, row in df.iterrows()
}

# Adjust the model based on the goal from the user input
if diet_goal == "1":
    model += lpSum([-row['kcal'] * variables[row['name']] for idx, row in df.iterrows()])
elif diet_goal == "2":
    model += lpSum([row['kcal'] * variables[row['name']] for idx, row in df.iterrows()])
elif diet_goal == "3":
    model += lpSum([-row['protein'] * variables[row['name']] for idx, row in df.iterrows()])
elif diet_goal == "4":
    model += lpSum([row['protein'] * variables[row['name']] for idx, row in df.iterrows()])
elif diet_goal == "5":
    model += lpSum([-row['fat'] * variables[row['name']] for idx, row in df.iterrows()])
elif diet_goal == "6":
    model += lpSum([row['fat'] * variables[row['name']] for idx, row in df.iterrows()])
elif diet_goal == "7":
    model += lpSum([-row['ch'] * variables[row['name']] for idx, row in df.iterrows()])
elif diet_goal == "8":
    model += lpSum([row['ch'] * variables[row['name']] for idx, row in df.iterrows()])


# Restricciones
calories = lpSum([row['kcal'] * variables[row['name']] for idx, row in df.iterrows()])
proteins = lpSum([row['protein'] * variables[row['name']] for idx, row in df.iterrows()])
fats = lpSum([row['fat'] * variables[row['name']] for idx, row in df.iterrows()])
carbs = lpSum([row['ch'] * variables[row['name']] for idx, row in df.iterrows()])

model += (calories >= min_cals, "Min Calories")
model += (calories <= max_cals, "Max Calories")
model += (proteins >= min_prot, "Min Proteins")
model += (proteins <= max_prot, "Max Proteins")
model += (fats >= min_fats, "Min Fats")
model += (fats <= max_fats, "Max Fats")
model += (carbs >= min_carbs, "Min Carbs")
model += (carbs <= max_carbs, "Max Carbs")

# Solve the problem with standard verbosity
# print(model)
solver = PULP_CBC_CMD(msg=False)
status = model.solve(solver)

# Mostrar resultados
print("\n")
if diet_goal == "9":
    print("Connecting to the stars...")
    count = 10**8
    while count > 0:
        count -= 1
    print("Connection failed. Connecting your soul, please meditate...")
    count = 10**8
    while count > 0:
        count -= 1
    print("Success!")
    count = 10**7
    while count > 0:
        count -= 1
    print("Solución óptima encontrada:")
    print("Café: 1 portion")
    print("Té matcha: 6g")
    print("HSN Extracto de té verde (25:1): 1 pill")
    print("HSN EGCG Complex (50:1): 1 pill")

elif LpStatus[status] == 'Optimal':
    print("Solución óptima encontrada:")
    for var in variables.values():
        if var.varValue > 0:
            if var.cat == 'Continuous':
                print(f"{var.name}: {var.varValue * 100:.0f} g")
            else:
                print(f"{var.name}: {var.varValue:.0f} portions") 
    print("\n")
    print(f"Diet Goal: {diet_goal}")
    print("\n")    
    print("Total Macros:")
    print(f"Total calorías: {value(calories):.2f} kcal")
    print(f"Total proteínas: {value(proteins):.2f} g")
    print(f"Total grasas: {value(fats):.2f} g")
    print(f"Total carbohidratos: {value(carbs):.2f} g")
else:
    print("No se encontró una solución óptima.")
print("\n")
print("test")
