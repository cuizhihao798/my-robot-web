import streamlit as st
import pandas as pd
import numpy as np

# 页面基本配置
st.set_page_config(page_title="轨道防溜作业监控", layout="wide")

# 侧边栏：模拟机器人状态
st.sidebar.header("🤖 机器人参数")
battery = st.sidebar.slider("剩余电量 (%)", 0, 100, 85)
st.sidebar.write(f"当前电量: {battery}%")
if battery < 20:
    st.sidebar.error("警告：电量过低！")

st.sidebar.header("📍 定位信息")
st.sidebar.info("当前坐标：X:124.5, Y:88.2")

# 主界面标题
st.title("🚄 列车自动防溜作业数字监控大屏")
st.markdown("---")

# 第一行：核心指标指标
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="设备状态", value="🟢 运行中", delta="在线")
with col2:
    st.metric(label="对位精度", value="0.12 mm", delta="-0.02 mm")
with col3:
    st.metric(label="环境温度", value="24.5 °C", delta="1.2 °C")

# 第二行：模拟传感器监测数据图表
st.subheader("实时作业压力波动 (模拟)")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['压力A轴', '压力B轴', '夹紧力']
)
st.line_chart(chart_data)

# 第三行：详细作业日志
st.subheader("📋 详细作业状态表")
log_data = pd.DataFrame({
    '轴位': ['1号轴', '2号轴', '3号轴', '4号轴'],
    '检测状态': ['✅ 正常', '✅ 正常', '⚠️ 略有偏差', '✅ 正常'],
    '机械臂动作': ['已归位', '已归位', '调整中', '已归位'],
    '完成度': ['100%', '100%', '85%', '100%']
})
st.table(log_data)

# 页脚
st.markdown("---")
st.caption("中南大学控制工程实验室 - 轨道机器人监测系统原型 v1.0")
