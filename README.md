# Facial_Recognition

This is a project that I made facial_regocnition using face recognition library. Also this project is rasberry pi project. 

This is a list what do you need:
Rasberry pi 3+
Rasberry picamera
monitor or laptop (if you have only a laptop connect vnc and ssh network)
mouse and keyboard

If you try this project, first of all you download opencv and other library you need. After then create folder that the folder name is your name, then open headshots_picam.py and write your name to name variable. Then run headshots_picam.py, this python file will take your photo and save your photo under dataset folder.

After take your photo, run train_model.py and train all photos. This trained file name is encodings.picle. Final step is run facial_req.py and done it, when the camera see your face draw rectangle and top of your head write your name.
