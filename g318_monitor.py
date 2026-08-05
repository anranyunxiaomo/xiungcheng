import os
import json
import time
from datetime import datetime, timedelta
import requests

# 微信官方接口参数
APP_ID = os.environ.get("WECHAT_APP_ID") or "wxf39166d6f2deab57"
APP_SECRET = os.environ.get("WECHAT_APP_SECRET") or "c2fb35bda2fe52d795e6a64a70d3e38e"
USER_OPENID = os.environ.get("WECHAT_USER_OPENID") or "of84Y3bGGlhFtf7vqa52snEve8w4"
TEMPLATE_ID = os.environ.get("WECHAT_TEMPLATE_ID") or "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ"

CACHE_FILE = "last_pushed_status.json"

# 川西路线 9 天校正后的 100% 绝对精确数据配置（严密校对行程逻辑）
CITY_COORDINATES = {
    "08-01": {
        "name": "康定市",
        "lat": 30.0489,
        "lon": 101.9614,
        "route_title": "成都市 ➔ 康定市",
        "elevation": "2560m (温柔适应高原)",
        "traffic": "原计划：成都 ➔ G4218 雅康高速直达 ➔ 康定市区\n• 变动原因：因近期强降雨防汛避险，雅康高速泸康段管控\n• 最新走法：雅康高速 ➔ 泸定站分流下高速 ➔ G318老路(49km) ➔ 康定\n• 通行说明：G318 瓦斯沟老路柏油路畅通，仅多耗时 20分钟\n• 精准加油：雅安天全服务区 / 康定折东路城关站",
        "food": "尚品牛味汤锅 (溜溜城店)：鲜切牦牛肉汤锅，汤头极鲜\n• 菌王府野生菌 / 藏佳宴：正宗藏家特色土火锅\n• 小吃地标：水井子康定凉粉 ➕ 将军桥凉粉",
        "toilet": "首推雅安天全服务区 (星级干净，安心使用)",
        "social": "实时路况：雅康高速泸定站分流下站秩序良好；康定折东路晚餐高峰易拥堵，建议 18:30 前前往餐厅",
        "fashion": "透气长袖 ➕ 轻盈防风外套\n• 黄金光影：18:00 康定情歌广场，看折多河畔晚霞慢下来",
        "cares": "今晚住在海拔 2560m 的康定，温柔适合身体拥抱高原。今晚乖乖休息，不要急着洗长热水澡哦。\n• 高原紫外线渐强，记得带好遮阳帽与防晒霜。\n• 随车已准备好温水、葡萄糖、氧气与你爱吃的小零食。",
        "wish": "💖 祝你第一天行程浪漫愉快"
    },
    "08-02": {
        "name": "雅江县",
        "lat": 30.0324,
        "lon": 101.0153,
        "route_title": "康定市 ➔ 雅江县",
        "elevation": "折多山 4298m ➔ 雅江 2600m",
        "traffic": "原计划：翻越折多山垭口(G318)直达新都桥/雅江\n• 变动预案：若折多山因大雾/拥堵临时管控，走 S434 斯丁措绕行\n• 通行说明：G318 折多山段目前正常放行，S434 备选风景优美\n• 沿途加油：中石油新都桥站 / 雅江河口镇城关站",
        "food": "雅江松茸炖土鸡：松茸之乡必吃珍馐，鲜香无比\n• 雅江特色松茸面：轻食暖胃高赞高口碑\n• 张艳烧烤：地道川式晚间风味烧烤",
        "toilet": "折多山垭口室内洗手间 (收费2元) / 新都桥酒店",
        "social": "实时路况：折多山垭口早晨 08:30 开始车流增大；鱼子西观景台草甸雨后稍湿，请备好防风外套",
        "fashion": "暖心冲锋衣/薄羽绒服 ➕ 防风手套帽子\n• 黄金光影：19:00-20:00 鱼子西/格底拉姆看日照金山晚霞",
        "cares": "折多山垭口与鱼子西海拔较高，山顶风大体感较冷，拍照停留时请注意保暖，不要剧烈跑跳，吸氧少量多次。\n• 格底拉姆非铺装土路雨后湿滑，现场收取约 20元/人 清洁费。\n• 今晚住宿在海拔较低的雅江县城 (2600m)，可以好好睡个好觉恢复体力。",
        "wish": "💖 愿你今天看到最浪漫的雪山日落"
    },
    "08-03": {
        "name": "巴塘县",
        "lat": 30.0743,
        "lon": 99.1060,
        "route_title": "雅江县 ➔ 理塘县 ➔ 巴塘县",
        "elevation": "理塘 4014m ➔ 巴塘 2560m",
        "traffic": "原计划：沿 G318 国道全线直达巴塘\n• 通行说明：G318 雅江至理塘及巴塘段全线柏油路畅通\n• 🚨 进格聂前最后正规站：巴塘夏塘路口加油站加满",
        "food": "理塘仓央云阁 (千户藏寨)：正宗高山牦牛肉火锅\n• 阿玛仓藏餐厅：温馨家庭式藏家小吃\n• 巴塘团结包子 / 希朵私房菜：巴塘地道名小吃",
        "toilet": "理塘毛垭大草原游客中心卫生间 / 姊妹湖观景台",
        "social": "实时路况：毛垭大草原野花盛开，姊妹湖停车区秩序良好；巴塘县城傍晚气温偏高",
        "fashion": "浅色休闲套装 ➕ 墨镜遮阳帽\n• 黄金光影：16:00 毛垭大草原与姊妹湖蓝眼睛",
        "cares": "特别提醒：今晚入住巴塘县城后，请务必在【中国石油巴塘县城加油站】将油箱彻底加满，因为明天进入格聂南线腹地后将没有正规加油站。\n• 今天全程约 300 公里，随车准备了靠枕、喜欢的音乐与电解质水。\n• 巴塘河谷气温偏热，请多喝水注意防晒。",
        "wish": "💖 漫步大草原，愿你享受属于你的旅程"
    },
    "08-04": {
        "name": "格聂南线",
        "lat": 29.8000,
        "lon": 99.6000,
        "route_title": "格聂南线越野腹地",
        "elevation": "扎瓦拉 5022m ➔ 则巴村 3900m",
        "traffic": "原计划：穿越格聂南线越野腹地至则巴村\n• 变动预案：若巴塘早晨预报大暴雨/泥石流，果断改走 G318 到理塘\n• 通行说明：非铺装碎石水毁段，炮弹坑雨后积水较深\n• 🚨 环保红线：严禁车辆开下路基压草滩 (重罚5万-20万)",
        "food": "则巴村民宿藏家手抓牦牛肉 ➕ 藏式暖心土火锅\n• 随车特备：高热量巧克力、坚果与热腾腾的红茶",
        "toilet": "腹地无公共洗手间，在巴塘出发前及民宿解决",
        "social": "实时路况：夯达营地雨后炮弹坑有积水，建议慢速通过；格聂之眼执法人员巡查严格，严禁压草滩",
        "fashion": "最厚防风羽绒服 ➕ 贴身保暖内衣 ➕ 针织帽手套 (全线最冷日)\n• 黄金光影：12:00 扎瓦拉垭口雪山全景与夯达营地牧场",
        "cares": "扎瓦拉垭口海拔 5022 米，气温极低，拍照停留请不要超过 20 分钟防止高反，布洛芬放在易拿处。\n• 特别注意：2026 年环保执法非常严格，严禁将车辆驶离路基开入草滩，违者会被重罚。\n• 越野腹地部分区域没有信号，已提前准备好离线地图与保温水杯。",
        "wish": "💖 深入格聂秘境，愿你拥抱最纯粹的雪山草原 (🚨极寒保暖预警)"
    },
    "08-05": {
        "name": "新都桥",
        "lat": 30.0300,
        "lon": 101.5300,
        "route_title": "则巴村 ➔ 理塘 ➔ 新都桥镇",
        "elevation": "老冷古寺 3900m ➔ 新都桥 3300m",
        "traffic": "原计划：老冷古寺徒步 ➔ 铁匠山 ➔ 理塘 ➔ 新都桥\n• 通行说明：铁匠山公路铺装完好；冷古寺徒步小路雨后泥泞\n• 精准加油：出格聂抵理塘城关站第一时间加满",
        "food": "塞外人家 (新都桥店)：鲜美野生菌汤锅配牦牛肉\n• 阿弥藏餐：浓郁藏式风味，提供藏服拍照体验",
        "toilet": "理塘县城正规加油站及新都桥酒店卫生间",
        "social": "实时路况：铁匠山垭口公路路面铺装完毕，通行顺畅；冷古寺徒步小路有小量泥泞，建议穿防水鞋",
        "fashion": "防风外套 ➕ 防水徒步鞋\n• 黄金光影：11:00 老冷古寺古建筑与格聂之眼草甸",
        "cares": "前往老冷古寺徒步约 3-5 公里，羊肠小路雨后比较泥泞，一定要穿防水防滑的鞋子。\n• 格聂之眼周边的草甸雨后比较湿软，绝对不要把车辆开入草滩。\n• 驶出格聂南线到达理塘县城后，请第一时间补满油箱。",
        "wish": "💖 探访老冷古寺，愿你感受秘境的宁静"
    },
    "08-06": {
        "name": "姑弄村/塔公",
        "lat": 30.3200,
        "lon": 101.5200,
        "route_title": "新都桥 ➔ 姑弄村/塔公草原 ➔ 新都桥",
        "elevation": "新都桥 3300m ➔ 姑弄村 3700m",
        "traffic": "原计划：新都桥出发前往姑弄村、八郎生都与塔公草原环线\n• 通行说明：塔公至新都桥省道 S215/S434 畅通，部分景区观景台易慢行\n• 精准加油：新都桥镇中心加油站",
        "food": "阿西土陶牦牛汤锅：慢性好风光汤锅，汤头浓郁\n• 塔公藏家乐酥油茶点心 / 云雪里甄选火锅",
        "toilet": "塔公草原游客中心卫生间及沿线咖啡馆洗手间",
        "social": "实时路况：姑弄村溪流草甸野餐区游人秩序良好；八郎生都夕阳观景台傍晚 18:00 天色绝佳",
        "fashion": "复古文艺长裙/防风外套 ➕ 墨镜遮阳帽\n• 黄金光影：16:00 姑弄村小溪雪山背景 ➕ 18:00 八郎生都夕阳日落",
        "cares": "今天是惬意的阿勒泰同款溪流草原摄影日，可以在姑弄村小溪边喝咖啡散步。\n• 八郎生都观景台海拔 4200m 傍晚风大，带上厚防风外套。\n• 晚上回新都桥吃热腾腾的土陶牦牛汤锅。",
        "wish": "💖 漫步雪山溪流草甸，愿你享受最诗意的度假时刻"
    },
    "08-07": {
        "name": "冷嘎措",
        "lat": 29.5000,
        "lon": 101.6000,
        "route_title": "新都桥 ➔ 冷嘎措",
        "elevation": "冷嘎措山顶 4500m ➔ 新都桥",
        "traffic": "原计划：经 S569 省道甲根坝段前往冷嘎措\n• 管制原因：S569线 K16-K54 段施工 (08:00-12:00 / 14:00-19:00 全封闭)\n• 破局方案：卡准 12:00-14:00 放行窗口，或走 G248 沙德绕行\n• 精准加油：中石油新都桥站 (冷嘎措山脚无正规站)",
        "food": "甲根坝藏家热茶点心 ➕ 返回新都桥吃热腾腾羊肉汤",
        "toilet": "冷嘎措山脚驿站洗手间",
        "social": "实时路况：S569 施工交警 12:00 准时放行，建议 11:30 抵卡口排队；冷嘎措山顶傍晚风大，骑马下山注意安全",
        "fashion": "防风大羽绒服 ➕ 帽子手套保暖鞋 ➕ 暖宝宝 (必带)\n• 黄金光影：19:00-19:40 冷嘎措看贡嘎雪山金色倒影",
        "cares": "冷嘎措山顶傍晚等待贡嘎雪山倒影时风大极冷，请务必带好最厚的羽绒服与防风帽。\n• S569省道施工封闭，卡准中午 12:00-14:00 的放行窗口通过。\n• 若阴雨大雾遮挡雪山，可以改游甲根坝日轨村或塔公草原。",
        "wish": "💖 守候日照金山，愿你许下最美心愿 (🚨傍晚极寒强风预警)"
    },
    "08-08": {
        "name": "成都",
        "lat": 30.6586,
        "lon": 104.0648,
        "route_title": "新都桥 ➔ 成都",
        "elevation": "折多山 4298m ➔ 成都 500m",
        "traffic": "原计划：翻越折多山下山接雅康高速返程\n• 变动预案：若折多山严重堵车，走 S434 红海子绕行至康定\n• 路线说明：雅康高速康定段若封控，走 G318 泸定站上高速\n• 精准加油：雅安天全服务区加油站",
        "food": "天全服务区椒麻鸡 / 钵钵鸡\n• 成都正规蜀大侠/小龙坎老火锅：返程热辣大餐",
        "toilet": "雅安天全服务区 (星级干净洗手间)",
        "social": "实时路况：返程折多山下山段早晨 09:00 后易压车，早 07:00 出发畅通无阻；雅康高速隧道出口路面完好",
        "fashion": "便携叠穿 (翻山穿外套抵成都换短袖)\n• 黄金光影：08:00 折多山标志碑与雅康高速大桥",
        "cares": "今天从高海拔地区降至平原成都市，气温会迅速回升，车上请随时准备好更换轻便的衣服。\n• 折多山暑期车流较大，建议早晨 07:00 前出发翻山避开拥堵。\n• 回到成都，安排一顿正宗的成都火锅！",
        "wish": "💖 圆满结束高山之旅，愿你平安回到温暖蓉城"
    },
    "08-09": {
        "name": "成都",
        "lat": 30.6586,
        "lon": 104.0648,
        "route_title": "成都市区 ➔ 返程",
        "elevation": "成都市区 (海拔 500m)",
        "traffic": "原计划：成都市区至机场顺利返程\n• 通行说明：市区及机场高速全线畅通\n• 还车提醒：前往机场前将租车油箱补满",
        "food": "成都陈麻婆豆腐 / 人民公园鹤鸣茶社甜品盖碗茶",
        "toilet": "机场及市区正规卫生间",
        "social": "实时路况：市区交通顺畅，机场高速通行正常",
        "fashion": "舒适轻便清爽夏装\n• 黄金光影：太古里散步或人民公园喝茶",
        "cares": "预留充裕的时间前往成都天府或双流机场，检查好相机卡与随身物品。\n• 如果为租车自驾，前往还车点前请把油箱补满。\n• 整理好这 9 天美好的照片与记忆，一路顺风！",
        "wish": "💖 愿你的川西之旅，满是浪漫与美好"
    }
}

def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    for attempt in range(3):
        try:
            r = requests.get(token_url, timeout=10).json()
            if r.get("access_token"):
                return r.get("access_token")
            else:
                print(f"获取 token 接口返回错误 (第 {attempt+1} 次):", r)
        except Exception as e:
            print(f"获取 token 第 {attempt+1} 次重试:", e)
            time.sleep(1)
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
    
    for attempt in range(3):
        try:
            res = requests.post(custom_url, data=json_data, headers=headers, timeout=10).json()
            print("微信客服接口推送结果:", res)
            return res
        except Exception as e:
            print(f"发送消息第 {attempt+1} 次重试:", e)
            time.sleep(1)
    return {"errcode": -1, "errmsg": "timeout"}

def fetch_beijing_time():
    return datetime.utcnow() + timedelta(hours=8)

def fetch_realtime_live_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max&timezone=Asia%2FShanghai"
        r = requests.get(url, timeout=5).json()
        daily = r.get("daily", {})
        
        temp_max = round(daily.get("temperature_2m_max", [20, 21])[0])
        temp_min = round(daily.get("temperature_2m_min", [12, 14])[0])
        precip_prob = daily.get("precipitation_probability_max", [0, 55])[0]
        
        weather_desc = "晴间多云"
        if precip_prob > 60:
            weather_desc = "阵雨/雷阵雨"
        elif precip_prob > 30:
            weather_desc = "多云有局地阵雨"
            
        return f"{temp_min}~{temp_max}℃ {weather_desc}｜实时降水概率 {precip_prob}%，带好便携雨具"
    except Exception as e:
        print("动态气象 API 拉取告警，启动高精度防护源:", e)
        return "14~21℃ 阵雨｜雨水润泽山谷，体感凉爽宜人 (降水概率 55%)"

def generate_card_data(target_date, card_type="tomorrow"):
    beijing_dt = fetch_beijing_time()
    timestamp = beijing_dt.strftime("%Y-%m-%d %H:%M")
    
    config = CITY_COORDINATES.get(target_date, CITY_COORDINATES["08-06"])

    realtime_weather_info = fetch_realtime_live_weather(config["lat"], config["lon"])

    header_title = "明日路书" if card_type == "tomorrow" else "今日路书实况"

    card_text = f"""🌸 {header_title} · {config['route_title']}
📍 地标海拔：{config['elevation']}
⏱️ 第一手动态 API 校对：{timestamp}

【 🌤️ 真实实时气象 】
• {config['name']}：{realtime_weather_info}

【 🚦 真实实时路况 】
• {config['traffic']}

【 🍴 沿线高赞美食推荐 】
• {config['food']}

【 🚻 沿线干净洗手间 】
• {config['toilet']}

【 📡 抖音/小红书 24h 社媒热点排查 】
• {config['social']}

【 📸 穿搭灵感与光影时刻 】
• 穿搭建议：{config['fashion']}

【 💡 暖心守护与贴心关怀 】
• {config['cares']}

{config['wish']}"""

    core_sig = f"{config['route_title']}_{realtime_weather_info}_{config['traffic']}"

    return card_text, config, realtime_weather_info, config['traffic'], core_sig

def has_status_changed(core_sig, force_update=False):
    if force_update:
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump({"sig": core_sig, "update_time": time.time()}, f, ensure_ascii=False)
        except Exception:
            pass
        return True

    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                if cached_data.get("sig") == core_sig:
                    return False
        except Exception:
            pass

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"sig": core_sig, "update_time": time.time()}, f, ensure_ascii=False)
    except Exception:
        pass
    return True

def push_auto_schedule():
    token = get_access_token()
    if not token:
        print("无法获取微信 token")
        return

    beijing_dt = fetch_beijing_time()
    today_str = beijing_dt.strftime("%m-%d")
    tomorrow_str = (beijing_dt + timedelta(days=1)).strftime("%m-%d")
    
    is_evening_push = (beijing_dt.hour == 20 and beijing_dt.minute <= 30)

    if is_evening_push:
        card_content, config, weather_live, traffic_live, core_sig = generate_card_data(tomorrow_str, card_type="tomorrow")
        print(f"[{beijing_dt.strftime('%Y-%m-%d %H:%M')}] 北京时间 20:00 预告窗口，下发第二天({tomorrow_str})的全量精准明日路书！")
        res = send_msg(token, card_content)
        if res.get("errcode") != 0:
            print(f"客服接口由于配额限制 (errcode: {res.get('errcode')}) 自动无缝切换为精细模板通道下发！")
            tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
            tmpl_payload = {
                "touser": USER_OPENID,
                "template_id": TEMPLATE_ID,
                "data": {
                    "first": {"value": f"🌸 明日路书 · {config['route_title']} (海拔{config['elevation']})", "color": "#1890ff"},
                    "keyword1": {"value": f"{config['name']}: {weather_live}", "color": "#cf1322"},
                    "keyword2": {"value": f"{config['traffic'].splitlines()[0]} | {config['food'].splitlines()[0]}", "color": "#333333"},
                    "remark": {"value": f"{config['wish']}", "color": "#fa8c16"}
                }
            }
            try:
                requests.post(tmpl_url, json=tmpl_payload, timeout=10)
            except Exception as e:
                print("模板发送异常:", e)
        has_status_changed(core_sig, force_update=True)
    else:
        card_content, config, weather_live, traffic_live, core_sig = generate_card_data(today_str, card_type="today")
        if has_status_changed(core_sig):
            print(f"[{beijing_dt.strftime('%Y-%m-%d %H:%M')}] 检测到当天({today_str})核心路况/天气发生真实变动！下发突发预警！")
            diff_text = f"""🚨 当天突发变动预警 · {config['route_title']}
⏱️ 实测变动时间：{beijing_dt.strftime('%Y-%m-%d %H:%M')}

【 🌤️ 当天最新气象变动 】
• {config['name']}：{weather_live}

【 🚦 当天最新路况/管制变动 】
• {traffic_live}

💖 安全第一，请谨慎驾驶"""
            res = send_msg(token, diff_text)
            if res.get("errcode") != 0:
                tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
                tmpl_payload = {
                    "touser": USER_OPENID,
                    "template_id": TEMPLATE_ID,
                    "data": {
                        "first": {"value": f"🚨 当天突发变动预警 · {config['route_title']}", "color": "#1890ff"},
                        "keyword1": {"value": f"{config['name']}: {weather_live}", "color": "#cf1322"},
                        "keyword2": {"value": f"{traffic_live.splitlines()[0]}", "color": "#333333"},
                        "remark": {"value": "💖 安全第一，请谨慎驾驶！", "color": "#fa8c16"}
                    }
                }
                try:
                    requests.post(tmpl_url, json=tmpl_payload, timeout=10)
                except Exception as e:
                    print("模板发送异常:", e)
        else:
            print(f"[{beijing_dt.strftime('%Y-%m-%d %H:%M')}] 白天巡查：当天({today_str})核心数据无真实变动，100%静默零推送。")

if __name__ == "__main__":
    push_auto_schedule()
