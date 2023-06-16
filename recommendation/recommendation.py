import recommend_pb2_grpc
from recommend_pb2 import Result
import json
from geopy.distance import geodesic as GD
import math
import sys
import warnings
import grpc
from concurrent import futures
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class Hotel():
    def __init__(self, HId, HLat, HLon, HRate, HPrice):
        self.HId=HId
        self.HLat=HLat
        self.HLon=HLon
        self.HRate=HRate
        self.HPrice=HPrice


def loadRecommendations():
    uri = "mongodb+srv://suvenjagtiani:<password>@cluster0.oxqritw.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["Hotel_Reservation"]
    table = db["recommendation"]
    hotels=[]
    for hotel in table.find():
        new_hotel = Hotel(hotel["id"], hotel["lat"], hotel["lon"], hotel["rate"], hotel["price"])
        hotels.append(new_hotel)
    client.close()
    return hotels        


class RecommendationService(recommend_pb2_grpc.RecommendationServicer):
    def __init__(self, hotels=[]):
        self.hotels=hotels

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

        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    service = RecommendationService()
    if (not service.hotels):
        service.hotels = loadRecommendations()
    recommend_pb2_grpc.add_RecommendationServicer_to_server(
        service, server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()