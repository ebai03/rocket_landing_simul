<h1 align="center">Simple Rocket Landing Optimization</h1>

## Description of the problem

Given a small rocketship with thrust ($F$) and ($h$) meters above the ground, find the best possible maneuver such that the time to land ($t$) is as small as possible, without going over the maximum amount of force ($I$) the rocket can tolerate upon impact.

To simplify the problem, and also due to time constraints, the problem has been reduced to only 1 axis. Where the rocket can only travel upwards, away from the ground, or down to it's landing site.

## Solutions

In total, 3 techniques have been used to find either optimal or the best solutions to a given landing scenario:

1. [Brute Force](./fuerzabruta.py)
2. [Heuristic](./heuristica.py)
3. [Metaheristic](./metaheuristica.py)

## Simulation

To demonstrate the results of finding an optimal maneuver, the landing algorithm used in the *brute force* and *heuristic* solutions has been modified to run at real time inside the space flight simulation game Kerbal Space Program:

* [Simulación](./ksp_simul.py)

The maneuver can be modified with several parameters like:

* Time Skip Length: Dictates the amount of time taken between steps of the maneuver.
* Velocity ROC: Rate of change at which the rocket's downwards speed is reduced
* Extra Altitude: Increases the altitude at which a step in the maneuver is to be performed  

## Manual de uso (para los distintos métodos)

1. Acceder a la carpeta que contiene los archivos .py

``` bash
$ cd ../tareas-programadas-importeinnecesario/TP2/entrega2
```

2. Ejecutar la técnica deseada con la version de python.

``` bash
$ python3 (fuerzabruta.py|heuristica.py|metaheuristica.py)
```

Cualquiera de los programas mostrará un gráfico en pantalla que representa la trayectoria que se siguió, en los casos de los algoritmos de fuerza bruta y meta heurística, esta será la más óptima (que se encontró):

![graphs]({4900AE86-E08D-4587-9B25-929838E2C96A}.png)

También se imprimira en la consola los parámetros finales de dicha maniobra:

![console]({32E150A5-D033-4910-A749-5EA48E1ED279}.png)

## Manual de uso (para ksp_simul.py)

Para ejecutar este programa se necesita:

* Una copia del videojuego de simulación espacial [Kerbal Space Program](https://es.wikipedia.org/wiki/Kerbal_Space_Program) (versión 12.5 para Windows).
* Instalar el plugin [kRPC](https://krpc.github.io/krpc/index.html) desde cualquiera de los [métodos sugeridos](https://krpc.github.io/krpc/getting-started.html#the-python-client)
* Instalar el cliente de Python para kRPC:

```bash
$ pip install krpc
```

Se recomienda verificar la instalación correcta de los requisitos anteriores antes de ejecutar este programa.

Luego se debe iniciar el servidor de kRPC (preferiblemente antes de intentar el aterrizaje). Ver [la guía de inicio de kRPC](https://krpc.github.io/krpc/index.html) para más info.


Una vez cumplidos los puntos anteriores, se puede ejecutar el programa desde la terminal con:

```bash
$ python3 ksp_simul.py
```

Ejemplo de programa en medio de una maniobra:
![ksp]({FC0DB047-C44E-4DE1-9122-28348AAAB935}.png)

El programa realizará un aterrizaje automático de la nave activa:

[Video de demonstración](https://drive.google.com/file/d/1Ry9quCB065hH0fEq62p1MfjmBa-87qxl/view?usp=drive_link)

(Solo funciona cuando la velocidad horizontal de la nave es poca, alrededor de los 3m/s y en un cuerpo celeste sin atmosfera).
## Autores: Importe Innecesario

* **Esteban Isaac Baires Cerdas**
* **Elizabeth Huang Wu**
