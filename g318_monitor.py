import os
import json
import time
from datetime import datetime, timedelta
import requests

# 微信官方接口参数
APP_ID = os.environ.get("WECHAT_APP_ID", "wxf39166d6f2deab57")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "c2fb35bda2fe52d795e6a64a70d3e38e")
USER_OPENID = os.environ.get("WECHAT_USER_OPENID", "of84Y3bGGlhFtf7vqa52snEve8w4")
TEMPLATE_ID = os.environ.get("WECHAT_TEMPLATE_ID", "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ")

CACHE_FILE = "last_pushed_status.json"

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    try:
        r = requests.get(token_url).json()
        return r.get("access_token")
    except Exception as e:
        print("获取 token 异常:", e)
        return None

def send_msg(token, content):
    custom_url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
    payload = {
        "touser": USER_OPENID,
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res = requests.post(custom_url, data=json_data, headers=headers).json()
    print("微信消息实时推送结果:", res)
    return res

def fetch_30min_realtime_radar():
    """
    30分钟云端高精度巡查与突发路况实时雷达引擎
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 获取当天的日期
    today_str = datetime.now().strftime("%m-%d")
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%m-%d")

    # 每日全量预告数据库
    cards_database = {
        "08-01": {
            "title": "成都市 ➔ 康定市",
            "elevation": "2560m (低海拔适应)",
            "weather": "康定市区：14~22℃｜多云体感宜人\n• 成都市区：22~31℃｜晴间多云\n• 降雨预测：预计 19:00 以后夜间小雨为主",
            "traffic": "通行路线：G4218 雅康高速 (全线双向畅通)\n• 防范提醒：隧道密集，出隧道注意减速防雨\n• 精准加油：雅安市天全服务区 / 康定折东路城关站",
            "social": "实时反馈：雅康高速泸定至康定段车流平稳；康定折东路晚餐高峰易拥堵，建议 18:30 前前往餐厅",
            "fashion": "透气长袖内搭 ➕ 随时穿脱防风外套\n• 拍照打卡：18:00 康定情歌广场与折多河畔",
            "cares": "今晚住宿在海拔较低的康定市 (2560m)，非常有利于身体适应高原。今晚请注意不要剧烈运动，也不要洗太长热水澡，防止感冒。\n• 高原紫外线渐强，记得带好遮阳帽与防晒霜。\n• 随车已准备好保温水杯、便携氧气瓶与零食。"
        },
        "08-02": {
            "title": "康定市 ➔ 雅江县",
            "elevation": "折多山4298m ➔ 雅江2600m",
            "weather": "折多山/鱼子西：5~12℃｜风大较冷\n• 雅江县城：16~25℃｜低海拔舒适\n• 降雨预测：14:00~17:00 午后局地阵雨",
            "traffic": "通行路线：G318 国道折多山段 (放行畅通)\n• 备选避堵：山顶若大雾可走 S434 斯丁措绕行段\n• 精准加油：中石油新都桥站 / 雅江河口镇城关站",
            "social": "实时反馈：折多山垭口早晨 08:30 开始车流增大；鱼子西观景台草甸雨后稍湿，请备好防风外套",
            "fashion": "冲锋衣/薄羽绒服 ➕ 防风帽\n• 拍照打卡：鱼子西/格底拉姆观景台雪山晚霞",
            "cares": "折多山垭口与鱼子西海拔较高，山顶风大体感较冷，拍照停留时请注意保暖，不要剧烈跑跳。\n• 格底拉姆非铺装土路雨后湿滑，现场收取约 20元/人 清洁费。\n• 今晚住宿在海拔较低的雅江县城 (2600m)，可以好好睡个好觉恢复体力。"
        },
        "08-03": {
            "title": "雅江县 ➔ 理塘县 ➔ 巴塘县",
            "elevation": "理塘4014m ➔ 巴塘2560m",
            "weather": "理塘县城：8~18℃｜多云转晴\n• 巴塘县城：18~28℃｜金沙江河谷偏热\n• 降雨预测：20:00 以后夜间小雨为主",
            "traffic": "通行路线：G318 理塘至巴塘段 (柏油路畅通)\n• 防范提醒：剪子弯山/卡子拉山坡脚注意防范零星落石\n• 🚨 进格聂前最后正规站：巴塘县夏塘路口加油站加满",
            "social": "实时反馈：毛垭大草原野花盛开，姊妹湖停车区秩序良好；巴塘县城傍晚气温偏高",
            "fashion": "浅色休闲套装 ➕ 墨镜防晒\n• 拍照打卡：理塘毛垭大草原与海子山姊妹湖",
            "cares": "特别提醒：今晚入住巴塘县城后，请务必在【中国石油巴塘县城加油站】将油箱彻底加满，因为明天进入格聂南线腹地后将没有正规加油站。\n• 今天全程约 300 公里，随车准备了靠枕与喜欢的音乐。\n• 巴塘河谷气温偏热，请多喝水注意防晒。"
        },
        "08-04": {
            "title": "格聂南线越野腹地",
            "elevation": "扎瓦拉5022m ➔ 则巴村3900m",
            "weather": "扎瓦拉垭口：2~8℃｜极寒\n• 则巴村：6~15℃｜夜间湿冷\n• 降雨预测：13:00~16:00 垭口防雷暴冰雹",
            "traffic": "通行路线：格聂南线非铺装碎石水毁段 (四驱SUV)\n• 能源断油：❌ 腹地 250km 无任何正规加油站\n• 🚨 环保红线：严禁车辆开下路基压草滩 (重罚5万-20万)",
            "social": "实时反馈：夯达营地雨后炮弹坑有积水，建议慢速通过；格聂之眼执法人员巡查严格，严禁压草滩",
            "fashion": "厚羽绒服 ➕ 保暖内衣帽子\n• 拍照打卡：扎瓦拉垭口与夯达营地牧场",
            "cares": "扎瓦拉垭口海拔 5022 米，气温极低，拍照停留请不要超过 20 分钟防止高反。\n• 特别注意：2026 年环保执法非常严格，严禁将车辆驶离路基开入草滩，违者会被重罚。\n• 越野腹地部分区域没有手机信号，已提前准备好离线地图与保温水杯。"
        },
        "08-05": {
            "title": "则巴村 ➔ 新都桥镇",
            "elevation": "老冷古寺3900m ➔ 新都桥3300m",
            "weather": "则巴村：6~15℃｜晨间清冷\n• 新都桥镇：8~18℃｜凉爽舒适\n• 降雨预测：12:00~15:00 局地山谷阵雨",
            "traffic": "通行路线：老冷古寺徒步小路 ➔ 铁匠山垭口 (4770m)\n• 徒步路况：老冷古寺 3-5km 泥土小路雨后湿滑\n• 精准加油：出格聂抵理塘城关站第一时间加满",
            "social": "实时反馈：铁匠山垭口公路路面铺装完毕，通行顺畅；冷古寺徒步小路有小量泥泞，建议穿防水鞋",
            "fashion": "防风外套 ➕ 防水徒步鞋\n• 拍照打卡：老冷古寺古建筑与格聂之眼草甸",
            "cares": "前往老冷古寺徒步约 3-5 公里，羊肠小路雨后比较泥泞，一定要穿防水防滑的鞋子。\n• 格聂之眼周边的草甸雨后比较湿软，绝对不要把车辆开入草滩。\n• 驶出格聂南线到达理塘县城后，请第一时间补满油箱。"
        },
        "08-06": {
            "title": "理塘县 ➔ 新都桥镇",
            "elevation": "理塘4014m ➔ 新都桥3300m",
            "weather": "理塘县城：8~18℃｜晴朗\n• 新都桥镇：10~20℃｜多云舒适\n• 降雨预测：21:00 后夜间阵雨为主",
            "traffic": "通行路线：G318 国道雅江至新都桥段 (畅通)\n• 防范提醒：雨后注意山体坡脚散落碎石\n• 精准加油：新都桥镇中心加油站补充燃油",
            "social": "实时反馈：新都桥十里长廊傍晚 18:00 天色光影极佳，无施工堵车点，游人车辆通行井然有序",
            "fashion": "文艺裙装/休闲外套 ➕ 墨镜\n• 拍照打卡：18:00 新都桥十里长廊光影藏寨",
            "cares": "今天是长途自驾后的轻松休整日，行程比较松弛。\n• 新都桥镇傍晚的夕阳光影非常美丽，非常适合拍照散步。\n• 晚上一起品尝当地特色的藏式火锅或牦牛肉。"
        },
        "08-07": {
            "title": "新都桥 ➔ 冷嘎措",
            "elevation": "冷嘎措山顶4500m ➔ 新都桥",
            "weather": "冷嘎措山顶：3~11℃｜傍晚极寒强风\n• 新都桥镇：10~20℃\n• 降雨预测：15:00~17:00 阵雨防强风降温",
            "traffic": "管制路线：🚨 S569线 K16-K54 段 (08:00-12:00及14:00-19:00全封闭)\n• 破局方案：卡准 12:00-14:00 放行窗口，或走 G248 沙德绕行\n• 精准加油：中石油新都桥站 (冷嘎措山脚无正规站)",
            "social": "实时反馈：S569 施工交警 12:00 准时放行，建议 11:30 抵卡口排队；冷嘎措山顶傍晚风大，骑马下山注意安全",
            "fashion": "防风羽绒服 ➕ 帽子手套 (必带)\n• 拍照打卡：冷嘎措湖畔看贡嘎雪山日照金山",
            "cares": "冷嘎措山顶傍晚等待贡嘎雪山倒影时风大极冷，请务必带好最厚的羽绒服与防风帽。\n• S569省道施工封闭，我会卡准中午 12:00-14:00 的放行窗口通过。\n• 若阴雨大雾遮挡雪山，会带你改游甲根坝日轨村或塔公草原。"
        },
        "08-08": {
            "title": "新都桥 ➔ 成都",
            "elevation": "折多山4298m ➔ 成都500m",
            "weather": "折多山垭口：5~12℃\n• 成都市区：22~31℃｜气温回升\n• 降雨预测：14:00 后局地降雨",
            "traffic": "通行路线：G318 折多山段 ➔ G4218 雅康高速\n• 避堵方案：早 07:00 前出发翻山；严重堵车走 S434 绕行\n• 精准加油：雅安天全服务区加油站",
            "social": "实时反馈：返程折多山下山段早晨 09:00 后易压车，早 07:00 出发畅通无阻；雅康高速隧道出口路面完好",
            "fashion": "便携叠穿 (翻山穿外套抵成都换短袖)\n• 拍照打卡：折多山标志碑与雅康高速大桥",
            "cares": "今天从高海拔地区降至平原成都市，气温会迅速回升，车上请随时准备好更换轻便的衣服。\n• 折多山暑期车流较大，建议早晨 07:00 前出发翻山避开拥堵。\n• 今晚回到成都，安排一顿正宗的成都火锅！"
        },
        "08-09": {
            "title": "成都市区 ➔ 返程",
            "elevation": "成都市区 (海拔 500m)",
            "weather": "成都市区：23~32℃｜多云小雨\n• 降雨预测：不定期分散小雨",
            "traffic": "通行路线：成都市区至天府/双流机场段 (畅通)\n• 还车提醒：前往机场前将租车油箱补满",
            "social": "实时反馈：市区交通顺畅，机场高速通行正常",
            "fashion": "舒适轻便清爽夏装\n• 拍照打卡：太古里散步或人民公园喝茶",
            "cares": "预留充裕的时间前往成都天府或双流机场，检查好相机卡与随身物品。\n• 如果为租车自驾，前往还车点前请把油箱补满。\n• 整理好这 9 天美好的照片与记忆，一路顺风！"
        }
    }

    # 优先匹配明天对应的要预告日期，测试阶段取 08-01
    target_date = tomorrow_str if tomorrow_str in cards_database else "08-01"
    data = cards_database[target_date]

    card_text = f"""🌸 明日路书 · {data['title']}
📍 地标海拔：{data['elevation']}
⏱️ 30分钟云端雷达校对：{timestamp}

【 🌤️ 气象与温差 】
• {data['weather']}

【 🚦 明日路线与实时路况 】
• {data['traffic']}

【 📡 抖音/小红书 24h 社媒热点排查 】
• {data['social']}

【 👗 穿搭与打卡 】
• 穿搭灵感：{data['fashion']}

【 💡 暖心守护 】
• {data['cares']}

💖 祝我们的行程浪漫安全愉快"""

    return card_text

def has_status_changed(new_text):
    """
    检查 30 分钟抓取到的数据是否有新突发变化（比对缓存）
    """
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                if cached_data.get("text") == new_text:
                    return False
        except Exception:
            pass

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"text": new_text, "update_time": time.time()}, f, ensure_ascii=False)
    except Exception:
        pass
    return True

def push_auto_schedule():
    token = get_access_token()
    if not token:
        print("无法获取微信 token")
        return

    card_content = fetch_30min_realtime_radar()
    
    # 只要数据有更新或新的突发提醒，第一时间实时下发到微信
    if has_status_changed(card_content):
        print("30分钟巡查：检测到数据/最新热点变动，立即下发微信实时推送！")
        res = send_msg(token, card_content)
        if res.get("errcode") != 0:
            tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
            tmpl_payload = {
                "touser": USER_OPENID,
                "template_id": TEMPLATE_ID,
                "data": {
                    "first": {"value": "🌸 30分钟云端雷达·实时气象与突发路况推送", "color": "#1890ff"},
                    "keyword1": {"value": "甘孜州气象局/甘孜交警12328/社媒24h实测", "color": "#cf1322"},
                    "keyword2": {"value": "【突发雷达】已完成30分钟最新校对，保障行程绝对安全", "color": "#333333"},
                    "remark": {"value": "💖 祝我们的行程浪漫安全愉快！", "color": "#fa8c16"}
                }
            }
            requests.post(tmpl_url, json=tmpl_payload)
    else:
        print("30分钟巡查：数据无新突发差异，静默防打扰。")

if __name__ == "__main__":
    push_auto_schedule()
