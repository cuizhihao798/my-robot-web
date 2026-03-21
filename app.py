import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ==========================================
# 0. 全局配置与高级 CSS 样式注入
# ==========================================
st.set_page_config(page_title="视觉定位铁鞋智能调度系统", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; }
    .stat-card {
        background: white; padding: 1.5rem; border-radius: 10px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); border: 1px solid #e2e8f0; margin-bottom: 1rem;
    }
    .csu-title { color: #0f172a; font-size: 24px; font-weight: 800; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-bottom: 20px;}
    .sub-title { color: #334155; font-size: 18px; font-weight: 600; margin-top: 15px; margin-bottom: 10px; }
    .alert-box { padding: 10px; border-radius: 5px; border-left: 5px solid #ef4444; background: #fef2f2; color: #991b1b; }
    .success-box { padding: 10px; border-radius: 5px; border-left: 5px solid #22c55e; background: #f0fdf4; color: #166534; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 全局数据初始化 (Session State)
# ==========================================
if 'init' not in st.session_state:
    now = datetime.now()
    # 模拟历史作业记录表
    st.session_state.history_db = pd.DataFrame({
        '时间戳': [(now - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M") for i in range(1, 11)],
        '设备编号': [f'AGV-0{random.randint(1,4)}' for _ in range(10)],
        '股道/列车': [f'{random.randint(1,5)}道/G{random.randint(100,999)}' for _ in range(10)],
        '操作类型': random.choices(['放铁鞋', '取铁鞋'], k=10),
        '视觉误差(mm)': [round(random.uniform(-1.8, 1.8), 2) for _ in range(10)],
        '放置精度(mm)': [round(random.uniform(-4.5, 4.5), 2) for _ in range(10)],
        '压力数据(kN)': [round(random.uniform(14.5, 16.5), 2) for _ in range(10)],
        '作业结果': ['成功'] * 9 + ['预警'],
        '故障代码': ['-'] * 9 + ['WARN-V02']
    })
    st.session_state.init = True

# ==========================================
# 2. 侧边栏：多页面路由导航
# ==========================================
with st.sidebar:
    st.markdown('<div style="font-size: 16px; font-weight: 800; color: #1e293b; margin-bottom:20px;">🛡️ 铁鞋智能调度管理系统</div>', unsafe_allow_html=True)
    
    page = st.radio("系统功能导航", [
        "📊 模块一：全景智能监控大屏", 
        "🎛️ 模块二：智能调度联控中心", 
        "📑 模块三：自动报表与产量分析", 
        "🚨 模块四：故障自诊断与报警", 
        "⚙️ 模块五：系统管理后台",
        "🏆 模块六：竞赛展示专区"
    ])
    
    st.markdown("---")
    st.caption("核心指标监控区")
    st.progress(0.999, text="系统开机率: 99.9%")
    st.progress(0.98, text="低照度识别率: 98.2%")

# ==========================================
# 3. 各模块页面渲染逻辑
# ==========================================

if page == "📊 模块一：全景智能监控大屏":
    st.markdown('<div class="csu-title">全景智能监控大屏 (Dashboard)</div>', unsafe_allow_html=True)
    
    # 核心技术指标看板
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div class="stat-card"><small>视觉轮轨接触点误差</small><br><b style="color:#22c55e; font-size:24px;">± 1.2 mm</b><br><small>目标：± 2.0 mm</small></div>', unsafe_allow_html=True)
    c2.markdown('<div class="stat-card"><small>铁鞋放置重复精度</small><br><b style="color:#22c55e; font-size:24px;">± 3.5 mm</b><br><small>目标：± 5.0 mm</small></div>', unsafe_allow_html=True)
    c3.markdown('<div class="stat-card"><small>在线防溜车/故障数</small><br><b style="color:#3b82f6; font-size:24px;">12 / 0 台</b><br><small>全站拓扑正常</small></div>', unsafe_allow_html=True)
    c4.markdown('<div class="stat-card"><small>紧急停机响应时长</small><br><b style="color:#1e293b; font-size:24px;">145 ms</b><br><small>目标：≤ 200 ms</small></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sub-title">单车精细化监控 (双重验证机制)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("📷 **视觉定位验证阶段 (亚像素级)**")
        st.write("顶部全局视觉：`已锁定` | 前后轮局部放取视觉：`对准中` | 当前照度：`850 Lux`")
        st.progress(0.85, text="视觉深度插入验证进度")
    with col2:
        st.success("⚙️ **压力传感器验证阶段**")
        st.write("车轮接触压力：`15.2 kN`")
        st.write("稳定时长：`2.4s (≥2s 合格)`")
        st.markdown("**综合判定：** ✅ 已到位 (双重验证通过)")

elif page == "🎛️ 模块二：智能调度联控中心":
    st.markdown('<div class="csu-title">智能调度联控中心 (全过程逻辑互锁)</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('**📝 标准化指令下发**')
        target_track = st.selectbox("目标股道", ["1道", "2道", "3道", "4道", "5道"])
        target_agv = st.selectbox("调动防溜车编号", ["AGV-01 (待机)", "AGV-02 (充电中)", "AGV-03 (待机)"])
        command = st.radio("执行指令", ["放铁鞋", "取铁鞋", "返回充电基地", "紧急停机"], horizontal=True)
        
        if st.button("🚀 下发任务指令", type="primary"):
            st.toast(f"指令已下发至 {target_agv}，正在进行互锁校验...")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('**🔒 放鞋前安全逻辑互锁状态**')
        st.checkbox("列车完全停稳且收到停车信号", value=True, disabled=True)
        st.checkbox("防溜车抵达指定位置", value=True, disabled=True)
        st.checkbox("视觉粗/精定位均已完成", value=True, disabled=True)
        st.checkbox("设备无故障且电量 > 20%", value=True, disabled=True)
        st.markdown('<div class="success-box">系统互锁已解除，允许执行作业指令。</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "📑 模块三：自动报表与产量分析":
    st.markdown('<div class="csu-title">自动报表与产量分析中心</div>', unsafe_allow_html=True)
    
    st.markdown("📈 **视觉与放置精度历史趋势**")
    chart_data = st.session_state.history_db[['视觉误差(mm)', '放置精度(mm)']]
    st.line_chart(chart_data)
    
    st.markdown("📑 **防溜作业记录表 (带唯一溯源编号)**")
    st.dataframe(st.session_state.history_db, use_container_width=True)
    
    st.download_button("📥 导出标准报表 (PDF/Excel)", data=st.session_state.history_db.to_csv().encode('utf-8'), file_name="report.csv")

elif page == "🚨 模块四：故障自诊断与报警":
    st.markdown('<div class="csu-title">故障自诊断与报警中心</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="alert-box"><b>[严重故障]</b> ERR-M01: 前轮旋转电机过载。位置：AGV-04。时间：刚刚。</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<div style="padding: 10px; border-radius: 5px; border-left: 5px solid #eab308; background: #fef9c3; color: #854d0e;"><b>[预警]</b> WARN-V02: 局部视觉传感器可见度降低 (镜头可能脏污)。位置：AGV-02。</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**🤖 智能诊断向导 (ERR-M01)**")
    st.write("- **可能原因 1：** 铁鞋被异物卡死，导致棘轮结构锁紧失败。")
    st.write("- **可能原因 2：** 电机驱动器反馈异常，电流超过 15A 阈值。")
    st.write("- **标准处理步骤：** 1. 触发紧急停机；2. 派遣人工前往 4道 查勘；3. 后台复位驱动器。")

elif page == "⚙️ 模块五：系统管理后台":
    st.markdown('<div class="csu-title">系统参数与权限配置</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown("**🔧 指标安全阈值设定**")
        st.slider("视觉误差容忍度 (mm)", 0.0, 5.0, 2.0, step=0.1)
        st.slider("强制回充最低电量 (%)", 0, 40, 20)
        st.slider("紧急停机响应时限 (ms)", 50, 500, 200)
        st.button("保存核心参数")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown("**👤 角色权限控制**")
        st.selectbox("当前登录角色", ["系统管理员 (全权限)", "调度员 (控制+报表)", "参观者 (仅查看)"])
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "🏆 模块六：竞赛展示专区":
    st.markdown('<div class="csu-title">✨ 交通运输科技大赛作品展示区</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="stat-card" style="border-top: 4px solid #3b82f6;">', unsafe_allow_html=True)
        st.markdown("### 💡 核心创新点归纳")
        st.write("1. **亚像素级视觉定位闭环**：突破传统机械盲放，识别精度达 ±2mm。")
        st.write("2. **视觉+压力双重防呆验证**：确保铁鞋100%卡扣到位，杜绝列车溜逸。")
        st.write("3. **全过程逻辑互锁设计**：故障导向安全，满足严苛的铁路安全标准。")
        st.write("4. **新能源自给自足架构**：基地与单车双重太阳能补能，开机率达 99.9%。")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="stat-card" style="border-top: 4px solid #10b981;">', unsafe_allow_html=True)
        st.markdown("### 💰 经济效益与推广模型")
        st.write("- **人工替代率**：单站可省去 4 名三班倒防溜作业员。")
        st.write("- **降本增效**：设备投资回报期（ROI）约为 1.5 年。")
        st.write("- **安全无价**：消除人员跨越股道作业带来的重大安全隐患。")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.info("📌 **评委演示提示**：请在左侧侧边栏切换各模块，体验完整的数据回溯与安全互锁机制。")
