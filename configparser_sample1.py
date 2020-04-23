#coding:UTF-8
import configparser
from PIL import Image, ImageDraw
from linebot import LineBotApi
from linebot.models import TextSendMessage,ImageSendMessage
# from ディレクトリ名 import ファイル名
from cpslab import CPS_API
import os

# --------------------------------------------------
# configparserの宣言とiniファイルの読み込み
# --------------------------------------------------
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

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
# LINEメッセージ送信
# --------------------------------------------------
def postMessage(message,userID):
    line_bot_api = LineBotApi(LineBotToken)
    messages = TextSendMessage(text=message)
    line_bot_api.push_message(userID, messages=messages)

# --------------------------------------------------
# LINE写真データ送信
# --------------------------------------------------
def postImage(userID):
    line_bot_api = LineBotApi(LineBotToken)
    messages = make_image_messages()
    line_bot_api.push_message(userID, messages=messages)

def make_image_messages():
    messages = ImageSendMessage(
        original_content_url="https://dad41150.ngrok.io/images/banana_240.png", #JPEG 最大画像サイズ：240×240 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
        preview_image_url="https://dad41150.ngrok.io /images/banana_800.png" #JPEG 最大画像サイズ：1024×1024 最大ファイルサイズ：1MB(注意:仕様が変わっていた)
    )
    return messages

# --------------------------------------------------
# main関数
# --------------------------------------------------


# --------------------------------------------------
# main関数
# --------------------------------------------------
if __name__ == "__main__":
    CPS_API.TA_Template()
    # postMessage("TEST","U12c4f3d6dd5cfc3c9ec79975b6a6684d")
    # postImage("U12c4f3d6dd5cfc3c9ec79975b6a6684d")
    # im = Image.open("CPSLabLogo_2019.png")
    #
    # size = 800
    # if im.width > size:
    #     proportion = size / im.width
    #     im = im.resize((int(im.width * proportion), int(im.height * proportion)))
    # im.save("./images/{0}_800.png".format("CPSLabLogo_2019"))
    #
    # size = 240
    # if im.width > size:
    #     proportion = size / im.width
    #     im = im.resize((int(im.width * proportion), int(im.height * proportion)))
    # im.save("./images/{0}_240.png".format("CPSLabLogo_2019"))