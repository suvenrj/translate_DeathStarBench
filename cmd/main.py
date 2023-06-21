import json
import sys
from db import *
from mongoengine import *

sys.path.insert(1, '/Users/suvenjagtiani/Desktop/hotel_recommend')

from recommendation.recommendation import RecommendationService

def main():
    f = open("config.json")
    config = json.load(f)

    session_ = initializeDatabase(config["RecommendMongoAddress"])
    port = config["RecommendPort"]
    ip = config["RecommendIP"]
    srv = RecommendationService(session_, port, ip, [])
    srv.serve()
    session_.close()

main()






