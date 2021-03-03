import random


def fitness(cromosoma, aristas, vecinos, baldosas):
    """
    La función fitness calcula el valor
    de cada cromosoma, es decir, el número
    de aristas rotas en el cromosoma
    :param cromosoma: el cromosoma cuyo valor queremos conocer
    :param aristas: las aristas de la instancia
    :param vecinos: lista de listas de vecinos de cada nodo
    :param baldosas: el conjunto de baldosas de la instancia
    :return: el número de aristas rotas de la solución
    """
    fit = 0
    for a in aristas:
        nodo1 = a[0]
        nodo2 = a[1]
        baldosa1 = baldosas[cromosoma[nodo1-1]]
        baldosa2 = baldosas[cromosoma[nodo2-1]]
        pos_nodo1 = vecinos[nodo2-1].index(nodo1)
        pos_nodo2 = vecinos[nodo1-1].index(nodo2)
        if baldosa1[pos_nodo2] != baldosa2[pos_nodo1]:
            fit += 1
    return fit


def conversion_probabilidades(lst, x):
    lst_2 = []
    for i in lst:
        lst_2.append(x-i)
    return lst_2


def gen_algorithm(nodos, aristas, baldosas, n_p, max_rep, pc, pm):
    """
    Esta función es la que ejecuta el algoritmo genético
    para obtener una solución del problema MIN AR con copias infinitas
    y con las baldosas fijas
    :param nodos: lista de nodos de la instancia de MIN AR,
    suponemos que se llaman 1,2,3... pero el nodo 1 no tiene
    por qué tener aridad 1, ni el 2 aridad 2, etc.
    :param aristas: aristas de la instancia de MIN AR
    :param baldosas: baldosas de la instancia de MIN AR (suponemos
    que hay, al menos, una baldosa válida para cada nodo y que las baldosas
    están colocadas en el orden de los vecinos que obtenga el algoritmo,
    es decir, si el algoritmo saca la lista de vecinos para el nodo
    3 como l = [2,1] y la baldosa en el nodo 3 es b = [a,b],
    entonces la baldosa tiene la arista {2,3} de color a y
    la arista {1,3} de color b)
    :param n_p: tamaño de la población
    :param max_rep: número de generaciones
    :param pc: probabilidad de recombinación
    :param pm: probabilidad de mutación
    :return: devuelve una lista con las baldosas escogidas
    Si devuelve la lista [x,y,z] quiere decir que el nodo
    1 ha tomado la baldosa en la posición x de la lista de
    baldosas, el nodo 2 la baldosa en la posición y de la lista
    de baldosas y el nodo 3 la baldosa en la posición z
    """
    num_nodos = len(nodos)       # Número de nodos
    n_b = len(baldosas)          # Número de baldosas
    n_a = len(aristas)           # Número de aristas
    n_p = n_p                    # Número de soluciones iniciales
    # Separamos las baldosas en listas dependiendo de su aridad
    l_b_orden = []
    impar = 0
    if n_p % 2 != 0:
        impar = 1
    i = 0
    while i < n_b:
        b = baldosas[i]
        aridad = len(b)
        while len(l_b_orden) < aridad:
            l_b_orden.append([])
        l_b_orden[aridad - 1].append(i)
        i += 1
    # Obtenemos la aridad de cada nodo
    l_aridades = [0] * num_nodos
    l_vecinos = []
    while len(l_vecinos) < num_nodos:
        l_vecinos.append([])
    for a in aristas:
        v1 = a[0]
        v2 = a[1]
        l_vecinos[v1-1].append(v2)
        l_vecinos[v2-1].append(v1)
        l_aridades[v1 - 1] += 1
        l_aridades[v2 - 1] += 1
    # Ponemos los nodos en listas por aridades
    l_nodos_orden = []
    j = 0
    while j < max(l_aridades):
        l_nodos_orden.append([])
        j += 1
    for n in nodos:
        l_nodos_orden[l_aridades[n-1]-1].append(n)
    # Creación de posibles soluciones (cromosomas)
    cromosomas = []
    valores_fitness = []
    while len(cromosomas) < n_p:
        x = []
        for n in nodos:
            x.append(random.choice(l_b_orden[l_aridades[n-1]-1]))
        cromosomas.append(x)
    rep = 0
    while rep < max_rep:
        # Calculamos el valor de cada cromosoma y lo almacenamos en una lista
        valores_fitness = []
        i = 0
        while len(valores_fitness) < n_p:
            valores_fitness.append(fitness(cromosomas[i], aristas, l_vecinos, baldosas))
            i += 1
        # Creamos una nueva población en la que
        # iremos añadiendo los descendientes de nuestra actual población
        nueva_pob = []
        # Ajustamos los valores de los cromosomas
        # para que sean todos mayores o iguales que 0
        while len(nueva_pob) < n_p:
            # Elegimos a una pareja de progenitores
            lst = []
            for w in range(0, n_p):
                lst.append(w)
            valores_fitness_probs = conversion_probabilidades(valores_fitness, n_a)
            padres_pos = random.choices(lst, valores_fitness_probs, k=2)
            padres = [cromosomas[padres_pos[0]], cromosomas[padres_pos[1]]]
            # Decidimos si se da una recombinación o no
            x = random.choices([0, 1], weights=[1 - pc, pc])
            descendiente1 = []
            descendiente2 = []
            # Recombinación
            if x[0] == 1:
                locus = random.randint(0, num_nodos - 1)
                # Creamos a los dos descendientes
                for j in range(locus):
                    descendiente1.append(padres[0][j])
                for k in range(locus, num_nodos):
                    descendiente1.append(padres[1][k])
                for j in range(locus):
                    descendiente2.append(padres[1][j])
                for k in range(locus, num_nodos):
                    descendiente2.append(padres[0][k])
            # No recombinación, los descendientes
            # son una copia exacta de los padres
            else:
                descendiente1 = padres[0]
                descendiente2 = padres[1]
            # Decidimos si el primer descenciente sufre una mutación o no
            y1 = random.choices([0, 1], weights=[1 - pm, pm])
            if y1[0] == 1:  # Mutación descendiente1
                locus = random.randint(0, num_nodos - 1)
                descendiente1[locus] = random.choice(l_b_orden[l_aridades[locus]-1])
            # Decidimos si el segundo descenciente sufre una mutación o no
            y2 = random.choices([0, 1], weights=[1 - pm, pm])
            if y2[0] == 1:  # Mutación descendiente2
                locus = random.randint(0, num_nodos - 1)
                descendiente2[locus] = random.choice(l_b_orden[l_aridades[locus]-1])
            # Incluimos los nuevos descendientes en la nueva población
            nueva_pob.append(descendiente1)
            nueva_pob.append(descendiente2)
        # Si la población es impar, eliminamos un
        # elemento aleatoriamente (el último elemento, por ejemplo)
        if impar:
            nueva_pob.pop()
        # Reemplazamos la antigua población con la nueva
        cromosomas = nueva_pob
        rep += 1
    valor_min = min(valores_fitness)
    ind_min = valores_fitness.index(valor_min)
    return cromosomas[ind_min]
