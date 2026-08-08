import os
import json
import time
from datetime import datetime, timedelta
import requests

# 项目状态开关 (按用户指令：项目已暂停)
PROJECT_PAUSED = True

# 微信官方接口参数
APP_ID = os.environ.get("WECHAT_APP_ID") or "wxf39166d6f2deab57"
APP_SECRET = os.environ.get("WECHAT_APP_SECRET") or "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = os.environ.get("WECHAT_USER_OPENID") or "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = os.environ.get("WECHAT_TEMPLATE_ID") or "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

CACHE_FILE = "last_pushed_status.json"

CITY_COORDINATES = {}

def push_auto_schedule():
    if PROJECT_PAUSED:
        print("[项目状态] 按照用户要求，川西自驾监控与路书推送项目已全量暂停，保持 100% 静默零推送。")
        return

if __name__ == "__main__":
    push_auto_schedule()
