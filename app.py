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

import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. 页面配置
st.set_page_config(page_title="中南大学-自动化防溜系统", layout="wide")

# 2. 模拟数据库持久化 (使用 Session State)
# 初始化：如果没数据，或者车次变了，就重新生成
if 'current_train' not in st.session_state:
    st.session_state.current_train = ""
if 'history_db' not in st.session_state:
    st.session_state.history_db = pd.DataFrame()

# 3. 侧边栏：输入车次
with st.sidebar:
    st.header("🤖 机器人状态遥测")
    train_id = st.text_input("输入当前作业车次", value="G8021-重载")
    battery = st.slider("剩余电量", 0, 100, 85)
    st.markdown("---")
    st.info("检测到新车次输入后，系统将自动同步历史台账")

# --- 【核心逻辑：自动感应车次变换并生成历史】 ---
if train_id != st.session_state.current_train:
    # 1. 更新当前车次记录
    st.session_state.current_train = train_id
    
    # 2. 模拟生成该车次的 4 条错开时间的历史记录
    base_time = datetime.now()
    new_data = pd.DataFrame({
        '记录时间': [
            (base_time - timedelta(minutes=45)).strftime("%H:%M:%S"),
            (base_time - timedelta(minutes=30)).strftime("%H:%M:%S"),
            (base_time - timedelta(minutes=15)).strftime("%H:%M:%S"),
            (base_time - timedelta(seconds=10)).strftime("%H:%M:%S")
        ],
        '车次编号': [train_id] * 4,
        '目标轴位': ['1号轴', '2号轴', '3号轴', '4号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '✅ 已收回(归位)', '🔒 已布放(锁死)', '⚠️ 作业中'],
        '夹紧压力(kN)': [15.2, 14.8, 15.6, 8.4],
        '对位误差(mm)': [0.11, 0.08, 0.13, 0.45]
    })
    # 存入 Session 供演示
    st.session_state.history_db = new_data
    st.toast(f"检测到新车次 {train_id}，已调取作业历史数据")

# 4. 主界面展示
st.title("🚄 轨道机器人防溜作业数字孪生大屏")
st.markdown(f"**中南大学控制工程实验室** | 监控目标：`{train_id}`")

# 顶部指标
c1, c2, c3 = st.columns(3)
c1.metric("系统电量", f"{battery}%")
c2.metric("当前轴位", "4号轴")
c3.metric("总计完成", f"{len(st.session_state.history_db)}/4")

st.markdown("---")

# 5. 实时压力折线图 (保留你的创意)
st.subheader("📊 实时铁鞋压力监测 (数据流)")
chart_data = pd.DataFrame(
    np.random.randn(20, 2) * 0.3 + 15,
    columns=['左侧压力', '右侧压力']
)
st.line_chart(chart_data, height=200)

# 6. 自动化报表展示 (核心演示区)
st.subheader("📑 铁鞋作业历史数据报表 (自动生成)")
# 实时显示根据车次感应生成的表格
st.dataframe(st.session_state.history_db, use_container_width=True)

# 下载功能
csv = st.session_state.history_db.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 导出本批次作业报表 (CSV)",
    data=csv,
    file_name=f"Report_{train_id}.csv",
    mime='text/csv'
)

# 7. 作业日志 (增加收回逻辑描述)
with st.expander("🔍 查看实时指令日志", expanded=True):
    last_log_time = st.session_state.history_db.iloc[-1]['记录时间']
    st.code(f"""
    [{last_log_time}] [INFO] 识别到车次 {train_id} 进入作业区
    [{last_log_time}] [ACTION] 1号、2号轴防溜铁鞋已完成撤回任务，传感器状态：归位
    [{last_log_time}] [ACTION] 3号轴铁鞋已锁定，压力反馈 15.6kN
    [{datetime.now().strftime("%H:%M:%S")}] [DEBUG] 4号轴正在进行视觉对位，请注意安全距离...
    """)

# --- 【核心修改：动态导出下载】 ---
csv_data = st.session_state.history_db.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 导出完整作业台账 (CSV格式)",
    data=csv_data,
    file_name=f'CSU_Robot_Report_{datetime.now().strftime("%m%d_%H%M")}.csv',
    mime='text/csv',
)

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
