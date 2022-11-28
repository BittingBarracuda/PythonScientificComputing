import math
import sympy
import numpy as np
import matplotlib.pyplot as plt
from sympy.utilities.lambdify import lambdify
from scipy.interpolate import barycentric_interpolate
from scipy.interpolate import lagrange
from time import time

# Función para calcula el error en valor absolutos
def abs_error(real, aprox):
    return abs(real - aprox)

# Función f(x) = sin(x)
def f1(x):
    return math.sin(x)

# Función f(x) = 1 / (1 + 25x^2)
def f2(x):
    return 1 / (1 + 25*(x**2))

# Función f(x) = e^(-20x^2)
def f3(x):
    return math.exp(-20*(x**2))

# Implementación de las diferencias divididas de Newton
def dif_newton(x, y):
    # Comenzamos obteniendo columna por columna la matriz de diferencias divididas
    n = len(x)
    matrix = np.zeros(shape = (n, n))
    matrix[:, 0] = y
    for i in range(1, n):
        for j in range(n - i):
            matrix[j, i] = (matrix[j + 1, i - 1] - matrix[j, i - 1]) / (x[j + 1] - x[j])
    coeffs = matrix[0, :]
    
    # Pasamos a obtener la expresión a devolver
    w = sympy.symbols("w")
    to_mult = [1]
    to_mult.append(w - x[0])
    for i in range(2, len(coeffs)):
        to_mult.append(to_mult[i-1]*(w - x[i-1]))
    expr = to_mult*coeffs
    return sympy.lambdify(w, expr(w), 'numpy')


def main():
    # Nodos equiespaciados -> 11 y 21 nodos
    x_eq_11 = np.linspace(-5, 5, num = 11)
    x_eq_21 = np.linspace(-5, 5, num = 21)

    # Raices del polinomio de Chebyshev -> 11 y 21 nodos
    coef_cheb_11 = [0]*11 + [1]
    coef_cheb_21 = [0]*21 + [1]
    pol_cheb_11 = np.polynomial.chebyshev.Chebyshev(coef_cheb_11, [-5, 5])
    pol_cheb_21 = np.polynomial.chebyshev.Chebyshev(coef_cheb_21, [-5, 5])
    roots_cheb_11 = pol_cheb_11.roots()
    roots_cheb_21 = pol_cheb_21.roots()

    # Pasamos a obtener los valores reales de las funciones
    vals_eq_11 = []; vals_eq_21 = []
    vals_cheb_11 = []; vals_cheb_21 = []
    fs = [np.vectorize(f1), np.vectorize(f2), np.vectorize(f3)]
    
    for i in range(3):
        f = fs[i]
        vals_eq_11.append(f(x_eq_11))
        vals_eq_21.append(f(x_eq_21))
        vals_cheb_11.append(f(roots_cheb_11))
        vals_cheb_21.append(f(roots_cheb_21))

    # Pasamos a obtener las aproximaciones
    x_eval = np.linspace(-5, -5, num = 100)
    bary_val = np.zeros(shape = (4, 3, 100))
    lag_val = np.zeros(shape = (4, 3, 100)) 
    dif_val = np.zeros(shape = (4, 3, 100)) 
    Xs = np.array([x_eq_11, x_eq_21, roots_cheb_11, roots_cheb_21], dtype = 'object')  
    vals = np.array([vals_eq_11, vals_eq_21, vals_cheb_11, vals_cheb_21], dtype = 'object')
    times = np.zeros(shape = (4, 3, 3))
 
    for i in range(4):
        for j in range(3):
            t0 = time()
            bary_val[i, j] = barycentric_interpolate(Xs[i], vals[i, j], x_eval)
            times[i, j, 0] = time() - t0
            t0 = time()
            lag_val[i, j] = lagrange(Xs[i], vals[i, j])(x_eval)
            times[i, j] = time() - t0
            #t0 = time()
            #dif_val[i, j] = dif_newton(Xs[i], vals[i, j])(x_eval)
            #times[i, j, 2] = time() - t0
    
    


if __name__ == "__main__":
    main()