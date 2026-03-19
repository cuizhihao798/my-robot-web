import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# 1. 页面全局配置 (必须放在第一行)
# ==========================================
st.set_page_config(
    page_title="防溜机器人智能调度大屏",
    page_icon="🚄",
    layout="wide"
)

# ==========================================
# 2. 侧边栏：模拟数据接收与参数调节
# ==========================================
st.sidebar.header("📡 机器人状态遥测")
st.sidebar.caption("模拟传感器传回的实时数据")

robot_status = st.sidebar.selectbox(
    "小车当前运行状态",
    ["🟢 作业中 (对位布放)", "🟡 待机寻迹中", "🔵 充电中", "🔴 视觉异常告警"]
)
battery = st.sidebar.slider("剩余电量 (%)", 0, 100, 82)
current_train = st.sidebar.text_input("当前作业车次", "G8021-重载编组")
refresh_btn = st.sidebar.button("手动刷新实时数据")

# ==========================================
# 3. 主界面 Header
# ==========================================
st.title("🚄 列车自动防溜作业数字监控大屏")
st.markdown("基于视觉定位的列车铁鞋智能调度防溜车系统")
st.divider()

# ==========================================
# 4. 核心模块一：实时运行状态概览
# ==========================================
st.header("📊 全局状态概览")
col1, col2, col3, col4 = st.columns(4)

col1.metric("设备网络状态", robot_status.split(" ")[1], "在线" if "异常" not in robot_status else "-掉线")
col2.metric("当前电量", f"{battery}%", "-2% (放电正常)" if battery > 20 else "-低电量警告")
col3.metric("今日完成防溜总数", "24 组 (48个铁鞋)", "+2 组 (上一小时)")
col4.metric("视觉平均对位精度", "0.18 mm", "+0.02 mm (毫米级)")

st.divider()

# ==========================================
# 5. 核心模块二：非对称布放状态 3D 逻辑监控
# ==========================================
st.header("🛞 当前转向架防溜作业监控 (实时映射)")
st.markdown(f"**目标车次：** `{current_train}` | **当前执行规程：** `双轴四点·非对称对角布放`")

# 使用列布局模拟前后两个车轴的铁鞋放置情况
axle1_col, axle2_col = st.columns(2)

# 模拟 1 号轴 (要求放在左侧 Leading Edge)
with axle1_col:
    st.subheader("📍 第 1 轴 (前轴)")
    st.info("执行逻辑：锁定轮轨左侧切点 (Leading Edge)")

    c1, c2 = st.columns(2)
    with c1:
        st.success("✅ 左侧铁鞋：已布放\n\n置信度: 99.2%")
    with c2:
        st.write("⚪ 右侧铁鞋：非作业侧\n\n(规程屏蔽)")

# 模拟 2 号轴 (要求放在右侧 Trailing Edge)
with axle2_col:
    st.subheader("📍 第 2轴 (后轴)")
    st.warning("执行逻辑：锁定轮轨右侧切点 (Trailing Edge)")

    c3, c4 = st.columns(2)
    with c3:
        st.write("⚪ 左侧铁鞋：非作业侧\n\n(规程屏蔽)")
    with c4:
        st.success("✅ 右侧铁鞋：已布放\n\n置信度: 98.8%")

st.divider()

# ==========================================
# 6. 核心模块三：作业日志与数据收集报表
# ==========================================
st.header("📝 铁鞋布放历史数据报表")


# 生成模拟的历史作业数据
@st.cache_data
def load_mock_data():
    base_time = datetime.now()
    data = []
    for i in range(10):
        # 模拟一前一后的逻辑数据
        is_axle_1 = (i % 2 == 0)
        axle = "1号轴" if is_axle_1 else "2号轴"
        position = "左侧 (Leading)" if is_axle_1 else "右侧 (Trailing)"

        data.append({
            "记录时间": (base_time - timedelta(minutes=i * 15)).strftime("%Y-%m-%d %H:%M:%S"),
            "车次编号": "G8021",
            "股道编号": "3道",
            "目标轴位": axle,
            "布放方位": position,
            "视觉计算耗时(s)": round(np.random.uniform(1.2, 2.5), 2),
            "极点贴合误差(mm)": round(np.random.uniform(0.05, 0.45), 2),
            "作业结果": "✅ 成功"
        })
    return pd.DataFrame(data)


df = load_mock_data()

# 在网页上展示可交互的表格，加入进度条样式展示极小的误差
st.dataframe(
    df,
    use_container_width=True,
    column_config={
        "极点贴合误差(mm)": st.column_config.ProgressColumn(
            "极点贴合误差(mm)",
            help="毫米级边缘检测误差",
            format="%.2f mm",
            min_value=0.0,
            max_value=0.5,  # 假设0.5mm是最大容忍误差
        ),
    }
)

# 提供 CSV 导出功能
csv = df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 导出完整作业台账 (CSV格式)",
    data=csv,
    file_name=f'防溜作业台账_{datetime.now().strftime("%Y%m%d")}.csv',
    mime='text/csv',
)
