import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 1. 页面配置与高级样式注入
st.set_page_config(page_title="轨道机器人监控系统", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* 全局背景与字体 */
    .main { background-color: #f8fafc; }
    .stApp { font-family: 'Inter', -apple-system, sans-serif; }
    
    /* 去除侧边栏深色 */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* 自定义卡片样式 */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #f1f5f9;
        margin-bottom: 20px;
    }
    
    /* 标题样式 */
    .system-title {
        font-size: 24px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 5px;
    }
    .sub-text {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 全局数据持久化逻辑 (Session State)
if 'global_db' not in st.session_state:
    now = datetime.now()
    # 预置初始数据（保证两台车、股道不同、时间逻辑正确）
    st.session_state.global_db = pd.DataFrame({
        '记录时间': [(now - timedelta(hours=1)).strftime("%H:%M:%S"), (now - timedelta(minutes=45)).strftime("%H:%M:%S")],
        '车次编号': ['G102-临客', 'G102-临客'],
        '股道编号': ['5道', '5道'],
        '目标轴位': ['1号轴', '2号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '🔒 已布放(锁死)'],
        '对位误差(mm)': [0.15, 0.11],
        '作业结果': ['✅ 成功', '✅ 成功']
    })
    st.session_state.active_train = ""

# 3. 侧边栏：状态遥测与参数输入
with st.sidebar:
    st.markdown('<div style="font-size: 20px; font-weight: 800; color: #0f172a; padding: 10px 0;">专业工业监控系统</div>', unsafe_allow_html=True)
    
    # 电量逻辑处理
    battery = st.slider("实时模拟电量 (%)", 0, 100, 82)
    if battery >= 80:
        b_color, b_bg = "#3b82f6", "#eff6ff"  # 蓝色
    elif battery >= 40:
        b_color, b_bg = "#eab308", "#fef9c3"  # 黄色
    else:
        b_color, b_bg = "#ef4444", "#fef2f2"  # 红色
    
    # 电池卡片显示 (颜色与电量数值保持一致)
    st.markdown(f"""
        <div style="background-color: {b_bg}; border: 1px solid {b_color}; padding: 15px; border-radius: 10px; text-align: center; margin: 10px 0;">
            <div style="color: {b_color}; font-size: 12px; font-weight: 600;">当前设备电量</div>
            <div style="color: {b_color}; font-size: 28px; font-weight: 800;">{battery}%</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    train_id = st.text_input("当前作业车次", value="G8021-重载")
    track_id = st.selectbox("作业股道", ["1道", "2道", "3道", "4道", "5道"], index=2)
    op_mode = st.selectbox("工作模式", ["全自动布放", "远程手动", "系统自检"])
    
    st.caption("系统将根据车次输入自动同步历史数据")

# 4. 自动感应逻辑：车次变更触发新任务
if train_id and train_id != st.session_state.active_train:
    ref_time = datetime.now()
    new_data = pd.DataFrame({
        '记录时间': [
            (ref_time - timedelta(minutes=30)).strftime("%H:%M:%S"),
            (ref_time - timedelta(minutes=15)).strftime("%H:%M:%S"),
            (ref_time - timedelta(seconds=2)).strftime("%H:%M:%S")
        ],
        '车次编号': [train_id] * 3,
        '股道编号': [track_id] * 3,
        '目标轴位': ['1号轴', '2号轴', '3号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '🔒 已布放(锁死)', '⚠️ 作业中'],
        '对位误差(mm)': [0.08, 0.12, 0.35],
        '作业结果': ['✅ 成功', '✅ 成功', '⏳ 进行中']
    })
    st.session_state.global_db = pd.concat([new_data, st.session_state.global_db], ignore_index=True)
    st.session_state.active_train = train_id

# 5. 主界面布局
# 标题区
st.markdown(f'<div class="system-title">轨道机器人铁鞋布放监控大屏</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-text">中南大学控制工程实验室 | 当前车次：{train_id} | 模式：{op_mode}</div>', unsafe_allow_html=True)

# 第一行：核心状态指标
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="stat-card"><div style="color:#64748b; font-size:12px;">系统状态</div><div style="color:#22c55e; font-size:20px; font-weight:700;">● 运行中</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-card"><div style="color:#64748b; font-size:12px;">当前股道</div><div style="color:#1e293b; font-size:20px; font-weight:700;">{track_id}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-card"><div style="color:#64748b; font-size:12px;">今日作业总数</div><div style="color:#1e293b; font-size:20px; font-weight:700;">{len(st.session_state.global_db)} 轴</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="stat-card"><div style="color:#64748b; font-size:12px;">平均误差</div><div style="color:#1e293b; font-size:20px; font-weight:700;">0.14 mm</div></div>', unsafe_allow_html=True)

# 第二行：压力监测图表
st.subheader("📊 实时压力传感器反馈 (kN)")
chart_data = pd.DataFrame(
    np.random.randn(25, 2) * 0.2 + 15.5,
    columns=['左侧铁鞋', '右侧铁鞋']
)
st.area_chart(chart_data, height=250) # 使用 area_chart 更有高级感

# 第三行：作业报表 (全量汇总 + 车次聚合排序)
st.subheader("📑 铁鞋作业全量报表汇总")

# 排序逻辑：车次排一起，组内时间倒序
display_df = st.session_state.global_history if 'global_history' in locals() else st.session_state.global_db
sorted_df = display_df.sort_values(by=['车次编号', '记录时间'], ascending=[True, False])

st.dataframe(
    sorted_df, 
    use_container_width=True,
    column_config={
        "对位误差(mm)": st.column_config.ProgressColumn("对位误差", min_value=0, max_value=0.5, format="%.2f mm"),
        "作业结果": st.column_config.TextColumn("状态判定")
    }
)

# 报表导出按钮
csv = sorted_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 导出每日全量作业台账 (CSV)",
    data=csv,
    file_name=f"CSU_Robot_Report_{datetime.now().strftime('%m%d')}.csv",
    mime='text/csv'
)

# 底部日志记录
with st.expander("🔍 实时执行日志 (Log)", expanded=False):
    st.code(f"""
    [{datetime.now().strftime("%H:%M:%S")}] 初始化完成。
    [{datetime.now().strftime("%H:%M:%S")}] 检测到车次: {train_id}。股道映射: {track_id}。
    [{datetime.now().strftime("%H:%M:%S")}] 视觉系统 Ready。铁鞋对位中...
    """)
