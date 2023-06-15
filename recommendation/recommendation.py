import recommend_pb2_grpc
from recommend_pb2 import Result
import json
from geopy.distance import geodesic as GD
import math
import sys
import warnings
import grpc
from concurrent import futures


class Hotel():
    def __init__(self, HId, HLat, HLon):
        self.HId=HId
        self.HLat=HLat
        self.HLon=HLon


def loadRecommendations():
    with open('hotels.json') as json_file:
        data = json.load(json_file)
    hotels=[]
    for hotel in data:
        new_hotel = Hotel(hotel["id"], hotel["address"]["lat"], hotel["address"]["lon"])
        hotels.append(new_hotel)
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