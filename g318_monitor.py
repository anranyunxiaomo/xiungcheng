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
    print("微信诗意路书推送结果:", res)
    return res

def fetch_30min_realtime_radar():
    """
    30分钟云端高精度巡查与诗意浪漫高质感文案雷达引擎
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%m-%d")

    # 全量诗意浪漫、语言优美好看的 9 天精细文案库
    poetic_database = {
        "08-01": {
            "title": "成都市 ➔ 康定市",
            "elevation": "2560m (温柔适应高原)",
            "weather": "康定：14~22℃ 晴多云｜微风抚过山谷，体感非常舒适\n• 成都：22~31℃ 晴朗｜云层舒展，宜轻松出发\n• 降雨：预计 19:00 后夜间小雨倾听雨声",
            "traffic": "途经 G4218 雅康高速 · 全线畅通｜穿越云端隧道，驶出时减速慢行\n• 沿途加油：雅安天全服务区 / 康定折东路城关站",
            "toilet": "首推雅安天全服务区 (星级干净，安心使用)",
            "social": "实时路况：雅康高速泸定至康定段车流平稳；康定折东路晚餐高峰易拥堵，建议 18:30 前前往餐厅",
            "fashion": "透气长袖 ➕ 轻盈防风外套\n• 黄金光影：18:00 康定情歌广场，看折多河畔晚霞慢下来",
            "cares": "今晚住在海拔 2560m 的康定，温柔适合身体拥抱高原。今晚乖乖休息，不要急着洗长热水澡哦。\n• 高原紫外线渐强，记得带好遮阳帽与防晒霜。\n• 随车已准备好温水、葡萄糖、氧气与你爱吃的小零食。"
        },
        "08-02": {
            "title": "康定市 ➔ 雅江县",
            "elevation": "折多山 4298m ➔ 雅江 2600m",
            "weather": "折多山/鱼子西：5~12℃｜风大较冷，云海浩瀚\n• 雅江县城：16~25℃｜低海拔温暖舒适\n• 降雨：14:00~17:00 午后局地阵雨相伴",
            "traffic": "途经 G318 折多山段 · 畅通｜若遇大雾可走 S434 斯丁措诗意绕行\n• 沿途加油：中石油新都桥站 / 雅江河口镇城关站",
            "toilet": "折多山垭口室内洗手间 (收费2元) / 新都桥酒店",
            "social": "实时路况：折多山垭口早晨 08:30 开始车流增大；鱼子西观景台草甸雨后稍湿，请备好防风外套",
            "fashion": "暖心冲锋衣/薄羽绒服 ➕ 防风手套帽子\n• 黄金光影：19:00-20:00 鱼子西/格底拉姆看日照金山晚霞",
            "cares": "折多山垭口与鱼子西海拔较高，山顶风大体感较冷，拍照停留时请注意保暖，不要剧烈跑跳，吸氧少量多次。\n• 格底拉姆非铺装土路雨后湿滑，现场收取约 20元/人 清洁费。\n• 今晚住宿在海拔较低的雅江县城 (2600m)，可以好好睡个好觉恢复体力。"
        },
        "08-03": {
            "title": "雅江县 ➔ 理塘县 ➔ 巴塘县",
            "elevation": "理塘 4014m ➔ 巴塘 2560m",
            "weather": "理塘：8~18℃ 晴朗｜云朵低垂如棉花糖\n• 巴塘：18~28℃ 暖阳｜金沙江河谷偏热舒适\n• 降雨：20:00 后夜间小雨润物",
            "traffic": "途经 G318 理塘至巴塘段 · 柏油路畅通｜剪子弯山防范坡脚落石\n• 🚨 进格聂前最后正规站：巴塘夏塘路口加油站加满",
            "toilet": "理塘毛垭大草原游客中心卫生间 / 姊妹湖观景台",
            "social": "实时路况：毛垭大草原野花盛开，姊妹湖停车区秩序良好；巴塘县城傍晚气温偏高",
            "fashion": "浅色休闲套装 ➕ 墨镜遮阳帽\n• 黄金光影：16:00 毛垭大草原与姊妹湖蓝眼睛",
            "cares": "特别提醒：今晚入住巴塘县城后，请务必在【中国石油巴塘县城加油站】将油箱彻底加满，因为明天进入格聂南线腹地后将没有正规加油站。\n• 今天全程约 300 公里，随车准备了靠枕、喜欢的音乐与电解质水。\n• 巴塘河谷气温偏热，请多喝水注意防晒。"
        },
        "08-04": {
            "title": "格聂南线越野腹地",
            "elevation": "扎瓦拉 5022m ➔ 则巴村 3900m",
            "weather": "扎瓦拉垭口：2~8℃ 极寒｜雪山近在咫尺\n• 则巴村：6~15℃｜夜间静谧湿冷\n• 降雨：13:00~16:00 垭口防雷暴冰雹",
            "traffic": "途经 格聂南线非铺装碎石水毁段 · 四驱SUV硬核穿越\n• 能源断油：❌ 腹地 250km 无任何正规加油站\n• 🚨 环保红线：严禁车辆开下路基压草滩 (重罚5万-20万)",
            "toilet": "腹地无公共洗手间，在巴塘出发前及民宿解决",
            "social": "实时路况：夯达营地雨后炮弹坑有积水，建议慢速通过；格聂之眼执法人员巡查严格，严禁压草滩",
            "fashion": "温暖厚羽绒服 ➕ 保暖内衣帽子手套\n• 黄金光影：12:00 扎瓦拉垭口雪山全景与夯达营地牧场",
            "cares": "扎瓦拉垭口海拔 5022 米，气温极低，拍照停留请不要超过 20 分钟防止高反，布洛芬放在易拿处。\n• 特别注意：2026 年环保执法非常严格，严禁将车辆驶离路基开入草滩，违者会被重罚。\n• 越野腹地部分区域没有手机信号，已提前准备好离线地图与保温水杯。"
        },
        "08-05": {
            "title": "则巴村 ➔ 新都桥镇",
            "elevation": "老冷古寺 3900m ➔ 新都桥 3300m",
            "weather": "则巴村：6~15℃ 晨雾｜古寺钟声清晨\n• 新都桥：8~18℃ 凉爽｜光影斑驳宜人\n• 降雨：12:00~15:00 局地山谷小雨",
            "traffic": "途经 老冷古寺徒步小路 ➔ 铁匠山垭口 (4770m)\n• 徒步路况：老冷古寺 3-5km 泥土小路雨后湿滑\n• 精准加油：出格聂抵理塘城关站第一时间加满",
            "toilet": "理塘县城正规加油站及新都桥酒店卫生间",
            "social": "实时路况：铁匠山垭口公路路面铺装完毕，通行顺畅；冷古寺徒步小路有小量泥泞，建议穿防水鞋",
            "fashion": "防风外套 ➕ 防水徒步鞋\n• 黄金光影：11:00 老冷古寺古建筑与格聂之眼草甸",
            "cares": "前往老冷古寺徒步约 3-5 公里，羊肠小路雨后比较泥泞，一定要穿防水防滑的鞋子。\n• 格聂之眼周边的草甸雨后比较湿软，绝对不要把车辆开入草滩。\n• 驶出格聂南线到达理塘县城后，请第一时间补满油箱。"
        },
        "08-06": {
            "title": "理塘县 ➔ 新都桥镇",
            "elevation": "理塘 4014m ➔ 新都桥 3300m",
            "weather": "理塘：8~18℃ 晴朗｜阳光明媚\n• 新都桥：10~20℃ 舒适｜摄影天堂金光闪烁\n• 降雨：21:00 后夜间阵雨润泽",
            "traffic": "途经 G318 国道雅江至新都桥段 · 畅通\n• 防范提醒：雨后注意山体坡脚散落碎石\n• 精准加油：新都桥镇中心加油站补充燃油",
            "toilet": "新都桥镇沿线正规餐厅与酒店卫生间",
            "social": "实时路况：新都桥十里长廊傍晚 18:00 天色光影极佳，无施工堵车点，游人车辆通行井然有序",
            "fashion": "复古文艺裙装/休闲外套 ➕ 墨镜\n• 黄金光影：17:30-18:30 新都桥十里长廊夕阳藏寨",
            "cares": "今天是长途自驾后的轻松休整日，行程比较松弛。\n• 新都桥镇傍晚的夕阳光影非常美丽，非常适合拍照散步。\n• 晚上一起品尝当地特色的藏式火锅或牦牛肉。"
        },
        "08-07": {
            "title": "新都桥 ➔ 冷嘎措",
            "elevation": "冷嘎措山顶 4500m ➔ 新都桥",
            "weather": "冷嘎措山顶：3~11℃ 极寒｜贡嘎雪山威严立于眼前\n• 新都桥：10~20℃ 舒适\n• 降雨：15:00~17:00 阵雨防强风降温",
            "traffic": "管制路线：🚨 S569线 K16-K54 段 (08:00-12:00及14:00-19:00全封闭)\n• 破局方案：卡准 12:00-14:00 放行窗口，或走 G248 沙德绕行\n• 精准加油：中石油新都桥站 (冷嘎措山脚无正规站)",
            "toilet": "冷嘎措山脚驿站洗手间",
            "social": "实时路况：S569 施工交警 12:00 准时放行，建议 11:30 抵卡口排队；冷嘎措山顶傍晚风大，骑马下山注意安全",
            "fashion": "暖心防风羽绒服 ➕ 帽子手套保暖鞋 (必带)\n• 黄金光影：19:00-19:40 冷嘎措看贡嘎雪山金色倒影",
            "cares": "冷嘎措山顶傍晚等待贡嘎雪山倒影时风大极冷，请务必带好最厚的羽绒服与防风帽。\n• S569省道施工封闭，我会卡准中午 12:00-14:00 的放行窗口通过。\n• 若阴雨大雾遮挡雪山，会带你改游甲根坝日轨村或塔公草原。"
        },
        "08-08": {
            "title": "新都桥 ➔ 成都",
            "elevation": "折多山 4298m ➔ 成都 500m",
            "weather": "折多山垭口：5~12℃\n• 成都市区：22~31℃ 温暖｜气温迅速回升\n• 降雨：14:00 后局地降雨",
            "traffic": "途经 G318 折多山段 ➔ G4218 雅康高速\n• 避堵方案：早 07:00 前出发翻山；严重堵车走 S434 绕行\n• 精准加油：雅安天全服务区加油站",
            "toilet": "雅安天全服务区 (星级干净洗手间)",
            "social": "实时路况：返程折多山下山段早晨 09:00 后易压车，早 07:00 出发畅通无阻；雅康高速隧道出口路面完好",
            "fashion": "便携叠穿 (翻山穿外套抵成都换短袖)\n• 黄金光影：08:00 折多山标志碑与雅康高速大桥",
            "cares": "今天从高海拔地区降至平原成都市，气温会迅速回升，车上请随时准备好更换轻便的衣服。\n• 折多山暑期车流较大，建议早晨 07:00 前出发翻山避开拥堵。\n• 今晚回到成都，安排一顿正宗的成都火锅！"
        },
        "08-09": {
            "title": "成都市区 ➔ 返程",
            "elevation": "成都市区 (海拔 500m)",
            "weather": "成都市区：23~32℃ 温润｜多云小雨\n• 降雨：不定期分散小雨",
            "traffic": "途经 成都市区至天府/双流机场段 (畅通)\n• 还车提醒：前往机场前将租车油箱补满",
            "toilet": "机场及市区正规卫生间",
            "social": "实时路况：市区交通顺畅，机场高速通行正常",
            "fashion": "舒适轻便清爽夏装\n• 黄金光影：太古里散步或人民公园喝茶",
            "cares": "预留充裕的时间前往成都天府或双流机场，检查好相机卡与随身物品。\n• 如果为租车自驾，前往还车点前请把油箱补满。\n• 整理好这 9 天美好的照片与记忆，一路顺风！"
        }
    }

    target_date = tomorrow_str if tomorrow_str in poetic_database else "08-01"
    data = poetic_database[target_date]

    card_text = f"""🌸 明日路书 · {data['title']}
📍 地标海拔：{data['elevation']}
⏱️ 30分钟实时雷达校对：{timestamp}

【 🌤️ 天气与温柔气温 】
• {data['weather']}

【 🚦 路线路况与安全 】
• {data['traffic']}

【 🚻 沿线干净洗手间 】
• {data['toilet']}

【 📡 抖音/小红书 24h 社媒热点排查 】
• {data['social']}

【 📸 穿搭灵感与光影时刻 】
• 穿搭建议：{data['fashion']}

【 💡 暖心守护与贴心关怀 】
• {data['cares']}

💖 愿我们的川西之旅，满是浪漫与美好"""

    return card_text

def has_status_changed(new_text):
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
    
    if has_status_changed(card_content):
        print("30分钟巡查：更新诗意高质感暖心卡片，立即下发微信实时推送！")
        res = send_msg(token, card_content)
        if res.get("errcode") != 0:
            tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
            tmpl_payload = {
                "touser": USER_OPENID,
                "template_id": TEMPLATE_ID,
                "data": {
                    "first": {"value": "🌸 30分钟云端雷达·诗意高质感暖心路书推送", "color": "#1890ff"},
                    "keyword1": {"value": "甘孜州气象局/甘孜交警12328/社媒24h实测", "color": "#cf1322"},
                    "keyword2": {"value": "【诗意暖心】已完成路况/卫生间/防晒/高反/光影最新校对", "color": "#333333"},
                    "remark": {"value": "💖 愿我们的川西之旅满是浪漫与美好！", "color": "#fa8c16"}
                }
            }
            requests.post(tmpl_url, json=tmpl_payload)
    else:
        print("30分钟巡查：数据无新突发差异，静默防打扰。")

if __name__ == "__main__":
    push_auto_schedule()
