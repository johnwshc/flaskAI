from config import Config

from pymongo import MongoClient
from pymongo.server_api import ServerApi

class MongoERConn:
    mongo_usr = "dev"
    sample_usrs_json = f"{Config.JSON_DIR}/sample_users.json"
    mongo_pw = 'youwillneverguess'
    atlas_radio_uri = f"mongodb+srv://{mongo_usr}:{mongo_pw}@cluster0.xj2jzta.mongodb.net/?retryWrites=true&w=majority"
    mongo_local_uri = f'mongodb://localhost:27017/'
    mongo_radio_url = f'mongodb://10.1.10.125:27017/'

    ##############################     clean!!        #############################

    atlas_bamazon_uri = f"mongodb+srv://{mongo_usr}:{mongo_pw}@sandbox.xtifj.mongodb.net/bamazon?retryWrites=true&w=majority"
    # mongosh_uri = "mongodb+srv://sandbox.xtifj.mongodb.net/myFirstDatabase"
    # mongo_json_export_dir = Config.playlists_json
    # data_api_url = 'https://data.mongodb-api.com/app/data-jqglk/endpoint/data/beta'
    # er_url = f"mongodb+srv://{mongo_usr}:{mongo_pw}@cluster0.xj2jzta.mongodb.net/?retryWrites=true&w=majority"
    # er_local_url = f"{mongo_local_uri}er"
    # server MongoClient args:    server_api=ServerApi('1')
    #### mongosh_conn = mongosh "mongodb+srv://sandbox.xtifj.mongodb.net/radio" --apiVersion 1 --username admin
    ######################################################


    # Three types of connections to Mongo:
    #   -- at_radio -- the Atlas Mongo radio db
    #   -- localhost -- 127.0.0.1
    #   -- localIP -- localhost net IP: 10.1.10.125
    def __init__(self, serv='at_radio'):
        if not serv:
            raise Exception("no server")

        if serv == 'at_radio':
            self.mc = MongoClient(MongoERConn.atlas_radio_uri, server_api=ServerApi('1'))
        elif serv == 'localhost':
            self.mc = MongoClient(MongoERConn.mongo_local_uri)
        elif serv == 'localIP':
            self.mc = MongoClient(MongoERConn.mongo_radio_url)
        else:
            raise Exception(f"unknown server{serv}")

    def __del__(self):
        print(f'in MongoERConn destructor')
        self.mc.close()
