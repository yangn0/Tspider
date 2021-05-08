import time
import json
import requests

url = "https://oapi.dingtalk.com/robot/send?access_token=dc23ca24723e9637df02daf1886c671f1ee710be92f01e166a0271b0ac76cb77"

def sendText(msg):
    message = {
        "msgtype": "text",
        "text": {
            "content": "爬虫: "+msg
        },
    }
    r = requests.post(url, json=message)
    print(r.text)

if __name__ =="__main__":
    sendText("hello, world")
