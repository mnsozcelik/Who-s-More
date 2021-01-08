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
import random
import os

# Soru Getirme Fonksiyonu
def GetQuestion(endBool):
    QP=["Kim Daha CIMRI",
        "Kim Daha KURNAZ",
        "Kim Daha YUREKLI",
        "Kim Daha HAYVAN SEVER",
        "Kim Daha INANCLI",
        "Kim Daha ACIMASIZ",
        "Kim Daha DENGESIZ",
        "Kim Daha HOSGORULU",
        "Kim Daha SASKIN",
        "Kim Daha GAMSIZ",
        "Kim Daha FEDAKAR",
        "Kim Daha SIRIN",
        "Kim Daha AC",
        "Kim Daha ZENGIN",
        "Kim Daha KORKAK",
        "Kim Daha TELASLI",
        "Kim Daha ZEKI",
        "Kim Daha ASABI"]
    questionvalue=(len(QP))-1
    a = random.randint(0,questionvalue)
    question=QP[a]
    QP.remove(QP[a])
    if(endBool):
        return "Kim Daha Bitti GORUSURUZ :)"
    return question
print("Oyun Basliyor..")
# Gerekli Değişkenlerin Tanımlanması
gamersPoint=0
gamersScore=0
getQuestionValue=0
timeCounter=0
nextQuestionValue=0
questionCounter=0
finishBool=False
questionText="Sorular Hemen Geliyor!"
r1=119
g1=136
b1=153
setPointValue=0
setpointValue=1

# dlib'in yüz algılayıcısını başlat ve sonra oluştur 
# Yüz simgesi belirleyici 
p = "shape_predictor_5_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cap = cv2.VideoCapture(0)
print("Kamera Açıldı Görüntü İşleme İşlemi Başlıyor..")
while True:
    # Kullanıcının yüzündeki dairenin renkler
    red=0
    green=0
    blue=0
    
    # Giriş görüntüsünü yükleyin ve gri tonlamaya dönüştür 
    _, image = cap.read()
    image = cv2.flip(image, 1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gri tonlamalı görüntüdeki yüzleri algıla 
    height, width, channels = image.shape
    rects = detector(gray, 0)

    # Oyuncuların verilerinin tutulduğu gamers dizisi 
    # gamers[0] => İlk oyuncunun yönü
    # gamers[1] => İkinci oyuncunun yönü 
    # gamers[2] => İlk oyuncunun çemberinin merkez koordinatı 
    # gamers[3] => İkinci oyuncunun çemberinin merkez koordinatı 
    gamers=["Null","Null",[_,_],[_,_]]
    
    # Yüz algılamalarının üzerinden geç 
    for (i, rect) in enumerate(rects):
        
        # Dizi 
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        # Yüzdeki 5 noktanın belirleme
        midPoint = [int((shape[1][0]+shape[3][0])/2),int((shape[1][1]+shape[3][1])/2)]
        direction = ""
        
        # İki noktadan elde edilen eğimi bulma |TR
        slope=math.atan((shape[4][1]-midPoint[1])/(shape[4][0]-midPoint[0]))
        
        # Bulunan eğim değerinin test edilen aralık ile anlamlandırma. 
        # Sağ için aralık (-1.35<slope<0) 
        # Sol için aralık (0<slope<1.35) 
        # Aralık dışı kalan değerler için "orta" 
        if(-1.35<slope and slope<0.0):
            direction = "sag"
        elif(0.0<slope and slope<1.35):
            direction = "sol"
        else:
            direction = "orta"
        if(i+1==1):
            # İlk Oyuncu
            gamers[0] =direction
            gamers[2][0] = shape[4][0]
            gamers[2][1] = shape[4][1]
            
        if(i+1==2):
            # İkinci Oyuncu
            gamers[1] = direction
            gamers[3][0] = shape[4][0]
            gamers[3][1] = shape[4][1]
        """
        # Yüzeki 5 noktayı temsil eden çemberlerin çizimi.
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        """
    # Oyuncuların baş pozisyonlarına göre bir çıktı değeri üreten koşul.    
    if((gamers[0]=="sag" and gamers[1]=="sag") or (gamers[0]=="sol" and gamers[1]=="sol")):
        blue=0
        green=255
        red=0
        cv2.putText(image, 'Birlikte +1', (int(width/2)-120,height-50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (blue, green, red), 2, cv2.LINE_AA)
        getQuestionValue=1
        gamersPoint=1     
    elif(gamers[0]=="orta" and gamers[1]=="orta"):
        blue=153
        green=136
        red=119
        gamersPoint=0
        cv2.putText(image, 'Lutfen Soruyu cevaplayin!', (int(width/2)-120,height-50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (blue, green, red), 2, cv2.LINE_AA)
    elif((gamers[0]=="sag" and gamers[1]=="sol") or (gamers[0]=="sol" and gamers[1]=="sag")):
        blue=0
        green=0
        red=255
        cv2.putText(image, 'Birlikte Degil -1', (int(width/2)-120,height-50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (blue, green, red), 2, cv2.LINE_AA) 
        getQuestionValue=1
        gamersPoint=-1
    else:
        gamersPoint=0
        blue=153
        green=136
        red=119
        cv2.putText(image, 'Lutfen Ikinci Oyuncuyu Bekleyin!', (int(width/2)-120,height-50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (blue, green, red), 2, cv2.LINE_AA)
   
    # Kullanıcıların Yüzünü Gösteren Çemberin Çizilmesi ve Renklendirilmesi.
    if(gamers[0]=="sag" or gamers[0]=="sol" or gamers[0]=="orta"):
        cv2.circle(image, (gamers[2][0], gamers[2][1] -50), 100, (blue, green, red), 5)
        
    if(gamers[1]=="sag" or gamers[1]=="sol" or gamers[1]=="orta"):
        cv2.circle(image, (gamers[3][0], gamers[3][1] -50), 100, (blue, green, red), 5)
    
    # İlk Açılışta Soru Gelmesini Sağlayan Şart
    if(questionText=="Sorular Hemen Geliyor!"):
        getQuestionValue=1
    # Zaman Sayacı (Programlama tarafında kullnıldı.)    
    timeCounter+=1
    # Zaman Sayacının Kontrolü
    if(timeCounter%40==0):
        nextQuestionValue=1
    # Bir Sonraki Soruya Geçme Değerinin Kontrolü
    if(nextQuestionValue==0):
        getQuestionValue=0
    
    # Toplam Kaç Soru Sorulacağının Kontrolü 
    if(questionCounter>=11):
        questionText=GetQuestion(True)
    # Soru Getirme Kontrolü
    elif(getQuestionValue==1 and nextQuestionValue==1):
        questionText=GetQuestion(False)
        questionCounter += 1
        gamersScore+=gamersPoint
        gamersPoint=0
        getQuestionValue=0
        nextQuestionValue=0
    
    # Cevap Yardımcısının Renk Kontrolü    
    if(nextQuestionValue==1):
        r1=0
        g1=255
        b1=0
    if(nextQuestionValue==0):
        r1=255
        g1=0
        b1=0
    
    # Arayüzün Ekrana Basılması
    cv2.rectangle(image, (int(width/2)-175,0) , (int(width/2)+175,50), ((blue, green, red)),cv2.FILLED)
    cv2.circle(image, (int(width/2)+155,15), 15, (b1, g1, r1), -1)
    cv2.putText(image, str(questionText), (int(width/2)-175,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(image, "Puan:"+str(gamersScore), (int(width/2)+95,45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    
    # Penceerede Gösterilmesi
    cv2.imshow("Who's More", image)
    
    # Oyun Sonu İşlemleri ve Kontrolleri
    if(questionText=="Kim Daha Bitti GORUSURUZ :)"):
        cv2.imwrite('oyun_sonucun.png', image)
        cv2.rectangle(image, (10,125) , (width-10,375), ((153, 136, 119)),cv2.FILLED)
        cv2.putText(image, "KAPATMAK ICIN", (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 3, cv2.LINE_AA)
        cv2.putText(image, " ESC ", (int(width/2)-100,200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 5, cv2.LINE_AA)
        cv2.putText(image, "TUSUNA BASINIZ", (width-320,250), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 3, cv2.LINE_AA)
        cv2.line(image,(10,270),((width-10),270),(255,0,0),2)
        cv2.putText(image, "Sonucunuz", (10,300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, os.path.dirname(os.path.abspath(__file__)), (10,325), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, "konumuna kaydedildi.", (10,350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        
        # Oyuncunun Çıkmak için "ESC" Tuşuna Basma Kontrolü
        while True:
            cv2.imshow("Who's More", image)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                finishBool=True
                
                break
    # Uygulamanın Kapatılaması        
    if finishBool==True:
        break
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        # ESC tuşunu kullanarak oyunu kapatabilirsiniz. |TR
        break

# Pencerelerin Kapatılması.
cv2.destroyAllWindows()
cap.release()