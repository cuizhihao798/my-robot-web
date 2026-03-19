import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta  # 核心：必须加上这个 timedelta

# ==========================================
# 1. 页面配置与中南大学主题风格 (淡蓝色工业风)
# ==========================================
st.set_page_config(page_title="中南大学交通运输工程学院", layout="wide")

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
# 2. 侧边栏 (变量初始化与状态遥测)
# ==========================================
with st.sidebar:
    st.markdown('<p class="csu-header">CENTRAL SOUTH UNIVERSITY</p>', unsafe_allow_html=True)
    st.header(" 机器人状态遥测")
    st.markdown("---")
    
    # --- A. 电量逻辑 (必须先定义变量再进行逻辑判断) ---
    battery = st.slider("模拟电量调节", 0, 100, 85)
    
    if battery >= 80:
        b_color = "#3B82F6"  # 蓝色
        b_status = "⚡ 电量充足"
    elif battery >= 40:
        b_color = "#EAB308"  # 黄色
        b_status = "⚠️ 电量中等"
    else:
        b_color = "#EF4444"  # 红色
        b_status = "🚨 电量过低"

    # 显示带颜色的电量卡片
    st.markdown(f"""
        <div style="padding:15px; border-radius:10px; background-color:{b_color}22; border:1px solid {b_color}; text-align:center;">
            <strong style="color:{b_color}; font-size:14px;">{b_status}</strong><br>
            <span style="font-size:28px; font-weight:bold; color:{b_color};">{battery}%</span>
        </div>
    """, unsafe_allow_html=True)
    st.progress(battery / 100)
    
    st.markdown("---")
    
    # --- B. 作业参数定义 (解决 NameError 的关键) ---
    # 必须在这里定义 op_mode, train_id, track_id，主界面才能引用
    op_mode = st.selectbox("当前作业模式", ["全自动布放", "手动微调", "安全锁定", "应急撤回"])
    train_id = st.text_input("当前作业车次", value="G85-重载")
    track_id = st.selectbox("作业股道", ["1道", "2道", "3道", "4道", "5道"], index=2)
    
    st.markdown("---")
    st.info("💡 提示：修改车次号并回车，下方报表将自动感应并生成新任务记录。")
# ==========================================
# 3. 主界面顶部 - 状态汇总
# ==========================================
st.title("轨道机器人铁鞋布放监控系统")
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
# 5. 报表系统 - 全自动感应与全量汇总版
# ==========================================
st.subheader(" 每日铁鞋作业全量报表 (自动感应更新)")

# --- A. 初始化全局总库 (Session State) ---
if 'global_db' not in st.session_state:
    # 预置一些初始演示数据，体现多车次和不同时间逻辑
    now = datetime.now()
    st.session_state.global_db = pd.DataFrame({
        '记录时间': [
            (now - timedelta(hours=2)).strftime("%H:%M:%S"), # 最早
            (now - timedelta(hours=1, minutes=30)).strftime("%H:%M:%S"),
            (now - timedelta(minutes=40)).strftime("%H:%M:%S") # 最新
        ],
        '车次编号': ['G102-临客', 'G102-临客', 'G102-临客'],
        '股道编号': ['5道', '5道', '5道'],
        '目标轴位': ['1号轴', '2号轴', '3号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '🔒 已布放(锁死)', '⚠️ 作业中'],
        '对位误差(mm)': [0.15, 0.11, 0.32],
        '作业结果': ['✅ 成功', '✅ 成功', '⏳ 进行中']
    })
    # 记录当前正在操作的车次，用于比对是否切换了新车
    st.session_state.active_train = ""

# --- B. 核心逻辑：检测车次号是否发生手动更改 ---
# 只有当你在侧边栏输入了新内容，且不等于上次记录的车次时，才触发自动生成
if train_id and train_id != st.session_state.active_train:
    # 模拟新车进入，自动生成该车次的一组逻辑严密的数据
    ref_time = datetime.now()
    new_records = pd.DataFrame({
        '记录时间': [
            (ref_time - timedelta(minutes=25)).strftime("%H:%M:%S"), # 时间最久
            (ref_time - timedelta(minutes=15)).strftime("%H:%M:%S"), # 中间
            (ref_time - timedelta(seconds=5)).strftime("%H:%M:%S")   # 最晚/最新
        ],
        '车次编号': [train_id] * 3,
        '股道编号': [f"{random.randint(1,4)}道"] * 3,
        '目标轴位': ['1号轴', '2号轴', '3号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '🔒 已布放(锁死)', '⚠️ 作业中'],
        '对位误差(mm)': [0.09, 0.14, 0.28],
        '作业结果': ['✅ 成功', '✅ 成功', '⏳ 进行中']
    })
    
    # 将新生成的车次数据追加到总库中
    st.session_state.global_db = pd.concat([new_records, st.session_state.global_db], ignore_index=True)
    # 更新当前激活的车次名，防止重复生成
    st.session_state.active_train = train_id
    st.toast(f"检测到新车次 {train_id} 进入，已自动更新作业台账")

# --- C. 数据展示排序：相同车次排一起，组内时间倒序 ---
# 这样能保证 G85 的所有数据在一起，且最新的作业在最上面
display_df = st.session_state.global_db.sort_values(
    by=['车次编号', '记录时间'], 
    ascending=[True, False]
)

# 渲染全量表格
st.dataframe(display_df, use_container_width=True)

# --- D. 全量导出功能 ---
csv_all = display_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label=" 导出每日全量作业台账 (CSV格式)",
    data=csv_all,
    file_name=f"CSU_Daily_Report_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv',
    key='main_download_btn'
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
st.markdown('<center style="color: #94A3B8;">中南大学交通运输工程学院 | 轨道防溜机器人数字化监测平台 v2.5</center>', unsafe_allow_html=True)
