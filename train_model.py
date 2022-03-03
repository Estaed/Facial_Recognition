#! /usr/bin/python
from imutils import paths
import face_recognition
import pickle
import cv2
import os

#Resimlerin Olduğu dataset dosyasının yolu
print("[BILGI] Yüz İşlemesi Başlatılıyor...")
imagePaths = list(paths.list_images("dataset"))

#Bilinen isim ve encode için dizi oluşturduk
knownEncodings = []
knownNames = []

# İmage path'ını devamlı dönüyor
for (i, imagePath) in enumerate(imagePaths):
    
	print("[BILGI] Görsel İşleniyor {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# opencv rgb yi bgr diye okuması gerek cv2 ya uyumlu hale çeviriyoruz
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# (x, y) kordinatlarını bounding box için alıyoruz(sol alt ve sağ üst noktaları)
	# resimlerimizdeki yüzleri karşılaştırıyoruz
	boxes = face_recognition.face_locations(rgb,
		model="hog")

	# face_recognition ile bounding box yardımıyla tespit edip tanımasını sağlıyoruz.
	encodings = face_recognition.face_encodings(rgb, boxes)

	# Encode döngüsünü sonlandırıyoruz
	for encoding in encodings:
		# encode edip isimleri diziye ekliyoruz
		knownEncodings.append(encoding)
		knownNames.append(name)

# Encodeları ve isimleri pickle ile saklıyoruz
print("[BILGI] encodelanıp sıkıştırılıyor...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
