#---------Librerías --------------------
#Usada para crear la visualización gráfica y actualizar la pantalla
import pygame
#Para generar valores aleatorios
import random
#Librería numérica usada en IA para trabajar con arreglos y operaciones matemáticas
import numpy as np 
#Vecinos cercanos para clasificación, usado como modelo de IA
from sklearn.neighbors import KNeighborsClassifier

# Inicializar todos los módulos de Pygame
pygame.init()

# --------------- Configuración de la pantalla y variables del juego --------------------
# Dimensiones de la pantalla (ancho, alto)
w, h = 800, 400
# Crear la pantalla con las dimensiones especificadas
pantalla = pygame.display.set_mode((w, h))
# Establecer el título de la ventana del juego
pygame.display.set_caption(" PROYECTO 2: JUEGO PHASER K NEAREST NEIGHBORS")

# Definicion de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
#Letrero del Menu Inicial
AMARILLO = (255, 255, 150) 
#Fondo del Menu Inicial
GRIS = (128, 128, 128)
AZUL = (0, 0, 255)  

# -----------Declaracion Inicial de variables y objetos del juego --------------------
# Se inicializa como None, luego se convertirá en un rectángulo
jugador = None
#Igual que jugador, será el disparo enemigo horizontal
bala = None
# Segundo tipo de bala, esta se moverá verticalmente
bala2 = None
#Imagen de fondo del juego
fondo = None
# Nave enemiga que lanza bala
nave = None
# Otra nave en la parte superior
nave2 = None
# Imagen del menú de inicio
menu = None

# ---- SALTO DEL JUGADOR ---------
# Variables de salto del jugador
# Indica si el jugador está actualmente saltando
salto = False
# Velocidad inicial hacia arriba cuando salta (cuanto mayor, más alto)
salto_altura = 15  
# Cantidad que se resta a salto_altura cada frame, simulando gravedad
gravedad = 1
# Indica si el jugador está tocando el suelo (evita doble salto)
en_suelo = True

#---------- Variables de movimiento del jugador (hacia adelante) -----------
# Indica si el jugador está haciendo ese movimiento especial (como esquivar hacia el frente)
mov_delantero = False 
# Cantidad de pixeles que se mueve por frame cuando se activa mov_delantero
mov_delantero_direccion = 9 
mov_delantero_velocidad = 1 
# Si el jugador está en su posición de inicio (x = 50)
en_posicion_inicial = True 
# Indica si el jugador ya va de regreso a su posición original después de haberse movido hacia adelante
jugador_regresando = False

#--------Variables del menú y pausa --------------
# Estado del juego (True = en pausa, False = en juego)
pausa = False
# Se define el tipo y tamaño de fuente para los textos del menú
fuente = pygame.font.SysFont('cambria', 24)
# Indica si el menú principal está activo
menu_activo = True
#Si es True, el juego se jugará automáticamente con IA
modo_auto = False 

# --------- Lista para almacenar los datos del modelo --------------
# Aquí se guardan los datos recolectados en modo manual (velocidades, distancias, acciones del jugador)
datos_modelo = []

# --- Carga de imágenes del juego -------
#Imagenes de las diferentes posiciones del personaje jugador

# jugador (kirby) en un tamaño adecuado para el juego
kirby_raw = pygame.image.load('pygamesc/assets/sprites/kirby.png')  
kirby_scaled = pygame.transform.scale(kirby_raw, (32, 32))  # Ajusta el tamaño a algo pequeño y jugable
jugador_frames = [kirby_scaled] * 4  # Se repite la misma imagen como animación básica

#Imagenes del "ciclo de animación"
bala_img = pygame.image.load('pygamesc/assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('pygamesc/assets/game/fondo2.png')
nave_img = pygame.image.load('pygamesc/assets/game/ufo.png')
menu_img = pygame.image.load('pygamesc/assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# -----Creacion de los objetos (rectángulos)
"""
pygame.Rect(x, y, ancho, alto)
Sirve tanto para posicionar como 
para detectar colisiones entre objetos del juego.
"""
# Posición inicial y tamaño del jugador
jugador = pygame.Rect(50, h - 100, 32, 48)
# Bala que viene desde la derecha hacia el jugador
bala = pygame.Rect(w - 50, h - 90, 16, 16)
# Segunda bala que viene desde arriba hacia abajo
bala2 = pygame.Rect(50, 0, 16, 16)  
# Nave enemiga ubicada en la parte derecha
nave = pygame.Rect(w - 100, h - 100, 64, 64)
# Nave enemiga superior desde donde cae bala2
nave2 = pygame.Rect(20, 0, 64, 64)
# Tamaño del área del menú
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# ---- Animación del jugador (control de cuadros) ----
#Índice actual del frame del jugador (cuadro de animación)
current_frame = 0
# Cuántos ciclos deben pasar antes de cambiar al siguiente frame
frame_speed = 10  
# Contador de ciclos para saber cuándo cambiar al siguiente frame
frame_count = 0

# ----Configuracion de las balas ----
# Velocidad de la bala horizontal (valor negativo = va hacia la izquierda)
velocidad_bala = -10  
# Si es False, la bala está "cargada"; si es True, ya fue disparada
bala_disparada = False

#---Bala2 (vertical) ----
# (Este valor se sobrescribirá luego) Velocidad de la segunda bala (vertical)
velocidad_bala2 = -10  
 # Estado de disparo de la bala2
bala_disparada2 = False

# ----Variables para movimiento del fondo----
# Posición inicial del primer fondo
fondo_x1 = 0
# Posición inicial del segundo fondo (inmediatamente después del primero)
fondo_x2 = w

#------ Función para disparar la bala horizontal ------
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        # Se asigna una velocidad aleatoria negativa (va hacia la izquierda)
        velocidad_bala = random.randint(-8, -3) 
        # Se marca que ya fue disparada para que no se dispare otra hasta que reinicie 
        bala_disparada = True
        
# -----Funcion para disparar la bala vertical ------
def disparar_bala2():
    global bala_disparada2, velocidad_bala2
    if not bala_disparada2:
        # Velocidad hacia abajo (constante, no aleatoria)
        velocidad_bala2 = 5  
        bala_disparada2 = True

# ----------Reinicio de la posicion de la bala horizontal-------
def reset_bala():
    global bala, bala_disparada
    # Regresa la bala a su posición inicial (derecha)
    bala.x = w - 50 
    # Se marca como no disparada para poder lanzarla de nuevo
    bala_disparada = False
    
# ----------Reinicio de la posicion de la bala vertical-------
def reset_bala2():
    global bala2, bala_disparada2
     # Posición inicial en X (igual que jugador)
    bala2.x = 50  
    # Arriba de la pantalla
    bala2.y = 0
    bala_disparada2 = False

# ------Manejo del salto del jugador-----------
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        # Se mueve hacia arriba
        jugador.y -= salto_altura 
        # La velocidad disminuye (efecto de gravedad) 
        salto_altura -= gravedad  

        # Si regresa al suelo
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            # Se reinicia la fuerza del salto
            salto_altura = 15  
            # Vuelve a estar en el suelo
            en_suelo = True
       
#-------- Manejo del movimiento delantero del jugador (hacia adelante y regreso) ----------           
def manejo_movimiento_delantero():
    global jugador, mov_delantero, jugador_regresando, mov_delantero_direccion, en_posicion_inicial

    if mov_delantero and not jugador_regresando:
        # Avanza a la derecha
        jugador.x += mov_delantero_direccion

        # Límite de avance
        if jugador.x >= w - 670:
            jugador.x = w - 670
            # Comienza el regreso
            jugador_regresando = True  

    elif jugador_regresando:
        # Vuelve a la izquierda
        jugador.x -= mov_delantero_direccion

        # Si regresa a su posición inicial
        if jugador.x <= 50:
            jugador.x = 50
            jugador_regresando = False
            mov_delantero = False
            en_posicion_inicial = True
            
# ----Actualización de juego (dibujos y colisiones)-------
def update():
    global bala, bala2, velocidad_bala, velocidad_bala2,  current_frame, frame_count, fondo_x1, fondo_x2

    # Movimiento de fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

   # Cuando el primer fondo sale de la pantalla, se moverá detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    #Cuando el segundo fondo sale de la pantalla, se moverá detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

   # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    #Dibujar naves y balas
    pantalla.blit(nave_img, (nave.x, nave.y))
    pantalla.blit(nave_img, (nave2.x, nave2.y))
#bala horizontal
    if bala_disparada:
        bala.x += velocidad_bala
    # Cuando la bala horizontal sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()
    pantalla.blit(bala_img, (bala.x, bala.y))
    
    # bala vertical
    if bala_disparada2:
        bala2.y += velocidad_bala2   
    # cuando la bala vertical sale de la pantalla, reiniciar su posición
    if bala2.y > h:
        reset_bala2()
        
    pantalla.blit(bala_img, (bala2.x, bala2.y))
        
    # Colisión entre la bala horizontal y el jugador
    if jugador.colliderect(bala):
        print("Colisión identificada!")
        reiniciar_juego()  # Termina juego y muestra menú
        
    # Colisión entre la bala vertical y el jugador
    if jugador.colliderect(bala2):
        print("Colisión identificada!")
        reiniciar_juego()  # Termina juego y muestra menú

# ----Registro de datos del modo manual ----
def guardar_datos():
    global jugador, bala, bala2, velocidad_bala, velocidad_bala2, salto, mov_delantero
    #Se calculan y almacenan
    distancia = abs(jugador.x - bala.x)
    distancia2 = abs(jugador.y - bala2.y)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    mov_delantero_hecho = 1 if mov_delantero else 0  # 1 si se movió hacia adelante, 0 si no se movió
    datos_modelo.append((velocidad_bala, distancia, salto_hecho, velocidad_bala2, distancia2, mov_delantero_hecho))

# ------Activar o desactivar pausa del juego ------
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado!. Datos registrados hasta este momento:", datos_modelo)
    else:
        print("Juego reanudado!")

# ----- Mostrar menú principal ----------
def mostrar_menu():
    global menu_activo, modo_auto
     # Inicialización de audio
    pygame.mixer.init()
    # Cargar recursos
    menu_img = pygame.image.load('pygamesc/assets/game/menu.png')
    menu_img = pygame.transform.scale(menu_img, (w, h))
     # Configuración de botones
    boton_ancho, boton_alto = 300, 60
    boton_x = w // 2 - boton_ancho // 2  # Centrado horizontal
    
    boton_manual = pygame.Rect(boton_x, h // 2 - 80, boton_ancho, boton_alto)
    boton_auto = pygame.Rect(boton_x, h // 2, boton_ancho, boton_alto)
    boton_salir = pygame.Rect(boton_x, h // 2 + 80, boton_ancho, boton_alto)

     # Sonidos 
    sonido_hover = pygame.mixer.Sound('pygamesc/assets/audio/boton_click.mp3')
    sonido_hover.set_volume(0.9)  # Volumen más bajo para hover
    sonido_hover = None

    # Control de hover activo
    hover_activo = {"manual": False, "auto": False, "salir": False}

    while menu_activo:
        mouse_pos = pygame.mouse.get_pos()
        pantalla.blit(menu_img, (0, 0))  # Dibujar fondo del menú

        # Efectos hover con sonido
        for boton_nombre, boton_rect in [("manual", boton_manual), ("auto", boton_auto), ("salir", boton_salir)]:
            if boton_rect.collidepoint(mouse_pos):
                if not hover_activo[boton_nombre] and sonido_hover:
                    sonido_hover.play()  # Sonido al entrar al botón
                hover_activo[boton_nombre] = True
            else:
                hover_activo[boton_nombre] = False

        # Colores de botones (visual hover)
        color_manual = (200, 200, 0) if hover_activo["manual"] else AMARILLO
        color_auto = (200, 200, 0) if hover_activo["auto"] else AZUL
        color_salir = (255, 150, 150) if hover_activo["salir"] else (255, 100, 100)

        # Dibujar botones
        pygame.draw.rect(pantalla, color_manual, boton_manual, border_radius=10)
        pygame.draw.rect(pantalla, color_auto, boton_auto, border_radius=10)
        pygame.draw.rect(pantalla, color_salir, boton_salir, border_radius=10)

        # Texto centrado
        textos = [
            ("Modo Manual (M)", boton_manual),
            ("Modo Auto (A)", boton_auto),
            ("Salir (Q)", boton_salir)
        ]
        for texto_str, boton in textos:
            texto = fuente.render(texto_str, True, NEGRO)
            texto_x = boton.x + (boton.width - texto.get_width()) // 2
            texto_y = boton.y + (boton.height - texto.get_height()) // 2
            pantalla.blit(texto, (texto_x, texto_y))

        pygame.display.flip()

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Verificar clic en botones
                if boton_manual.collidepoint(mouse_pos):
                    modo_auto = False
                    menu_activo = False
                elif boton_auto.collidepoint(mouse_pos):
                    entrenar_modelo()
                    modo_auto = True
                    menu_activo = False
                elif boton_salir.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_m:
                        modo_auto = False
                        menu_activo = False
                    elif evento.key == pygame.K_a:
                        entrenar_modelo()
                        modo_auto = True
                        menu_activo = False
                    elif evento.key == pygame.K_q:
                        print("Saliendo del juego. Datos recopilados:", datos_modelo)
                        pygame.quit()
                        exit()
                

# ---Reinicio del juego tras una colisión---
def reiniciar_juego():
    global menu_activo, jugador, bala, bala2, nave, nave2, bala_disparada, bala_disparada2, salto, en_suelo
    global en_posicion_inicial, mov_delantero, jugador_regresando
    #Restaurar posiciones 
    menu_activo = True  
    jugador.x, jugador.y = 50, h - 100  
    bala.x = w - 50 
    nave.x, nave.y = w - 100, h - 100  
    nave2.x, nave2.y = 20, 0  
    bala2.x = 50  
    bala2.y = 0 
    #Reset de estado 
    bala_disparada = False
    bala_disparada2 = False  
    en_posicion_inicial = True  
    mov_delantero = False 
    jugador_regresando = False  
    salto = False
    en_suelo = True
    # Mostrar datos y volver al menú
    print("Datos recopilados para el entrenamiento del modelo: ", datos_modelo)
    mostrar_menu()  
#---------------------------------------------------------------------------- 
# INICIALIZACION DE LOS MODELOS DE VECINOS CERCANOS -------------------
# Modelo para decidir salto
modelo_salto = None  
# Modelo para decidir movimiento delantero
modelo_mov_delantero = None  

# ----Entrenamiento del modelo de árbol de decisión----
def entrenar_modelo():
    global modelo_salto, modelo_mov_delantero
    #Verificar si hay suficientes datos para entrenar
    if len(datos_modelo) < 5:
        print("En este momento no hay suficientes datos para entrenar.")
        return
    print("Los modelos de vecinos cercanos se entrenan con", len(datos_modelo), "datos...")

    #Separar datos de entrada y salida
    # para salto
    # Velocidad y distancia horizontal
    X_salto = np.array([[v, d] for v, d, _, _, _, _ in datos_modelo]) 
    # Saltó o no (1 o 0)
    Y_salto = np.array([s for _, _, s, _, _, _ in datos_modelo]) 

    # Datos para movimiento delantero
    mov_x_delantero = np.array([[v2, d2] for _, _, _, v2, d2, _ in datos_modelo])
    mov_y_delantero = np.array([m for _, _, _, _, _, m in datos_modelo])

    # Entrenamiento de los dos modelos
    # Entrenar los clasificadores k-NN (k=3 por defecto)
    modelo_salto = KNeighborsClassifier(n_neighbors=3)
    modelo_salto.fit(X_salto, Y_salto)

    # Modelo de vecinos cercanos para movimiento delantero
    modelo_mov_delantero = KNeighborsClassifier(n_neighbors=3)
    modelo_mov_delantero.fit(mov_x_delantero, mov_y_delantero)
    print("Modelos de vecinos cercanos entrenados.")

# ----IA decide si saltar automáticamente basado en la predicción del modelo------
def decidir_salto_auto():
    global velocidad_bala, jugador, bala, modelo_salto

    if modelo_salto is None: 
        print("Modelo de decisión no entrenado. No se puede decidir salto!")
        return False

    # Predicción basada en distancia y velocidad de la bala horizontal
    distancia = abs(jugador.x - bala.x)
    entrada = np.array([[velocidad_bala, distancia]])
    prediccion = modelo_salto.predict(entrada)[0]
    # Si la predicción es 1, salta
    return prediccion == 1 

# ----IA decide si moverse hacia adelante automáticamente basado en la predicción del modelo------
def decidir_mov_delantero_auto():
    global velocidad_bala2, jugador, bala2, modelo_mov_delantero

    if modelo_mov_delantero is None:
        print("Modelo de movimiento de decisión no entrenado.")
        return False

    distancia2 = abs(jugador.y - bala2.y)
    entrada = np.array([[velocidad_bala2, distancia2]])
    prediccion = modelo_mov_delantero.predict(entrada)[0]

    return prediccion == 1
#-------------------------------- --------------------------
#-----Función principal del juego----------
def main():
    global salto, en_suelo, bala_disparada, bala_disparada2, mov_delantero, en_posicion_inicial

# Inicialización del reloj y menú
# Crea un reloj para controlar la velocidad de los FPS
    reloj = pygame.time.Clock()
    # Muestra el menú antes de empezar el juego
    mostrar_menu()  
    # Variable que mantiene el bucle del juego activo
    correr = True

#Bucle principal del juego
    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                # Detectar tecla space para saltar
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  
                    salto = True
                    en_suelo = False
                # Detectar 'z' para moverse hacia adelante
                if evento.key == pygame.K_z: 
                    # Cambiar la variable de movimiento a True
                    mov_delantero = True  
                    # Cambiar la variable de posición inicial a False
                    en_posicion_inicial = False  
                    # Detectar 'c' para pausar el juego
                if evento.key == pygame.K_c:  
                    pausa_juego()
                    #Detectar 'q' para terminar el juego
                if evento.key == pygame.K_q:  
                    print("Felicidades, Juego terminado!. Los Datos recopilados son:", datos_modelo)
                    pygame.quit()
                    exit()
#Si no está en pausa, se actualiza el juego
        if not pausa:
            # Si está en modo automatico
            if modo_auto:
                # decide saltar usando el modelo de IA
                if en_suelo and decidir_salto_auto():
                    salto = True
                    en_suelo = False
                    #ejecutar salto
                if salto:
                    manejar_salto()
                    
                # Decidir si moverse hacia adelante automáticamente a traves del modelo decision de IA
                if en_posicion_inicial and decidir_mov_delantero_auto():
                    mov_delantero = True
                    en_posicion_inicial = False
                    # ejecutar movimiento delantero
                if mov_delantero:
                    manejo_movimiento_delantero()
          # Si está en modo manual         
            else: 
                if salto:
                    manejar_salto()
                
                if mov_delantero:
                    manejo_movimiento_delantero()
                # Guardar datos para entrenar el modelo IA
                guardar_datos()

            #--------- Control de disparo de balas-------
            if not bala_disparada:
                disparar_bala()
            # Actualiza el estado del juego (fondo, animaciones, colisiones)
            update()
            
            if not bala_disparada2:
                disparar_bala2()
            update()

        # Muestra los cambios en la pantalla
        pygame.display.flip()
       # Limita el juego a 30 FPS
        reloj.tick(30)  
#salida del juego
    pygame.quit()
#punto de entrada del juego
if __name__ == "__main__":
    main()
