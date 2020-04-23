from pymongo import MongoClient
from datetime import timedelta
import datetime
class DBAcsess():
    def __init__(self):
        self.DBserver = "mongodb+srv://nogu626:Nogu.d8940626@cluster0-ly4mm.mongodb.net/test?retryWrites=true&w=majority"
        self.Connection()

    def Connection(self):
        self.client = MongoClient(self.DBserver)

    def LoadConf(self,team_id,channel_id):
        db = self.client["Slack"]
        co = db["ChanelList"]
        data_colection = co.find(
            filter={'$and': [{"team_id": team_id}, {"channel_id": channel_id}]}).sort('_id', -1).limit(1)
        return [i for i in data_colection][0]['BotURL']

    #  MongoDB Atlasに対してSlackのチャンネルかつユーザのメッセージ一件
    def MongoDBV_2(self,Database,record,dic):
        db = self.client[Database]
        co = db[record]
        result = co.insert(dic)
        data_colection = co.find(
            filter={'$and': [{"channel_id": dic["channel_id"]}, {"user_id": dic["user_id"]}]}).sort('_id', -1).limit(2)
        data = [i for i in data_colection]
        co.delete_many({"channel_id": dic["channel_id"], "user_id": dic["user_id"]})
        result = co.insert(data)

    def TimeCard(self,userID,team_id,status,dt_now,Today):
        db = self.client["TimeCard"]
        co = db["record"]
        data_colection = co.find(
            filter={'$and': [{"userID": userID}, {"date": Today},{"team_id": team_id}]}).sort('_id', -1).limit(1)
        data = [i for i in data_colection]

        # 出勤
        if(status == 0 and data ==[]):
            clock_in = dt_now.strftime("%H:%M:%S")
            clock_out = (dt_now + timedelta(minutes=1)).strftime("%H:%M:%S")
            dic = {"userID":userID,"team_id":team_id,"date": Today,"clock_in":clock_in,"clock_out":clock_out,"break_begin":0,"break_end":0}
            result = co.insert(dic)

            return 200

        # 退勤　& 休憩
        if((status == 1 or status == 2 or status == 3 )and data !=[]):
            dictionaly = {1:"clock_out",2:"break_begin",3:"break_end"}
            key = dictionaly[status]
            data = data[0]
            now_time = dt_now.strftime("%H:%M:%S")

            # 休憩開始と休憩終わり処理
            if(status != 1 and  data["clock_in"] == 0):
                d1 = datetime.datetime.combine(dt_now.date(), dt_now.time())
                axis_time = data["clock_in"].split(':')
                axis_time = datetime.time(int(axis_time[0]), int(axis_time[1]), int(axis_time[2]))
                d2 = datetime.datetime.combine(dt_now.date(), axis_time)
                if((d2-d1).total_seconds() > 0):
                    print("更新できません")
                    return 404
                co.update_one({"userID": userID, "team_id": team_id, "date": Today}, {'$set': {"break_begin": now_time,"break_end": now_time}})

            elif (status == 2 and data["break_begin"] != 0 ):
                co.update_one({"userID": userID, "team_id": team_id, "date": Today},{'$set': {"break_begin": now_time, "break_end": now_time}})

            if(key !="clock_out"):
                co.update_one({"userID": userID, "team_id": team_id, "date": Today}, {'$set': {key: now_time,"clock_out":now_time}})
            else:
                co.update_one({"userID": userID, "team_id": team_id, "date": Today}, {'$set': {key: now_time}})
            return 200
        return 404