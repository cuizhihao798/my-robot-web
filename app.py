import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta  # 核心：必须加上这个 timedelta

# ==========================================
# 1. 页面配置与中南大学主题风格 (淡蓝色工业风)
# ==========================================
st.set_page_config(page_title="中南大学-轨道机器人监控", layout="wide")

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
    st.header("📝 机器人状态遥测")
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
st.title("🚄 轨道机器人铁鞋布放监控系统")
st.markdown(f"**单位：中南大学控制工程实验室** | 当前模式：`{op_mode}` | 执行车次：`{train_id}`")

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
st.subheader("📊 铁鞋放置压力传感实时折线图 (kN)")

# 模拟压力数据：左侧和右侧
chart_data = pd.DataFrame(
    np.random.randn(20, 2) * 0.5 + 15, # 围绕15kN波动
    columns=['左铁鞋压力', '右铁鞋压力']
)
st.line_chart(chart_data, height=250)
st.caption("注：标准施加压力区间为 14.5kN - 16.5kN。波动符合机械臂反馈特征。")

# ==========================================
# 5. 报表系统 - 全量作业台账 (逻辑增强版)
# ==========================================
st.subheader("📑 每日铁鞋作业全量报表 (自动汇总)")

# 核心逻辑：确保同一车次内，时间戳符合【收回 < 布放 < 作业中】
if 'global_history' not in st.session_state:
    now = datetime.now()
    # 预置两台车、两个股道的数据，体现多样性
    init_data = pd.DataFrame({
        '记录时间': [
            (now - timedelta(minutes=10)).strftime("%H:%M:%S"), # 最新：作业中
            (now - timedelta(minutes=45)).strftime("%H:%M:%S"), # 较早：布放
            (now - timedelta(hours=2)).strftime("%H:%M:%S"),    # 最早：已收回
            (now - timedelta(minutes=5)).strftime("%H:%M:%S"),  # 另一台车：作业中
            (now - timedelta(hours=1)).strftime("%H:%M:%S")     # 另一台车：布放
        ],
        '车次编号': ['G85-重载', 'G85-重载', 'G85-重载', 'G102-临客', 'G102-临客'],
        '股道编号': ['3道', '3道', '3道', '5道', '5道'],
        '目标轴位': ['3号轴', '2号轴', '1号轴', '2号轴', '1号轴'],
        '铁鞋状态': ['⚠️ 作业中', '🔒 已布放(锁死)', '✅ 已收回(归位)', '⚠️ 作业中', '🔒 已布放(锁死)'],
        '对位误差(mm)': [0.42, 0.12, 0.08, 0.35, 0.11],
        '作业结果': ['⏳ 进行中', '✅ 成功', '✅ 成功', '⏳ 进行中', '✅ 成功']
    })
    st.session_state.global_history = init_data

# 交互逻辑：点击侧边栏按钮时，将当前车次/股道信息追加到全量表顶部
# (注：此逻辑建议配合侧边栏按钮使用，若仅单提第五部分，此处显示当前库内所有数据)

# 排序：按时间倒序排列，保证最新的动作永远在表格最上方
display_df = st.session_state.global_history.sort_values(by='记录时间', ascending=False)

# 渲染表格
st.dataframe(display_df, use_container_width=True)

# 下载逻辑：导出全天所有车次数据
csv_all = display_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📊 导出每日全量作业台账 (CSV格式)",
    data=csv_all,
    file_name=f"CSU_Daily_Report_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv',
    key='download-all-csv' # 唯一键值防止冲突
)
# ==========================================
# 6. 底部日志 - 动作放置检测记录
# ==========================================
with st.expander("🔍 查看实时动作检测日志", expanded=True):
    st.code(f"""
    [{datetime.now().strftime("%H:%M:%S")}] [INFO] 视觉对位完成，偏移量 0.02mm
    [{datetime.now().strftime("%H:%M:%S")}] [ACTION] 机械臂开始执行 1号轴 铁鞋布放...
    [{datetime.now().strftime("%H:%M:%S")}] [SENSOR] 探测到接触压力，当前读数: 15.42kN
    [{datetime.now().strftime("%H:%M:%S")}] [SUCCESS] 铁鞋放置完毕，液压锁死已激活
    [{datetime.now().strftime("%H:%M:%S")}] [SYSTEM] 自动生成本条作业报表记录
    """)

# 页脚
st.markdown("---")
st.markdown('<center style="color: #94A3B8;">中南大学控制工程实验室 | 轨道机器人数字化监测平台 v2.5</center>', unsafe_allow_html=True)
