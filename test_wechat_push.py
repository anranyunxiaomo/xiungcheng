import os
import json
import requests

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    r = requests.get(token_url).json()
    return r.get("access_token")

def send_luxury_text(token, text_content):
    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "text",
        "text": {
            "content": text_content
        }
    }
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res = requests.post(custom_url, data=json_data, headers=headers).json()
    print("高奢极简设计感文本推送结果:", res)
    return res

def run():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    # 彻底取消图片，采用【高奢极简设计感视觉文本 (Luxury Minimalist Design Layout)】
    luxury_design_text = """✦ 8.1 DAY 1 · 成都 ➔ 康定 ✦
┊ 目的地海拔 2560m · 适宜适应 ┊

◇ 气象与温差
  · 康定市区：14℃ ~ 22℃ (多云体感宜人)
  · 成都市区：22℃ ~ 31℃ (晴间多云)
  · 降雨窗口：预计集中于夜间 19:00 以后

◇ 穿搭与打卡
  · 穿搭灵感：透气长袖内搭 ➕ 随身防风外套
  · 拍照时刻：18:00 康定情歌广场与折多河畔

◇ 路线与能源
  · G4218 雅康高速全线畅通，隧道出口减速防雨
  · 已安排在天全服务区或康定市区补满油箱

◇ 暖心守护
  · 第一晚宿康定极利于高原适应，今晚切勿剧烈运动或洗长热水澡防高反哦
  · 高原紫外线渐强，记得带好遮阳帽、墨镜与防晒霜
  · 随车已准备好保温水杯、便携氧气瓶与高热量零食

💌 祝我们的川西自驾之旅第一天浪漫愉快"""

    send_luxury_text(token, luxury_design_text)

if __name__ == "__main__":
    run()
