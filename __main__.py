#-*- coding: utf-8 -*-
# =============================================================
#
#                       -- ROBOCAR --
# 
# TIME: CarNotFound
# CARRO: 404
#  
# =============================================================
#
# DESCRICAO: __main__.py 
# Python versao: 3
#
# Arquivo principal que vai instânciar os objetos das classes 
# CarHandler e ImageHandler para mover o carrinho de acordo 
# com as imagens obtidas pela webcam
#
# =============================================================

import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from CarHandler import CarHandler
from ImageHandler import ImageHandler
from constants import *
import cv2
# INSTANCIANDO OBJETOS DAS CLASSES IMAGEHANDLER E CARHANDLER
objImageHandler = ImageHandler() # Objeto para ImageHandler
objCarHandler = CarHandler()

#PREPARANDO A CAMERA
camera = PiCamera(sensor_mode = CAMERA_MODE) # Objeto para a Pi Camera
camera.resolution = CAMERA_RESOLUCAO
camera.framerate = CAMERA_FRAMERATE
rawCapture = PiRGBArray(camera, size=CAMERA_RESOLUCAO)
time.sleep(0.1)
print("CAMERA PREPARADA\n")

time.sleep(0.5)
#objCarHandler.rotinaDeTestes()



print("Iniciando rotina de tomada de decisão a partir das imagens da câmera.")

#PEGANDO FRAME POR FRAME PARA TRATAR E TOMAR UMA DECISAO
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	start = time.time()
	image = frame.array
	print("Frame Capturado")
	#DEPOIS DE CAPTURAR O FRAME EU TENTO TRATA-LO
	try:
		#print("Tentando tratar frame")
		Direcao, QtdeLinhas = objImageHandler.tratarImagem(image)

		#DEPOIS DE TRATAR, EU TOMO UMA DECISAO
		objCarHandler.tomadaDeDecisao(Direcao, QtdeLinhas)

		#print("Frame tratado")
	except (KeyboardInterrupt):
		objCarHandler.cleanupPins()
		exit(1)

	elapsed_time_fl = (time.time() - start)
	fps = 1/elapsed_time_fl
	print('FPS: ' + str(fps))

	rawCapture.truncate(0)	

# Libera os pinos
objCarHandler.cleanupPins()

