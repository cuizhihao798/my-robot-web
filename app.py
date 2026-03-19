import streamlit as st
import pandas as pd
import numpy as np
import time

# 页面配置
st.set_page_config(page_title="中南大学-轨道防溜监控", layout="wide")

# 极简科技感样式 (确保兼容性)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { color: #00f2ff; text-shadow: 0 0 5px #00f2ff; }
    .metric-box { border: 1px solid #1e3a8a; padding: 10px; border-radius: 5px; background: #161b22; }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.header("⚙️ 机器人控制")
    battery = st.slider("模拟电量 (%)", 0, 100, 85)
    mode = st.selectbox("作业模式", ["自动部署", "手动微调", "安全锁定"])
    st.info("中南大学控制工程实验室")

# 主界面
st.title("🚄 列车自动防溜作业数字监控大屏")
st.write(f"当前状态：🟢 系统在线 | 模式：{mode}")

# 第一行：核心指标
col1, col2, col3, col4 = st.columns(4)
col1.metric("防溜状态", "已锁定", "安全")
col2.metric("对位精度", "0.12 mm", "-0.02")
col3.metric("主夹紧力", "15.8 kN", "正常")
col4.metric("电量", f"{battery}%", "-1%")

st.markdown("---")

# 第二行：铁鞋压力动态检测 (核心升级)
st.subheader("📊 铁鞋夹紧压力实时监测 (kN)")
# 生成模拟动态数据
chart_data = pd.DataFrame(
    np.random.randn(20, 2) + 15,
    columns=['左侧压力', '右侧压力']
)
st.line_chart(chart_data)

st.markdown("---")

# 第三行：作业日志
st.subheader("📋 实时作业日志")
log_data = pd.DataFrame({
    '时间': [time.strftime("%H:%M:%S") for _ in range(5)],
    '位置': ['1号轴', '2号轴', '3号轴', '4号轴', '系统'],
    '动作': ['压力补偿', '位置校准', '铁鞋锁死', '完成部署', '自检通过'],
    '状态': ['✅ 正常', '✅ 正常', '✅ 正常', '✅ 正常', '🟢 正常']
})
st.table(log_data)
