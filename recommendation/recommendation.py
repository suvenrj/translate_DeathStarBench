import json
from geopy.distance import geodesic as GD
import math
import sys
import warnings
import grpc
from concurrent import futures
from mongoengine import *

sys.path.insert(1, '/Users/suvenjagtiani/Desktop/hotel_recommend')

from cmd.db import *
from recommendation.recommend_pb2_grpc import *
from recommendation.recommend_pb2 import Result

# class Hotel():
#     def __init__(self, HId, HLat, HLon, HRate, HPrice):
#         self.HId=HId
#         self.HLat=HLat
#         self.HLon=HLon
#         self.HRate=HRate
#         self.HPrice=HPrice


def loadRecommendations(session):
    hotels=[]
    for hotel in Hotel.objects:
        hotels.append(hotel)
    return hotels        


class RecommendationService(RecommendationServicer):
    def __init__(self, mongo_session, port, ip, hotels=[]):
        self.hotels=hotels
        self.MongoSession = mongo_session
        self.Port=port
        self.IpAddr=ip
    
    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        if (not self.hotels):
            self.hotels = loadRecommendations(self.MongoSession)
        add_RecommendationServicer_to_server(
            self, server
        )
        server.add_insecure_port(self.IpAddr+":"+self.Port)
        server.start()
        server.wait_for_termination()

    def GetRecommendations(self, request, context):
        res_ids = []
        if (request.require=="dis"):
            p_user = (request.lat, request.lon)
            min_distance = sys.float_info.max
            for hotel in self.hotels:
                p_hotel = (hotel.HLat, hotel.HLon)
                distance = GD(p_user, p_hotel).km
                if (distance < min_distance):
                    min_distance = distance
            for hotel in self.hotels:
                p_hotel = (hotel.HLat, hotel.HLon)
                distance = GD(p_user, p_hotel).km
                if (distance==min_distance):
                    res_ids.append(hotel.HId)
        elif (request.require=="rate"):
            max_rate = 0
            for hotel in self.hotels:
                if (hotel.HRate > max_rate):
                    max_rate = hotel.HRate
            for hotel in self.hotels:
                if (hotel.HRate==max_rate):
                    res_ids.append(hotel.HId)
        elif (request.require=="price"):
            min_price = sys.float_info.max
            for hotel in self.hotels:
                if (hotel.HPrice < min_price):
                    min_price=hotel.HPrice
            for hotel in self.hotels:
                if (hotel.HPrice==min_price):
                    res_ids.append(hotel.HId)
        else:
            warnings.warn(f"Wrong require parameter: {request.require}")
        return Result(HotelIds=res_ids)