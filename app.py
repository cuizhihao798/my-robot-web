import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 1. 页面配置与专业样式注入
st.set_page_config(page_title="轨道机器人数字孪生监控系统", layout="wide")

st.markdown("""
    <style>
    /* 全局背景与字体 */
    .main { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* 自定义侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
        color: white;
    }
    .csu-logo {
        color: #60A5FA;
        font-weight: 800;
        font-size: 1.2rem;
        margin-bottom: 20px;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
    }
    
    /* 卡片样式 */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        border: 1px solid #E2E8F0;
    }
    
    /* 状态标签样式 */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 核心逻辑：数据持久化与自动感应初始化
if 'global_db' not in st.session_state:
    now = datetime.now()
    # 预置初始演示数据 (满足：收回 < 布放 < 作业中 逻辑)
    st.session_state.global_db = pd.DataFrame({
        '记录时间': [
            (now - timedelta(hours=2)).strftime("%H:%M:%S"),
            (now - timedelta(hours=1, minutes=30)).strftime("%H:%M:%S"),
            (now - timedelta(minutes=40)).strftime("%H:%M:%S")
        ],
        '车次编号': ['G102-预设', 'G102-预设', 'G102-预设'],
        '股道编号': ['5道', '5道', '5道'],
        '目标轴位': ['1号轴', '2号轴', '3号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '🔒 已布放(锁死)', '⚠️ 作业中'],
        '对位误差(mm)': [0.15, 0.11, 0.32],
        '作业结果': ['✅ 成功', '✅ 成功', '⏳ 进行中']
    })
    st.session_state.active_train = ""

# 3. 侧边栏：输入组件 (优先定义变量防止 NameError)
with st.sidebar:
    st.markdown('<div class="csu-logo">CSU RAILWAY SYSTEM</div>', unsafe_allow_html=True)
    
    st.subheader("⚙️ 任务配置")
    train_id = st.text_input("当前作业车次", value="G85-重载编组")
    track_id = st.selectbox("作业股道", ["1道", "2道", "3道", "4道", "5道"], index=2)
    op_mode = st.selectbox("作业模式", ["全自动布放", "手动微调", "应急撤回"])
    
    st.markdown("---")
    st.subheader("🔋 机器人状态")
    battery = st.slider("模拟电量调节", 0, 100, 85)
    
    # 电量颜色分级逻辑
    if battery >= 80:
        b_color, b_status = "#3B82F6", "⚡ 电量充足" # 蓝色
    elif battery >= 40:
        b_color, b_status = "#EAB308", "⚠️ 电量中等" # 黄色
    else:
        b_color, b_status = "#EF4444", "🚨 电量过低" # 红色

    st.markdown(f"""
        <div style="padding:15px; border-radius:10px; background-color:{b_color}11; border:1px solid {b_color};">
            <small style="color:{b_color};">{b_status}</small><br>
            <span style="font-size:24px; font-weight:bold; color:{b_color};">{battery}%</span>
        </div>
    """, unsafe_allow_html=True)
    st.progress(battery / 100)

# 4. 车次感应逻辑：切换车次自动生成历史记录
if train_id and train_id != st.session_state.active_train:
    ref_time = datetime.now()
    new_records = pd.DataFrame({
        '记录时间': [
            (ref_time - timedelta(minutes=25)).strftime("%H:%M:%S"), # 收回：最早
            (ref_time - timedelta(minutes=15)).strftime("%H:%M:%S"), # 布放：中期
            (ref_time - timedelta(seconds=5)).strftime("%H:%M:%S")   # 作业：最新
        ],
        '车次编号': [train_id] * 3,
        '股道编号': [track_id] * 3,
        '目标轴位': ['1号轴', '2号轴', '3号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '🔒 已布放(锁死)', '⚠️ 作业中'],
        '对位误差(mm)': [round(random.uniform(0.05, 0.15), 2), 
                        round(random.uniform(0.1, 0.2), 2), 
                        round(random.uniform(0.3, 0.5), 2)],
        '作业结果': ['✅ 成功', '✅ 成功', '⏳ 进行中']
    })
    st.session_state.global_db = pd.concat([new_records, st.session_state.global_db], ignore_index=True)
    st.session_state.active_train = train_id

# 5. 主界面布局
# 标题行
st.title("🛡️ 轨道机器人铁鞋布放监控大屏")
st.markdown(f"**单位：中南大学控制工程实验室** | 模式：`{op_mode}` | 目标：`{train_id}`")

# 顶部指标卡片
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown(f'<div class="metric-card"><small>当前电量</small><h2 style="color:{b_color}">{battery}%</h2></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="metric-card"><small>作业股道</small><h2>{track_id}</h2></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown('<div class="metric-card"><small>今日累计作业</small><h2>12 轴</h2></div>', unsafe_allow_html=True)
with col_m4:
    st.markdown('<div class="metric-card"><small>系统状态</small><h2 style="color:#10B981">🟢 正常</h2></div>', unsafe_allow_html=True)

st.markdown("###")

# 图表与实时监控区
col_chart, col_log = st.columns([2, 1])
with col_chart:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📊 铁鞋夹紧压力实时监测 (kN)")
    # 模拟压力波动数据
    chart_data = pd.DataFrame(np.random.randn(30, 2) * 0.2 + 15, columns=['左侧铁鞋', '右侧铁鞋'])
    st.line_chart(chart_data)
    st.markdown('</div>', unsafe_allow_html=True)

with col_log:
    st.markdown('<div class="metric-card" style="height:375px; overflow-y:auto;">', unsafe_allow_html=True)
    st.subheader("📑 实时指令流")
    st.caption("系统内核反馈")
    st.code(f"""
[{datetime.now().strftime("%H:%M:%S")}] 视觉算法锁定 {track_id}
[{datetime.now().strftime("%H:%M:%S")}] 正在进行 {train_id} 3号轴对位
[{datetime.now().strftime("%H:%M:%S")}] 压力补偿机制已启动...
[{datetime.now().strftime("%H:%M:%S")}] 无线链路RSSI: -65dBm
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("###")

# 6. 数据报表区：相同车次聚合，组内时间倒序
st.subheader("📅 每日全量作业台账报表")
# 排序：先按车次排一起，同一车次最新的在上面
display_df = st.session_state.global_db.sort_values(
    by=['车次编号', '记录时间'], 
    ascending=[True, False]
)

# 使用 Dataframe 展示并开启搜索/过滤功能
st.dataframe(
    display_df,
    use_container_width=True,
    column_config={
        "铁鞋状态": st.column_config.TextColumn("状态及反馈"),
        "对位误差(mm)": st.column_config.ProgressColumn("对位精度", min_value=0, max_value=0.6, format="%.2f mm")
    }
)

# 7. 全量数据下载
csv = display_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 导出全天作业汇总报表 (CSV)",
    data=csv,
    file_name=f"Daily_Report_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv',
)
