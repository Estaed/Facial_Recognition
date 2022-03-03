import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

name = 'Onur' #Kişinin ismini yazıyoruz (İngilizce Hafler videoda bozuk çıkıyor)

cam = PiCamera()
cam.resolution = (512, 304)
cam.framerate = 10
rawCapture = PiRGBArray(cam, size=(512, 304))
    
img_counter = 0

while True:
    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True): #Frame frame fotoğraf birleştirip video
        image = frame.array
        cv2.imshow("Fotoğraf çekmek için boşluğa basınız", image)
        rawCapture.truncate(0)
    
        k = cv2.waitKey(1)
        rawCapture.truncate(0)
        if k%256 == 27: # ESC
            break
        elif k%256 == 32:
            # BOŞLUK
            img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, image)
            print("{} yazıldı!".format(img_name))
            img_counter += 1
            
    if k%256 == 27:
        print("ESC'ye basıldı kapatılıyor...")
        break

cv2.destroyAllWindows()
