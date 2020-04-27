import cv2
import sys
import pandas as pd
import shutil
import os

def resolucion():
    #define the screen resolution
    screen_res = 800, 600
    scale_width = screen_res[0] / frame.shape[1]
    scale_height = screen_res[1] / frame.shape[0]
    scale = min(scale_width, scale_height)

    #resized window width and height
    window_width = int(frame.shape[1] * scale)
    window_height = int(frame.shape[0] * scale)

    #cv2.WINDOW_NORMAL makes the output window resizealbe
    cv2.namedWindow('Analisis del Movimiento', cv2.WINDOW_NORMAL)

    #resize the window according to the screen resolution
    cv2.resizeWindow('Analisis del Movimiento', window_width, window_height)

def revisarDirectorio(directorio):
    try:
        shutil.rmtree(directorio)
    except OSError as e:
        print('Creando directorio')

    if not os.path.exists(directorio):
        os.makedirs(directorio)

def descomponerVideo(nombre):
    vidcap = cv2.VideoCapture(nombre)
    revisarDirectorio('frames')

    success,image = vidcap.read()
    count = 0
    while success:

        x="frames/frame%d.png" % count
        cv2.imwrite(x, image)
        # frames.append(x)    # save frame as JPEG file
        success,image = vidcap.read()
        #print('Read a new frame: ', success)
        count += 1
    print('Video Capturado')

trackers=[]
# Iniciar trackers
for i in range(0,5):
    trackers.append(cv2.TrackerCSRT_create())

x=input('Ingresa el nombre del video: ')
y=input('¿Convertir a frames? (Y/N) ')

if y=='Y' or y=='y' :
    descomponerVideo(x)

# Leer video
video = cv2.VideoCapture(x)

# Leer frames
frames=[]
nombreMarcas=['cadera','UCF','rodilla','tobillo','falanges']
ok, frame = video.read()
for i in range(0,5):
    frameEditado=frame.copy()
    cv2.putText(frameEditado, 'Selecciona '+nombreMarcas[i], (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    frames.append(frameEditado)

# ROI es Region Of Interest
# False es para no seleccionar del centro hacia afuera
resolucion()
bbox=[]
for i in range(0,5):
    bbox.append(cv2.selectROI('Analisis del Movimiento',frames[i], False))
    # Initialize tracker with first frame and bounding box
    trackers[i].init(frame, bbox[i])

# Crear tabla
datos = pd.DataFrame(columns=["Cadera X","Cadera Y","UCF X","UCF Y","Rodilla X","Rodilla Y",
                "Tobillo X","Tobillo Y","Falanges X","Falanges Y"])

while True:
    # Leer siguiente frame
    ok, frame = video.read()
    if not ok:
        break

    # Actualizar trackers
    for i in range(0,5):
        ok, bbox[i] = trackers[i].update(frame)

    # Dibujar bounding box
    if ok:
        # Trackeo exitoso
        centros=[]
        for i in range(0,5):
            p1 = (int(bbox[i][0]), int(bbox[i][1]))
            p2 = (int(bbox[i][0] + bbox[i][2]), int(bbox[i][1] + bbox[i][3]))
            xc = (bbox[i][0]+bbox[i][2])/2
            yc = (bbox[i][1]+bbox[i][3])/2
            centros.append(xc)
            centros.append(yc)
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

        datos=datos.append({'Cadera X':centros[0],'Cadera Y':centros[1],'UCF X':centros[2],
                            'UCF Y':centros[3],'Rodilla X':centros[4],'Rodilla Y':centros[5],
                            'Tobillo X':centros[6],'Tobillo Y':centros[7],'Falanges X':centros[8],
                            'Falanges Y':centros[9]},ignore_index=True)

    else :
        # Trackeo fallido
        cv2.putText(frame, 'Tracking fallido', (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Ver resultado
    cv2.imshow('Analisis del Movimiento', frame)

    # Salir al presionar ESC
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

# Obtener el nombre del video sin la extension
x=x.split('.')[0]
datos.to_csv(x+'.csv',index=True,header=True)
