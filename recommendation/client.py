import grpc
from recommend_pb2_grpc import RecommendationStub
from recommend_pb2 import Request


channel = grpc.insecure_channel("localhost:50051")
client = RecommendationStub(channel)

request = Request(require="pri", lat=37.7867, lon=-122.4112)
print(client.GetRecommendations(request))

