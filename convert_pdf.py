import os
import re
import subprocess
import shutil

cwd = "/Users/anranyunxiaomo/Desktop/project/xiungcheng"
md_path = os.path.join(cwd, "travel_plan_guide.md")
html_path = os.path.join(cwd, "travel_plan_guide.html")
pdf_path = os.path.join(cwd, "travel_plan_guide.pdf")

artifact_dir = "/Users/anranyunxiaomo/.gemini/antigravity/brain/e9fa3775-d78d-4c87-aa71-8fa833e8885d"
artifact_pdf_path = os.path.join(artifact_dir, "travel_plan_guide.pdf")

# 注意事项直接精准内嵌至每日卡片 (Day Cards) 的出版级渲染引擎
css = """
@page {
    size: A4;
    margin: 12mm 12mm 12mm 12mm;
}
* {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
    color: #1d1d1f;
    background-color: #f5f5f7;
    line-height: 1.55;
    padding: 0;
    margin: 0;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: #ffffff;
    padding: 24px;
    border-radius: 12px;
}

.header-hero {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    color: #ffffff;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.header-hero h1 {
    font-size: 22px;
    font-weight: 700;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
    color: #ffffff;
    border: none;
    padding: 0;
    text-align: left;
}
.header-meta {
    font-size: 12px;
    color: #94a3b8;
    display: flex;
    gap: 16px;
}

.gas-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 24px;
}
.gas-card h3 {
    margin: 0 0 12px 0;
    font-size: 15px;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 8px;
}
.gas-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
}
.gas-table th {
    background: #e2e8f0;
    color: #334155;
    text-align: left;
    padding: 6px 10px;
    font-weight: 600;
}
.gas-table td {
    padding: 8px 10px;
    border-bottom: 1px solid #f1f5f9;
}

.section-title {
    font-size: 17px;
    font-weight: 700;
    color: #0f172a;
    margin: 24px 0 16px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #2563eb;
    display: flex;
    align-items: center;
    gap: 8px;
}

.day-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    page-break-inside: avoid;
}

.day-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid #f1f5f9;
}
.day-title-group {
    display: flex;
    align-items: center;
    gap: 10px;
}
.day-badge {
    background: #2563eb;
    color: #ffffff;
    font-weight: 700;
    font-size: 12px;
    padding: 3px 8px;
    border-radius: 6px;
}
.day-route {
    font-size: 15px;
    font-weight: 700;
    color: #0f172a;
}
.risk-badge {
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;
}
.risk-green { background: #dcfce7; color: #15803d; }
.risk-yellow { background: #fef9c3; color: #a16207; }
.risk-red { background: #fee2e2; color: #b91c1c; }

.day-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    font-size: 12.5px;
}

.grid-block {
    background: #f8fafc;
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid #f1f5f9;
}
.block-title {
    font-weight: 700;
    color: #475569;
    font-size: 12px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
}
.block-content {
    color: #1e293b;
    line-height: 1.5;
}

/* 本日核心注意事项高亮卡片 (内嵌于 DAY 卡片底部) */
.notice-block {
    grid-column: span 2;
    background: #fffbeb;
    border: 1px solid #fef3c7;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 10px 12px;
}
.notice-block .block-title {
    color: #b45309;
    font-size: 12.5px;
}
.notice-block ul {
    margin: 4px 0 0 0;
    padding-left: 18px;
    color: #92400e;
}
.notice-block li {
    margin-bottom: 4px;
}

.notice-danger {
    background: #fef2f2;
    border-color: #fecaca;
    border-left-color: #ef4444;
}
.notice-danger .block-title {
    color: #b91c1c;
}
.notice-danger ul {
    color: #991b1b;
}

.full-width-block {
    grid-column: span 2;
    background: #eff6ff;
    border-color: #dbeafe;
}
.full-width-block .block-title {
    color: #1d4ed8;
}
"""

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>川西 8.1-8.9 秘境自驾全景路书与安全指南</title>
<style>""" + css + """</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header-hero">
    <h1>🏔️ 川西 8.1–8.9 路线·天气·路况·防汛·加油站全景路书</h1>
    <div class="header-meta">
      <span>⏱️ 注意事项精细内嵌版：2026-07-22 15:54</span>
      <span>🛡️ 官方数据源：甘孜州气象局 / 甘孜州公安局交警支队</span>
      <span>💡 特色：注意事项直接精准归嵌至每日行程卡片</span>
    </div>
  </div>

  <!-- 规范化加油站表格 -->
  <div class="gas-card">
    <h3>⛽ 沿线正规中国石油 / 中国石化加油站分布清单</h3>
    <table class="gas-table">
      <thead>
        <tr>
          <th>行政区域/节点</th>
          <th>正规加油站全称与具体位置</th>
          <th>标准加油与能源补给策略</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>成都市 ➔ 康定市</strong></td>
          <td>G4218雅康高速天全服务区加油站 / 中石油康定城关加油站 (折东路)</td>
          <td>驶入高速前于天全服务区加满；抵达康定市区后补充。</td>
        </tr>
        <tr>
          <td><strong>康定市新都桥镇</strong></td>
          <td>中石油新都桥加油站 (G318国道旁新都桥镇中心)</td>
          <td>翻越折多山后、前往雅江县或冷嘎措前的核心补给站。</td>
        </tr>
        <tr>
          <td><strong>雅江县城</strong></td>
          <td>中石油雅江城关加油站 (G318国道雅江县河口镇段)</td>
          <td>8月2日入住雅江后加满油箱，准备次日翻越剪子弯山。</td>
        </tr>
        <tr>
          <td><strong>理塘县城</strong></td>
          <td>中石油理塘城关加油站 / 中石油理塘长青春加油站 (县城西入口)</td>
          <td>8月3日途经理塘可补充；8月5日结束格聂穿越回理塘后<strong>必加满</strong>。</td>
        </tr>
        <tr>
          <td><strong>巴塘县城 (核心点)</strong></td>
          <td>中石油巴塘县城加油站 (巴塘县夏塘路口) / 金沙江加油站</td>
          <td><strong>🚨 进入格聂南线前的最后正规加油站！必须彻底加满！</strong></td>
        </tr>
        <tr>
          <td><strong>格聂南线越野腹地</strong></td>
          <td><strong>❌ 全线无任何正规中国石油/中国石化加油站</strong></td>
          <td>严禁空油箱单车深入！严禁依赖非法私售的劣质油桶。</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section-title">📅 8.1 – 8.9 逐日精细行程·气象·路况·【本日注意事项】全景卡片</div>

  <!-- DAY 1 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge">DAY 1</span>
        <span class="day-route">8月1日：成都市 ➔ 康定市</span>
      </div>
      <span class="risk-badge risk-green">🟢 安全 / 绿灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">成都市 (海拔 500m) ➔ 康定市 (海拔 2560m)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">成都市 22~31℃ / 康定市 14~22℃ (多云转阴有小雨)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">预计降水集中于 19:00 以后及夜间时段</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">雅安市天全县服务区加油站 / 康定城关加油站</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与灾害排查</div>
        <div class="block-content">G4218 雅康高速全线双向畅通；山洪落石🟢低风险；隧道出口需注意突发强降雨。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">高速公路通行秩序良好；泸定至康定段请保持安全跟车距离。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 当天驾驶与观景实操指南</div>
        <div class="block-content">下午抵达康定市入住。可在雅安市天全县服务区或康定市区将油箱补满。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block">
        <div class="block-title">⚠️ 8.1 本日核心注意事项与防范指南</div>
        <ul>
          <li>第一晚入住低海拔的康定市 (2560m) 极有利于高原适应，当晚切勿剧烈运动或长时间洗热水澡，防止感冒及诱发高反。</li>
          <li>G4218 雅康高速隧道密集，雨季隧道出口易遇到突发强降水，驶出隧道时请减速慢行。</li>
          <li>抵达康定后提前采购好随车便携式氧气瓶、高热量干粮与饮水。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- DAY 2 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge">DAY 2</span>
        <span class="day-route">8月2日：康定市 ➔ 折多山垭口 ➔ 鱼子西/格底拉姆 ➔ 雅江县</span>
      </div>
      <span class="risk-badge risk-yellow">🟡 注意 / 黄灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">折多山垭口 (海拔 4298m) / 鱼子西 (海拔 4200m) ➔ 雅江县 (海拔 2600m)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">折多山垭口 5~12℃ / 雅江县城 16~25℃ (山顶大雾湿冷)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">14:00 - 17:00 (高海拔山顶午后局地雷阵雨)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">中石油新都桥加油站 / 中石油雅江城关加油站</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与灾害排查</div>
        <div class="block-content">全线无大型阻断事故；折多山防高山大雾与零星飞石🟡中风险。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">折多山车流量密集，交警实施间歇性放行；格底拉姆观景台收取约20元场地清洁费。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 当天驾驶与观景实操指南</div>
        <div class="block-content">早晨 07:30 出发翻折多山。若山顶大雾被盖，可选 S434 绕行新都桥，晚上宿低海拔雅江县城。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block">
        <div class="block-title">⚠️ 8.2 本日核心注意事项与防范指南</div>
        <ul>
          <li>折多山垭口 (4298m) 与鱼子西 (4200m) 山顶风大体感极寒，切勿剧烈跑跳，随身携带防风冲锋衣保暖。</li>
          <li>通往鱼子西/格底拉姆包含非铺装土路，雨后极为湿滑，请控制车速慢行；格底拉姆现场收取约 20元/人 清洁费。</li>
          <li>晚上入住低海拔的雅江县城 (2600m) 利于睡眠恢复，抵雅江后顺便将油箱补满。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- DAY 3 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge">DAY 3</span>
        <span class="day-route">8月3日：雅江县 ➔ 理塘县 ➔ 巴塘县</span>
      </div>
      <span class="risk-badge risk-green">🟢 安全 / 绿灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">雅江县 ➔ 理塘县 (海拔 4014m) ➔ 巴塘县 (海拔 2560m)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">理塘县城 8~18℃ / 巴塘县城 18~28℃ (巴塘河谷偏热)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">20:00 以后 (夜间降水为主)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">理塘城关加油站 / <strong>巴塘县城加油站 (必须加满)</strong></div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与灾害排查</div>
        <div class="block-content">G318 国道柏油路面全线畅通；临崖坡脚需注意落石防范🟡中风险。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">毛垭大草原与海子山姊妹湖段通行良好，国道无管控封路。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 当天驾驶与观景实操指南</div>
        <div class="block-content">全天长途行驶约 300km+，注意拉开跟车距离。毛垭大草原与姊妹湖观景台停车注意安全。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block notice-danger">
        <div class="block-title">🚨 8.3 本日核心注意事项 (格聂断油特警)</div>
        <ul>
          <li><strong>断油特警：</strong>巴塘县城是进入格聂南线前的<strong>最后正规加油站</strong>！晚上抵达巴塘后，<strong>必须在【中国石油巴塘县城加油站】将油箱彻底加满</strong>！</li>
          <li>全天行驶经过剪子弯山与卡子拉山等高海拔垭口，跟车拉开安全距离，防范陡峭山壁坡脚的零星落石。</li>
          <li>采购好次日穿越格聂南线腹地所需的 2-3 天高热量路餐与充足饮水。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- DAY 4 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge" style="background:#dc2626;">DAY 4</span>
        <span class="day-route">8月4日：巴塘县 ➔ 扎瓦拉垭口 ➔ 夯达营地 ➔ 则巴村 (格聂南线)</span>
      </div>
      <span class="risk-badge risk-red">🔴 高危预警 / 红灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">扎瓦拉垭口 (海拔 5022m) ➔ 夯达营地 ➔ 则巴村 (海拔 3900m)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">扎瓦拉垭口 2~8℃ / 则巴村 6~15℃ (全天极寒/高反风险高)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">13:00 - 16:00 (高海拔垭口雷暴/冰雹高发)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">❌ 越野腹地全程无正规加油站 (满油箱可持续行驶)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与灾害排查</div>
        <div class="block-content">非铺装碎石水毁路段；溪流水位上涨/底盘陷车🔴高风险。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">越野车主实拍炮弹坑雨后积水较深；多车挂彩。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 当天驾驶与观景实操指南</div>
        <div class="block-content">必须驾驶四驱高底盘 SUV 满油通行；扎瓦拉垭口停留切勿超过 20 分钟；腹地无手机信号须备离线地图。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block notice-danger">
        <div class="block-title">🚨 8.4 本日核心注意事项 (环保红线与安全熔断)</div>
        <ul>
          <li><strong>⚖️ 2026 环保执法红线：</strong>严禁车辆开离路基碾压草甸！在格聂之眼、夯达营地等区域，<strong>违法将车辆开下路基碾压草滩将被处以 5万~20万元 行政重罚</strong>！车辆必须行驶于既有路基上。</li>
          <li><strong>扎瓦拉垭口 (5022m)：</strong>海拔极高极易诱发剧烈高反，降雨时易发冰雹，建议拍照即走，停留切勿超过 20 分钟。</li>
          <li><strong>熔断预案 (Plan B)：</strong>若早晨巴塘预报有强暴雨或泥石流通告，果断放弃格聂南线，沿 G318 国道直奔理塘县城。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- DAY 5 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge">DAY 5</span>
        <span class="day-route">8月5日：则巴村 ➔ 冷古寺 ➔ 铁匠山垭口 ➔ 理塘/新都桥</span>
      </div>
      <span class="risk-badge risk-yellow">🟡 注意 / 黄灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">老冷古寺 (海拔 3900m) ➔ 铁匠山垭口 (海拔 4770m) ➔ 新都桥镇</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">则巴村 6~15℃ / 新都桥镇 8~18℃ (湿度大体感寒凉)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">12:00 - 15:00 (山谷局地短时阵雨)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">出格聂抵理塘县后：中石油理塘城关站 (必须补充)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与灾害排查</div>
        <div class="block-content">冷古寺徒步泥土小路雨后湿滑；泥泞陷车风险🟡中风险。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">冷古寺开放徒步；格聂之眼周边草甸雨后湿软。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 当天驾驶与观景实操指南</div>
        <div class="block-content">前往冷古寺徒步请准备防水登山鞋。驶出格聂抵达理塘县城后，第一时间将油箱补满。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block">
        <div class="block-title">⚠️ 8.5 本日核心注意事项与防范指南</div>
        <ul>
          <li>前往老冷古寺徒步约 3-5km，雨后羊肠小路极为泥泞湿滑，请务必穿防水防滑登山鞋。</li>
          <li>格聂之眼周边的草甸在雨季非常湿软，<strong>绝对禁止将车辆开入草滩</strong>，防止陷车或触犯环保法规受罚。</li>
          <li>驶出格聂南线到达理塘县城后，请第一时间在中国石油加油站补充油箱。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- DAY 6 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge">DAY 6</span>
        <span class="day-route">8月6日：理塘县 ➔ 新都桥镇</span>
      </div>
      <span class="risk-badge risk-green">🟢 安全 / 绿灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">理塘县城 (海拔 4014m) ➔ 新都桥镇 (海拔 3300m)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">理塘县 8~18℃ / 新都桥镇 10~20℃ (多云舒适)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">21:00 以后 (夜间阵雨为主)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">理塘长青春站 / 雅江城关站 / 新都桥站</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与灾害排查</div>
        <div class="block-content">G318 国道全线正常通行；防范坡脚零星落石🟢低风险。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">国道路段通行良好；新都桥十里长廊光影效果佳。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 当天驾驶与观景实操指南</div>
        <div class="block-content">本日为长途行程后的休整赶路日，可在新都桥镇十里长廊游览摄影。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block">
        <div class="block-title">⚠️ 8.6 本日核心注意事项与防范指南</div>
        <ul>
          <li>若前一天在格聂或理塘停留较晚，本日主要为国道赶路。G318 雅江至新都桥段雨后注意避开山体坡脚散落的碎石。</li>
          <li>新都桥镇海拔 3300m，傍晚气候宜人，可在十里长廊或薰衣草庄园轻松休整与摄影。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- DAY 7 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge" style="background:#d97706;">DAY 7</span>
        <span class="day-route">8月7日：新都桥镇 ➔ 冷嘎措 ➔ 新都桥镇</span>
      </div>
      <span class="risk-badge risk-yellow">🟡 修路管制 / 黄灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">冷嘎措 (海拔 4500m) ➔ 新都桥镇 (海拔 3300m)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">冷嘎措山顶 3~11℃ / 新都桥镇 10~20℃ (傍晚寒风刺骨)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">15:00 - 17:00 (阵雨) / 18:30 以后 (强风剧烈降温)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">中石油新都桥加油站 (冷嘎措山脚无正规站)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与 S569 管制</div>
        <div class="block-content">🚨 S569线 K16-K54 段施工，08:00-12:00 及 14:00-19:00 全封闭。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">经甲根坝前往需卡准 12:00-14:00 放行窗口，或绕行 G248 国道沙德段。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 冲突破局三大实操方案</div>
        <div class="block-content">方案1：卡准 <code>12:00-14:00</code> 窗口期通行；方案2：走 G248 国道经沙德绕行；若大雨大雾可执行方案3：改游甲根坝日轨村或塔公草原。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block notice-danger">
        <div class="block-title">🚨 8.7 本日核心注意事项 (S569 管制与冷嘎措防寒)</div>
        <ul>
          <li><strong>🚧 S569 修路管制破局：</strong>K16-K54 段 <code>08:00-12:00</code> 及 <code>14:00-19:00</code> 全封闭。方案1(推荐)：早晨 10:30 从新都桥出发，<strong>卡准 `12:00-14:00` 放行窗口通过施工段</strong>；傍晚看完日落于 `19:00 以后` 夜间窗口返回。方案2：沿 G248 国道经沙德镇绕行（车程多40分钟）。</li>
          <li>冷嘎措山顶 (4500m) 傍晚等待贡嘎雪山倒影与日照金山时寒风刺骨，必须携带薄羽绒服、防风帽与手条。</li>
          <li>若当天阴雨大雾遮挡雪山，果断执行方案3（改游甲根坝日轨村或塔公草原）。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- DAY 8 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge">DAY 8</span>
        <span class="day-route">8月8日：新都桥镇 ➔ 折多山 ➔ 康定市 ➔ 成都市</span>
      </div>
      <span class="risk-badge risk-yellow">🟡 避堵提醒 / 黄灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">折多山垭口 (海拔 4298m) ➔ 成都市 (海拔 500m)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">折多山垭口 5~12℃ / 成都市 22~31℃ (海拔骤降/气温回升)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">14:00 以后 (下午及夜间高速段局地降雨)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">新都桥站 / 康定城关站 / 雅安天全服务区站</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与灾害排查</div>
        <div class="block-content">折多山易发生压车拥堵；落石与堵车🟡中风险。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">折多山暑期车流量巨大，降雨易引发大雾视线受阻。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 当天驾驶与观景实操指南</div>
        <div class="block-content">在新都桥镇补充燃油。从高原 (3300m) 降至平原 (500m)，注意气温剧升，及时增减衣物。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block">
        <div class="block-title">⚠️ 8.8 本日核心注意事项与防范指南</div>
        <ul>
          <li>折多山垭口暑期车流量极大，且雨季易发大雾导致降速压车。<strong>建议早晨 07:00 前从新都桥镇出发翻山避堵</strong>。</li>
          <li>若折多山发生大面积堵车，可选择 <strong>S434 省道（经红海子/斯丁措方向）</strong> 绕行下山至康定。</li>
          <li>返程雅康高速隧道出口注意局地强降雨减速。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- DAY 9 -->
  <div class="day-card">
    <div class="day-header">
      <div class="day-title-group">
        <span class="day-badge">DAY 9</span>
        <span class="day-route">8月9日：成都市区 ➔ 返程</span>
      </div>
      <span class="risk-badge risk-green">🟢 安全 / 绿灯</span>
    </div>
    <div class="day-grid">
      <div class="grid-block">
        <div class="block-title">📍 路线节点与海拔</div>
        <div class="block-content">成都市区 ➔ 机场</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌤️ 实时气象预测与温差</div>
        <div class="block-content">成都市区 23~32℃ (多云偶有分散小雨)</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🌧️ 降雨高峰时段预测</div>
        <div class="block-content">不定期分散小雨</div>
      </div>
      <div class="grid-block">
        <div class="block-title">⛽ 正规加油站位置</div>
        <div class="block-content">成都市区各正规加油站</div>
      </div>
      <div class="grid-block">
        <div class="block-title">🛣️ 道路通行与灾害排查</div>
        <div class="block-content">交通秩序正常；灾害风险🟢低风险。</div>
      </div>
      <div class="grid-block">
        <div class="block-title">📱 社交平台实测反馈</div>
        <div class="block-content">市区交通状况良好。</div>
      </div>
      <div class="grid-block full-width-block">
        <div class="block-title">💡 当天驾驶与观景实操指南</div>
        <div class="block-content">低海拔市区休整，前往机场顺利返程。</div>
      </div>
      <!-- 内嵌本日专属注意事项 -->
      <div class="notice-block">
        <div class="block-title">⚠️ 8.9 本日核心注意事项与防范指南</div>
        <ul>
          <li>若为租车自驾，请在前往成都市区还车点前将油箱补满。</li>
          <li>预留充裕时间前往成都天府机场或双流机场，结束完美的川西秘境自驾之旅。</li>
        </ul>
      </div>
    </div>
  </div>

</div>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file://{html_path}"
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"注意事项内嵌版 PDF 生成成功: {pdf_path}")
    if os.path.exists(artifact_dir):
        try:
            shutil.copy(pdf_path, artifact_pdf_path)
            print(f"副本已同步至: {artifact_pdf_path}")
        except Exception as e:
            print(f"复制到 artifact 失败: {e}")
else:
    print(f"转换错误: {result.stderr}")
