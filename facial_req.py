#! /usr/bin/python
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

#Tanınan birisi gelene kadar bilinmeyen kişi diye tanımlıyoruz
currentname = "Bilinmeyen kisi"
#train_model.py ile eğittip sakladığımız verileri alıyoruz
encodingsP = "encodings.pickle"

# Bilinen yüzleri yüklüyoruz
# Yüz tanıma için
print("[BILGI] encodelar ve yüz tanıma yükleniyor...")
data = pickle.loads(open(encodingsP, "rb").read())

# Yayın için kamerayı başlatıp hata oluşmaması için süre ayırıyoruz
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# FPS sayacını başlatıyoruz
fps = FPS().start()

# Her bir turda 1 frame aldığından bunu sonsuz döngüye sokuyoruz
while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	# Framedeki yüzü tanıma
	boxes = face_recognition.face_locations(frame)
	encodings = face_recognition.face_encodings(frame, boxes)
	names = []

	for encoding in encodings:
		# Her bir yüz için kontrol ediyor
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Bilinmeyen Kisi" #Eğer tanıdık biri değil ise

		# Tanıdık birisi mi diye kontrol
		if True in matches:
			# Tanıdık birisini bulana kadar listeyi döndürüyor
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# Her bir tanıdık yüzü listeye aldığında eşleştiriyor
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# Tanımlanan yüzün en büyüğünü alıyor(yapmazsak en ufak tanımlamada dikdörtgen çizdirir)
			name = max(counts, key=counts.get)

			#Eğer database'de tanımlıysa ismini konsola yazdır
			if currentname != name:
				currentname = name
				print(currentname)
				
				f = open("Yoklama.txt", "a")
				f.write(currentname)
				f.write("\n")

		# isim listesine ekle
		names.append(name)

	for ((top, right, bottom, left), name) in zip(boxes, names):
		# Tanımlanmış yüzü dikdörtgen içine al ve ismini yaz
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 225), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			.8, (0, 255, 255), 2)

	cv2.imshow("Yüz Tanıma çalışıyor...", frame)
	key = cv2.waitKey(1) & 0xFF

	# q ya basıldığında kapat
	if key == ord("q"):
		break

	fps.update()

#Program kapatıldığında fps bilgisini konsola yazdır
fps.stop()
print("[BILGI] toplam frame: {:.2f}".format(fps.elapsed()))
print("[BILGI] ortalama fps: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
