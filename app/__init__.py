from flask import Flask
# from flask_cors import CORS
from analz.mongo.mongo_conn import MongoERConn
from app.jinjautils import JinjaUtils as JU
from analz.chatgpt.gpt_tests import SummaryManager as SM


app = Flask(__name__)
# init local db
mconn = MongoERConn(serv='localIP')
mclient = mconn.mc
# CORS(app)
app.config['SECRET_KEY'] = "you will never gue55"
app.config['WTF_CSRF_ENABLED'] = False
ju = JU()
sm = SM()
sm.loadSummaryDB()


from app import routes