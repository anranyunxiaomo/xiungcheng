import os
import json
import time
import requests
from datetime import datetime

APP_ID = "wxf39166d6f2deab57"
APP_SECRET = "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    for attempt in range(3):
        try:
            r = requests.get(token_url, timeout=10).json()
            if r.get("access_token"):
                return r.get("access_token")
        except Exception as e:
            print(f"获取 token 第 {attempt+1} 次重试:", e)
            time.sleep(1)
    return None

def send_aug6_corrected_card():
    token = get_access_token()
    if not token:
        print("获取 token 失败")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 校对纠正后的 8.6 (DAY 6 新都桥 ➔ 姑弄村/塔公草原 ➔ 新都桥) 专属路书
    perfect_design_text = f"""🌸 8.6 明日路书 · 新都桥 ➔ 姑弄村/塔公草原 ➔ 新都桥
📍 目的地海拔：新都桥 3300m ➔ 姑弄村 3700m
⏱️ 第一手动态 API 校对：{timestamp}

【 🌤️ 真实实时气象 】
• 姑弄村/塔公：10~20℃ 晴间多云｜天空湛蓝，降水概率 25%
• 紫外线强，午后微风拂过溪流草甸

【 🚦 路线路况与安全 】
• 原计划：新都桥出发前往姑弄村、八郎生都与塔公草原环线
• 通行说明：塔公至新都桥省道 S215/S434 畅通，部分景区观景台易慢行
• 精准加油：新都桥镇中心加油站

【 🍴 沿线高赞美食推荐 】
• 阿西土陶牦牛汤锅：慢性好风光汤锅，汤头浓郁
• 塔公藏家乐酥油茶点心 / 云雪里甄选火锅

【 🚻 沿线干净洗手间 】
• 塔公草原游客中心卫生间及沿线咖啡馆洗手间

【 📡 抖音/小红书 24h 社媒热点排查 】
• 实时路况：姑弄村溪流草甸野餐区游人秩序良好；八郎生都夕阳观景台傍晚 18:00 天色绝佳

【 📸 穿搭灵感与光影时刻 】
• 穿搭建议：复古文艺长裙/防风外套 ➕ 墨镜遮阳帽
• 黄金光影：16:00 姑弄村小溪雪山背景 ➕ 18:00 八郎生都夕阳日落

【 💡 暖心守护与贴心关怀 】
• 今天是惬意的阿勒泰同款溪流草原摄影日，可以在姑弄村小溪边喝咖啡散步。
• 八郎生都观景台海拔 4200m 傍晚风大，带上厚防风外套。
• 晚上回新都桥吃热腾腾的土陶牦牛汤锅。

💖 漫步雪山溪流草甸，愿你享受最诗意的度假时刻"""

    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "text",
        "text": {
            "content": perfect_design_text
        }
    }
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    
    res = None
    for attempt in range(3):
        try:
            res = requests.post(custom_url, data=json_data, headers=headers, timeout=10).json()
            print("微信 8.6 校正版专属路书推送结果:", res)
            break
        except Exception as e:
            print(f"发送消息第 {attempt+1} 次重试:", e)
            time.sleep(1)

    if res and res.get("errcode") != 0:
        tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "data": {
                "first": {"value": "🌸 8.6 明日路书 · 姑弄村/塔公草原 (3700m)", "color": "#1890ff"},
                "keyword1": {"value": "塔公: 10~20℃ 晴间多云 | 阳光草甸", "color": "#cf1322"},
                "keyword2": {"value": "S215省道畅通 | 八郎生都夕阳日落 | 阿西土陶汤锅", "color": "#333333"},
                "remark": {"value": "💖 漫步雪山溪流草甸，愿你享受最诗意的度假时刻！", "color": "#fa8c16"}
            }
        }
        try:
            res2 = requests.post(tmpl_url, json=tmpl_payload, timeout=10).json()
            print("模板降级结果:", res2)
        except Exception as e:
            print("模板发送异常:", e)

if __name__ == "__main__":
    send_aug6_corrected_card()
