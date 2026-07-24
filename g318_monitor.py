import os
import json
import time
from datetime import datetime, timedelta
import requests

APP_ID = os.environ.get("WECHAT_APP_ID", "wxf39166d6f2deab57")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "c2fb35bda2fe52d795e6a64a70d3e38e")
USER_OPENID = os.environ.get("WECHAT_USER_OPENID", "of84Y3bGGlhFtf7vqa52snEve8w4")
TEMPLATE_ID = os.environ.get("WECHAT_TEMPLATE_ID", "oaJwSb8IrjhC6pNlMas4jSOo2p5J1ETu976H1wGpLrQ")

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
    print("微信文本推送结果:", res)
    return res

# 经过【防折行断字 (<=16字)】、【天然【 】框线】与【彩色 Emoji 对齐】的顶级微信大厂排版卡片库
PERFECT_DAILY_CARDS = {
    "08-01": """🌸 8.1 明日路书 · 成都 ➔ 康定
📍 目的地海拔：2560m (低海拔适应)

【 🌤️ 气象与温差 】
• 康定：14~22℃｜多云体感宜人
• 成都：22~31℃｜晴间多云
• 降雨：预计 19:00 后夜间小雨

【 👗 穿搭与打卡 】
• 穿搭：长袖内搭 ➕ 随时穿脱外套
• 打卡：18:00 康定情歌广场夕阳

【 🚗 路线与加油 】
• 雅康高速畅通，隧道出口防雨
• 已在天全服务区加满油箱

【 💡 暖心守护 】
• 今晚宿康定利于适应高反，切勿洗长热水澡或剧烈运动
• 紫外线渐强，带好遮阳帽与防晒
• 随车备有保温杯、氧气与零食

💖 祝我们第一天行程浪漫愉快""",

    "08-02": """🌸 8.2 明日路书 · 康定 ➔ 雅江
📍 目的地海拔：折多山4298m ➔ 雅江2600m

【 🌤️ 气象与温差 】
• 折多山/鱼子西：5~12℃｜风大较冷
• 雅江：16~25℃｜低海拔舒适
• 降雨：14:00~17:00 午后局地阵雨

【 👗 穿搭与打卡 】
• 穿搭：冲锋衣/薄羽绒服 ➕ 防风帽
• 打卡：鱼子西/格底拉姆雪山晚霞

【 🚗 路线与加油 】
• 早 07:30 出发翻折多山避堵，大雾走 S434 绕行
• 新都桥或雅江补充油箱

【 💡 暖心守护 】
• 山顶极冷勿剧烈跑跳，穿好保暖外套
• 格底拉姆路滑，现场收约20元清洁费
• 晚上宿低海拔雅江(2600m)好入睡

💖 明天带你看浪漫的雪山日落""",

    "08-03": """🌸 8.3 明日路书 · 雅江 ➔ 巴塘
📍 目的地海拔：理塘4014m ➔ 巴塘2560m

【 🌤️ 气象与温差 】
• 理塘：8~18℃｜多云转晴
• 巴塘：18~28℃｜金沙江河谷偏热
• 降雨：20:00 后夜间小雨为主

【 👗 穿搭与打卡 】
• 穿搭：浅色休闲套装 ➕ 墨镜防晒
• 打卡：毛垭大草原与姊妹湖

【 🚗 路线与加满提醒 】
• G318 国道全线柏油路畅通
• 🚨 进格聂前的最后正规站！今晚必须在【巴塘加油站】彻底加满

【 💡 暖心守护 】
• 车程稍长，随车准备了靠枕与音乐
• 翻越垭口跟车拉开距离，防零星落石
• 在巴塘采购好接下来 2-3 天的小零食

💖 漫步大草原，享受属于我们的旅程""",

    "08-04": """🌸 8.4 明日路书 · 格聂南线秘境
📍 目的地海拔：扎瓦拉5022m ➔ 则巴村3900m

【 🌤️ 气象与温差 】
• 扎瓦拉垭口：2~8℃｜极寒
• 则巴村：6~15℃｜夜间湿冷
• 降雨：13:00~16:00 垭口防雷暴

【 👗 穿搭与打卡 】
• 穿搭：厚羽绒服 ➕ 保暖内衣帽子
• 打卡：扎瓦拉垭口与夯达营地牧场

【 🚗 路线与规则 】
• 越野碎石路，炮弹坑雨后积水
• ❌ 腹地 250km 无任何正规加油站
• 🚨 严禁车开下路基压草滩(重罚)

【 💡 暖心守护 】
• 扎瓦拉垭口拍照停留勿超 20 分钟
• 腹地无信号，备好离线地图与保温杯
• 若大暴雨果断开启预案改走 G318

💖 深入格聂秘境，拥抱纯粹的雪山草原""",

    "08-05": """🌸 8.5 明日路书 · 则巴村 ➔ 新都桥
📍 目的地海拔：老冷古寺3900m ➔ 新都桥3300m

【 🌤️ 气象与温差 】
• 则巴村：6~15℃｜晨间清冷
• 新都桥：8~18℃｜凉爽舒适
• 降雨：12:00~15:00 局地阵雨

【 👗 穿搭与打卡 】
• 穿搭：防风外套 ➕ 防水徒步鞋
• 打卡：老冷古寺古建筑与格聂之眼

【 🚗 路线与加油 】
• 出格聂抵理塘后第一时间加满油箱

【 💡 暖心守护 】
• 冷古寺徒步小路泥泞，穿防水鞋
• 格聂之眼草甸湿软，严禁开车压草
• 晚上入住新都桥，好好放松休整

💖 探访老冷古寺，感受秘境的宁静""",

    "08-06": """🌸 8.6 明日路书 · 理塘 ➔ 新都桥
📍 目的地海拔：理塘4014m ➔ 新都桥3300m

【 🌤️ 气象与温差 】
• 理塘：8~18℃｜晴朗
• 新都桥：10~20℃｜多云舒适
• 降雨：21:00 后夜间阵雨

【 👗 穿搭与打卡 】
• 穿搭：文艺裙装/休闲外套 ➕ 墨镜
• 打卡：18:00 新都桥十里长廊夕阳

【 🚗 路线与加油 】
• G318 国道全线畅通，随时补充燃油

【 💡 暖心守护 】
• 今天是轻松休整日，行程松弛
• 新都桥傍晚夕阳光影极美，适合拍照
• 晚上品尝特色藏式火锅

💖 漫步摄影天堂，享受惬意光影时刻""",

    "08-07": """🌸 8.7 明日路书 · 新都桥 ➔ 冷嘎措
📍 目的地海拔：冷嘎措山顶4500m ➔ 新都桥

【 🌤️ 气象与温差 】
• 冷嘎措山顶：3~11℃｜傍晚极寒
• 新都桥：10~20℃
• 降雨：15:00~17:00 阵雨防强风

【 👗 穿搭与打卡 】
• 穿搭：防风羽绒服 ➕ 帽子手套
• 打卡：冷嘎措湖畔看日照金山倒影

【 🚗 路线与修路破局 】
• 🚨 S569 施工封闭(08:00-12:00 / 14:00-19:00)
• 卡准 12:00-14:00 窗口通过，或走 G248 沙德绕行

【 💡 暖心守护 】
• 山顶看日照金山风大极冷，带厚羽绒服
• 若阴雨大雾改游甲根坝日轨村或塔公
• 下山路暗注意安全，紧跟在我身边

💖 一起守候日照金山，许下最美心愿""",

    "08-08": """🌸 8.8 明日路书 · 新都桥 ➔ 成都
📍 目的地海拔：折多山4298m ➔ 成都500m

【 🌤️ 气象与温差 】
• 折多山垭口：5~12℃
• 成都市区：22~31℃｜气温回升
• 降雨：14:00 后局地降雨

【 👗 穿搭与打卡 】
• 穿搭：便携叠穿 (翻山穿外套抵成都换短袖)
• 打卡：折多山标志碑与雅康高速大桥

【 🚗 路线与避堵 】
• 建议早 07:00 出发翻折多山避堵
• 天全服务区补充燃油

【 💡 暖心守护 】
• 从高海拔降至平原气温剧升，准备换轻便衣服
• 雅康高速隧道出口防雨，安心休养
• 今晚回到成都安排正宗火锅

💖 圆满结束高山之旅，回到温暖蓉城""",

    "08-09": """🌸 8.9 明日路书 · 成都市区 ➔ 返程
📍 目的地海拔：成都市区 (海拔 500m)

【 🌤️ 气象与温差 】
• 成都市区：23~32℃｜多云小雨
• 降雨：不定期分散小雨

【 👗 穿搭与打卡 】
• 穿搭：舒适轻便清爽夏装
• 打卡：太古里散步或人民公园喝茶

【 🚗 还车与行程结束 】
• 前往机场前将租车油箱补满

【 💡 暖心守护 】
• 预留充裕时间前往机场，检查相机卡
• 整理 9 天美好的照片与记忆
• 一路顺风，期待下一次精彩出发

💖 感谢 9 天有你相伴，行程圆满落幕"""
}

def push_auto_schedule():
    token = get_access_token()
    if not token:
        print("无法获取微信 token")
        return

    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%m-%d")
    card_content = PERFECT_DAILY_CARDS.get(tomorrow_str, PERFECT_DAILY_CARDS["08-01"])

    res = send_msg(token, card_content)
    # 若 45047 配额满，降级模板消息保证送达
    if res.get("errcode") != 0:
        tmpl_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
        tmpl_payload = {
            "touser": USER_OPENID,
            "template_id": TEMPLATE_ID,
            "data": {
                "first": {"value": "🌸 8.1 明日路书 · 成都 ➔ 康定 (2560m)", "color": "#1890ff"},
                "keyword1": {"value": "康定: 14~22℃ 多云 | 成都: 22~31℃", "color": "#cf1322"},
                "keyword2": {"value": "【穿搭】长袖内搭+外套 | 【守护】第一晚勿洗长热水澡，备好保温杯氧气", "color": "#333333"},
                "remark": {"value": "💖 祝我们第一天行程浪漫愉快！", "color": "#fa8c16"}
            }
        }
        requests.post(tmpl_url, json=tmpl_payload)

if __name__ == "__main__":
    push_auto_schedule()
