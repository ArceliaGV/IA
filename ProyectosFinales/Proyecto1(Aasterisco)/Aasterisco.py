import sys  # Para terminar el programa correctamente
import pygame  # Pygame para visualización gráfica
from queue import PriorityQueue  # cola de prioridad para A*

# --- CONFIGURACIÓN GLOBAL ---
FILAS = 11  # Número de filas y columnas de la cuadrícula
ANCHO_GRID = 600  # Tamaño en píxeles de la cuadrícula cuadrada
ANCHO_NODO = ANCHO_GRID // FILAS  # Tamaño de cada celda (nodo)
ANCHO_PANEL_INFO = 300  # Ancho del panel derecho de información
ANCHO_TOTAL_VENTANA = ANCHO_GRID + ANCHO_PANEL_INFO  # Ancho total de la ventana
ALTO_VENTANA = ANCHO_GRID  # Alto total de la ventana (igual al grid)

# Inicializar Pygame y fuentes
pygame.init()
FONT_NODO_SCORES = pygame.font.SysFont('cambria', ANCHO_NODO // 5)       # Fuente para g, h, f
FONT_NODO_TITULO = pygame.font.SysFont('cambria', ANCHO_NODO // 3, bold=True)  # Fuente para INICIO/FIN
FONT_PANEL = pygame.font.SysFont('Segoe UI', 18)        # Fuente para texto de panel
FONT_PANEL_TITULO = pygame.font.SysFont('Georgia', 20, bold=True)  # Fuente para títulos en panel

# Creación ventana principal
#cuadrícula y panel lateral.
VENTANA = pygame.display.set_mode((ANCHO_TOTAL_VENTANA, ALTO_VENTANA))
# Título de la ventana
pygame.display.set_caption("Proyecto1- AGV 21120211 - Algoritmo A*")

# --- COLORES RGB ---
BLANCO = (255, 255, 255) # fondo de la cuadrícula
NEGRO = (0, 0, 0) #obstaculos
GRIS = (128, 128, 128) #celda de la cuadrícula
TURQUESA = (64, 224, 208)  # Color para nodos en lista abierta
AMARILLO = (255, 255, 150)       # Color para camino solucionado
ROJO = (255, 0, 0)        # Color para nodos cerrados
LAVANDA = (220, 208, 255)   # Color para nodo inicio
LIMA_PASTEL = (216, 255, 168)    # Color para nodo fin
COLOR_PANEL_FONDO = (211, 221, 237)  # Color de fondo del panel derecho
AZUL = (0, 0, 255)         # Color para títulos en panel


class Nodo:
    """
    Representa una celda individual dentro de la cuadrícula para el algoritmo A*.
    Cada nodo almacena su posición, estado visual, vecinos válidos y los valores
    g, h, f necesarios para el cálculo del camino óptimo.
    """
    # Constructor del nodo
    def __init__(self, fila, col, ancho, total_filas):
        # Posición en la cuadrícula
        self.fila = fila #Indice de fila
        # Indice de columna
        self.col = col
        # ID único (1-100) que representa su número dentro del grid
        self.id = fila * total_filas + col + 1
        # Posición gráfica en pantalla (píxeles)
        self.x = col * ancho # Posición horizontal en píxeles
        self.y = fila * ancho   # Posición vertical en píxeles
        # Atributos visuales y estructurales

        # Estado visual inicial: nodo vacío
        self.color = BLANCO
        # Tamaño de la celda en píxeles
        self.ancho = ancho
        # Total de filas/columnas en la cuadrícula
        self.total_filas = total_filas
        # Lista de vecinos válidos (se llena dinámicamente)
        self.vecinos = []
        # Scores de A*
        self.g = float('inf')  # Costo acumulado desde inicio 
        self.h = float('inf')  # Estimación de la distancia al nodo final (heurística)
        self.f = float('inf')  # Costo total estimado: f = g + h

    def get_pos(self):
        """
        Devuelve la posición lógica del nodo en la cuadrícula como una tupla (fila, columna).
        Esta función es útil para comparaciones de posición, cálculos de distancia (heurística)
        y para identificar la ubicación del nodo dentro del grid.
        """
        return (self.fila, self.col)

    # --- Métodos de consulta de estado del nodo ---
    def es_pared(self): return self.color == NEGRO
    """
    Retorna True si el nodo representa una pared u obstáculo.
    En ese caso, el algoritmo A* no podrá atravesarlo.
    """
    def es_inicio(self): return self.color == LAVANDA
    """
    Retorna True si el nodo está marcado como el nodo de inicio.
    Esto se evalúa mediante su color (LAVANDA).
    """
    def es_fin(self): return self.color == LIMA_PASTEL
    """
    Retorna True si el nodo está marcado como el nodo final.
    Esto se evalúa mediante su color (LIMA_PASTEL).
    """

    # --- Método para reiniciar el nodo a su estado original ---
    def restablecer(self):
        """
        Reinicia el nodo a su estado inicial:
        - Lo pinta de blanco (vacío)
        - Restablece los valores g, h y f 
        Es útil al borrar el grid o reiniciar una búsqueda.
        """
        self.color = BLANCO
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')

# --- Métodos para cambiar el estado visual del nodo ---
    def hacer_inicio(self): 
        """Marca este nodo como el punto de INICIO (color LAVANDA)."""
        self.color = LAVANDA
    def hacer_pared(self): 
        """Convierte el nodo en una PARED (color NEGRO), no transitable."""
        self.color = NEGRO
    def hacer_fin(self): 
        """Marca este nodo como el punto FINAL (color LIMA_PASTEL)."""
        self.color = LIMA_PASTEL
    def lista_abierta(self): 
        """Marca el nodo como parte de la LISTA ABIERTA"""
        self.color = TURQUESA
    def lista_cerrada(self): 
        """Marca el nodo como parte de la LISTA CERRADA"""
        self.color = ROJO
    def pintar_camino(self): 
        """Colorea el nodo como parte del CAMINO FINAL encontrado"""
        self.color = AMARILLO

    def dibujar(self, ventana):
        """
        Dibuja gráficamente el nodo en la ventana:
        - Colorea el fondo según su estado (camino, abierto, cerrado, etc.)
        - Muestra los valores g, h y f si ya fueron calculados
        - Escribe “INICIO” o “FIN” si el nodo representa esos roles
        - Muestra el ID del nodo en la esquina inferior derecha
        """
         # 1) Dibujar fondo del nodo (según su color actual)
        pygame.draw.rect(ventana, self.color,
                         (self.x, self.y, self.ancho, self.ancho))
        padding = 2 # Margen interno para los textos
        lh = FONT_NODO_SCORES.get_height()
          # 2) Mostrar scores (g, h, f) en la esquina superior izquierda
        if self.g != float('inf') and not self.es_pared():
            ventana.blit(FONT_NODO_SCORES.render(f"g:{int(self.g)}", True, NEGRO),
                         (self.x+padding, self.y+padding))
            ventana.blit(FONT_NODO_SCORES.render(f"h:{int(self.h)}", True, NEGRO),
                         (self.x+padding, self.y+padding+lh))
            ventana.blit(FONT_NODO_SCORES.render(f"f:{int(self.f)}", True, NEGRO),
                         (self.x+padding, self.y+padding+2*lh))
         # 3) Mostrar etiqueta “INICIO” o “FIN” centrada en el nodo
        if self.es_inicio():
            surf = FONT_NODO_TITULO.render("INICIO", True, BLANCO)
            rect = surf.get_rect(center=(self.x+self.ancho//2,
                                         self.y+self.ancho//2))
            ventana.blit(surf, rect)
        elif self.es_fin():
            surf = FONT_NODO_TITULO.render("FIN", True, BLANCO)
            rect = surf.get_rect(center=(self.x+self.ancho//2,
                                         self.y+self.ancho//2))
            ventana.blit(surf, rect)
        # 4) ID en esquina inferior derecha
        id_surf = FONT_NODO_SCORES.render(str(self.id), True, GRIS)
        ventana.blit(id_surf, (self.x+self.ancho-18,
                               self.y+self.ancho-15))

    def buscar_vecinos(self, grid):
        """
        Calcula y almacena en self.vecinos la lista de nodos accesibles desde este nodo.
        Sigue un orden específico de direcciones:
        - Primero movimientos ortogonales: abajo, arriba, derecha, izquierda
        - Luego diagonales: abajo-derecha, abajo-izquierda, arriba-derecha, arriba-izquierda

        Solo se consideran como vecinos válidos:
        - Nodos dentro de los límites del grid
        - Nodos que no son paredes
        - En caso de movimiento diagonal, se valida que no se atraviese una esquina bloqueada
        """
        self.vecinos = []
        # Direcciones ordenadas: ortogonales y luego diagonales
        dirs = [
            # abajo, arriba, derecha, izquierda
            (1, 0), (-1, 0), (0, 1), (0, -1),
            # diagonales
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        # Iterar sobre direcciones y agregar vecinos válidos
        for dr, dc in dirs:
           r, c = self.fila + dr, self.col + dc
           # Verificar que el vecino está dentro de los límites del grid
           if 0 <= r < self.total_filas and 0 <= c < self.total_filas:
                 # Omitir si es una pared
                if not grid[r][c].es_pared():
                     # Si es un movimiento diagonal, validar que no haya corte de esquina
                    if abs(dr) == 1 and abs(dc) == 1:
                        nodo_ortogonal_1 = grid[self.fila][self.col + dc]
                        nodo_ortogonal_2 = grid[self.fila + dr][self.col]
                        if nodo_ortogonal_1.es_pared() or nodo_ortogonal_2.es_pared():
                            continue  # Se bloquea la diagonal si hay una pared ortogonal
                    # Si todo está correcto, se agrega como vecino válido
                    self.vecinos.append(grid[r][c])

    def __lt__(self, other):
        """
        Método requerido por PriorityQueue para comparar nodos en caso de empate de prioridad.
        En este caso, siempre devuelve False para evitar errores de comparación entre objetos Nodo.
        El desempate real se realiza usando el contador 'count' que se incrementa en cada inserción.
        """
        return False


# --- Heurística Manhattan (distancia estimada al objetivo) ---
def heuristica_m(p1, p2):
    """
    Calcula la heurística entre dos posiciones (p1 y p2) usando la distancia Manhattan.
    Multiplica el resultado por 10 para que coincida con el costo ortogonal estándar.
    Esta heurística es admisible (no sobreestima) y garantiza la optimalidad de A*.
    """
    return (abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])) * 10

# --- Costo real de moverse entre dos nodos ---
def costo(a, b):
    """
    Devuelve el costo de moverse del nodo 'a' al nodo 'b'.
    - Movimiento ortogonal (horizontal o vertical): costo 10
    - Movimiento diagonal (cambia fila y columna): costo 14
    """
    dx = abs(a.fila - b.fila)
    dy = abs(a.col - b.col)
    return 14 if dx == 1 and dy == 1 else 10

# -----Construir el camino final marcado como solucionado ---

def construir_camino(came_from, actual, draw):
    """
    Recorre hacia atrás desde el nodo final usando el diccionario 'came_from'
    para marcar todos los nodos que forman parte del camino óptimo.

    A cada nodo del camino se le aplica el color AMARILLO con .pintar_camino()
    y se actualiza la pantalla en cada paso mediante la función draw().
    """
    while actual in came_from:
        actual = came_from[actual]
        actual.pintar_camino()
        draw()

# --- Algoritmo principal de búsqueda A* ---
def camino_optimo(draw, grid, inicio, fin):
    """
    Implementación del algoritmo A* para encontrar el camino más corto
    entre los nodos 'inicio' y 'fin' sobre la cuadrícula 'grid'.

    - Usa una cola de prioridad para extraer el nodo con menor f = g + h
    - Expande vecinos válidos y actualiza sus costos
    - Cuando se alcanza el nodo final, construye el camino
    - Retorna True si se encuentra una solución, junto con las listas cerrada y abierta
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, inicio))  # (f, count para desempate, nodo)
    came_from = {}
    # Inicializar scores
    g_score = {n: float('inf') for row in grid for n in row}
    f_score = {n: float('inf') for row in grid for n in row}
    g_score[inicio] = 0
    f_score[inicio] = heuristica_m(inicio.get_pos(), fin.get_pos())
     # Guardar los valores directamente en el nodo de inicio
    inicio.g = 0
    inicio.h = f_score[inicio]
    inicio.f = f_score[inicio]
    open_hash = {inicio}
    # lista cerrada para mostrar el recorrido hecho
    closed = []

    while not open_set.empty():
         # Detectar cierre de ventana mientras corre el algoritmo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Obtener nodo con f más bajo
        current = open_set.get()[2]
        open_hash.remove(current)
        closed.append(current)

        # Si llegamos al fin, construir y devolver ambas listas
        if current == fin:
            construir_camino(came_from, fin,
                               lambda: draw(list(open_hash), closed))
            fin.hacer_fin()
            inicio.hacer_inicio()
            return True, closed, list(open_hash)

        # Explorar vecinos del nodo actual
        for vecino in current.vecinos:
            temp_g = g_score[current] + costo(current, vecino)
            # Si el camino a través de este nodo es mejor, se actualiza
            if temp_g < g_score[vecino]:
                came_from[vecino] = current
                g_score[vecino] = temp_g
                vecino.g = temp_g
                vecino.h = heuristica_m(vecino.get_pos(), fin.get_pos())
                vecino.f = vecino.g + vecino.h
                # Si el vecino no está en la lista abierta, se añade
                if vecino not in open_hash:
                    count += 1
                    open_set.put((vecino.f, count, vecino))
                    open_hash.add(vecino)
                    vecino.lista_abierta()

        # Visualizar nodo procesado como cerrado (excepto el inicio)
        draw(list(open_hash), closed)
        if current != inicio:
            current.lista_cerrada()
# No se encontró camino
    return False, closed, list(open_hash)

# --- Crear la cuadrícula de nodos ---
def crear_grid(filas, ancho):
    """
    Crea una matriz bidimensional de nodos vacíos según el número de filas.
    Cada nodo contiene su posición lógica, tamaño en píxeles y estado inicial.
    """
    grid = []
    nodo_ancho = ancho // filas
    for i in range(filas):
        fila = []
        for j in range(filas):
            fila.append(Nodo(i, j, nodo_ancho, filas))
        grid.append(fila)
    return grid

# --- Dibujar líneas grises para mostrar la cuadrícula ---

def dibujar_grid(vent, filas, ancho):
    """
    Dibuja las líneas horizontales y verticales del grid sobre la ventana,
    usando el color GRIS para delimitar las celdas.
    """
    nodo_ancho = ancho // filas
    for i in range(filas+1):
        pygame.draw.line(vent, GRIS, (0, i*nodo_ancho), (ancho, i*nodo_ancho))
        pygame.draw.line(vent, GRIS, (i*nodo_ancho, 0), (i*nodo_ancho, ancho))

# --- Dibujar panel lateral con las listas abierta y cerrada ---
def dibujar_panel(vent, abierta, cerrada, rect):
    """
    Dibuja el panel lateral donde se muestran:
    - La lista de nodos abiertos (azul)
    - La lista de nodos cerrados (rojos)
    """
    pygame.draw.rect(vent, COLOR_PANEL_FONDO, rect)
    x, y = rect.left+10, rect.top+10
    # Título y contenido de lista abierta
    vent.blit(FONT_PANEL_TITULO.render("Lista Abierta:", True, AZUL), (x, y))
    y += 25
    # Lista Abierta dividida en líneas de máximo 10 elementos
    MAX_NODOS_POR_LINEA = 10
    abierta_str = [", ".join(str(n.id) for n in abierta[i:i+MAX_NODOS_POR_LINEA])
                for i in range(0, len(abierta), MAX_NODOS_POR_LINEA)]
    for linea in abierta_str:
        vent.blit(FONT_PANEL.render(linea, True, AZUL), (x, y))
        y += 20  # Avanza hacia abajo

    # Título y contenido de lista cerrada
    vent.blit(FONT_PANEL_TITULO.render("Lista Cerrada:", True, ROJO), (x, y)); y += 25
    cerrada_str = [", ".join(str(n.id) for n in cerrada[i:i+MAX_NODOS_POR_LINEA])
                for i in range(0, len(cerrada), MAX_NODOS_POR_LINEA)]
    for linea in cerrada_str:
        vent.blit(FONT_PANEL.render(linea, True, ROJO), (x, y))
        y += 20

# --- Función principal de dibujo que actualiza toda la interfaz ---
def refrescar_interfaz(vent, grid, open_list, closed_list, rect):
    """
    Limpia la ventana y redibuja:
    - Todos los nodos del grid (con sus colores y datos)
    - La cuadrícula gris
    - El panel lateral con las listas abiertas/cerradas
    Luego actualiza la pantalla con pygame.display.update().
    """
    vent.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(vent)
    dibujar_grid(vent, FILAS, ANCHO_GRID)
    dibujar_panel(vent, open_list, closed_list, rect)
    pygame.display.update()

# Convierte click a coordenadas de malla (fila, col)
def obtener_click(pos, filas, ancho):
    nodo_ancho = ancho // filas
    return pos[1]//nodo_ancho, pos[0]//nodo_ancho

# Función principal
def main(ventana, ancho_grid):
    grid = crear_grid(FILAS, ancho_grid)
    panel_rect = pygame.Rect(ancho_grid, 0, ANCHO_PANEL_INFO, ALTO_VENTANA)
    inicio = fin = None
    abierta = []
    cerrada = []

    while True:
        refrescar_interfaz(ventana, grid, abierta, cerrada, panel_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Click izquierdo para inicio/fin/obstáculos
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                if x < ancho_grid:
                    r, c = obtener_click((x,y), FILAS, ancho_grid)
                    nodo = grid[r][c]
                    if not inicio and nodo != fin:
                        inicio = nodo; inicio.hacer_inicio()
                    elif not fin and nodo != inicio:
                        fin = nodo; fin.hacer_fin()
                    elif nodo not in (inicio, fin):
                        nodo.hacer_pared()
            # Click derecho para reset
            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                if x < ancho_grid:
                    r, c = obtener_click((x,y), FILAS, ancho_grid)
                    nodo = grid[r][c]
                    nodo.restablecer()
                    if nodo == inicio: inicio = None
                    if nodo == fin: fin = None

            # Tecla espacio para lanzar A*
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    # Actualizar vecinos antes de ejecutar
                    for fila in grid:
                        for nodo in fila:
                            nodo.buscar_vecinos(grid)
                    # Ejecutar A*, obtener listas para panel
                    found, cerrada, abierta = camino_optimo(
                        lambda o,c: refrescar_interfaz(ventana, grid, o, c, panel_rect),
                        grid, inicio, fin)

if __name__ == "__main__":
    """
    Esta línea verifica si el script está siendo ejecutado directamente
    (y no importado como módulo desde otro archivo).

    Si es así, se llama a la función main() que:
    - Inicializa la cuadrícula de nodos
    - Ejecuta el bucle principal del programa
    - Permite interacción del usuario para construir escenarios
    y ejecutar el algoritmo A*
    """
    main(VENTANA, ANCHO_GRID)
