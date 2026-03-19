import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

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
# 5. 报表系统 - 动态感应式历史数据 (仅修改此处)
# ==========================================
st.subheader("📑 铁鞋作业历史数据报表 (自动生成)")

# 核心逻辑：根据车次号产生“种子”，确保同一车次数据固定，不同车次数据不同
# 使用车次号字符串的长度和内容作为随机种子
import random
seed_value = sum(ord(c) for c in train_id)
random.seed(seed_value)
np.random.seed(seed_value)

# 随机决定该车次的记录条数 (3到6条)
num_rows = random.randint(3, 6)

# 随机生成错开的时间点
base_time = datetime.now()
time_list = [(base_time - timedelta(minutes=random.randint(10, 60))).strftime("%H:%M:%S") for _ in range(num_rows)]
time_list.sort() # 按时间先后排序

# 构造动态报表
dynamic_history = pd.DataFrame({
    '记录时间': time_list,
    '车次编号': [train_id] * num_rows,
    '股道编号': [f"{random.randint(1, 5)}道"] * num_rows, # 增加股道信息，体现变化
    '目标轴位': [f"{i+1}号轴" for i in range(num_rows)],
    '布放方位': [random.choice(['左侧(Leading)', '右侧(Trailing)']) for _ in range(num_rows)],
    '铁鞋状态': [random.choice(['✅ 已收回(归位)', '🔒 已布放(锁死)', '✅ 已收回(归位)']) for _ in range(num_rows-1)] + ['⚠️ 作业中'],
    '对位误差(mm)': [round(random.uniform(0.05, 0.45), 2) for _ in range(num_rows)],
    '作业结果': ['✅ 成功'] * (num_rows - 1) + ['⏳ 进行中']
})

# 渲染表格
st.dataframe(dynamic_history, use_container_width=True)

# 报表下载功能
csv = dynamic_history.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label=f"📥 导出 {train_id} 作业台账 (CSV)",
    data=csv,
    file_name=f"Report_{train_id}_{datetime.now().strftime('%m%d')}.csv",
    mime='text/csv'
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
