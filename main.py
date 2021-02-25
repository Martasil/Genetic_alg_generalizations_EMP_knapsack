import random
import copy

def fitness(chromosome, nodos, vecinos, baldosas):
    """
    La función fitness calcula el valor
    de cada cromosoma, es decir, el número
    de nodos satisfechos en el cromosoma
    :param chromosome: el cromosoma cuyo valor queremos conocer
    :param nodos: los nodos de la instancia
    :param vecinos: la lista de vecinos de cada nodo
    :param baldosas: el conjunto de baldosas de la instancia
    :return: el número de nodos satisfechos de la solución
    """
    fit = 0
    for n in nodos:
        nodo = n
        # Para cada nodo buscamos si hay alguna arista rota. Si
        # no la hay, el nodo está satisfecho y aumentamos un
        # unidad su valor. Si la hay, pasamos al siguiente nodo.
        satisfecho = True
        vecinos_nodo = vecinos[nodo-1]
        num_vecinos = len(vecinos_nodo)
        #print("nodo:", nodo)
        # Obtenemos la baldosa del nodo en estudio en esta solución
        baldosa = baldosas[chromosome[nodo-1]]
        j = 0
        while satisfecho & (j < num_vecinos):
            # Recorremos cada vecino del nodo
            vecino = vecinos_nodo[j]
            pos_nodo = vecinos[vecino-1].index(n)
            # Obtenemos la baldosa del vecino en estudio en esta solución
            baldosa_vecino = baldosas[chromosome[vecino-1]]
            # Comparamos los colores de la arista que tienen en común
            if baldosa[j] != baldosa_vecino[pos_nodo]:
                satisfecho = False
            else:
                j += 1
        if satisfecho:
            fit += 1
    return fit

def gen_algorithm(nodos, aristas, baldosas, n_pop, maxRep, pc, pm):
    """
    Esta función es la que ejecuta el algoritmo genético
    para obtener una solución del problema MAX NS3, con las
    baldosas fijas
    :param nodos: lista de nodos de la instancia de MAX NS1,
    suponemos que se llaman 1,2,3... pero el nodo 1 no tiene
    por qué tener aridad 1, ni el 2 aridad 2, etc.
    :param aristas: aristas de la instancia de MAX NS1
    :param baldosas: baldosas de la instancia de MAX NS1 (suponemos
    que hay, al menos, una baldosa para cada nodo y que las baldosas
    están colocadas en el orden de los vecinos que obtenga el algoritmo,
    es decir, si el algoritmo saca la lista de vecinos para el nodo
    3 como l = [2,1] y la baldosa en el nodo 3 es b = [a,b],
    entonces la baldosa tiene la arista {2,3} de color a y
    la arista {1,3} de color b)
    :param n_pop: tamaño de la población
    :param maxRep: número de generaciones
    :param pc: probabilidad de recombinación
    :param pm: probabilidad de mutación
    :return: devuelve una lista con las baldosas escogidas
    Si devuelve la lista [x,y,z] quiere decir que el nodo
    1 ha tomado la baldosa en la posición x de la lista de
    baldosas, el nodo 2 la baldosa en la posición y de la lista
    de baldosas y el nodo 3 la baldosa en la posición z
    """
    n = len(nodos)  # Número de nodos
    n_b = len(baldosas)  # Número de baldosas
    if n_b < n:
        print("The input is not valid. There must be at least one tile "
              "per node")
        return 0
    n_pop = n_pop # Número de soluciones iniciales
    # Separamos las baldosas en listas dependiendo de su aridad
    l_b_orden = []
    odd = 0
    if n_pop is odd:
        odd = 1
    i = 0
    while i < n_b:
        b = baldosas[i]
        aridad = len(b)
        while len(l_b_orden) < aridad:
            l_b_orden.append([])
        l_b_orden[aridad - 1].append(i)
        i += 1
    # Obtenemos la aridad de cada nodo
    l_aridades = [0] * n
    l_vecinos = []
    while len(l_vecinos) < n:
        l_vecinos.append([])
    for a in aristas:
        v1 = a[0]
        v2 = a[1]
        l_vecinos[v1-1].append(v2)
        l_vecinos[v2-1].append(v1)
        l_aridades[v1 - 1] += 1
        l_aridades[v2 - 1] += 1
    #Ponemos los nodos en listas por aridades
    l_nodos_orden = []
    j = 0
    while j < max(l_aridades):
        l_nodos_orden.append([])
        j+= 1
    for n in nodos:
        l_nodos_orden[l_aridades[n-1]-1].append(n)
    # Creación de posibles soluciones (cromosomas)
    chromosomes = []
    fitness_values = []
    while len(chromosomes) < n_pop:
        x = [0]*n
        for group in l_nodos_orden:
            num_nodos = len(group)
            if num_nodos > 0:
                baldosas_group = random.sample(l_b_orden[l_aridades[group[0]-1]-1], num_nodos)
                j = 0
                while j < num_nodos:
                    x[group[j]-1] = baldosas_group[j]
                    j += 1
        chromosomes.append(x)
    #print(chromosomes)
    rep = 0
    while (rep < maxRep):
        # Calculamos el valor de cada cromosoma y lo almacenamos en una lista
        fitness_values = []
        i = 0
        while len(fitness_values) < n_pop:
            fitness_values.append(fitness(chromosomes[i], nodos, l_vecinos,baldosas))
            i += 1
        # Creamos una nueva población en la que
        # iremos añadiendo los descendientes de nuestra actual población
        new_population = []
        # Ajustamos los valores de los cromosomas
        # para que sean todos mayores o iguales que 0
        while len(new_population) < n_pop:
            # Elegimos a una pareja de progenitores
            list = []
            for w in range(0, n_pop):
                list.append(w)
            parents_pos = random.choices(list, fitness_values, k=2)
            parents = [chromosomes[parents_pos[0]], chromosomes[parents_pos[1]]]
            # Decidimos si se da una recombinación o no
            x = random.choices([0, 1], weights=[1 - pc, pc])
            descendant1 = []
            descendant2 = []
            if x[0] == 1:  # Recombinación
                locus = random.randint(0, n - 1)
                l_b_orden_descendant_1 = copy.deepcopy(l_b_orden)
                # Creamos a los dos descendientes
                for j in range(locus):
                    ar_nodo = l_aridades[j]
                    descendant1.append(parents[0][j])
                    l_b_orden_descendant_1[ar_nodo - 1].remove(parents[0][j])
                for k in range(locus, n):
                    ar_nodo = l_aridades[k]
                    if (parents[1][k] not in l_b_orden_descendant_1[ar_nodo-1]):
                        b_new = random.choice(l_b_orden_descendant_1[ar_nodo - 1])
                        descendant1.append(b_new)
                        l_b_orden_descendant_1[ar_nodo-1].remove(b_new)
                    else:
                        descendant1.append(parents[1][k])
                        l_b_orden_descendant_1[ar_nodo - 1].remove(parents[1][k])
                l_b_orden_descendant_2 = copy.deepcopy(l_b_orden)
                for j in range(locus):
                    ar_nodo = l_aridades[j]
                    descendant2.append(parents[1][j])
                    l_b_orden_descendant_2[ar_nodo - 1].remove(parents[1][j])
                for k in range(locus, n):
                    ar_nodo = l_aridades[k]
                    if parents[0][k] not in l_b_orden_descendant_2[ar_nodo-1]:
                        b_new = random.choice(l_b_orden_descendant_2[ar_nodo - 1])
                        descendant2.append(b_new)
                        l_b_orden_descendant_2[ar_nodo - 1].remove(b_new)
                    else:
                        descendant2.append(parents[0][k])
                        l_b_orden_descendant_2[ar_nodo - 1].remove(parents[0][k])
            else:  # No recombinación, los descendientes
                   # son una copia exacta de los padres
                descendant1 = parents[0]
                descendant2 = parents[1]
            # Decidimos si el primer descenciente sufre una mutación o no
            y1 = random.choices([0, 1], weights=[1 - pm, pm])
            if y1[0] == 1:  # Mutación descendiente1
                locus = random.randint(0, n - 1)
                # Lista de baldosas en orden libres para descendiente1
                l_b_orden_2 = copy.deepcopy(l_b_orden)
                k = 0
                while k < n:
                    if k != locus:
                        ar = l_aridades[k]
                        l_b_orden_2[ar-1].remove(descendant1[k])
                    k += 1
                descendant1[locus] = random.choice(l_b_orden_2[l_aridades[locus]-1])
            # Decidimos si el segundo descenciente sufre una mutación o no
            y2 = random.choices([0, 1], weights=[1 - pm, pm])
            if y2[0] == 1:  # Mutación descendiente2
                locus = random.randint(0, n - 1)
                l_b_orden_3 = copy.deepcopy(l_b_orden)
                k = 0
                while k < n:
                    if k != locus:
                        ar = l_aridades[k]
                        l_b_orden_3[ar-1].remove(descendant2[k])
                    k += 1
                descendant2[locus] = random.choice(l_b_orden_3[l_aridades[locus]-1])
            # Incluimos los nuevos descendientes en la nueva población
            new_population.append(descendant1)
            new_population.append(descendant2)
        # Si la población es impar, eliminamos un
        # elemento aleatoriamente (el último elemento, por ejemplo)
        if odd:
            new_population.pop()
        # Reemplazamos la antigua población con la nueva
        chromosomes = new_population
        rep += 1
    max_value = max(fitness_values)
    max_index = fitness_values.index(max_value)
    print(max_value)
    return chromosomes[max_index]

gen_algorithm([1,2,3,4,5,6,7,8,9,10], [[1,9],[1,5],[1,2],[5,6],[1,3],[2,4],[3,4],[5,7],[7,8],[6,8],[2,6],[5,10],[9,10],[3,10],[4,8],[3,7],[9,5]], [[1,2,3,7],[3,5,6],[7,1,1,3],[5,1,1],[2,1,4,5,6],[1,3,6],[4,2,4],[2,3,1],[1,5,6],[5,5,2]], 200, 250, 0.7, 0.01)
