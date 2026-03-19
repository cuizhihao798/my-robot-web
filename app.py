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
# 5. 报表系统 - 带有持久化记忆的记录表
# ==========================================
st.subheader("📑 铁鞋布放历史数据报表 (实时保存)")

# --- 【核心修改：初始化缓存数据库】 ---
if 'history_db' not in st.session_state:
    # 初始默认数据
    st.session_state.history_db = pd.DataFrame({
        '记录时间': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        '车次编号': ['G8021-初始示例'],
        '目标轴位': ['1号轴'],
        '布放方位': ['左侧(Leading)'],
        '贴合误差(mm)': [0.12],
        '作业结果': ['✅ 成功']
    })

# --- 【核心修改：添加新记录的按钮】 ---
col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    if st.button("💾 提交当前作业记录"):
        # 创建新的一行数据
        new_record = pd.DataFrame({
            '记录时间': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            '车次编号': [train_id], # 使用侧边栏输入的车次
            '目标轴位': [f"{np.random.randint(1,5)}号轴"], # 模拟自动分配轴位
            '布放方位': [np.random.choice(['左侧(Leading)', '右侧(Trailing)'])],
            '贴合误差(mm)': [round(np.random.uniform(0.05, 0.35), 2)],
            '作业结果': ['✅ 成功']
        })
        # 将新数据拼接到缓存数据库中
        st.session_state.history_db = pd.concat([new_record, st.session_state.history_db], ignore_index=True)
        st.toast(f"记录已存入台账：{train_id}")

# --- 显示表格 ---
# 始终显示缓存数据库里的所有内容
st.dataframe(st.session_state.history_db, use_container_width=True)

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
