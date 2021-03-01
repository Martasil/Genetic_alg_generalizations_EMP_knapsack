source_file = open("EMP_7x7_2_7_1.txt", "r")

baldosas = []

line1 = source_file.readline()
stripped_line1 = line1.strip()
for s in stripped_line1:
  if s.isdigit():
    size = int(s)

line2 = source_file.readline()
stripped_line2 = line2.strip()
colores = []
for s in stripped_line2:
  if s.isdigit():
     colores.append(int(s))
colores_interiores = colores[0]
colores_exteriores = colores[1]

line3 = source_file.readline()

# Creamos las baldosas de los nodos interiores
for line in source_file:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  baldosa = list()
  for s in line_list:
    if s.isdigit():
      baldosa.append(int(s))
  baldosas.append(baldosa)

source_file.close()

size2 = size * 2
size3 = size * 3
size4 = size * 4
size_squared = size*size
total_nodos = size4 + size_squared

# Creamos las baldosas del marco:
for i in range(size4):
    baldosas.append([0])

# Creamos los nodos de la instancia
nodos = []
for i in range(1, total_nodos+1):
  nodos.append(i)

# Creamos la lista en la que vamos a almacenar los vecinos
vecinos = []
for i in range(total_nodos-1):
  vecinos.append([])

# Creamos la lista de vecinos para los nodos del marco

# Fila superior marco
for i in range(size):
  vecinos[i].append(i + size4 + 1)

# Fila derecha marco
for i in range(size, size2):
  pos_fila = i- size
  vecinos[i].append(size+size4 + size*pos_fila)

# Fila inferior marco
for i in range(size2, size3):
  pos_columna_clockwise = i- size2
  vecinos[i].append(total_nodos - pos_columna_clockwise)

# Fila izquierda marco
for i in range(size3, size4):
  pos_fila_clockwise = i- size3
  vecinos[i].append(total_nodos-size+1 - size*pos_fila_clockwise)

# Creamos la lista de vecinos para la esquina arriba izquierda

nodo_esquina1 = size4 + 1
vecinos.append([])
vecinos[nodo_esquina1 - 1].append(1)
vecinos[nodo_esquina1 - 1].append(nodo_esquina1 + 1)
vecinos[nodo_esquina1 - 1].append(nodo_esquina1 + size)
vecinos[nodo_esquina1 - 1].append(nodo_esquina1 - 1)

# Creamos la lista de vecinos para la esquina arriba derecha

nodo_esquina2 = size4 + size
vecinos[nodo_esquina2 - 1].append(size)
vecinos[nodo_esquina2 - 1].append(size + 1)
vecinos[nodo_esquina2 - 1].append(nodo_esquina2 + size)
vecinos[nodo_esquina2 - 1].append(nodo_esquina2 - 1)

# Creamos la lista de vecinos para la esquina abajo derecha

nodo_esquina3 = total_nodos
vecinos[nodo_esquina3 - 1].append(nodo_esquina3 - size)
vecinos[nodo_esquina3 - 1].append(size2)
vecinos[nodo_esquina3 - 1].append(size2 + 1)
vecinos[nodo_esquina3 - 1].append(nodo_esquina3 -1)


# Creamos la lista de vecinos para la esquina abajo derecha

nodo_esquina4 = total_nodos - size + 1
vecinos[nodo_esquina4 - 1].append(nodo_esquina4 - size)
vecinos[nodo_esquina4 - 1].append(nodo_esquina4 + 1)
vecinos[nodo_esquina4 - 1].append(size3)
vecinos[nodo_esquina4 - 1].append(size3 + 1)

# Creamos la lista de vecinos para los nodos de la fila superior (no esquinas)

nodos_superior = range(size4 + 1, size4 + size - 1)
for i in nodos_superior:
  nodo = i + 1
  pos_columna = i - size4 + 1
  vecinos[i].append(pos_columna)
  vecinos[i].append(nodo + 1)
  vecinos[i].append(nodo + size)
  vecinos[i].append(nodo - 1)

# Creamos la lista de vecinos para los nodos de la fila derecha (no esquinas)

nodos_derecha = []

for pos_fila in range(1,size-1):
  nodos_derecha.append(size+size4 + size*pos_fila)

pos_fila = 2
for n in nodos_derecha:
  vecinos[n - 1].append(n - size)
  vecinos[n - 1].append(pos_fila + size)
  vecinos[n - 1].append(n + size)
  vecinos[n - 1].append(n - 1)
  pos_fila += 1

# Creamos la lista de vecinos para los nodos de la fila inferior (no esquinas)

nodos_inferior = []

for pos_columna_clockwise in range(1,size-1):
  nodos_inferior.append(total_nodos - pos_columna_clockwise)

pos_columna = 2
for n in nodos_inferior:
  vecinos[n - 1].append(n - size)
  vecinos[n - 1].append(n + 1)
  vecinos[n - 1].append(size2 + pos_columna)
  vecinos[n - 1].append(n - 1)
  pos_columna += 1

# Creamos la lista de vecinos para los nodos de la fila izquierda (no esquinas)

nodos_izquierda = []

for pos_fila_clockwise in range(2,size):
  nodos_izquierda.append(total_nodos - size*pos_fila_clockwise  + 1)

pos_fila = 2
for n in nodos_izquierda:
  vecinos[n - 1].append(n - size)
  vecinos[n - 1].append(n + 1)
  vecinos[n - 1].append(n + size)
  vecinos[n - 1].append(pos_fila + size3)
  pos_fila += 1

# Creamos la lista de vecinos para los nodos que no comparten ninguna arista con el marco

nodos_dentro = []
for pos_columna in range(2,size):
  num_filas_dentro = size - 2
  i = 1
  while i <= num_filas_dentro:
    nodos_dentro.append(size4 + size * i + pos_columna)
    i += 1

for n in nodos_dentro:
  vecinos[n - 1].append(n - size)
  vecinos[n - 1].append(n + 1)
  vecinos[n - 1].append(n + size)
  vecinos[n - 1].append(n - 1)
