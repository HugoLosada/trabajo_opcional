# Código en Python para implementar el Juego de la Vida de Conway
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
 
# Configuración de los valores para la cuadrícula
ON = 255
OFF = 0
vals = [ON, OFF]
 
def randomGrid(N):
    """Devuelve una cuadrícula de valores aleatorios de tamaño NxN"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)
 
def addGlider(i, j, grid):
    """Añade un planeador con la celda superior izquierda en (i, j)"""
    glider = np.array([[0,    0, 255],
                       [255,  0, 255],
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider
 
def addGosperGliderGun(i, j, grid):
    """Añade una Pistola Planeadora de Gosper con la celda superior izquierda en (i, j)"""
    gun = np.zeros(11*38).reshape(11, 38)
 
    # ... (omitiendo la definición completa de la pistola planeadora de Gosper por brevedad)
 
    grid[i:i+11, j:j+38] = gun
 
def update(frameNum, img, grid, N):
    # Copiar la cuadrícula ya que requerimos 8 vecinos
    # para el cálculo y avanzamos línea por línea
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # Calcular la suma de los 8 vecinos
            # utilizando condiciones de límite toroidales - x e y se envuelven
            # para que la simulación tenga lugar en una superficie toroidal.
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
 
            # Aplicar las reglas de Conway
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
 
    # Actualizar datos
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,
 
# Función principal main()
def main():
    # Los argumentos de la línea de comandos están en sys.argv[1], sys.argv[2], ...
    # sys.argv[0] es el nombre del script en sí mismo y puede ser ignorado
    # Analizar los argumentos
    parser = argparse.ArgumentParser(description="Ejecuta la simulación del Juego de la Vida de Conway.")
 
    # Añadir argumentos
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()
     
    # Configurar el tamaño de la cuadrícula
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)
         
    # Configurar el intervalo de actualización de la animación
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)
 
    # Declarar la cuadrícula
    grid = np.array([])
 
    # Verificar si se especifica la bandera de demostración "glider"
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(N*N).reshape(N, N)
        addGosperGliderGun(10, 10, grid)
    else:   # Poblar la cuadrícula con aleatorios encendidos/apagados -
            # más apagados que encendidos
        grid = randomGrid(N)
 
    # Configurar la animación
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)
 
    # # de frames?
    # Configurar el archivo de salida
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
 
    plt.show()
 
# Llamar a la función principal main
if __name__ == '__main__':
    main()

