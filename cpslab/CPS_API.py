# coding:UTF-8
import configparser
from linebot.models import (FlexSendMessage, TextSendMessage, ImageSendMessage)
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
    return ([i for i in json_load.values()])


# --------------------------------------------------
# Slackのユーザネーム修正関係
# --------------------------------------------------

def ChanegName(name):
    dic = ast.literal_eval(config_ini['CPSLAB']['modefyName'])
    if (str(name) in dic):
        return dic[name]
    else:
        return str(name)


# --------------------------------------------------
# File管理をする場所
# --------------------------------------------------
def jsonLoad(FILE_PATH):
    # ファイルを開く
    json_open = open(FILE_PATH, 'r')
    json_load = json.load(json_open)
    return json_load


def SlackFileList(chanelID):
    token = config_ini['CPSLAB']['SlackToken']
    url = "https://slack.com/api/files.list?token={0}&channel={1}&page=1&count=1&pretty=1".format(token, chanelID)
    result = requests.get(url)
    datas = json.loads(result.text)
    print(datas)
    if ("files" in datas):
        data = datas["files"][0]
        return data["url_private_download"], data["title"]
    else:
        return 0


def ChacheFileList(ChanelID):
    FILE_PATH = "./cpslab/DataRecord.json"
    if not (os.path.exists(FILE_PATH)):
        str = {}
        with open(FILE_PATH, 'w') as f:
            json.dump(str, f)

    # JSONファイル読み込み
    Dictionary = jsonLoad(FILE_PATH)

    # チャンネルにキーがない場合は作成
    if not (ChanelID in Dictionary):
        Dictionary[ChanelID] = []
        print("Check")
        print(Dictionary)

    try:
        FileURL, FileName = SlackFileList(ChanelID)
    except TypeError:
        return 0

    # 過去に保存されていルカ判定
    if (FileName in Dictionary[ChanelID]):
        return 0
    SendLineFileLink(FileURL, "TAチャンネル", FileName)
    print("Done")

    Dictionary[ChanelID].append(FileName)
    countNum = len(Dictionary[ChanelID]) - 3
    if (countNum > 0):
        del Dictionary[ChanelID][:countNum]

    # ファイル書き出し
    with open(FILE_PATH, 'w') as f:
        json.dump(Dictionary, f)


# --------------------------------------------------
# SlackのTAチャンネルから来たものをテンプレートメッセージとしてLINEへ転送
# --------------------------------------------------
def TA_Template(autourName, message):
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
    # line_bot_api.push_message("U12c4f3d6dd5cfc3c9ec79975b6a6684d", messages=container_obj)
    for i in CatcheMaterLineID():
        line_bot_api.push_message(i, messages=container_obj)

def TA_Template1(autourName, message):
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
    line_bot_api.push_message("U12c4f3d6dd5cfc3c9ec79975b6a6684d", messages=container_obj)
    # for i in CatcheMaterLineID():
    #     line_bot_api.push_message(i, messages=container_obj)
# --------------------------------------------------
# Slackのチャンネル(ファイル転送)
# --------------------------------------------------
def SendLineFileLink(FileURL,ChannelName,FileTitle):
    line_bot_api = LineBotApi(LineBotToken)
    payload = {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "action": {
                    "type": "uri",
                    "uri": FileURL
                },
                "contents": [
                    {
                        "type": "text",
                        "text": ChannelName,
                        "size": "lg",
                        "align": "center"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "action": {
                    "type": "uri",
                    "uri": FileURL
                },
                "contents": [
                    {
                        "type": "text",
                        "text": FileTitle,
                        "align": "start",
                        "weight": "regular",
                        "color": "#C3B3B3"
                    },
                    {
                        "type": "separator"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "action": {
                    "type": "uri",
                    "uri": FileURL
                },
                "contents": [
                    {
                        "type": "text",
                        "text": "メッセージをクリックすることでDownloadできます",
                        "size": "xs",
                        "align": "center",
                        "wrap": True
                    }
                ]
            }
        }
    }
    container_obj = FlexSendMessage.new_from_json_dict(payload)
    line_bot_api.push_message("U12c4f3d6dd5cfc3c9ec79975b6a6684d", messages=container_obj)