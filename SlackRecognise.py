import datetime
from DBConnect import DBAcsess
import requests, json
# タイムカード処理を行うクラス
class TimeCard:
    def __init__(self, status,json):
        self.status = status
        self.TimeChecker()
        self.dic = json
        if(json != {""} ):
            self.separateInfo()
        self.DumpDB()
        self.Massge = ""

    def separateInfo(self):
        self.userID = [v for k, v in self.dic.items() if k == "user_id"][0]
        self.user_name = [v for k, v in self.dic.items() if k == "user_name"][0]
        self.team_id = [v for k, v in self.dic.items() if k == "team_id"][0]
        self.team_domain = [v for k, v in self.dic.items() if k == "team_domain"][0]

    def SlackMessage(self):
        tmp = ["出勤", "退勤", "休憩開始", "休憩終了"]
        self.Massge = "{0}さんの{2}を受け付けました。\n {1}".format(self.user_name,self.dt_now.strftime('%Y年%m月%d日 %H:%M:%S'), tmp[self.status])
        return self.Massge

    def DumpDB(self):
        mondb = DBAcsess()
        mondb.TimeCard(self.userID,self.team_id,self.status,self.dt_now,self.Today)

    def TimeChecker(self):
        self.dt_now = datetime.datetime.now()
        self.Today = str(self.dt_now.strftime('%Y-%m-%d'))


# Slackのスタンプから機能判別をするところ
class SlackRecognise:
    def __init__(self, txt, json = {""}):
        self.text = txt
        self.dic = json
        self.message = ""
        self.type = ""

    def Judge(self):
        wordDic = [":started_sagyo:", ":finished_sagyo:", ":started_kyukei:", ":finished_kyukei:"]
        count = [i for i in range(0,len(wordDic))]
        odd_even = [True if i in self.text else False for i in wordDic]
        dic = {key: val for key, val in zip(count, odd_even)}
        self.Doworking(dic)

    def Doworking(self, dic):
        self._dic = dic
        keys = [k for k, v in self._dic.items() if v == True]
        for i in keys:
            # 1~4の場合は出勤判定
            if i < 4:
                TC = TimeCard(i,self.dic)
                self.message = TC.SlackMessage()
                self.type = "TimeCard"

# incomming webHook用
class SlackPost():
    def __init__(self,type,team_id="",channel_id=""):
        self.type = type
        self.botName = ""
        self.message = ""
        self.team_id = team_id
        self.Icon = ""
        self.channel_id = channel_id
        if(self.type == "Slack"):
            self.configRead()
            # self.POSTSlack()
    def configRead(self):
        AAA = DBAcsess()
        self.BotUrl = AAA.LoadConf(self.team_id,self.channel_id)

    def POSTSlack(self):
        print(self.message)
        requests.post(self.BotUrl, data=json.dumps({
            'text': self.message,
            'username': self.botName,  # ユーザー名
            'icon_emoji': self.Icon,  # アイコン
            'link_names': 1,  # 名前をリンク化
        }))
