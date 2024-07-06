import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, value

# Leer datos del CSV
df = pd.read_csv('food.csv')

# Definir el problema
model = LpProblem(name="dieta", sense=LpMaximize)

# Crear variables
variables = {row['name']: LpVariable(name=row['name'], lowBound=0, cat='Continuous') for idx, row in df.iterrows()}

# Función objetivo (no es necesario maximizar nada en este caso, pero se puede usar una constante)
model += lpSum([0 * variables[row['name']] for idx, row in df.iterrows()])

# Restricciones
calories = lpSum([row['kcal'] * variables[row['name']] for idx, row in df.iterrows()])
proteins = lpSum([row['protein'] * variables[row['name']] for idx, row in df.iterrows()])
fats = lpSum([row['fat'] * variables[row['name']] for idx, row in df.iterrows()])
carbs = lpSum([row['ch'] * variables[row['name']] for idx, row in df.iterrows()])

model += (calories <= 2000, "Max Calories")
model += (proteins >= 185, "Min Proteins")
model += (fats >= 60, "Min Fats")

# Resolver el problema
status = model.solve()

# Mostrar resultados
if LpStatus[status] == 'Optimal':
    print("Solución óptima encontrada:")
    for var in variables.values():
        if var.varValue > 0:
            print(f"{var.name}: {var.varValue:.2f} g")
    print(f"Total calorías: {value(calories):.2f} kcal")
    print(f"Total proteínas: {value(proteins):.2f} g")
    print(f"Total grasas: {value(fats):.2f} g")
    print(f"Total carbohidratos: {value(carbs):.2f} g")
else:
    print("No se encontró una solución óptima.")

