import random
import copy


def fitness(cromosoma, nodos, vecinos, baldosas):
    """
    La función fitness calcula el valor
    de cada cromosoma, es decir, el número
    de nodos satisfechos en el cromosoma
    :param cromosoma: el cromosoma cuyo valor queremos conocer
    :param nodos: los nodos de la instancia
    :param vecinos: lista de listas de vecinos de cada nodo
    :param baldosas: el conjunto de baldosas de la instancia
    :return: el número de nodos satisfechos de la solución
    """
    fit = 0
    for nodo in nodos:
        # Para cada nodo buscamos si hay alguna arista rota. Si
        # no la hay, el nodo está satisfecho y aumentamos un
        # unidad su valor. Si la hay, pasamos al siguiente nodo.
        vecinos_nodo = vecinos[nodo-1]
        num_vecinos = len(vecinos_nodo)
        # Obtenemos la baldosa del nodo en estudio en esta solución
        baldosa = baldosas[cromosoma[nodo-1]]
        j = 0
        while  j < num_vecinos:
            # Recorremos cada vecino del nodo
            vecino = vecinos_nodo[j]
            if nodo < vecino:
                pos_nodo = vecinos[vecino - 1].index(nodo)
                # Obtenemos la baldosa del vecino en estudio en esta solución
                baldosa_vecino = baldosas[cromosoma[vecino - 1]]
                # Comparamos los colores de la arista que tienen en común
                if baldosa[j] != baldosa_vecino[pos_nodo]:
                    fit += 1
                j += 1
            else:
                j += 1
    return fit

def conversion_probabilidades(lst, x):
    lst_2 = []
    for i in lst:
        lst_2.append(x-i)
    return lst_2

def gen_algorithm(nodos, num_aristas, vecinos, baldosas, n_p, max_rep, pc, pm):
    """
    Esta función es la que ejecuta el algoritmo genético
    para obtener una solución del problema MIN AR, con las
    baldosas fijas
    :param nodos: lista de nodos de la instancia de MIN AR,
    suponemos que se llaman 1,2,3... pero el nodo 1 no tiene
    por qué tener aridad 1, ni el 2 aridad 2, etc.
    :param vecinos: lista de listas de vecinos de los nodos de
    la instancia de MIN AR
    :param baldosas: baldosas de la instancia de MIN AR (suponemos
    que hay, al menos, una baldosa para cada nodo y que las baldosas
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
    n = len(nodos)       # Número de nodos
    n_b = len(baldosas)  # Número de baldosas
    n_p = n_p            # Número de soluciones iniciales
    if n_b < n:
        print("Los datos de entrada no son válidos. Debe haber, al menos, "
              "una baldosa para cada nodo.")
        return 1
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
    l_aridades = [0] * n
    for n in nodos:
        vecinos_n = vecinos[n - 1]
        l_aridades[n - 1] = len(vecinos_n)
    # Ponemos los nodos en listas por aridades
    l_nodos_orden = []
    k = 0
    while k < max(l_aridades):
        l_nodos_orden.append([])
        k += 1
    for n in nodos:
        l_nodos_orden[l_aridades[n-1]-1].append(n)
    # Creación de posibles soluciones (cromosomas)
    cromosomas = []
    valores_fitness = []
    while len(cromosomas) < n_p:
        x = [0]*n
        for grupo in l_nodos_orden:
            num_nodos = len(grupo)
            if num_nodos > 0:
                baldosas_grupo = random.sample(l_b_orden[l_aridades[grupo[0]-1]-1], num_nodos)
                j = 0
                while j < num_nodos:
                    x[grupo[j]-1] = baldosas_grupo[j]
                    j += 1
        cromosomas.append(x)
    rep = 0
    while rep < max_rep:
        # Calculamos el valor de cada cromosoma y lo almacenamos en una lista
        valores_fitness = []
        i = 0
        while len(valores_fitness) < n_p:
            valores_fitness.append(fitness(cromosomas[i], nodos, vecinos, baldosas))
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
            valores_fitness_probs = conversion_probabilidades(valores_fitness, num_aristas)
            padres_pos = random.choices(lst, valores_fitness_probs, k=2)
            padres = [cromosomas[padres_pos[0]], cromosomas[padres_pos[1]]]
            # Decidimos si se da una recombinación o no
            x = random.choices([0, 1], weights=[1 - pc, pc])
            descendiente1 = []
            descendiente2 = []
            # Recombinación
            if x[0] == 1:
                locus = random.randint(0, n - 1)
                l_b_orden_descendiente_1 = copy.deepcopy(l_b_orden)
                # Creamos a los dos descendientes
                for j in range(locus):
                    ar_nodo = l_aridades[j]
                    descendiente1.append(padres[0][j])
                    l_b_orden_descendiente_1[ar_nodo - 1].remove(padres[0][j])
                for k in range(locus, n):
                    ar_nodo = l_aridades[k]
                    # Si una baldosa ya ha sido elegida, elegimos una de las disponibles
                    if padres[1][k] not in l_b_orden_descendiente_1[ar_nodo-1]:
                        b_nueva = random.choice(l_b_orden_descendiente_1[ar_nodo - 1])
                        descendiente1.append(b_nueva)
                        l_b_orden_descendiente_1[ar_nodo-1].remove(b_nueva)
                    else:
                        descendiente1.append(padres[1][k])
                        l_b_orden_descendiente_1[ar_nodo - 1].remove(padres[1][k])
                l_b_orden_descendiente_2 = copy.deepcopy(l_b_orden)
                for j in range(locus):
                    ar_nodo = l_aridades[j]
                    descendiente2.append(padres[1][j])
                    l_b_orden_descendiente_2[ar_nodo - 1].remove(padres[1][j])
                for k in range(locus, n):
                    ar_nodo = l_aridades[k]
                    # Si una baldosa ya ha sido elegida, elegimos una de las disponibles
                    if padres[0][k] not in l_b_orden_descendiente_2[ar_nodo-1]:
                        b_nueva = random.choice(l_b_orden_descendiente_2[ar_nodo - 1])
                        descendiente2.append(b_nueva)
                        l_b_orden_descendiente_2[ar_nodo - 1].remove(b_nueva)
                    else:
                        descendiente2.append(padres[0][k])
                        l_b_orden_descendiente_2[ar_nodo - 1].remove(padres[0][k])
            # No recombinación, los descendientes
            # son una copia exacta de los padres
            else:
                descendiente1 = padres[0]
                descendiente2 = padres[1]
            # Decidimos si el primer descenciente sufre una mutación o no
            y1 = random.choices([0, 1], weights=[1 - pm, pm])
            if y1[0] == 1:  # Mutación descendiente1
                locus = random.randint(0, n - 1)
                # Lista de baldosas libres para descendiente1 ordenadas por aridad
                l_b_orden_2 = copy.deepcopy(l_b_orden)
                k = 0
                while k < n:
                    if k != locus:
                        ar = l_aridades[k]
                        l_b_orden_2[ar-1].remove(descendiente1[k])
                    k += 1
                descendiente1[locus] = random.choice(l_b_orden_2[l_aridades[locus]-1])
            # Decidimos si el segundo descenciente sufre una mutación o no
            y2 = random.choices([0, 1], weights=[1 - pm, pm])
            if y2[0] == 1:  # Mutación descendiente2
                locus = random.randint(0, n - 1)
                # Lista de baldosas libres para descendiente2 ordenadas por aridad
                l_b_orden_3 = copy.deepcopy(l_b_orden)
                k = 0
                while k < n:
                    if k != locus:
                        ar = l_aridades[k]
                        l_b_orden_3[ar-1].remove(descendiente2[k])
                    k += 1
                descendiente2[locus] = random.choice(l_b_orden_3[l_aridades[locus]-1])
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
