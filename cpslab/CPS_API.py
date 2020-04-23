# coding:UTF-8
import configparser
from linebot.models import (FlexSendMessage,TextSendMessage,ImageSendMessage)
from linebot import LineBotApi
import os, ast

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
MasterMemberLine = config_ini['CPSLAB']['MasterMemberLine']

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

def ChanegName(name):
    dic = ast.literal_eval(config_ini['CPSLAB']['modefyName'])
    if(str(name) in dic):
        return dic[name]
    else:
        return str(name)

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
    print('Done')
    container_obj = FlexSendMessage.new_from_json_dict(payload)
    line_bot_api.push_message("U12c4f3d6dd5cfc3c9ec79975b6a6684d", messages=container_obj)