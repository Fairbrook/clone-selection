import functools
import random
from matplotlib import pyplot as plt
import numpy as np

from selections import ClonesSelection

domain = (0, np.pi)
m = 10


# Ecuacion general
def F(x, i) -> float:
    return -np.sin(x) * np.power(np.sin((i * x**2) / np.pi), 2 * m)


# Ecuación a dos dimensiones
def f(x, y):
    return F(x, 1) + F(y, 2)


# Punto a buscar
# print(f(2.20,1.57))


def evaluate(point):
    x, y = point
    return f(x, y)


evol = ClonesSelection(evaluate=lambda item: f(item[0], item[1])/-1,
                       random=lambda: (random.uniform(
                           domain[0], domain[1]), random.uniform(domain[0], domain[1])),
                       mutate=lambda a, b: (a[0], b[1])
                       )
evol.init_population(20)

best = None
best_counter = 0
bests = []
averages = []
coverage_percent = 0
while best_counter < 3:
    evol.epoc()
    population = evol.population

    total = 0
    new_best = None
    for receptor in population:
        eval = f(receptor[0], receptor[1])
        if new_best == None or eval < f(new_best[0], new_best[1]):
            new_best = receptor
        total += eval

    if new_best != best:
        best_counter = 0

    best_counter += 1
    best = new_best
    bests.append(f(best[0], best[1]))

    averages.append(total/len(population))


best_x, best_y = best
best_z = f(best_x, best_y)
indexes = [f'{x + 1}' for x in range(len(bests))]
print("Mejor punto: ", best_x, best_y, best_z)

# Graficación del proceso
resolution = 150
fig = plt.figure(figsize=plt.figaspect(0.4))
fig.suptitle("Busqueda de solución mediante Selección Clonal")
fig.tight_layout(pad=10)

# Evolucion
ax = fig.add_subplot(1, 2, 2)
ax.set_title("Evolución")
ax.plot(indexes, bests, label="Mejores")
ax.plot(indexes, averages, label="Promedios")
ax.set_xlabel("Generación")
ax.set_ylabel("Evaluación")
ax.legend()

# Grafica de la función
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.set_title("Función de Michalewicz")
x = np.linspace(0, np.pi, resolution)
y = np.linspace(0, np.pi, resolution)
X, Y = np.meshgrid(x, y)
Z = F(X, 1) + F(Y, 2)
ax.contourf(X, Y, Z, resolution)
ax.scatter(best_x, best_y, best_z, label="Mejor punto encontrado")
ax.legend()

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.85,
                    wspace=0.4,
                    hspace=0.4)
plt.figtext(
    0.5,
    0.01,
    f"Mejor punto encontrado x={best_x:.3f} y={best_y:.3f} z={best_z:.3f}",
    ha="center",
    fontsize=10,
)
plt.show()
