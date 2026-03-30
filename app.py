import streamlit as st
import os
from dotenv import load_dotenv
from database import init_db, get_session, User, PersonalInfo, Education, WorkExperience, JobPreference
from datetime import datetime

# 加载环境变量
load_dotenv()

# 初始化数据库
init_db()

# 页面配置
st.set_page_config(
    page_title="AI助残求职辅助工具",
    page_icon="🤝",
    layout="wide"
)

# 检测设备类型
def get_device_type():
    # 由于Streamlit的request属性可能不可用，使用默认值
    return 'desktop'

# 获取设备类型
device_type = get_device_type()
st.session_state.device_type = device_type

# 无障碍功能设置
if 'font_size' not in st.session_state:
    st.session_state.font_size = "中"
if 'contrast' not in st.session_state:
    st.session_state.contrast = "正常"
if 'screen_reader' not in st.session_state:
    st.session_state.screen_reader = False
if 'keyboard_shortcuts' not in st.session_state:
    st.session_state.keyboard_shortcuts = True

# 无障碍功能控制面板
with st.sidebar.expander("无障碍设置"):
    st.session_state.font_size = st.selectbox(
        "字体大小",
        ["小", "中", "大", "超大"],
        index=["小", "中", "大", "超大"].index(st.session_state.font_size),
        help="调整应用中所有文本的字体大小"
    )
    st.session_state.contrast = st.selectbox(
        "对比度",
        ["正常", "高对比度", "低对比度"],
        index=["正常", "高对比度", "低对比度"].index(st.session_state.contrast),
        help="调整应用的色彩对比度"
    )
    st.session_state.screen_reader = st.checkbox(
        "启用屏幕阅读器模式",
        value=st.session_state.screen_reader,
        help="优化应用以支持屏幕阅读器"
    )
    st.session_state.keyboard_shortcuts = st.checkbox(
        "启用键盘快捷键",
        value=st.session_state.keyboard_shortcuts,
        help="启用应用的键盘快捷键"
    )
    
    st.write("\n**键盘导航提示：**")
    st.write("- 使用Tab键在元素之间导航")
    st.write("- 使用Enter键选择或提交")
    st.write("- 使用箭头键在选项之间移动")
    
    if st.session_state.keyboard_shortcuts:
        st.write("\n**键盘快捷键：**")
        st.write("- Alt+1: 切换到首页")
        st.write("- Alt+2: 切换到个人信息")
        st.write("- Alt+3: 切换到简历分析")
        st.write("- Alt+4: 切换到职位推荐")
        st.write("- Alt+5: 切换到面试模拟")

# 根据无障碍设置调整样式
font_size_map = {
    "小": "0.8rem",
    "中": "1rem",
    "大": "1.2rem",
    "超大": "1.5rem"
}

contrast_map = {
    "正常": "",
    "高对比度": "filter: contrast(1.2); background-color: #000; color: #fff;",
    "低对比度": "filter: contrast(0.8);"
}

screen_reader_css = """
    /* 屏幕阅读器模式样式 */
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }
    /* 为所有元素添加 aria-label */
    button, input, select, textarea { aria-label: attr(placeholder); }
"""

st.markdown(
    f"""
    <style>
        body {{ 
            font-size: {font_size_map[st.session_state.font_size]}; 
            {contrast_map[st.session_state.contrast]}
        }}
        .stButton>button {{ 
            font-size: {font_size_map[st.session_state.font_size]}; 
            padding: 0.5rem 1rem;
            margin: 0.25rem 0;
        }}
        .stTextInput>div>div>input {{ 
            font-size: {font_size_map[st.session_state.font_size]}; 
            padding: 0.5rem;
        }}
        .stTextArea>div>div>textarea {{ 
            font-size: {font_size_map[st.session_state.font_size]}; 
            padding: 0.5rem;
        }}
        .stSelectbox>div>div>select {{ 
            font-size: {font_size_map[st.session_state.font_size]}; 
            padding: 0.5rem;
        }}
        .stDateInput>div>div>input {{ 
            font-size: {font_size_map[st.session_state.font_size]}; 
            padding: 0.5rem;
        }}
        .stNumberInput>div>div>input {{ 
            font-size: {font_size_map[st.session_state.font_size]}; 
            padding: 0.5rem;
        }}
        /* 提高链接和按钮的可访问性 */
        a, button {{ 
            outline: 2px solid transparent;
            transition: outline 0.2s ease;
        }}
        a:focus, button:focus {{ 
            outline: 2px solid #0066cc;
            outline-offset: 2px;
        }}
        /* 键盘导航指示 */
        .keyboard-nav-indicator {{ 
            position: fixed; 
            bottom: 10px; 
            right: 10px; 
            background: #333; 
            color: #fff; 
            padding: 5px 10px; 
            border-radius: 5px; 
            font-size: 12px; 
            z-index: 1000;
        }}
        {screen_reader_css if st.session_state.screen_reader else ""}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            /* 移动设备样式 */
            .stButton>button {{ 
                width: 100%;
                margin: 0.5rem 0;
            }}
            .stTextInput>div>div>input, 
            .stTextArea>div>div>textarea, 
            .stSelectbox>div>div>select, 
            .stDateInput>div>div>input, 
            .stNumberInput>div>div>input {{ 
                width: 100%;
            }}
            .stColumns {{ 
                flex-direction: column;
            }}
            .stColumn {{ 
                width: 100% !important;
                margin: 0.5rem 0;
            }}
            /* 调整侧边栏 */
            .css-1d391kg {{ 
                width: 100% !important;
                max-width: 100% !important;
            }}
            /* 调整主内容区 */
            .css-1lcbmhc {{ 
                padding: 1rem !important;
            }}
        }}
        
        /* 平板设备样式 */
        @media (min-width: 769px) and (max-width: 1024px) {{
            .stButton>button {{ 
                margin: 0.25rem;
            }}
            .stColumns {{ 
                flex-wrap: wrap;
            }}
            .stColumn {{ 
                width: 48% !important;
                margin: 0.5%;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# 添加键盘快捷键支持
if st.session_state.keyboard_shortcuts:
    st.markdown(
        """
        <script>
            document.addEventListener('keydown', function(e) {
                // Alt+1: 首页
                if (e.altKey && e.key === '1') {
                    e.preventDefault();
                    document.querySelector('input[value="首页"]').click();
                }
                // Alt+2: 个人信息
                else if (e.altKey && e.key === '2') {
                    e.preventDefault();
                    document.querySelector('input[value="个人信息"]').click();
                }
                // Alt+3: 简历分析
                else if (e.altKey && e.key === '3') {
                    e.preventDefault();
                    document.querySelector('input[value="简历分析"]').click();
                }
                // Alt+4: 职位推荐
                else if (e.altKey && e.key === '4') {
                    e.preventDefault();
                    document.querySelector('input[value="职位推荐"]').click();
                }
                // Alt+5: 面试模拟
                else if (e.altKey && e.key === '5') {
                    e.preventDefault();
                    document.querySelector('input[value="面试模拟"]').click();
                }
            });
        </script>
        """,
        unsafe_allow_html=True
    )

# 从数据库获取用户数据
def get_users_from_db():
    session = get_session()
    users = {}
    try:
        db_users = session.query(User).all()
        for user in db_users:
            users[user.email] = {
                "name": user.name,
                "password": user.password,
                "disabled": user.disabled
            }
    finally:
        session.close()
    return users

# 初始化测试用户
def init_test_user():
    session = get_session()
    try:
        # 检查是否已存在测试用户
        existing_user = session.query(User).filter_by(email="test@example.com").first()
        if not existing_user:
            # 创建测试用户
            test_user = User(
                email="test@example.com",
                name="测试用户",
                password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # 密码: 123456
                disabled=False
            )
            session.add(test_user)
            session.commit()
    finally:
        session.close()

# 初始化测试用户
init_test_user()

# 获取用户数据
users = get_users_from_db()

# 简单的登录表单
st.title("🤝 AI助残求职辅助工具")

# 登录表单
with st.form("login_form"):
    st.subheader("用户登录")
    email = st.text_input("邮箱")
    password = st.text_input("密码", type="password")
    login_button = st.form_submit_button("登录")

# 认证逻辑
if login_button:
    # 从数据库获取用户
    session = get_session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            # 简单的密码比较（实际项目中应使用哈希验证）
            if password == "123456":  # 测试密码
                st.session_state["authentication_status"] = True
                st.session_state["name"] = user.name
                st.session_state["username"] = user.email
                st.success(f"登录成功！欢迎回来，{user.name}！")
                # 重新加载页面
                st.rerun()
            else:
                st.error("密码错误")
        else:
            # 如果用户不存在，创建默认测试用户
            if email == "test@example.com" and password == "123456":
                new_user = User(
                    email="test@example.com",
                    name="测试用户",
                    password="123456",  # 实际项目中应使用哈希密码
                    disabled=False
                )
                session.add(new_user)
                session.commit()
                st.session_state["authentication_status"] = True
                st.session_state["name"] = "测试用户"
                st.session_state["username"] = "test@example.com"
                st.success("登录成功！欢迎使用AI助残求职辅助工具！")
                # 重新加载页面
                st.rerun()
            else:
                st.error("用户不存在")
    finally:
        session.close()

# 检查认证状态
if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    name = st.session_state["name"]
    username = st.session_state["username"]
    authentication_status = st.session_state["authentication_status"]
    # 主页面
    st.write(f"欢迎回来，{name}！")
    
    # 侧边栏导航
    st.sidebar.title("导航")
    page = st.sidebar.radio(
        "选择功能",
        ["首页", "个人信息", "简历分析", "职位推荐", "面试模拟"]
    )
    
    # 登出按钮
    if st.sidebar.button("退出"):
        st.session_state["authentication_status"] = False
        st.session_state.pop("name", None)
        st.session_state.pop("username", None)
        st.rerun()
    
    # 首页
    if page == "首页":
        st.header("欢迎使用AI助残求职辅助工具")
        st.write("本工具旨在帮助残障人士更有效地寻找工作机会，提供以下功能：")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📄 简历分析")
            st.write("AI智能分析您的简历，提供优化建议")
        
        with col2:
            st.subheader("🔍 职位推荐")
            st.write("根据您的技能和偏好推荐合适的职位")
        
        with col3:
            st.subheader("💬 面试模拟")
            st.write("模拟面试场景，提供反馈和改进建议")
    
    # 个人信息页面
    elif page == "个人信息":
        st.header("个人信息管理")
        
        # 获取用户ID
        session = get_session()
        try:
            user = session.query(User).filter_by(email=username).first()
            user_id = user.id
        finally:
            session.close()
        
        # 个人基本信息
        st.subheader("基本信息")
        # 从数据库获取个人信息
        session = get_session()
        try:
            personal_info = session.query(PersonalInfo).filter_by(user_id=user_id).first()
            phone = personal_info.phone if personal_info else ""
            disability_type = personal_info.disability_type if personal_info else "视力障碍"
            disability_level = personal_info.disability_level if personal_info else "一级"
        finally:
            session.close()
        
        with st.form("personal_info_form"):
            name = st.text_input("姓名", value=name)
            email = st.text_input("邮箱", value=username)
            phone = st.text_input("电话", value=phone)
            disability_type = st.selectbox(
                "残疾类型",
                ["视力障碍", "听力障碍", "言语障碍", "肢体障碍", "智力障碍", "精神障碍", "其他"],
                index=["视力障碍", "听力障碍", "言语障碍", "肢体障碍", "智力障碍", "精神障碍", "其他"].index(disability_type)
            )
            disability_level = st.selectbox(
                "残疾等级",
                ["一级", "二级", "三级", "四级"],
                index=["一级", "二级", "三级", "四级"].index(disability_level)
            )
            submitted = st.form_submit_button("保存信息")
            if submitted:
                # 保存个人信息到数据库
                session = get_session()
                try:
                    personal_info = session.query(PersonalInfo).filter_by(user_id=user_id).first()
                    if personal_info:
                        personal_info.phone = phone
                        personal_info.disability_type = disability_type
                        personal_info.disability_level = disability_level
                    else:
                        personal_info = PersonalInfo(
                            user_id=user_id,
                            phone=phone,
                            disability_type=disability_type,
                            disability_level=disability_level
                        )
                        session.add(personal_info)
                    # 更新用户姓名
                    user = session.query(User).filter_by(id=user_id).first()
                    user.name = name
                    session.commit()
                    st.success("个人信息保存成功！")
                finally:
                    session.close()
        
        # 教育背景
        st.subheader("教育背景")
        # 从数据库获取教育背景
        session = get_session()
        try:
            educations = session.query(Education).filter_by(user_id=user_id).all()
        finally:
            session.close()
        
        # 显示现有教育背景
        for edu in educations:
            with st.expander(f"{edu.school} - {edu.education_level}"):
                st.write(f"专业: {edu.major}")
                st.write(f"毕业年份: {edu.graduation_year}")
                if st.button(f"删除教育背景", key=f"delete_edu_{edu.id}"):
                    session = get_session()
                    try:
                        edu_to_delete = session.query(Education).filter_by(id=edu.id).first()
                        session.delete(edu_to_delete)
                        session.commit()
                        st.success("教育背景删除成功！")
                        st.rerun()
                    finally:
                        session.close()
        
        # 添加新教育背景
        with st.form("education_form"):
            education_level = st.selectbox(
                "学历",
                ["小学", "初中", "高中", "大专", "本科", "硕士", "博士"]
            )
            school = st.text_input("学校")
            major = st.text_input("专业")
            graduation_year = st.number_input("毕业年份", min_value=1990, max_value=2026, step=1)
            submitted = st.form_submit_button("保存教育信息")
            if submitted:
                # 保存教育背景到数据库
                session = get_session()
                try:
                    new_education = Education(
                        user_id=user_id,
                        education_level=education_level,
                        school=school,
                        major=major,
                        graduation_year=graduation_year
                    )
                    session.add(new_education)
                    session.commit()
                    st.success("教育信息保存成功！")
                finally:
                    session.close()
        
        # 工作经验
        st.subheader("工作经验")
        # 从数据库获取工作经验
        session = get_session()
        try:
            work_experiences = session.query(WorkExperience).filter_by(user_id=user_id).all()
        finally:
            session.close()
        
        # 显示现有工作经验
        for work in work_experiences:
            with st.expander(f"{work.company} - {work.position}"):
                st.write(f"开始日期: {work.start_date}")
                st.write(f"结束日期: {work.end_date}")
                st.write(f"工作职责: {work.responsibilities}")
                if st.button(f"删除工作经验", key=f"delete_work_{work.id}"):
                    session = get_session()
                    try:
                        work_to_delete = session.query(WorkExperience).filter_by(id=work.id).first()
                        session.delete(work_to_delete)
                        session.commit()
                        st.success("工作经验删除成功！")
                        st.rerun()
                    finally:
                        session.close()
        
        # 添加新工作经验
        with st.form("work_experience_form"):
            company = st.text_input("公司名称")
            position = st.text_input("职位")
            start_date = st.date_input("开始日期")
            end_date = st.date_input("结束日期")
            responsibilities = st.text_area("工作职责")
            submitted = st.form_submit_button("保存工作经验")
            if submitted:
                # 保存工作经验到数据库
                session = get_session()
                try:
                    new_work = WorkExperience(
                        user_id=user_id,
                        company=company,
                        position=position,
                        start_date=start_date,
                        end_date=end_date,
                        responsibilities=responsibilities
                    )
                    session.add(new_work)
                    session.commit()
                    st.success("工作经验保存成功！")
                finally:
                    session.close()
    
    # 简历分析页面
    elif page == "简历分析":
        st.header("简历分析与优化")
        
        # 简历上传
        st.subheader("上传简历")
        resume_file = st.file_uploader("选择简历文件", type=["txt", "pdf"])
        
        # 目标职位
        target_job = st.text_input("目标职位", placeholder="例如：前端开发工程师")
        
        if resume_file:
            st.success("简历上传成功！")
            
            # 显示简历内容
            st.subheader("简历内容")
            if resume_file.type == "text/plain":
                resume_content = resume_file.read().decode("utf-8")
                st.text_area("简历文本", resume_content, height=300)
            else:
                st.write("PDF文件内容预览功能开发中...")
            
            # AI分析按钮
            if st.button("开始AI分析"):
                st.info("AI正在分析您的简历...")
                
                # 集成通义千问API进行真实的简历分析
                try:
                    import requests
                    
                    # 获取API密钥
                    api_key = os.getenv("QIANWEN_API_KEY")
                    if not api_key:
                        st.error("请在.env文件中配置通义千问API密钥")
                    else:
                        # 构建分析提示
                        prompt = f"请分析以下简历，并针对目标职位'{target_job}'提供详细的分析结果，包括：\n1. 简历的优势\n2. 需要改进的地方\n3. 具体的优化建议\n4. 优化后的简历片段示例\n\n简历内容：\n{resume_content}"
                        
                        # 调用通义千问API
                        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_key}"
                        }
                        data = {
                            "model": "qwen-turbo",
                            "input": {
                                "prompt": prompt
                            },
                            "parameters": {
                                "temperature": 0.7
                            }
                        }
                        
                        response = requests.post(url, headers=headers, json=data)
                        response_data = response.json()
                        
                        if "output" in response_data and "text" in response_data["output"]:
                            # 显示分析结果
                            st.subheader("分析结果")
                            st.markdown(response_data["output"]["text"])
                            st.success("简历分析完成！")
                        else:
                            st.error(f"API调用失败: {response_data.get('message', '未知错误')}")
                        
                except Exception as e:
                    # 如果API调用失败，使用模拟结果
                    st.warning(f"AI分析暂时不可用，显示模拟分析结果: {str(e)}")
                    
                    # 模拟AI分析结果
                    st.subheader("分析结果")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 优势")
                        st.write("1. 教育背景完整，专业与目标职位匹配")
                        st.write("2. 工作经验丰富，有相关行业经验")
                        st.write("3. 技能清单全面，包含所需核心技能")
                    
                    with col2:
                        st.markdown("### 改进建议")
                        st.write("1. 增加具体的工作成果和量化指标")
                        st.write("2. 优化简历格式，使重点更加突出")
                        st.write("3. 添加与目标职位相关的项目经验")
                    
                    # 优化后的简历示例
                    st.subheader("优化建议示例")
                    st.text_area("优化后的简历片段", "**工作经验**\n\n**公司名称** - 职位 (2020-2023)\n- 负责项目管理，带领团队完成10+项目，成功率95%以上\n- 优化工作流程，提高效率30%\n- 获得年度优秀员工称号", height=200)
                    
                    st.success("简历分析完成！")
    
    # 职位推荐页面
    elif page == "职位推荐":
        st.header("职位推荐")
        
        # 获取用户ID
        session = get_session()
        try:
            user = session.query(User).filter_by(email=username).first()
            user_id = user.id
        finally:
            session.close()
        
        # 职位偏好设置
        st.subheader("职位偏好设置")
        # 从数据库获取职位偏好
        session = get_session()
        try:
            job_preference = session.query(JobPreference).filter_by(user_id=user_id).first()
            job_category = job_preference.job_category if job_preference else "IT/互联网"
            location = job_preference.location if job_preference else ""
            salary_range = job_preference.salary_range if job_preference else "5000-8000"
            work_type = job_preference.work_type if job_preference else "全职"
        finally:
            session.close()
        
        with st.form("job_preference_form"):
            job_category = st.selectbox(
                "职位类别",
                ["IT/互联网", "教育/培训", "金融/银行", "医疗/健康", "零售/销售", "行政/人事", "其他"],
                index=["IT/互联网", "教育/培训", "金融/银行", "医疗/健康", "零售/销售", "行政/人事", "其他"].index(job_category)
            )
            location = st.text_input("工作地点", value=location)
            salary_range = st.selectbox(
                "薪资范围",
                ["3000以下", "3000-5000", "5000-8000", "8000-12000", "12000以上"],
                index=["3000以下", "3000-5000", "5000-8000", "8000-12000", "12000以上"].index(salary_range)
            )
            work_type = st.selectbox(
                "工作类型",
                ["全职", "兼职", "实习", "远程"],
                index=["全职", "兼职", "实习", "远程"].index(work_type)
            )
            submitted = st.form_submit_button("保存偏好")
            if submitted:
                # 保存职位偏好到数据库
                session = get_session()
                try:
                    job_preference = session.query(JobPreference).filter_by(user_id=user_id).first()
                    if job_preference:
                        job_preference.job_category = job_category
                        job_preference.location = location
                        job_preference.salary_range = salary_range
                        job_preference.work_type = work_type
                    else:
                        job_preference = JobPreference(
                            user_id=user_id,
                            job_category=job_category,
                            location=location,
                            salary_range=salary_range,
                            work_type=work_type
                        )
                        session.add(job_preference)
                    session.commit()
                    st.success("职位偏好保存成功！")
                finally:
                    session.close()
        
        # 推荐职位列表
        st.subheader("推荐职位")
        
        # 职位搜索
        st.subheader("职位搜索")
        search_keyword = st.text_input("搜索关键词")
        search_location = st.text_input("搜索地点")
        search_button = st.button("搜索")
        
        # 从数据库获取职位数据
        session = get_session()
        try:
            from database import Job
            # 基本查询
            query = session.query(Job)
            
            # 应用搜索条件
            if search_keyword:
                query = query.filter(
                    (Job.title.ilike(f"%{search_keyword}%") | 
                     Job.description.ilike(f"%{search_keyword}%") |
                     Job.company.ilike(f"%{search_keyword}%"))
                )
            if search_location:
                query = query.filter(Job.location.ilike(f"%{search_location}%"))
            
            jobs = query.all()
            
            # 如果数据库中没有职位数据，添加更丰富的模拟数据
            if not jobs:
                # 添加更丰富的模拟职位数据
                mock_jobs = [
                    Job(
                        title="前端开发工程师",
                        company="科技有限公司",
                        location="北京",
                        salary="8000-12000",
                        description="负责公司网站和应用的前端开发，要求熟悉HTML、CSS、JavaScript等技术，有React或Vue开发经验优先。",
                        category="IT/互联网",
                        work_type="全职"
                    ),
                    Job(
                        title="后端开发工程师",
                        company="互联网科技公司",
                        location="上海",
                        salary="10000-15000",
                        description="负责服务器端应用开发，要求熟悉Java、Python或Node.js，有数据库设计经验。",
                        category="IT/互联网",
                        work_type="全职"
                    ),
                    Job(
                        title="行政助理",
                        company="商务服务公司",
                        location="广州",
                        salary="5000-8000",
                        description="负责公司日常行政事务，包括文件管理、会议安排、接待等，要求细心负责，有良好的沟通能力。",
                        category="行政/人事",
                        work_type="全职"
                    ),
                    Job(
                        title="客服专员",
                        company="电商平台",
                        location="深圳",
                        salary="3000-5000",
                        description="负责客户咨询和投诉处理，要求有良好的服务意识和沟通能力，能熟练使用办公软件。",
                        category="零售/销售",
                        work_type="全职"
                    ),
                    Job(
                        title="市场营销专员",
                        company="广告公司",
                        location="北京",
                        salary="6000-10000",
                        description="负责公司产品的市场推广和营销活动策划，要求有良好的市场敏感度和创意能力。",
                        category="零售/销售",
                        work_type="全职"
                    ),
                    Job(
                        title="教师",
                        company="教育培训中心",
                        location="上海",
                        salary="5000-9000",
                        description="负责中小学课程教学，要求有相关学科教学经验，有教师资格证优先。",
                        category="教育/培训",
                        work_type="全职"
                    ),
                    Job(
                        title="财务助理",
                        company="金融服务公司",
                        location="广州",
                        salary="4000-7000",
                        description="负责公司日常财务工作，包括账务处理、报表编制等，要求熟悉财务软件，有会计从业资格证。",
                        category="金融/银行",
                        work_type="全职"
                    ),
                    Job(
                        title="护士",
                        company="医院",
                        location="北京",
                        salary="4000-8000",
                        description="负责患者护理工作，要求有护士执业证书，有相关工作经验。",
                        category="医疗/健康",
                        work_type="全职"
                    ),
                    Job(
                        title="销售代表",
                        company="医疗器械公司",
                        location="上海",
                        salary="6000-12000",
                        description="负责公司产品的销售和推广，要求有良好的沟通能力和销售技巧，有相关行业经验优先。",
                        category="零售/销售",
                        work_type="全职"
                    ),
                    Job(
                        title="人事专员",
                        company="人力资源公司",
                        location="深圳",
                        salary="5000-8000",
                        description="负责人力资源管理工作，包括招聘、培训、绩效考核等，要求熟悉人力资源管理流程。",
                        category="行政/人事",
                        work_type="全职"
                    )
                ]
                for job in mock_jobs:
                    session.add(job)
                session.commit()
                # 重新查询
                jobs = query.all()
        finally:
            session.close()
        
        # 显示职位列表
        for job in jobs:
            # 计算匹配度（模拟）
            match_score = 80 + (hash(job.title) % 20)
            with st.expander(f"{job.title} - {job.company} (匹配度: {match_score}%)"):
                st.write(f"**工作地点:** {job.location}")
                st.write(f"**薪资范围:** {job.salary}")
                st.write(f"**职位描述:** {job.description}")
                st.button("申请职位", key=job.title)
        
        # 加载更多按钮
        if st.button("加载更多职位"):
            st.info("正在加载更多职位...")
    
    # 面试模拟页面
    elif page == "面试模拟":
        st.header("面试模拟与准备")
        
        # 面试类型选择
        st.subheader("面试类型")
        interview_type = st.selectbox(
            "选择面试类型",
            ["技术面试", "行为面试", "情景面试", "压力面试"]
        )
        
        # 面试岗位
        job_position = st.text_input("面试岗位")
        
        # 开始模拟面试
        if st.button("开始模拟面试"):
            st.info("面试模拟开始，请准备回答以下问题...")
            
            # 模拟面试问题
            questions = [
                "请简单介绍一下你自己",
                "你为什么对这个职位感兴趣？",
                "你认为自己的优势是什么？",
                "你如何应对工作中的挑战？",
                "你对我们公司有什么了解？"
            ]
            
            # 显示问题和回答区域
            for i, question in enumerate(questions, 1):
                st.subheader(f"问题 {i}: {question}")
                answer = st.text_area(f"你的回答 {i}", height=150, key=f"answer_{i}")
                
                if answer:
                    st.button(f"获取反馈 {i}", key=f"feedback_{i}")
            
            # 面试结束按钮
            if st.button("结束面试"):
                st.success("面试模拟结束！")
                st.subheader("面试反馈")
                st.write("1. 回答内容全面，条理清晰")
                st.write("2. 语言表达流畅，逻辑严谨")
                st.write("3. 对职位和公司有一定了解")
                st.write("4. 建议：可以增加更多具体的例子来支持你的观点")
        
        # 面试准备资源
        st.subheader("面试准备资源")
        st.write("### 常见面试问题")
        st.write("- 请介绍一下你自己")
        st.write("- 你为什么想加入我们公司？")
        st.write("- 你的优缺点是什么？")
        st.write("- 你如何处理工作中的冲突？")
        
        st.write("### 面试技巧")
        st.write("1. 提前了解公司和职位信息")
        st.write("2. 准备具体的例子来展示你的能力")
        st.write("3. 保持积极的态度和自信的形象")
        st.write("4. 注意倾听问题，思考后再回答")
    
    # 页脚
    st.markdown("---")
    st.write("© 2026 AI助残求职辅助工具 | 为残障人士提供平等的就业机会")

elif "authentication_status" in st.session_state and st.session_state["authentication_status"] == False:
    st.error("用户名或密码错误")
elif "authentication_status" not in st.session_state:
    st.warning("请输入用户名和密码")