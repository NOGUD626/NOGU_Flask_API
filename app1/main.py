from flask import *
import sys , ast , json
import requests as prequests
sys.path.append('../')
from DBConnect import DBAcsess
from SlackRecognise import SlackRecognise
from SlackRecognise import SlackPost
from cpslab import CPS_API
app1 = Blueprint('app1', __name__)

def PostSlack(URL,TEXT):
    data = json.dumps({
        'text': u'Notifycation From Python.'})
    prequests.post(URL, data)

@app1.route("/test", methods=["GET", "POST"])
def test():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        jsonDic = ast.literal_eval(data)
        MongoDB("Slack","Chanel_data",jsonDic)
        # print(jsonDic)
        return jsonify(jsonDic), 200

# Slack Outgoing Webhook
@app1.route("/post-slack", methods=["GET", "POST"])
def post_slack():
    if request.method == 'POST':
        if(request.headers.get("User-Agent") != "Slackbot 1.0 (+https://api.slack.com/robots)"):
            return {"status": "Request illegal User-Agent Eroor"}, 500

        if(request.form['channel_id'] and request.form['channel_name']
                and request.form['timestamp'] and request.form['user_name']
                and request.form['user_id'] and request.form['text'] and request.form['user_id'] != "USLACKBOT"):
            data = dict(request.form)
            SR = SlackRecognise(request.form['text'], data)
            SR.Judge()

            # 修士副手チャンネルを設定ファイルから参照
            TA_Chanel = CPS_API.TA_Chanel()

            # スタンプで出勤かを判断
            if(SR.type == "TimeCard"):
                SLACKBOT = SlackPost("Slack",request.form["team_id"],request.form["channel_id"])
                SLACKBOT.botName = "CPSLAB勤怠システム"
                SLACKBOT.message = SR.message
                SLACKBOT.Icon = ":minecraft:"
                SLACKBOT.POSTSlack()

            # 副手チャンネルの場合の処理
            elif(TA_Chanel == request.form['channel_id']):
                userName = CPS_API.ChanegName(request.form["user_name"])
                CPS_API.TA_Template(userName,request.form['text'])
                CPS_API.CatcheMaterLineID()
            # その他チャネルでの処理
            else:
                mondb = DBAcsess()
                mondb.MongoDBV_2("Slack","Chanel_data",data)
                # SLACKBOT = SlackPost("Slack", request.form["team_id"], request.form["channel_id"])
                # SLACKBOT.message = request.form['text']
                # SLACKBOT.POSTSlack()
                CPS_API.ChacheFileList(request.form["channel_id"])

        # if(request.form['user_id'] != "USLACKBOT"):
        #     URL = "https://hooks.slack.com/services/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"
        #     TEXT = ""
        #     PostSlack(URL,TEXT)

        return {"status":"ok"}, 200
