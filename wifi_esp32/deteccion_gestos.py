import sensor,image,lcd,time
import KPU as kpu


lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)
clock = time.clock()
classes = ["Baloto", "Good", "Look", "Palma", "Rock", "Piedra"]
task = kpu.load(0x300000)
#"/sd/mobilenet_5_sp.kmodel"
a = kpu.set_outputs(task, 0,7,7,55)
anchor = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
a = kpu.init_yolo2(task, 0.8, 0.3, 5, anchor)


while(True):
    img = sensor.snapshot().rotation_corr(z_rotation=180.0)
    a = img.pix_to_ai()
    code = kpu.run_yolo2(task, img)
    if code:
        for i in code:
            a = img.draw_rectangle(i.rect(),color = (0, 255, 0))
            a = img.draw_string(i.x(),i.y(), classes[i.classid()], color=(255,0,0), scale=3)


        a = lcd.display(img)
        print(classes[i.classid()])
    else:
        a = lcd.display(img)
a = kpu.deinit(task)




