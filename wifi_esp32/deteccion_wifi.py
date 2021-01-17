import sensor,image,lcd
import KPU as kpu

import network
import utime
from Maix import GPIO
from fpioa_manager import *
from network_esp32 import wifi


SSID = "GOMEZ"
PASW = "1102381153"

#Conexiones del ESp32
fm.register(25,fm.fpioa.GPIOHS10)#cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#mosi
fm.register(26,fm.fpioa.GPIOHS14)#miso
fm.register(27,fm.fpioa.GPIOHS15)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12,
mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)


lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)#Asigna el formato de color a la imagen 5Red 6Green 5blue
sensor.set_framesize(sensor.QVGA)#Define la resolucion para la camara del sensor
sensor.set_windowing((224, 224))#Tamaño de imagen con la que se entrenó la red
sensor.set_vflip(1)#Gira verticalmente la camara
sensor.run(1)#inicia el sensor
classes = ["Baloto", "Good", "Look", "Palma", "Rock", "Piedra"]#clases utlizadas en el entrenamiento
task = kpu.load(0x300000)#Carga el modelo en formato kmodel ya sea en la memoria flash o sd
#"/sd/mobilenet7_5_sp.kmodel"
a = kpu.set_outputs(task, 0,7,7,55)#Valores de la ultima capa de la red
anchor = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828) #anclaje de yolov2
a = kpu.init_yolo2(task, 0.8, 0.3, 5, anchor)#modelo/precision de clase/precion cajas/numero de anclas/ anclas

while(True):
    img = sensor.snapshot().rotation_corr(z_rotation=90.0)#Captura la imagen
    a = img.pix_to_ai()
    code = kpu.run_yolo2(task, img)#ejecuta la red neuronal con la imagen tomada
    if code:
        for i in code: #Muestra en la lcd la respuesta
            a=img.draw_rectangle(i.rect(),color = (0, 255, 0))
            a = img.draw_string(i.x(),i.y(), classes[i.classid()], color=(255,0,0), scale=3)
            etiqueta=classes[i.classid()]#obtene la case

#CLASE GOOD
            if etiqueta == 'Good':
                print("Escaeno de redes wifi iniciado")
#Hace el escaneo de redes wifi disponible
                enc_str = ["OPEN", "", "WPA PSK", "WPA2 PSK", "WPA/WPA2 PSK", "", "", ""]
                aps = nic.scan()
                for ap in aps:
                    print("SSID:{:^20}, ENC:{:>5} , RSSI:{:^20}".format(ap[0], enc_str[ap[1]], ap[2]))

#CLASE BALOTO
            if etiqueta == 'Baloto':
                print("Conexion a red Wifi iniciada")
                nic.connect("GOMEZ", "1102381153")#Se conecta a una red wifi

                if nic.isconnected() == False:
                    for i in range(5):
                        try:
                            nic.reset()
                            print('try AT connect wifi...')
                            nic.connect(SSID, PASW)
                            if nic.isconnected():
                                break
                        except Exception as e:
                            print(e)
                print('Network state:', nic.isconnected(), nic.ifconfig())

#CLASE ROCK
            if etiqueta == 'Rock':
                print("Desconexión de red Wifi")
                nic.disconnect()#Se desconecta a una red wifi
                print('Network state:', nic.isconnected(), nic.ifconfig())


#CLASE PIEDRA
            if etiqueta == 'Piedra':
                print("Obtenteniendo ping de www.uis.edu.co ...")
                nic.connect("GOMEZ", "1102381153")#Se conecta a una red wifi
                print('Network state:', nic.isconnected(), nic.ifconfig())
                if nic.isconnected() == False:
                    for i in range(5):
                        try:
                            nic.reset()
                            print('try AT connect wifi...')
                            nic.connect(SSID, PASW)
                            if nic.isconnected():
                                break
                        except Exception as e:
                            print(e)
                print("ping_uis.edu.co:", nic.ping("www.uis.edu.co"), "ms")#Obtiene el ping de una pag web
                nic.disconnect()

#CLASE LOCK
            if etiqueta == 'Look':
#Obtiene la direccion IP de un sitio WEB
                print("Obteniendo IP de sitio web www.uis.edu.co")

                def enable_esp32():
                    from network_esp32 import wifi
                    if wifi.isconnected() == False:
                        for i in range(5):
                            try:
                                # Running within 3 seconds of power-up can cause an SD load error
                                # wifi.reset(is_hard=False)
                                wifi.reset(is_hard=True)
                                print('try AT connect wifi...')
                                wifi.connect(SSID, PASW)
                                if wifi.isconnected():
                                    break
                            except Exception as e:
                                print(e)
                    print('network state:', wifi.isconnected(), wifi.ifconfig())

                enable_esp32()

                def enable_espat():
                    from network_espat import wifi
                    if wifi.isconnected() == False:
                        for i in range(5):
                            try:
                                # Running within 3 seconds of power-up can cause an SD load error
                                # wifi.reset(is_hard=False)
                                wifi.reset()
                                print('try AT connect wifi...')
                                wifi.connect(SSID, PASW)
                                if wifi.isconnected():
                                    break
                            except Exception as e:
                                print(e)
                    print('network state:', wifi.isconnected(), wifi.ifconfig())

                #enable_espat()

                # from network_w5k import wlan

                try:
                    import usocket as socket
                except:
                    import socket

                TestHttps = False

                def main(use_stream=True):
                    s = socket.socket()
                    s.settimeout(1)
                    host = "www.uis.edu.co"
                    if TestHttps:
                        ai = socket.getaddrinfo(host, 443)
                    else:
                        ai = socket.getaddrinfo(host, 80)
                    print("Address infos:", ai)
                    addr = ai[0][-1]
                    for i in range(5):
                        try:
                            print("Connect address:", addr)
                            s.connect(addr)

                            if TestHttps: # ssl
                                try:
                                    import ussl as ssl
                                except:
                                    import ssl
                                tmp = ssl.wrapsocket(s, server_hostname=host)
                                tmp.write(b"GET / HTTP/1.1\r\n\r\n")
                            else:
                                s.write(b"GET / HTTP/1.1\r\n\r\n")
                            data = (s.readline('\r\n'))
                            print(data)
                            with open('test.txt', 'wb') as f:
                                f.write(data)

                        except Exception as e:
                          print(e)

                    s.close()

                main()

            print(etiqueta)
        a = lcd.display(img)

    else:
        a = lcd.display(img)
a = kpu.deinit(task)
