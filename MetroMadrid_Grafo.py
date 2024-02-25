import pandas as pd
# el directorio donde se guarda el archivo que contiene los datos
data_address = "C:/Users/masca/Desktop/ComputerStructure/Metro/Simple/etiquetas_grafos_metro_PRO.csv"
data = pd.read_csv(data_address)

# Diccionario de vertices y aristas
vertices = {}
aristas = {}

# Funcion que crea los vertices del grafo con nombre de la estacion
# Los atributos son las cordenadas de la estacion y sus vecinos
def crear_vertice(nombre, vecinos, coordenadas_origen):
    x = coordenadas_origen[0]
    y = coordenadas_origen[1]
    if nombre not in vertices:
        vertices[nombre] = {"vecinos": vecinos, "x": x, "y": y}
    else:
        for vecino in vecinos:
            vertices[nombre]["vecinos"].append(vecino)

# Funcion que crea las aristas del grafo
# Tiene como atributos los nombres del origen y destino asi como sus coordenadas respectivas
def crear_arista(origen_nombre, destino_nombre, coordenadas_origen, coordenadas_destino):
    origen_x = coordenadas_origen[0]
    origen_y = coordenadas_origen[1]
    
    destino_x = coordenadas_destino[0]
    destino_y = coordenadas_destino[1]
    
    distancia = distancia_euclidiana(origen_x, origen_y, destino_x, destino_y)
    
    aristas[(origen_nombre, destino_nombre)] = {"distancia": distancia}

# Funcion que elimina un vertice
def eliminar_vertice(vertice):
    if vertice in vertices: 
        del vertices[vertice]

# Funcion que busca un vertice
def buscar_vertice(nombre):
    return vertices.get(nombre, None)

# Funcion que calcula el tamaño del grafo teniendo en cuenta el numero de nodos
def calcular_size():
    return len(vertices)

# La distancia entre origen y destino, utilizada como funcion heuristica en la busqueda de caminos
def distancia_euclidiana(origen_x, origen_y, destino_x, destino_y):
    return ((destino_x - origen_x)**2 + (destino_y - origen_y)**2)**(1/2)

# Funcion f del algoritmo A*
def f(vecino, h):
    return vecino + h

# Funcion que busca el camino más corto entre dos estaciones utilizando el algoritmo de busqueda A*
def buscar_camino(origen_nombre, destino_nombre):
    origen = vertices[origen_nombre]
    destino = vertices[destino_nombre]
    
    print("ORIGEN: ", origen)
    print("DESTINO: ", destino)
    
    # La pila utilizada, open_set contiene nodos inexplorados y closed_set contiene nodos explorados
    open_set = {origen_nombre: 0}
    closed_set = set()
    
    # g_values contiene todos los nodos junto con el coste desde el origen
    g_values = {origen_nombre: 0}
    
    #anterior_nodo contiene todos los nodos explorados para despues retroceder y crear la ruta
    anterior_nodo = {}
    
    while open_set:
        
        # utilizando una funcion anonima para extraer de open_set el nodo con la menor coste hasta el destino
        current_node = min(open_set, key=lambda n: f(g_values[n], distancia_euclidiana(vertices[n]["x"], vertices[n]["y"], destino["x"], destino["y"])))
        
        # finalizar el bucle
        if current_node == destino_nombre:
            print("llegao")
            break
        
        # descolar el nodo de la lista y añadirlo a la lista de nodos explorados
        del open_set[current_node]
        closed_set.add(current_node)
        
        
        for vecino in vertices[current_node]["vecinos"]:
            
            # si el vecino ya se ha explorado pasar al proximo vecino
            if vecino in closed_set:
                continue 
            
            # la suma del coste desde el origen hasta ese nodo más el coste ha sus vecinos
            potential_g_score = g_values[current_node] + distancia_euclidiana(vertices[current_node]["x"], vertices[current_node]["y"], vertices[vecino]["x"], vertices[vecino]["y"])
            
            # Si el vecino no esta en la pila añadir para ser explorado y añadir su coste desde el origen
            # Si el vecino si esta en open_set pero el camino encontrado es menor que el que ya esta guardado, actualizar g_values
            if vecino not in open_set or potential_g_score < g_values[vecino]:
                open_set[vecino] = potential_g_score
                g_values[vecino] = potential_g_score
                anterior_nodo[vecino] = current_node
                
    # se construye la ruta y se devuelve
    return construir_ruta(anterior_nodo, origen_nombre, destino_nombre)

# Funcion que retrocede el camino y construye la ruta más corta
def construir_ruta(anterior_nodo, origen, destino):
    ruta = [destino]
    
    # Empezando desde el destino se retrocede añadiendo los nodos a la lista de ruta y luego se le da la vuelta
    while destino != origen:
        destino = anterior_nodo[destino]
        ruta.append(destino)
    ruta.reverse()
    
    return ruta
    
def main():
    # bucle que guarda la informacion del archivo de datos
    for estacion in data.id:
        # se guardan el nombre, linea y coordenadas de cada estacion
        nombre = data.nombre[estacion]
        linea = data.linea[estacion]
        coordenadas_origen = (data.x[estacion], data.y[estacion])
        
        # si en el archivo dos estaciones aparecen consecutivamente y pertenecen a la misma linea se guardan en el vertice como vecinos
        vecinos =  []
        if data.id[estacion]+1 < len(data.id) and data.id[estacion]-1 > 0 and data.linea[estacion] == data.linea[estacion+1]:
            vecinos.append(data.nombre[estacion+1])
            vecinos.append(data.nombre[estacion-1])
            
            # Con las coordenadas del vecino anterior se crea una arista entre el vecino anterior y la estacion
            coordenadas_vecino_anterior = (data.x[estacion-1], data.y[estacion-1])
            crear_arista(nombre, data.nombre[estacion-1], coordenadas_origen, coordenadas_vecino_anterior)
        
        # se crea el vertice en el nodo con el nombre, vecinos y coordenadas 
        crear_vertice(nombre, vecinos, coordenadas_origen)
    
    while True:
        input_estacion_origen = input("Estación de Origen: ")
        input_estacion_destino = input("Estación de Destino: ")
        
        print(buscar_camino(input_estacion_origen, input_estacion_destino), "\n")
    
if __name__ == "__main__":
    main()