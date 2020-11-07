# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 22:02:19 2020

@author: mnsoz
"""

# import the necessary packages |EN
# Gerekli paketleri içe aktar |TR
from imutils import face_utils
import dlib
import cv2
import math
 
# initialize dlib's face detector and then create |EN
# dlib'in yüz algılayıcısını başlat ve sonra oluştur |TR
# the facial landmark predictor |EN
# Yüz simgesi belirleyici |TR
p = "shape_predictor_5_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cap = cv2.VideoCapture(0)
 
while True:
    # Colors of the circle on the wearer's face |EN
    # Kullanıcının yüzündeki dairenin renkleri |TR
    red=0
    green=0
    blue=0
    
    # Load the input image and convert it to grayscale |EN
    # Giriş görüntüsünü yükleyin ve gri tonlamaya dönüştür |TR
    _, image = cap.read()
    image = cv2.flip(image, 1)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the grayscale image |EN
    # Gri tonlamalı görüntüdeki yüzleri algıla |TR
    
    height, width, channels = image.shape
    
    rects = detector(gray, 0)
    
    # The gamers array where players' data is kept |EN
    # gamers[0] => Direction of the first player |EN
    # gamers[1] => Second player direction |EN
    # gamers[2] => Center coordinate of the first player's circle |EN
    # gamers[3] => Center coordinate of the second player's circle |EN
    # Oyuncuların verilerinin tutulduğu gamers dizisi |TR
    # gamers[0] => İlk oyuncunun yönü |EN
    # gamers[1] => İkinci oyuncunun yönü |EN
    # gamers[2] => İlk oyuncunun çemberinin merkez koordinatı |EN
    # gamers[3] => İkinci oyuncunun çemberinin merkez koordinatı |EN
    gamers=["Null","Null",[_,_],[_,_]]
    
    # Loop over the face detections |EN
    # Yüz algılamalarının üzerinden geç |TR
    for (i, rect) in enumerate(rects):
        # Determine the facial landmarks for the face region, then
        # Convert the facial landmark (x, y)-coordinates to a NumPy
        # Array |EN
        # Dizi |TR
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # Determining the 5 points on the face |EN
        # Yüzdeki 5 noktanın belirleme
        
        midPoint = [int((shape[1][0]+shape[3][0])/2),int((shape[1][1]+shape[3][1])/2)]
        direction = ""
        # Finding the slope obtained from two points |EN
        # İki noktadan elde edilen eğimi bulma |TR
        slope=math.atan((shape[4][1]-midPoint[1])/(shape[4][0]-midPoint[0]))
        # Interpretation of the slope value found with the tested range. |EN
        # Interval for Right (-1.35<slope<0) |EN
        # Interval for Left (0<slope<1.35) |EN
        # "orta" for values out of range |EN
        # Bulunan eğim değerinin test edilen aralık ile anlamlandırma. |TR
        # Sağ için aralık (-1.35<slope<0) |TR
        # Sol için aralık (0<slope<1.35) |TR
        # Aralık dışı kalan değerler için "orta" |TR
        if(-1.35<slope and slope<0.0):
            direction = "sag"
        elif(0.0<slope and slope<1.35):
            direction = "sol"
        else:
            direction = "orta"
        if(i+1==1):
            # One Player
            # Bir Oyuncu
            gamers[0] =direction
            gamers[2][0] = shape[4][0]
            gamers[2][1] = shape[4][1]
            
        if(i+1==2):
            # Two player
            # İki Oyuncu
            gamers[1] = direction
            gamers[3][0] = shape[4][0]
            gamers[3][1] = shape[4][1]
        """
        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        """
    if((gamers[0]=="sag" and gamers[1]=="sag") or (gamers[0]=="sol" and gamers[1]=="sol")):
        print ("Doğru")
        blue=0
        green=255
        red=0
    elif(gamers[0]=="orta" or gamers[1]=="orta"):
        print("Soruyu cevaplayın!")
        blue=153
        green=136
        red=119
    else:
        print("Yanlış")
        blue=0
        green=0
        red=255
    
    
    if(gamers[0]=="sag" or gamers[0]=="sol" or gamers[0]=="orta"):
        cv2.circle(image, (gamers[2][0], gamers[2][1] -50), 100, (blue, green, red), 5)
        
    if(gamers[1]=="sag" or gamers[1]=="sol" or gamers[1]=="orta"):
        cv2.circle(image, (gamers[3][0], gamers[3][1] -50), 100, (blue, green, red), 5)
    
    cv2.rectangle(image, (int(width/2)-150,0) , (int(width/2)+150,50), ((blue, green, red)),cv2.FILLED)
    cv2.putText(image, 'Kim daha cimri?', (int(width/2)-140,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA) 
    # show the output image with the face detections + facial landmarks
    
   
    cv2.imshow("Who's More", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
