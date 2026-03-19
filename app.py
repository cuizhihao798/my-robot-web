import streamlit as st
import pandas as pd
import numpy as np
import time

# ==============================
# 1. 页面基本配置 (保留最初的大屏风格)
# ==============================
st.set_page_config(
    page_title="中南大学 - 轨道防溜监控",
    layout="wide",  # 使用宽屏模式
    initial_sidebar_state="expanded" # 默认展开侧边栏
)

# 自定义 CSS：注入更多科技感和中南大学元素
st.markdown("""
<style>
    /* 整体背景：更深的科技蓝 */
    .stApp {
        background-color: #050A18;
        color: #E0E6ED;
    }
    
    /* 侧边栏样式优化 */
    .css-1d391kg {
        background-color: #0A122A !important;
        border-right: 1px solid #1E3A8A;
    }
    
    /* 标题文字：增加发光效果 */
    h1 {
        color: #00D2FF !important;
        text-shadow: 0 0 10px #00D2FF, 0 0 20px #00D2FF;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* 大号数字指标样式 */
    [data-testid="stMetricValue"] {
        font-size: 40px !important;
        color: #00FFC2 !important;
        font-family: 'Orbitron', sans-serif; /* 需要浏览器支持该字体，否则回退 */
    }
    [data-testid="stMetricLabel"] {
        color: #8899A6 !important;
    }

    /* 模拟“闪烁”的状态灯 */
    .status-indicator {
        height: 15px;
        width: 15px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
    }
    .status-online {
        background-color: #00FF00;
        box-shadow: 0 0 10px #00FF00;
        animation: blink-green 2s infinite;
    }
    @keyframes blink-green {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    
    /* 优化表格样式 */
    .stDataFrame table {
        border: 1px solid #1E3A8A;
        background-color: #0A122A;
    }
</style>
""", unsafe_allow_stdio=True)

# ==============================
# 2. 侧边栏设计 (保留最初设计)
# ==============================
with st.sidebar:
    # 中南大学校徽（如果需要，可以替换为网络图片URL）
    # st.image("https://你的校徽图片链接.png", width=100)
    st.markdown("## ⚙️ 机器人控制面板")
    st.markdown("---")
    
    # 机器人选择
    robot_id = st.selectbox("选择操作机器人", ["CSU-Robot-01", "CSU-Robot-02"])
    
    st.markdown("### 实时参数设定")
    # 模拟电量 slider
    battery = st.slider("模拟剩余电量 (%)", 0, 100, 85)
    
    # 作业模式
    mode = st.radio("作业模式", ["自动部署", "远程操控", "设备维护"])
    
    st.markdown("---")
    st.caption("中南大学控制工程实验室 © 2024")

# ==============================
# 3. 主界面设计 (优化并加入折线图)
# ==============================

# A. 顶部标题栏 (增加科技感)
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("🚄 列车自动防溜作业数字监控大屏")
with col_logo:
    # 模拟一个呼吸灯效果的状态
    st.markdown('<h3><span class="status-indicator status-online"></span><span style="color:#00FF00">系统在线</span></h3>', unsafe_allow_stdio=True)

st.markdown("---")

# B. 第一行：核心指标大号数字显示 (保留最初设计，CSS优化)
st.subheader("🖥️ 核心作业指标")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(label="当前防溜状态", value="已锁定🔒", delta="工作模式: "+mode)
with c2:
    st.metric(label="对位精度 (mm)", value="0.12", delta="-0.03 (优)")
with c3:
    st.metric(label="主夹紧力 (kN)", value="15.8", delta="正常范围内")
with c4:
    # 这里的 metric 值随侧边栏的 slider 动态变化
    st.metric(label="机器人电量", value=f"{battery}%", delta="-2% (下降中)")

st.markdown("---")

# C. 第二行：核心升级！加入铁鞋压力检测折线图
st.subheader("📊 铁鞋夹紧压力动态监测 (模拟实时数据)")

# 模拟生成动态数据
# 我们创建两组压力数据：左侧夹板压力 和 右侧夹板压力
chart_data = pd.DataFrame(
    np.random.randn(50, 2) + [15, 15], # 基数设为15kN，模拟随机波动
    columns=['左侧压力 (kN)', '右侧压力 (kN)']
)

# 使用 Streamlit 原生折线图，它支持交互（放大、缩小）
st.line_chart(chart_data)

# 增加一点图表说明，增强专业感
st.caption("注：正常作业压力区间为 12kN - 18kN。当前波形显示机器人正在平稳施加夹紧力。")

st.markdown("---")

# D. 第三行：详细作业日志表格 (保留最初设计)
st.subheader("📋 详细作业日志文件 (最新10条)")

# 模拟一些更有现场感的日志数据
log_data = pd.DataFrame({
    '时间戳': [time.strftime("%H:%M:%S", time.localtime(time.time() - i*60)) for i in range(10)],
    '作业轴位': ['1号轴', '1号轴', '2号轴', '2号轴', '3号轴', '3号轴', '4号轴', '4号轴', '总控', '总控'],
    '检测动作': ['对位寻标', '机械臂伸出', '铁鞋放置', '主夹紧力施加', '对位寻标', '机械臂伸出', '铁鞋放置', '主夹紧力施加', '状态自检', '电量上报'],
    '传感器读数': ['精度0.11mm', '到位确认', '放置成功', '压力15.9kN', '精度0.13mm', '到位确认', '放置成功', '压力15.7kN', '所有系统正常', f'电量{battery}%'],
    '作业结果': ['✅ 成功', '✅ 成功', '✅ 成功', '✅ 成功', '⚠️ 精度微调', '✅ 成功', '✅ 成功', '✅ 成功', '🟢 正常', '🟢 正常']
})

# 显示表格，不显示索引序号
st.table(log_data)

# 页脚
st.markdown("---")
st.caption("中南大学自动化学院 - 机器人防溜系统答辩演示原型 v2.1")
