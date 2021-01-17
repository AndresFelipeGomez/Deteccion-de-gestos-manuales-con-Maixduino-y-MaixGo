import sensor,image,lcd
import KPU as kpu

import network
import utime
from Maix import GPIO
from fpioa_manager import *
from network_espat import wifi

SSID = "GOMEZ"
PASW = "1102381153"

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
    img = sensor.snapshot().rotation_corr(z_rotation=180.0)#Captura la imagen
    a = img.pix_to_ai()
    code = kpu.run_yolo2(task, img)#ejecuta la red neuronal con la imagen tomada
    if code:
        for i in code: #Muestra en la lcd la respuesta
            a=img.draw_rectangle(i.rect(),color = (0, 255, 0))
            a = img.draw_string(i.x(),i.y(), classes[i.classid()], color=(255,0,0), scale=3)
            etiqueta=classes[i.classid()]#obtene la case

#CLASE Palma
            if etiqueta == 'Palma':
                print("Escaeno de redes wifi iniciado")
#Hace el escaneo de redes wifi disponible
                wifi.reset()

                print(wifi.at_cmd("AT\r\n"))

                ap_info = []

                import time
                while True:
                    time.sleep(1)
                    print('ap-scan...')
                    try:
                        tmp = wifi.at_cmd('AT+CWLAP\r\n')
                        #ap_info = wifi.nic.scan()
                        if tmp != None and len(tmp) > 64:
                            #print(tmp[len('+CWLAP:'):].split(b"\r\n"))
                            aps = tmp.replace(b'+CWLAP:', b'').replace(b'\r\n\r\nOK\r\n', b'')
                            #print(aps)
                            ap_info = aps.split(b"\r\n")
                            #print(ap_info)
                            break
                    except Exception as e:
                        print('error', e)

                def wifi_deal_ap_info(info):
                    res = []
                    for ap_str in info:
                        ap_str = ap_str.split(b",")
                        #print(ap_str)
                        info_one = []
                        for node in ap_str[1:-1]:
                            if node.startswith(b'"'):
                                info_one.append(node[1:-1])
                            else:
                                info_one.append(int(node))
                        res.append(info_one)
                    return res

                #print(ap_info)

                ap_info = wifi_deal_ap_info(ap_info)

                ap_info.sort(key=lambda x:x[2], reverse=True) # sort by rssi
                for ap in ap_info:
                    print("SSID:{:^20}, RSSI:{:>5} , MAC:{:^20}".format(ap[0], ap[1], ap[2]) )

#CLASE Baloto
            if etiqueta == 'Baloto':
                print("Conexion a red Wifi iniciada")
                wifi.connect("GOMEZ", "1102381153")#Se conecta a una red wifi

                if wifi.isconnected() == False:
                    for i in range(5):
                        try:
                            wifi.reset()
                            print('try AT connect wifi...')
                            wifi.connect(SSID, PASW)
                            if wifi.isconnected():
                                break
                        except Exception as e:
                            print(e)
                print('Network state:', wifi.isconnected(), wifi.ifconfig())

#CLASE ROCK
            if etiqueta == 'Rock':
                print("Desconexión de red Wifi")
                wifi.reset()
                wifi.isconnected()
                print('Network state:', wifi.isconnected(), wifi.ifconfig())



#CLASE LOCK
            if etiqueta == 'Look':
#Obtiene la direccion IP de un sitio WEB
                print("Obteniendo IP de sitio web www.uis.edu.co")

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
