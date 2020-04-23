# coding:UTF-8
import configparser
from linebot.models import (FlexSendMessage,TextSendMessage,ImageSendMessage)
from linebot import LineBotApi
import os, ast
import json
import requests

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config_ini = configparser.ConfigParser()
config_ini.read('./cpslab/config.ini', encoding='utf-8')

# --------------------------------------------------
# config,iniから値取得
# --------------------------------------------------
# config.iniの値取得その1
LineBotToken = config_ini['CPSLAB']['LineBotToken']

# --------------------------------------------------
# config,iniから値取得
# --------------------------------------------------

SAVE_DIR = "./images"

if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

# --------------------------------------------------
# SlackのTAチャンネルから来たものをテンプレートメッセージとしてLINEへ転送
# --------------------------------------------------

def TA_Chanel():
    return config_ini['CPSLAB']['MasterChanel']

# --------------------------------------------------
# Slackのユーザネーム修正関係
# --------------------------------------------------

def CatcheMaterLineID():
    json_open = open('./cpslab/MasterLineList.json', 'r')
    json_load = json.load(json_open)
    return ([ i for i in json_load.values()])
# --------------------------------------------------
# Slackのユーザネーム修正関係
# --------------------------------------------------

def ChanegName(name):
    dic = ast.literal_eval(config_ini['CPSLAB']['modefyName'])
    if(str(name) in dic):
        return dic[name]
    else:
        return str(name)


# --------------------------------------------------
# Slackのユーザネーム修正関係
# --------------------------------------------------
def ChacheFileList(chanelID):
    token = config_ini['CPSLAB']['SlackToken']
    url = "https://slack.com/api/files.list?token={0}&channel={1}&count=1&pretty=1".format(token,chanelID)
    result = requests.get(url)
    data = json.loads(result.text)
    for file in data["files"]:
        print(file["url_private_download"],file["title"])
# --------------------------------------------------
# SlackのTAチャンネルから来たものをテンプレートメッセージとしてLINEへ転送
# --------------------------------------------------
def TA_Template(autourName,message):
    line_bot_api = LineBotApi(LineBotToken)
    payload = {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "hero": {
                "type": "image",
                "url": "https://dad41150.ngrok.io/images/CPSLabLogo_2019_800.png",
                "size": "full",
                "aspectRatio": "16:9",
                "aspectMode": "fit",
                "backgroundColor": "#FFFFFF"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "@" + autourName,
                        "size": "lg",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "TAチャンネルのメッセージ",
                        "color": "#988484"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": message,
                        "flex": 0,
                        "align": "start",
                        "wrap": True
                    }
                ]
            }
        }
    }
    container_obj = FlexSendMessage.new_from_json_dict(payload)
    for i in  CatcheMaterLineID():
        line_bot_api.push_message(i, messages=container_obj)
