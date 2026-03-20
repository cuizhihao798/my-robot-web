import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ==========================================
# 1. 页面配置：必须是第一行
# ==========================================
st.set_page_config(page_title="中南大学-轨道机器人监控", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 2. 高级样式注入：尝试接近参考图的轻量化高质感
# ==========================================
st.markdown("""
    <style>
    /* 全局背景色，去掉 AI 味儿 */
    .main { background-color: #f8fafc; }
    
    /* 去掉深色侧边栏，改为全白底色配合淡色边框 */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* 自定义卡片样式 (尝试模拟参考图的形状和阴影) */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* 系统标题样式 */
    .csu-title {
        color: #1e293b;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心持久化逻辑：放在所有 UI 之前，确保绝无 NameError
# ==========================================
if 'db' not in st.session_state:
    # 初始默认两台车数据
    now = datetime.now()
    st.session_state.db = pd.DataFrame({
        '记录时间': [(now - timedelta(minutes=90)).strftime("%H:%M:%S"), (now - timedelta(minutes=60)).strftime("%H:%M:%S")],
        '车次编号': ['G102-临客', 'G102-临客'],
        '股道编号': ['5道', '5道'],
        '目标轴位': ['1号轴', '2号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '🔒 已布放(锁死)'],
        '对位误差(mm)': [0.12, 0.08],
        '作业结果': ['✅ 成功', '✅ 成功']
    })
    # 用于记录上一次的车次，从而判定是否切换了新任务
    st.session_state.last_train = ""

# ==========================================
# 4. 侧边栏：先定义变量
# ==========================================
with st.sidebar:
    st.markdown('<div style="font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom:20px;">SYSTEM CONTROL</div>', unsafe_allow_html=True)
    
    # 电量逻辑与颜色保持一致
    battery = st.slider("实时电量模拟 (%)", 0, 100, 85)
    
    if battery >= 80:
        b_c, b_bg = "#3b82f6", "#eff6ff"  # 蓝色 (正常/充足)
    elif battery >= 40:
        b_c, b_bg = "#eab308", "#fef9c3"  # 黄色 (中等)
    else:
        b_c, b_bg = "#ef4444", "#fef2f2"  # 红色 (警示)
    
    # 颜色随电量数值保持一致
    st.markdown(f"""
        <div style="background-color:{b_bg}; border:1px solid {b_c}; padding:15px; border-radius:8px; text-align:center;">
            <div style="color:{b_c}; font-size:12px; font-weight:600;">BATTERY STATUS</div>
            <div style="color:{b_c}; font-size:28px; font-weight:800;">{battery}%</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 输入项
    op_mode = st.selectbox("作业模式", ["全自动巡检", "远程遥控", "维护模式"])
    train_id = st.text_input("当前作业车次", value="G8021-重载")
    track_id = st.selectbox("作业股道", ["1道", "2道", "3道", "4道", "5道"], index=2)
    
    st.markdown("---")
    st.caption("提示：修改车次号并回车，系统将自动感应并生成新任务报表。")

# ==========================================
# 5. 自动感应触发逻辑 (核心业务逻辑)
# ==========================================
if train_id and train_id != st.session_state.last_train:
    # 模拟新车进入，自动生成该车次的一组逻辑严密的数据
    ref_time = datetime.now()
    # 强制时间时序：收回(很久前) -> 布放(稍后) -> 作业中(现在)
    new_data = pd.DataFrame({
        '记录时间': [
            (ref_time - timedelta(minutes=20)).strftime("%H:%M:%S"), # 时间最久
            (ref_time - timedelta(minutes=10)).strftime("%H:%M:%S"), # 中间
            ref_time.strftime("%H:%M:%S")                           # 最晚/最新
        ],
        '车次编号': [train_id] * 3,
        '股道编号': [track_id] * 3,
        '目标轴位': ['1号轴', '2号轴', '3号轴'],
        '铁鞋状态': ['✅ 已收回(归位)', '🔒 已布放(锁死)', '⚠️ 作业中'],
        '对位误差(mm)': [0.09, 0.15, 0.38],
        '作业结果': ['✅ 成功', '✅ 成功', '⏳ 进行中']
    })
    
    # 将新数据追加到总库，并更新状态
    st.session_state.db = pd.concat([new_data, st.session_state.db], ignore_index=True)
    st.session_state.last_train = train_id
    st.toast(f"检测到新车次 {train_id} 进入，已自动同步历史作业台账")

# ==========================================
# 6. 主界面布局 (此时所有变量已就绪，绝无 NameError)
# ==========================================
# 标题区
st.markdown(f'<div class="csu-title">轨道机器人防溜监控系统</div>', unsafe_allow_html=True)
st.markdown(f"**中南大学控制工程实验室** | 模式: `{op_mode}` | 目标: `{train_id}` | 股道: `{track_id}`")

# 第一行：指标卡片 (仿参考图布局)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-card"><small style="color:#64748b;">系统状态</small><br><b style="color:#22c55e; font-size:20px;">🟢 正常运行</b></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><small style="color:#64748b;">当前电量</small><br><b style="color:{b_c}; font-size:20px;">{battery}%</b></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><small style="color:#64748b;">累计作业次数</small><br><b style="color:#1e293b; font-size:20px;">{len(st.session_state.db)} 轴次</b></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card"><small style="color:#64748b;">通讯延迟</small><br><b style="color:#1e293b; font-size:20px;">12 ms</b></div>', unsafe_allow_html=True)

st.markdown("---")

# 第二行：压力传感器折线图
st.subheader("📊 实时压力传感器反馈 (kN)")
# 生成模拟动态数据
chart_data = pd.DataFrame(
    np.random.randn(20, 2) * 0.2 + 15, # 围绕15kN波动
    columns=['A侧铁鞋', 'B侧铁鞋']
)
st.area_chart(chart_data, height=250) # 使用 area_chart 更有参考图的高级感

# 第三行：作业报表 (聚合排序 + 动态条形图)
st.subheader("📑 每日铁鞋作业全量报表台账")

# --- 核心修改：双重排序逻辑 ---
# 1. 先按“车次编号”排序，让相同车次挨在一起
# 2. 在相同车次内部，按“记录时间”倒序，让最新的动作排在最前面
final_df = st.session_state.db.sort_values(
    by=['车次编号', '记录时间'], 
    ascending=[True, False]
)

# 使用 dataframe 的 column_config 功能来美化特定列（模拟参考图的进度条）
st.dataframe(
    final_df, 
    use_container_width=True,
    column_config={
        "对位误差(mm)": st.column_config.ProgressColumn(
            "对位误差", 
            min_value=0, 
            max_value=0.5, 
            format="%.2f mm"
        ),
        "记录时间": st.column_config.TextColumn("时间节点"),
        "作业结果": st.column_config.TextColumn("状态判定")
    }
)

# 报表导出功能
csv_all = final_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 导出每日全量作业台账 (CSV格式)",
    data=csv_all,
    file_name=f"CSU_Robot_Report_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv'
)
