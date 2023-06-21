from mongoengine import *

class Hotel(Document):
   HId = StringField(required=True)
   HLat = FloatField()
   HLon = FloatField()
   HRate = FloatField()
   HPrice = FloatField()
   def _init__(self, id, lat, lon, rate, price):
       self.HId=id
       self.HLat=lat
       self.HLon=lon
       self.HRate=rate
       self.HPrice=price

def initializeDatabase(url):
    session = connect('HotelReservation', host=url)
    if (not Hotel.objects(HId = "1")):
        h=Hotel(HId = "1", HLat=37.7867, HLon= -122.4112, HRate= 109.00, HPrice=150.00)
        try:
            h.save()
        except Exception as e:
            print(e)
    if (not Hotel.objects(HId = "2")):
        h=Hotel(HId = "2", HLat=37.7854, HLon= -122.4005, HRate= 139.00, HPrice=120.00)
        try:
            h.save()
        except Exception as e:
            print(e)
    if (not Hotel.objects(HId = "3")):
        h=Hotel(HId = "3", HLat=37.7834, HLon= -122.4071, HRate= 109.00, HPrice=190.00)
        try:
            h.save()
        except Exception as e:
            print(e)
    if (not Hotel.objects(HId = "4")):
        h=Hotel(HId = "4", HLat=37.7936, HLon= -122.3930, HRate= 129.00, HPrice=160.00)
        try:
            h.save()
        except Exception as e:
            print(e)
    if (not Hotel.objects(HId = "5")):
        h=Hotel(HId = "5", HLat=37.7831, HLon= -122.4181, HRate=119.00, HPrice=140.00)
        try:
            h.save()
        except Exception as e:
            print(e)
    if (not Hotel.objects(HId = "6")):
        h=Hotel(HId = "6", HLat=37.7863, HLon= -122.4015, HRate=149.00, HPrice=200.00)
        try:
            h.save()
        except Exception as e:
            print(e)

    for i in range(7, 81):
        hotel_id = str(i)
        
        lat = 37.7835 + i/500.0*3
        lon = -122.41 + i/500.0*4
        rate = 135.00
        rate_inc = 179.00

        if (i%3==0):
            if (i%5==0):
                rate = 109.00
                rate_inc=123.17
            elif(i%5==1):
                rate = 120.00
                rate_inc = 140.00
            elif(i%5==2):
                rate = 124.00
                rate_inc = 144.00
            elif (i%5==3):
                rate = 132.00
                rate_inc=158.00
            elif (i%5==4):
                rate = 232.00
                rate_inc = 258.00

        if (not Hotel.objects(HId=hotel_id)):
            h=Hotel(HId=hotel_id, HLat=lat, HLon=lon, HRate=rate, HPrice=rate_inc)
            try:
                h.save()
            except Exception as e:
                print(e)
    return session
