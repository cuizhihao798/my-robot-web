import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# ==========================================
# 1. 页面配置与中南大学主题风格 (淡蓝色工业风)
# ==========================================
st.set_page_config(page_title="中南大学-轨道防溜小车监控", layout="wide")

# 自定义 CSS 样式
st.markdown("""
    <style>
    /* 整体背景与文字 */
    .stApp { background-color: #F0F5F9; }
    h1, h2, h3 { color: #1E3A8A; font-family: "Microsoft YaHei"; }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] { background-color: #E2E8F0; border-right: 2px solid #CBD5E1; }
    
    /* 卡片式容器 */
    .metric-container {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3B82F6;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    
    /* 中南大学元素标识 */
    .csu-header {
        font-size: 14px;
        color: #64748B;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏 (机器人状态遥测)
# ==========================================
with st.sidebar:
    st.markdown('<p class="csu-header">CENTRAL SOUTH UNIVERSITY</p>', unsafe_allow_html=True)
    st.header(" 机器人状态遥测")
    st.markdown("---")
    
    # 作业模式选择
    op_mode = st.selectbox("当前作业模式", ["全自动布放", "远程手动接管", "应急撤回", "系统维护"])
    
    # 模拟电量滑动条
    battery = st.slider("剩余电量 (%)", 0, 100, 82)
    st.progress(battery / 100)
    
    # 车辆信息输入
    train_id = st.text_input("当前作业车次", "G8021-重载编组")
    
    if st.button("手动刷新实时数据"):
        st.toast("正在同步机器人传感器数据...")
        time.sleep(0.5)

# ==========================================
# 3. 主界面顶部 - 状态汇总
# ==========================================
st.title(" 轨道机器人铁鞋布放监控系统")
st.markdown(f"**单位：中南大学交通运输工程学院** | 当前模式：`{op_mode}` | 执行车次：`{train_id}`")

# 四个状态卡片
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.info("🤖 **机器人状态**\n\n 作业中 (对位布放)")
with col_b:
    st.success("🛰️ **定位精度**\n\n 0.12mm (厘米级)")
with col_c:
    st.warning("⚖️ **左侧铁鞋**\n\n 状态: 已布放 (99.2%)")
with col_d:
    st.warning("⚖️ **右侧铁鞋**\n\n 状态: 已布放 (98.8%)")

st.markdown("---")

# ==========================================
# 4. 核心功能 - 铁鞋压力检测折线图
# ==========================================
st.subheader("铁鞋放置压力传感实时折线图 (kN)")

# 模拟压力数据：左侧和右侧
chart_data = pd.DataFrame(
    np.random.randn(20, 2) * 0.5 + 15, # 围绕15kN波动
    columns=['左铁鞋压力', '右铁鞋压力']
)
st.line_chart(chart_data, height=250)
st.caption("注：标准施加压力区间为 14.5kN - 16.5kN。波动符合机械臂反馈特征。")

# ==========================================
# 5. 报表系统 - 铁鞋布放历史数据 (修复动态关联逻辑)
# ==========================================
st.subheader("📑 铁鞋布放历史数据报表")

# 模拟一个较大的原始数据库
raw_data = pd.DataFrame({
    '记录时间': [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(20)],
    '车次编号': ['G8021-重载编组']*10 + ['G9999-临客']*10, # 模拟两个不同的车次
    '目标轴位': ['1号轴', '2号轴'] * 10,
    '布放方位': ['左侧(Leading)', '右侧(Trailing)'] * 10,
    '贴合误差(mm)': np.random.uniform(0.05, 0.45, 20).round(2),
    '作业结果': ['✅ 成功'] * 20
})

# 【关键改动】：根据侧边栏输入的 train_id 进行筛选
# 如果输入框里的车次在数据库里能找到，就只显示该车次的数据
if train_id in raw_data['车次编号'].values:
    filtered_data = raw_data[raw_data['车次编号'] == train_id]
else:
    # 如果是新输入的未知车次，动态生成一组该车次的新数据（模拟新作业）
    filtered_data = pd.DataFrame({
        '记录时间': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        '车次编号': [train_id],
        '目标轴位': ['临时轴'],
        '布放方位': ['自动对位'],
        '贴合误差(mm)': [0.00],
        '作业结果': ['⏳ 等待作业']
    })

# 显示筛选后的表格
st.dataframe(filtered_data, use_container_width=True)

# ==========================================
# 6. 底部日志 - 动作放置检测记录
# ==========================================
with st.expander(" 查看实时动作检测日志", expanded=True):
    st.code(f"""
    [{datetime.now().strftime("%H:%M:%S")}] [INFO] 视觉对位完成，偏移量 0.02mm
    [{datetime.now().strftime("%H:%M:%S")}] [ACTION] 机械臂开始执行 1号轴 铁鞋布放...
    [{datetime.now().strftime("%H:%M:%S")}] [SENSOR] 探测到接触压力，当前读数: 15.42kN
    [{datetime.now().strftime("%H:%M:%S")}] [SUCCESS] 铁鞋放置完毕，液压锁死已激活
    [{datetime.now().strftime("%H:%M:%S")}] [SYSTEM] 自动生成本条作业报表记录
    """)

# 页脚
st.markdown("---")
st.markdown('<center style="color: #94A3B8;">中南大学交通运输工程学院| 轨道防溜小车数字化监测平台 v2.5</center>', unsafe_allow_html=True)
