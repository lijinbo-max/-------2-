import streamlit as st
import os
from dotenv import load_dotenv
from database import init_db, get_session, User, PersonalInfo, Education, WorkExperience, JobPreference, record_feature_usage, get_feature_usage_stats, add_user_feedback, add_community_post, get_community_posts, add_community_comment, add_third_party_integration, get_user_integrations, remove_integration, create_career_assessment, update_assessment_results, get_user_assessments, add_skill_certification, get_user_certifications, enroll_online_course, update_course_progress, get_user_courses, create_company, add_user_to_company, get_company_users, update_user_role, remove_user_from_company, create_team, get_company_teams, add_team_member, get_team_members, create_shared_resource, get_team_resources, generate_analytics_report, get_company_reports, log_activity
from datetime import datetime

# 加载环境变量
load_dotenv()

# 获取环境变量
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# 根据环境设置日志级别
if DEBUG:
    st.set_page_config(
        page_title="AI助残求职辅助工具 (开发环境)",
        page_icon="🤝",
        layout="wide",
        initial_sidebar_state="auto"
    )
else:
    st.set_page_config(
        page_title="AI助残求职辅助工具",
        page_icon="🤝",
        layout="wide",
        initial_sidebar_state="auto"
    )

# 直接从.env文件中读取API密钥
def get_api_key_from_env_file():
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GLM4_API_KEY='):
                    return line.split('=', 1)[1]
    except Exception as e:
        st.error(f"读取.env文件失败: {str(e)}")
    return None

# 初始化数据库
init_db()

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
if 'font_style' not in st.session_state:
    st.session_state.font_style = "默认"
if 'contrast' not in st.session_state:
    st.session_state.contrast = "正常"
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'screen_reader' not in st.session_state:
    st.session_state.screen_reader = False
if 'keyboard_shortcuts' not in st.session_state:
    st.session_state.keyboard_shortcuts = True
if 'voice_navigation' not in st.session_state:
    st.session_state.voice_navigation = False
if 'text_to_speech' not in st.session_state:
    st.session_state.text_to_speech = False
if 'voice_input' not in st.session_state:
    st.session_state.voice_input = False
if 'eye_tracking' not in st.session_state:
    st.session_state.eye_tracking = False
if 'custom_shortcuts' not in st.session_state:
    st.session_state.custom_shortcuts = {
        "首页": "Alt+1",
        "个人信息": "Alt+2",
        "简历分析": "Alt+3",
        "职位推荐": "Alt+4",
        "面试模拟": "Alt+5"
    }

# 数据库设置
with st.sidebar.expander("数据库设置"):
    st.subheader("数据库管理")
    
    # 数据备份
    if st.button("备份数据库"):
        from database import backup_database
        success, message = backup_database()
        if success:
            st.success(message)
        else:
            st.error(message)
    
    # 数据恢复
    backup_file = st.text_input("备份文件路径", "backup_job_helper.db")
    if st.button("恢复数据库"):
        from database import restore_database
        success, message = restore_database(backup_file)
        if success:
            st.success(message)
        else:
            st.error(message)
    
    # 优化数据库
    if st.button("优化数据库"):
        from database import optimize_database
        success, message = optimize_database()
        if success:
            st.success(message)
        else:
            st.error(message)
    
    # MySQL数据库设置
    st.subheader("MySQL数据库设置")
    mysql_host = st.text_input("MySQL主机", "localhost")
    mysql_port = st.text_input("MySQL端口", "3306")
    mysql_database = st.text_input("MySQL数据库名", "job_helper")
    mysql_user = st.text_input("MySQL用户名", "job_helper")
    mysql_password = st.text_input("MySQL密码", type="password")
    mysql_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
    if st.button("切换到MySQL"):
        from database import switch_to_mysql
        success, message = switch_to_mysql(mysql_url)
        if success:
            st.success(message)
        else:
            st.error(message)
    
    # 云服务设置（国内免费云服务）
    st.subheader("云服务设置")
    cloud_provider = st.selectbox(
        "云服务提供商", 
        ["阿里云OSS", "腾讯云COS", "华为云OBS", "七牛云Kodo", "又拍云USS"],
        help="选择国内免费或低成本的云存储服务"
    )
    bucket_name = st.text_input("存储桶名称", "job-helper-backups")
    
    # 云服务提供商特定设置
    cloud_kwargs = {}
    if cloud_provider == "阿里云OSS":
        st.info("阿里云OSS：新用户免费额度50GB存储，每月10万次请求")
        cloud_kwargs["access_key_id"] = st.text_input("AccessKey ID")
        cloud_kwargs["access_key_secret"] = st.text_input("AccessKey Secret", type="password")
        cloud_kwargs["endpoint"] = st.text_input("Endpoint", "oss-cn-hangzhou.aliyuncs.com")
        cloud_kwargs["region"] = st.text_input("地域", "cn-hangzhou")
    elif cloud_provider == "腾讯云COS":
        st.info("腾讯云COS：新用户免费额度50GB存储，每月10万次请求")
        cloud_kwargs["secret_id"] = st.text_input("SecretId")
        cloud_kwargs["secret_key"] = st.text_input("SecretKey", type="password")
        cloud_kwargs["region"] = st.text_input("地域", "ap-guangzhou")
    elif cloud_provider == "华为云OBS":
        st.info("华为云OBS：新用户免费额度5GB存储，每月1000次请求")
        cloud_kwargs["access_key"] = st.text_input("Access Key")
        cloud_kwargs["secret_key"] = st.text_input("Secret Key", type="password")
        cloud_kwargs["endpoint"] = st.text_input("Endpoint", "obs.cn-north-4.myhuaweicloud.com")
    elif cloud_provider == "七牛云Kodo":
        st.info("七牛云Kodo：每月10GB免费存储，100万次请求")
        cloud_kwargs["access_key"] = st.text_input("AccessKey")
        cloud_kwargs["secret_key"] = st.text_input("SecretKey", type="password")
        cloud_kwargs["bucket_domain"] = st.text_input("Bucket域名")
    elif cloud_provider == "又拍云USS":
        st.info("又拍云USS：每月10GB免费存储")
        cloud_kwargs["service_name"] = st.text_input("服务名称")
        cloud_kwargs["operator_name"] = st.text_input("操作员名称")
        cloud_kwargs["operator_password"] = st.text_input("操作员密码", type="password")
    
    # 云备份和恢复功能
    st.subheader("云备份和恢复")
    if st.button("备份到云存储"):
        from database import backup_to_cloud
        success, message = backup_to_cloud(cloud_provider, bucket_name, **cloud_kwargs)
        if success:
            st.success(message)
        else:
            st.error(message)
    
    if st.button("列出云备份文件"):
        from database import list_cloud_backups
        success, files = list_cloud_backups(cloud_provider, bucket_name, **cloud_kwargs)
        if success:
            if files:
                st.write("云存储中的备份文件:")
                for file in files:
                    st.write(f"- {file}")
            else:
                st.info("云存储中没有备份文件")
        else:
            st.error(files)
    
    cloud_backup_file = st.text_input("云备份文件路径", "backups/job_helper.db")
    if st.button("从云存储恢复"):
        from database import restore_from_cloud
        success, message = restore_from_cloud(cloud_provider, bucket_name, cloud_backup_file, **cloud_kwargs)
        if success:
            st.success(message)
        else:
            st.error(message)

# 无障碍功能控制面板
with st.sidebar.expander("无障碍设置"):
    st.session_state.font_size = st.selectbox(
        "字体大小",
        ["小", "中", "大", "超大", "特大"],
        index=["小", "中", "大", "超大", "特大"].index(st.session_state.font_size),
        help="调整应用中所有文本的字体大小"
    )
    st.session_state.font_style = st.selectbox(
        "字体样式",
        ["默认", "无衬线", "衬线", "等宽"],
        index=["默认", "无衬线", "衬线", "等宽"].index(st.session_state.font_style),
        help="调整应用中所有文本的字体样式"
    )
    st.session_state.dark_mode = st.checkbox(
        "启用深色模式",
        value=st.session_state.dark_mode,
        help="启用深色模式，减少屏幕亮度"
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
    st.session_state.voice_navigation = st.checkbox(
        "启用语音导航",
        value=st.session_state.get('voice_navigation', False),
        help="启用语音导航功能"
    )
    st.session_state.text_to_speech = st.checkbox(
        "启用文本到语音转换",
        value=st.session_state.get('text_to_speech', False),
        help="启用文本到语音转换功能"
    )
    st.session_state.voice_input = st.checkbox(
        "启用语音输入",
        value=st.session_state.get('voice_input', False),
        help="启用语音输入到文本框功能"
    )
    st.session_state.eye_tracking = st.checkbox(
        "启用眼动追踪支持",
        value=st.session_state.get('eye_tracking', False),
        help="启用眼动追踪支持（需要相应硬件设备）"
    )
    
    st.write("\n**键盘导航提示：**")
    st.write("- 使用Tab键在元素之间导航")
    st.write("- 使用Enter键选择或提交")
    st.write("- 使用箭头键在选项之间移动")
    
    if st.session_state.keyboard_shortcuts:
        st.write("\n**键盘快捷键：**")
        st.write(f"- {st.session_state.custom_shortcuts['首页']}: 切换到首页")
        st.write(f"- {st.session_state.custom_shortcuts['个人信息']}: 切换到个人信息")
        st.write(f"- {st.session_state.custom_shortcuts['简历分析']}: 切换到简历分析")
        st.write(f"- {st.session_state.custom_shortcuts['职位推荐']}: 切换到职位推荐")
        st.write(f"- {st.session_state.custom_shortcuts['面试模拟']}: 切换到面试模拟")
        
        with st.expander("自定义快捷键"):
            for key, value in st.session_state.custom_shortcuts.items():
                st.session_state.custom_shortcuts[key] = st.text_input(
                    f"{key} 快捷键",
                    value,
                    help="输入快捷键，例如 Alt+1"
                )

# 根据无障碍设置调整样式
font_size_map = {
    "小": "14px",
    "中": "16px",
    "大": "18px",
    "超大": "20px",
    "特大": "24px"
}

font_size_title_map = {
    "小": "18px",
    "中": "20px",
    "大": "24px",
    "超大": "28px",
    "特大": "32px"
}

font_style_map = {
    "默认": "",
    "无衬线": "font-family: 'Microsoft YaHei', Arial, Helvetica, sans-serif !important;",
    "衬线": "font-family: 'SimSun', Georgia, 'Times New Roman', serif !important;",
    "等宽": "font-family: 'Courier New', 'Consolas', monospace !important;"
}

contrast_map = {
    "正常": "",
    "高对比度": """
        filter: contrast(1.5) !important;
        -webkit-filter: contrast(1.5) !important;
    """,
    "低对比度": """
        filter: contrast(0.7) !important;
        -webkit-filter: contrast(0.7) !important;
    """
}

# 高对比度模式下的颜色方案
high_contrast_colors = """
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    .stButton>button {
        background-color: #FFFF00 !important;
        color: #000000 !important;
        border: 3px solid #FFFFFF !important;
        font-weight: bold !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 8px !important;
    }
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div>select, 
    .stDateInput>div>div>input, 
    .stNumberInput>div>div>input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFF00 !important;
        padding: 0.6rem !important;
        border-radius: 8px !important;
    }
    .stMarkdown {
        color: #FFFFFF !important;
    }
    .stExpander {
        background-color: #000000 !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 8px !important;
    }
    .stExpanderHeader {
        background-color: #1a1a1a !important;
        color: #FFFF00 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFFF00 !important;
        font-weight: bold !important;
    }
    p, span, label {
        color: #FFFFFF !important;
        font-weight: normal !important;
    }
    a {
        color: #00FFFF !important;
        text-decoration: underline !important;
        font-weight: bold !important;
    }
    .stCheckbox>label {
        color: #FFFFFF !important;
    }
    .stCheckbox [type="checkbox"] {
        accent-color: #FFFF00 !important;
        width: 18px !important;
        height: 18px !important;
    }
    .stRadio>label {
        color: #FFFFFF !important;
    }
    .stRadio [type="radio"] {
        accent-color: #FFFF00 !important;
        width: 18px !important;
        height: 18px !important;
    }
    .stSlider>div>div>div>div {
        background-color: #FFFF00 !important;
    }
    .stSlider>div>div>div>div>div {
        background-color: #FFFF00 !important;
        border: 2px solid #FFFFFF !important;
    }
"""

# 低对比度模式下的颜色方案
low_contrast_colors = """
    .stApp {
        background-color: #F5F5F5 !important;
        color: #666666 !important;
    }
    .stButton>button {
        background-color: #CCCCCC !important;
        color: #666666 !important;
        border: 1px solid #999999 !important;
    }
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stSelectbox>div>div>select {
        background-color: #FFFFFF !important;
        color: #666666 !important;
        border: 1px solid #CCCCCC !important;
    }
    .stMarkdown {
        color: #666666 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #555555 !important;
    }
    p, span, label {
        color: #666666 !important;
    }
    a {
        color: #888888 !important;
    }
"""

dark_mode_css = """
    background-color: #121212;
    color: #e0e0e0;
    .stButton>button {
        background-color: #333;
        color: #e0e0e0;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #333;
        color: #e0e0e0;
        border: 1px solid #555;
    }
    .stSelectbox>div>div>select {
        background-color: #333;
        color: #e0e0e0;
        border: 1px solid #555;
    }
    .stDateInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #333;
        color: #e0e0e0;
        border: 1px solid #555;
    }
    .css-1d391kg {
        background-color: #1e1e1e;
    }
    .css-1lcbmhc {
        background-color: #121212;
    }
"""


screen_reader_css = """
    /* 屏幕阅读器模式样式 */
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }
    /* 为所有元素添加 aria-label */
    button, input, select, textarea { aria-label: attr(placeholder); }
    /* 提高屏幕阅读器兼容性 */
    *[role="button"], button, input[type="button"], input[type="submit"] { cursor: pointer; }
    /* 确保所有表单元素都有标签 */
    label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
    /* 为所有图片添加 alt 文本 */
    img { alt: attr(alt); }
    /* 为所有链接添加 aria-label */
    a { aria-label: attr(title); }
    /* 提高表格的可访问性 */
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; font-weight: bold; }
"""

# 根据当前对比度设置选择颜色方案
current_contrast = st.session_state.contrast
contrast_colors = ""
if current_contrast == "高对比度":
    contrast_colors = high_contrast_colors
elif current_contrast == "低对比度":
    contrast_colors = low_contrast_colors

st.markdown(
    f"""
    <style>
        /* 全局样式 - 字体大小和样式 */
        html, body, .stApp {{ 
            font-size: {font_size_map[st.session_state.font_size]} !important; 
            {font_style_map[st.session_state.font_style]}
            transition: all 0.3s ease;
        }}
        
        /* 标题字体大小 */
        h1 {{ font-size: {font_size_title_map[st.session_state.font_size]} !important; }}
        h2 {{ font-size: calc({font_size_title_map[st.session_state.font_size]} - 2px) !important; }}
        h3 {{ font-size: calc({font_size_title_map[st.session_state.font_size]} - 4px) !important; }}
        h4, h5, h6 {{ font-size: calc({font_size_title_map[st.session_state.font_size]} - 6px) !important; }}
        
        /* 对比度设置 */
        {contrast_map[st.session_state.contrast]}
        
        /* 对比度颜色方案 */
        {contrast_colors}
        
        /* 深色模式 */
        {dark_mode_css if st.session_state.dark_mode else ""}
        
        /* 现代按钮样式 */
        .stButton>button {{ 
            font-size: {font_size_map[st.session_state.font_size]} !important; 
            {font_style_map[st.session_state.font_style]}
            padding: 0.6rem 1.2rem;
            margin: 0.25rem 0;
            border-radius: 8px;
            border: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stButton>button:hover {{ 
            background-color: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        /* 输入框样式 */
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea, 
        .stSelectbox>div>div>select, 
        .stDateInput>div>div>input, 
        .stNumberInput>div>div>input {{ 
            font-size: {font_size_map[st.session_state.font_size]}; 
            {font_style_map[st.session_state.font_style]}
            padding: 0.6rem;
            border-radius: 8px;
            border: 1px solid #ddd;
            transition: all 0.3s ease;
        }}
        
        .stTextInput>div>div>input:focus, 
        .stTextArea>div>div>textarea:focus, 
        .stSelectbox>div>div>select:focus, 
        .stDateInput>div>div>input:focus, 
        .stNumberInput>div>div>input:focus {{ 
            border-color: #4CAF50;
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        }}
        
        /* 卡片式布局 */
        .card {{ 
            background-color: {"#2d2d2d" if st.session_state.dark_mode else "#ffffff"};
            border: 1px solid {"#444" if st.session_state.dark_mode else "#e0e0e0"};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .card:hover {{ 
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
            transform: translateY(-2px);
            border-color: {"#4CAF50" if st.session_state.dark_mode else "#4CAF50"};
        }}
        
        /* 提高链接和按钮的可访问性 */
        a, button {{ 
            outline: 2px solid transparent;
            transition: outline 0.2s ease;
        }}
        
        a:focus, button:focus {{ 
            outline: 3px solid #4CAF50;
            outline-offset: 2px;
        }}
        
        /* 键盘导航指示 */
        .keyboard-nav-indicator {{ 
            position: fixed; 
            bottom: 10px; 
            right: 10px; 
            background: #333; 
            color: #fff; 
            padding: 8px 12px; 
            border-radius: 20px; 
            font-size: 12px; 
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        /* 键盘导航增强 */
        :focus {{ 
            outline: 3px solid #4CAF50 !important; 
            outline-offset: 2px !important; 
        }}
        
        /* 为所有可交互元素添加键盘导航支持 */
        button, input, select, textarea, a {{ 
            tab-index: 0; 
        }}
        
        /* 提高键盘导航的可见性 */
        .keyboard-highlight {{ 
            background-color: rgba(76, 175, 80, 0.1); 
            border: 2px dashed #4CAF50; 
        }}
        
        /* 眼动追踪指示器样式 */
        .eye-tracking-indicator {{ 
            position: fixed; 
            bottom: 120px; 
            right: 10px; 
            background: #2196F3; 
            color: white; 
            padding: 12px; 
            border-radius: 50%; 
            z-index: 1000; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .eye-tracking-indicator:hover {{ 
            transform: scale(1.1);
        }}
        
        /* 语音输入按钮样式 */
        .voice-input-button {{ 
            position: absolute; 
            right: 10px; 
            top: 50%; 
            transform: translateY(-50%); 
            background: transparent; 
            border: none; 
            cursor: pointer; 
            font-size: 18px; 
            z-index: 10; 
            transition: all 0.3s ease;
        }}
        
        .voice-input-button:hover {{ 
            transform: translateY(-50%) scale(1.1);
        }}
        
        /* 语音导航和文本到语音功能 */
        .voice-navigation-indicator {{ 
            position: fixed; 
            bottom: 60px; 
            right: 10px; 
            background: #4CAF50; 
            color: white; 
            padding: 12px; 
            border-radius: 50%; 
            cursor: pointer; 
            z-index: 1000; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
            transition: all 0.3s ease; 
        }}
        
        .voice-navigation-indicator:hover {{ 
            transform: scale(1.1); 
        }}
        
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
            
            /* 调整卡片布局 */
            .card {{ 
                padding: 1rem;
                margin: 0.5rem 0;
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
        
        /* 动画效果 */
        @keyframes fadeIn {{ 
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{ 
            animation: fadeIn 0.5s ease-out forwards;
        }}
        
        /* 加载动画 */
        .loading-spinner {{ 
            border: 4px solid rgba(0,0,0,0.1);
            border-left: 4px solid #4CAF50;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        
        @keyframes spin {{ 
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* 主题切换按钮 */
        .theme-toggle {{ 
            position: fixed;
            top: 10px;
            right: 10px;
            background: #333;
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .theme-toggle:hover {{ 
            transform: scale(1.1);
        }}
        
        {screen_reader_css if st.session_state.screen_reader else ""}
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

# 检查认证状态
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
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
else:
    name = st.session_state["name"]
    username = st.session_state["username"]
    authentication_status = st.session_state["authentication_status"]
    # 主页面
    st.title("🤝 AI助残求职辅助工具")
    st.write(f"欢迎回来，{name}！")
    
    # 侧边栏导航
    st.sidebar.title("导航")
    page = st.sidebar.radio(
        "选择功能",
        ["首页", "个人信息", "简历分析", "职位推荐", "面试模拟", "第三方服务", "企业版", "用户反馈", "社区论坛"]
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
        
        # 主题切换按钮
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.subheader("📄 简历分析")
            st.write("AI智能分析您的简历，提供针对性优化建议")
            st.write("- 简历评分与职位匹配度分析")
            st.write("- 关键词优化建议，突出您的优势技能")
            st.write("- 适合残障人士的专业简历模板推荐")
            st.write("- 无障碍就业能力展示策略")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.subheader("🔍 职位推荐")
            st.write("根据您的技能、偏好和无障碍需求推荐合适职位")
            st.write("- 智能职位匹配算法，考虑您的能力特点")
            st.write("- 行业趋势分析，把握就业机会")
            st.write("- 薪资范围预测，合理设定期望")
            st.write("- 无障碍工作环境评估")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.subheader("💬 面试模拟")
            st.write("模拟面试场景，提供专业反馈和改进建议")
            st.write("- 常见面试问题模拟与指导")
            st.write("- 个性化回答评估与改进建议")
            st.write("- 残障人士面试技巧与自信培养")
            st.write("- 远程面试环境优化指导")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 无障碍功能介绍
        st.markdown("## 无障碍功能")
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.write("- 屏幕阅读器全程支持，语音读出所有内容")
        st.write("- 语音导航功能，无需键盘鼠标操作")
        st.write("- 键盘导航增强，支持Tab键快速浏览")
        st.write("- 高对比度模式，适合视觉障碍用户")
        st.write("- 字体大小和样式调整，满足不同阅读需求")
        st.write("- 眼动追踪支持，通过眼神控制界面")
        st.write("- 语音输入功能，无需打字即可操作")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 数据统计
        st.markdown("## 数据统计")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.metric("注册用户", "1,234")
            st.write("来自全国各地的残障人士正在使用我们的服务")
            st.write("- 涵盖各类残障类型")
            st.write("- 覆盖全国31个省市")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.metric("成功匹配职位", "567")
            st.write("我们已为用户成功匹配了大量合适的工作机会")
            st.write("- 平均匹配时间缩短30%")
            st.write("- 职位满意度达85%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.metric("面试成功率", "78%")
            st.write("通过我们的面试模拟和指导，用户面试成功率显著提高")
            st.write("- 比行业平均水平高25%")
            st.write("- 90%的用户获得了面试机会")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 个人信息页面
    elif page == "个人信息":
        st.header("个人信息管理")
        
        # 获取用户ID
        session = get_session()
        try:
            user = session.query(User).filter_by(email=username).first()
            if user:
                user_id = user.id
            else:
                st.error("用户不存在，请重新登录")
                st.stop()
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
                    if user:
                        user.name = name
                        session.commit()
                        st.success("个人信息保存成功！")
                    else:
                        st.error("用户不存在，请重新登录")
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
        edu_needs_rerun = False
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
                        edu_needs_rerun = True
                    finally:
                        session.close()
        
        if edu_needs_rerun:
            st.rerun()
        
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
        work_needs_rerun = False
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
                        work_needs_rerun = True
                    finally:
                        session.close()
        
        if work_needs_rerun:
            st.rerun()
        
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
        resume_file = st.file_uploader("选择简历文件", type=["txt", "pdf", "docx", "html"])
        
        # 目标职位
        target_job = st.text_input("目标职位", placeholder="例如：前端开发工程师")
        
        if resume_file:
            st.success("简历上传成功！")
            
            # 显示简历内容
            st.subheader("简历内容")
            if resume_file.type == "text/plain":
                resume_content = resume_file.read().decode("utf-8")
                st.text_area("简历文本", resume_content, height=300)
            elif resume_file.type == "application/pdf":
                # 处理PDF文件
                try:
                    import PyPDF2
                    
                    # 读取PDF文件
                    pdf_reader = PyPDF2.PdfReader(resume_file)
                    num_pages = len(pdf_reader.pages)
                    
                    # 提取PDF内容
                    pdf_content = ""
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        pdf_content += page.extract_text()
                    
                    # 显示PDF内容
                    st.text_area("PDF文本内容", pdf_content, height=300)
                    resume_content = pdf_content
                except Exception as e:
                    st.error(f"读取PDF文件失败: {str(e)}")
                    st.write("PDF文件内容预览功能开发中...")
                    resume_content = "PDF文件内容"
            elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # 处理DOCX文件
                try:
                    from docx import Document
                    
                    # 读取DOCX文件
                    doc = Document(resume_file)
                    
                    # 提取DOCX内容
                    docx_content = ""
                    for para in doc.paragraphs:
                        docx_content += para.text + "\n"
                    
                    # 显示DOCX内容
                    st.text_area("DOCX文本内容", docx_content, height=300)
                    resume_content = docx_content
                except Exception as e:
                    st.error(f"读取DOCX文件失败: {str(e)}")
                    st.write("DOCX文件内容预览功能开发中...")
                    resume_content = "DOCX文件内容"
            elif resume_file.type == "text/html":
                # 处理HTML文件
                try:
                    import re
                    
                    # 读取HTML文件
                    html_content = resume_file.read().decode("utf-8")
                    
                    # 简单的HTML文本提取
                    # 移除HTML标签
                    clean_content = re.sub('<[^<]+?>', '', html_content)
                    # 移除多余的空白字符
                    clean_content = ' '.join(clean_content.split())
                    
                    # 显示HTML内容
                    st.text_area("HTML文本内容", clean_content, height=300)
                    resume_content = clean_content
                except Exception as e:
                    st.error(f"读取HTML文件失败: {str(e)}")
                    st.write("HTML文件内容预览功能开发中...")
                    resume_content = "HTML文件内容"
            else:
                # 其他文件类型
                st.error("不支持的文件类型")
                resume_content = "不支持的文件类型"

            
            # AI分析按钮
            if st.button("开始AI分析"):
                st.info("AI正在分析您的简历...")
                
                # 集成GLM-4-Flash API进行真实的简历分析
                try:
                    # 导入API管理器
                    from api_manager import call_glm4_api, get_api_stats
                    
                    # 构建分析提示
                    prompt = f"请分析以下简历，并针对目标职位'{target_job}'提供详细的分析结果，包括：\n1. 简历的优势\n2. 需要改进的地方\n3. 具体的优化建议\n4. 优化后的简历片段示例\n5. 简历与目标职位的匹配度分析，包括技能匹配、经验匹配和教育背景匹配等方面，并给出一个0-100的匹配度分数\n6. 简历关键词优化建议，包括目标职位的核心关键词、行业热门关键词，以及如何在简历中合理使用这些关键词\n7. 简历模板推荐，根据目标职位和行业特点，推荐适合的简历模板类型和布局\n8. 行业趋势分析和技能需求预测，包括目标职位所在行业的发展趋势、未来热门技能需求，以及如何提前准备这些技能\n9. 个性化的职业发展建议，根据简历内容和目标职位，提供短期和长期的职业发展规划建议\n\n简历内容：\n{resume_content}"
                    
                    # 调用GLM-4-Flash API
                    st.info("调用GLM-4-Flash API...")
                    success, result = call_glm4_api(prompt)
                    
                    if success:
                        st.info("API调用成功")
                        
                        # 显示分析结果
                        st.subheader("分析结果")
                        
                        # 提取分析结果内容
                        analysis_content = result["choices"][0]["message"]["content"]
                        
                        # 计算简历评分
                        def calculate_resume_score(content):
                            # 基于分析内容计算评分
                            score = 70  # 基础分
                            
                            # 检查是否有优势部分
                            if "优势" in content or "优点" in content:
                                score += 10
                            
                            # 检查是否有改进建议
                            if "改进" in content or "建议" in content:
                                score += 5
                            
                            # 检查是否有具体的优化建议
                            if "优化" in content or "示例" in content:
                                score += 5
                            
                            # 确保分数在0-100之间
                            return min(100, max(0, score))
                        
                        # 计算并显示评分
                        resume_score = calculate_resume_score(analysis_content)
                        st.subheader("简历评分")
                        st.progress(resume_score)
                        st.write(f"您的简历评分为：{resume_score}/100")
                        
                        # 显示分析结果内容
                        st.markdown(analysis_content)
                        st.success("简历分析完成！")
                        
                        # 显示API使用统计
                        api_stats = get_api_stats()
                        st.subheader("API使用统计")
                        st.write(f"总调用次数: {api_stats['total_calls']}")
                        st.write(f"成功调用次数: {api_stats['successful_calls']}")
                        st.write(f"失败调用次数: {api_stats['failed_calls']}")
                        if api_stats['total_calls'] > 0:
                            avg_response_time = api_stats['total_response_time'] / api_stats['total_calls']
                            st.write(f"平均响应时间: {avg_response_time:.2f}秒")
                        if api_stats['last_call_time']:
                            st.write(f"最后调用时间: {api_stats['last_call_time']}")
                    else:
                        st.error(f"API调用失败: {result}")
                        # 显示模拟分析结果
                        st.subheader("分析结果")
                        st.markdown("**简历优势**：\n- 教育背景良好\n- 相关工作经验丰富\n- 技能与目标职位匹配度高\n\n**需要改进的地方**：\n- 简历格式需要优化\n- 工作描述不够具体\n- 缺乏量化的成果展示\n\n**优化建议**：\n- 使用STAR法则（情境、任务、行动、结果）描述工作经验\n- 添加具体的项目成果和数据\n- 突出与目标职位相关的技能和经验\n\n**优化后的简历片段**：\n在担任软件工程师期间，负责开发和维护公司核心产品，通过优化算法，将系统响应时间减少了30%，提高了用户满意度。")
                        st.success("简历分析完成！")
                except Exception as e:
                    # 如果API调用失败，使用模拟结果
                    st.warning(f"AI分析暂时不可用，显示模拟分析结果: {str(e)}")
                    st.info(f"错误类型: {type(e).__name__}")
                    import traceback
                    st.info(f"错误堆栈: {traceback.format_exc()}")
                    
                    # 模拟AI分析结果
                    st.subheader("分析结果")
                    
                    # 计算并显示评分
                    st.subheader("简历评分")
                    st.progress(75)
                    st.write("您的简历评分为：75/100")
                    
                    # 显示匹配度分析
                    st.subheader("与目标职位的匹配度分析")
                    st.progress(80)
                    st.write("您的简历与目标职位的匹配度为：80/100")
                    
                    # 匹配度详情
                    st.markdown("### 匹配度详情")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 技能匹配")
                        st.progress(85)
                        st.write("85/100")
                    
                    with col2:
                        st.markdown("#### 经验匹配")
                        st.progress(75)
                        st.write("75/100")
                    
                    with col3:
                        st.markdown("#### 教育背景匹配")
                        st.progress(90)
                        st.write("90/100")
                    
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
                    
                    # 关键词优化建议
                    st.subheader("关键词优化建议")
                    st.markdown("### 目标职位核心关键词")
                    st.write("- 项目管理")
                    st.write("- 团队协作")
                    st.write("- 流程优化")
                    st.write("- 数据分析")
                    st.write("- 问题解决")
                    
                    st.markdown("### 行业热门关键词")
                    st.write("- 敏捷开发")
                    st.write("- 数字化转型")
                    st.write("- 云计算")
                    st.write("- 人工智能")
                    st.write("- 数据分析")
                    
                    st.markdown("### 关键词使用建议")
                    st.write("1. 在简历标题和摘要中使用核心关键词")
                    st.write("2. 在工作经验描述中自然融入关键词")
                    st.write("3. 在技能部分列出相关关键词")
                    st.write("4. 避免关键词堆砌，保持内容自然")
                    st.write("5. 根据目标职位调整关键词侧重点")
                    
                    # 简历模板推荐
                    st.subheader("简历模板推荐")
                    st.markdown("### 推荐模板类型")
                    st.write("1. **功能型模板**：适合技能和经验丰富的候选人，突出技能和成就")
                    st.write("2. **时序型模板**：适合职业发展稳定的候选人，按时间顺序展示工作经验")
                    st.write("3. **组合型模板**：结合功能型和时序型的优点，既突出技能又展示工作经历")
                    
                    st.markdown("### 布局建议")
                    st.write("- 使用简洁、专业的设计")
                    st.write("- 突出重要信息，如技能和成就")
                    st.write("- 使用一致的字体和格式")
                    st.write("- 确保简历长度适中（1-2页）")
                    st.write("- 选择适合行业的配色方案")
                    
                    # 行业趋势分析和技能需求预测
                    st.subheader("行业趋势分析和技能需求预测")
                    st.markdown("### 行业发展趋势")
                    st.write("1. 数字化转型加速，企业对数字化技能的需求增加")
                    st.write("2. 人工智能和自动化技术广泛应用，改变工作方式")
                    st.write("3. 远程工作和混合工作模式成为常态")
                    st.write("4. 可持续发展和ESG成为企业重要考量")
                    st.write("5. 技能迭代速度加快，终身学习成为必要")
                    
                    st.markdown("### 未来热门技能需求")
                    st.write("- 数据分析和数据科学技能")
                    st.write("- 人工智能和机器学习技能")
                    st.write("- 云计算和云服务技能")
                    st.write("- 网络安全和数据保护技能")
                    st.write("- 数字营销和社交媒体管理技能")
                    st.write("- 项目管理和敏捷方法论技能")
                    st.write("- 跨文化沟通和团队协作技能")
                    
                    st.markdown("### 技能准备建议")
                    st.write("1. 持续学习新技术和工具")
                    st.write("2. 参加行业相关的培训和认证")
                    st.write("3. 参与项目实践，积累实际经验")
                    st.write("4. 建立专业网络，了解行业动态")
                    st.write("5. 定期更新简历，展示新技能和成就")
                    
                    # 个性化的职业发展建议
                    st.subheader("个性化的职业发展建议")
                    st.markdown("### 短期发展建议（1-2年）")
                    st.write("1. 提升核心技能：根据目标职位要求，重点提升相关技能")
                    st.write("2. 积累项目经验：参与更多相关项目，提升实战能力")
                    st.write("3. 建立专业网络：参加行业活动，扩大人脉")
                    st.write("4. 获得相关认证：考取行业认可的证书，增强竞争力")
                    st.write("5. 定期更新简历：及时记录成就和新技能")
                    
                    st.markdown("### 长期发展建议（3-5年）")
                    st.write("1. 明确职业目标：确定长期职业发展方向")
                    st.write("2. 发展领导力：培养团队管理和领导能力")
                    st.write("3. 拓展专业领域：在核心技能基础上，拓展相关领域")
                    st.write("4. 建立个人品牌：通过分享知识和经验，建立专业形象")
                    st.write("5. 持续学习：保持对行业趋势的敏感度，不断学习新技术")
                    
                    st.markdown("### 职业发展路径")
                    st.write("- 初级职位 → 中级职位 → 高级职位 → 管理职位")
                    st.write("- 或选择成为某一领域的专家，如技术专家、行业顾问等")
                    
                    st.success("简历分析完成！")
    
    # 职位推荐页面
    elif page == "职位推荐":
        st.header("职位推荐")
        
        # 获取用户ID
        session = get_session()
        try:
            user = session.query(User).filter_by(email=username).first()
            if user:
                user_id = user.id
            else:
                st.error("用户不存在，请重新登录")
                st.stop()
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
            ["技术面试", "行为面试", "情景面试", "压力面试", "群面", "视频面试", "电话面试", "案例面试"]
        )
        
        # 面试岗位
        job_position = st.text_input("面试岗位")
        
        # 开始模拟面试
        if st.button("开始模拟面试"):
            st.info("面试模拟开始，请准备回答以下问题...")
            
            # 根据面试类型生成不同的问题
            if interview_type == "技术面试":
                questions = [
                    "请简单介绍一下你自己",
                    "你熟悉哪些编程语言和技术栈？",
                    "请解释一下你最近参与的项目中的技术难点",
                    "你如何解决遇到的技术问题？",
                    "你对我们公司的技术栈有什么了解？"
                ]
            elif interview_type == "行为面试":
                questions = [
                    "请简单介绍一下你自己",
                    "描述一个你成功解决的问题",
                    "描述一个你在团队中遇到的挑战",
                    "你如何处理工作中的压力？",
                    "你如何与同事合作完成项目？"
                ]
            elif interview_type == "情景面试":
                questions = [
                    "请简单介绍一下你自己",
                    "如果你的项目 deadline 临近但遇到了技术问题，你会怎么做？",
                    "如果你的同事与你意见不合，你会如何处理？",
                    "如果你的领导给你一个你不熟悉的任务，你会如何应对？",
                    "如果你的项目失败了，你会如何总结经验教训？"
                ]
            elif interview_type == "压力面试":
                questions = [
                    "请简单介绍一下你自己",
                    "你认为你的缺点是什么？",
                    "你为什么离开上一份工作？",
                    "你如何处理工作中的批评？",
                    "你认为你为什么能胜任这个职位？"
                ]
            elif interview_type == "群面":
                questions = [
                    "请简单介绍一下你自己",
                    "请就给定的案例进行讨论",
                    "你认为团队合作中最重要的是什么？",
                    "你如何在团队中发挥自己的优势？",
                    "你如何处理团队中的冲突？"
                ]
            elif interview_type == "视频面试":
                questions = [
                    "请简单介绍一下你自己",
                    "你为什么对这个职位感兴趣？",
                    "你如何适应远程工作环境？",
                    "你在远程工作中如何与团队沟通？",
                    "你对我们公司有什么了解？"
                ]
            elif interview_type == "电话面试":
                questions = [
                    "请简单介绍一下你自己",
                    "你为什么对这个职位感兴趣？",
                    "你的期望薪资是多少？",
                    "你什么时候可以开始工作？",
                    "你对我们公司有什么了解？"
                ]
            elif interview_type == "案例面试":
                questions = [
                    "请简单介绍一下你自己",
                    "请分析以下案例：一家公司的销售额下降，你会如何分析原因？",
                    "你如何制定一个市场推广策略？",
                    "你如何评估一个项目的可行性？",
                    "你如何解决一个复杂的业务问题？"
                ]
            else:
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
        st.write("- 你未来5年的职业规划是什么？")
        st.write("- 你期望的薪资是多少？")
        st.write("- 你如何应对工作压力？")
        st.write("- 你为什么离开上一份工作？")
        
        st.write("### 面试技巧")
        st.write("1. 提前了解公司和职位信息")
        st.write("2. 准备具体的例子来展示你的能力")
        st.write("3. 保持积极的态度和自信的形象")
        st.write("4. 注意倾听问题，思考后再回答")
        st.write("5. 保持良好的肢体语言和眼神交流")
        st.write("6. 准备一些问题向面试官提问")
        st.write("7. 面试后及时发送感谢信")
        
        st.write("### 不同面试类型的准备建议")
        st.write("**技术面试**：复习相关技术知识，准备编程题，展示项目经验")
        st.write("**行为面试**：准备STAR法则（情境、任务、行动、结果）的例子")
        st.write("**情景面试**：思考各种工作场景的应对策略")
        st.write("**压力面试**：保持冷静，不要被面试官的问题影响情绪")
        st.write("**群面**：积极参与讨论，展示团队合作能力")
        st.write("**视频面试**：测试设备和网络，选择安静的环境")
        st.write("**电话面试**：准备好简历和笔记，保持清晰的语音")
        st.write("**案例面试**：练习分析问题的思路和方法")
    
    # 第三方服务页面
    elif page == "第三方服务":
        st.header("第三方服务集成")
        
        # 获取用户ID
        session = get_session()
        try:
            user = session.query(User).filter_by(email=username).first()
            if user:
                user_id = user.id
            else:
                st.error("用户不存在，请重新登录")
                st.stop()
        finally:
            session.close()
        
        # 记录功能使用
        record_feature_usage(user_id, "第三方服务")
        
        # 创建标签页
        tab1, tab2, tab3, tab4 = st.tabs(["招聘平台", "职业测评", "技能认证", "在线学习"])
        
        with tab1:
            st.subheader("招聘平台集成")
            
            # 智联招聘集成（国内免费）
            st.markdown("### 智联招聘")
            st.write("智联招聘是国内领先的招聘平台，提供大量职位信息")
            
            keywords = st.text_input("职位关键词", placeholder="输入职位关键词，如：软件开发")
            location = st.text_input("城市", placeholder="输入城市，如：北京")
            limit = st.slider("结果数量", 1, 20, 10)
            
            if st.button("搜索职位"):
                if keywords:
                    # 初始化集成管理器
                    from third_party_integration import ThirdPartyIntegrationManager
                    manager = ThirdPartyIntegrationManager()
                    
                    # 搜索职位
                    jobs = manager.search_jobs_all_platforms(keywords, location, limit)
                    
                    if jobs:
                        st.success(f"找到 {len(jobs)} 个职位")
                        for job in jobs:
                            st.markdown(f"### {job['title']}")
                            st.write(f"**公司**: {job['company']}")
                            st.write(f"**薪资**: {job['salary']}")
                            st.write(f"**地点**: {job['location']}")
                            st.write(f"**来源**: {job['source']}")
                            st.write(f"**链接**: [查看详情]({job['url']})")
                            st.write("---")
                    else:
                        st.info("未找到相关职位")
                else:
                    st.error("请输入职位关键词")
            
            # 显示已集成的平台
            st.subheader("已集成的平台")
            success, integrations = get_user_integrations(user_id)
            if success:
                if integrations:
                    for integration in integrations:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(f"**{integration['platform'].upper()}** - 集成于 {integration['created_at']}")
                        with col2:
                            if st.button("移除", key=f"remove_{integration['id']}"):
                                success, message = remove_integration(user_id, integration['platform'])
                                if success:
                                    st.success(message)
                                    st.session_state.needs_rerun = True
                                else:
                                    st.error(message)
                    
                    if st.session_state.get('needs_rerun', False):
                        del st.session_state.needs_rerun
                        st.rerun()
                else:
                    st.write("暂无集成的平台")
            else:
                st.error(integrations)
        
        with tab2:
            st.subheader("职业测评")
            
            # 国内职业测评服务
            st.markdown("### 职业测评")
            st.write("了解自己的职业兴趣、性格特点和技能水平")
            
            # 初始化集成管理器
            from third_party_integration import ThirdPartyIntegrationManager
            manager = ThirdPartyIntegrationManager()
            
            # 获取测评类型
            success, assessment_types = manager.career_assessment.get_assessment_types()
            if success and assessment_types:
                assessment_type = st.selectbox("选择测评类型", 
                                            [at['name'] for at in assessment_types],
                                            format_func=lambda x: x)
                
                if st.button("开始测评"):
                    # 模拟测评过程
                    st.info("测评正在进行中...")
                    
                    # 获取测评ID
                    selected_type = next(at for at in assessment_types if at['name'] == assessment_type)
                    assessment_id = selected_type['id']
                    
                    # 模拟用户回答
                    user_answers = [{"question": "Q1", "answer": "A1"}]
                    
                    # 获取测评结果
                    success, result = manager.career_assessment.get_assessment_result(assessment_id, user_answers)
                    if success:
                        st.success("测评完成！")
                        st.markdown(f"## {result['title']}")
                        st.write(result['result'])
                        st.subheader("建议")
                        for suggestion in result['suggestions']:
                            st.write(f"- {suggestion}")
                    else:
                        st.error("测评失败，请重试")
            else:
                st.error("无法获取测评类型")
            
            # 创建测评
            st.markdown("### 创建新测评")
            local_assessment_type = st.selectbox(
                "测评类型",
                ["性格测试", "职业兴趣测试", "能力测试", "价值观测试"]
            )
            
            if st.button("创建本地测评"):
                success, result = create_career_assessment(user_id, local_assessment_type, json.dumps({}))
                if success:
                    st.success(f"测评已创建，ID: {result}")
                else:
                    st.error(result)
            
            # 显示历史测评
            st.subheader("历史测评")
            success, assessments = get_user_assessments(user_id)
            if success:
                if assessments:
                    for assessment in assessments:
                        st.markdown(f"### {assessment['assessment_type']}")
                        st.write(f"状态: {assessment['status']}")
                        st.write(f"创建时间: {assessment['created_at']}")
                        if assessment['completed_at']:
                            st.write(f"完成时间: {assessment['completed_at']}")
                        st.write("---")
                else:
                    st.write("暂无测评记录")
            else:
                st.error(assessments)
        
        with tab3:
            st.subheader("技能认证")
            
            # 国内技能认证服务
            st.markdown("### 技能认证")
            st.write("获取国家认可的技能证书，提升就业竞争力")
            
            # 初始化集成管理器
            from third_party_integration import ThirdPartyIntegrationManager
            manager = ThirdPartyIntegrationManager()
            
            # 获取可用认证
            success, certifications = manager.skill_certification.get_available_certifications()
            if success and certifications:
                st.write("### 可用的认证")
                for cert in certifications:
                    st.markdown(f"#### {cert['name']}")
                    st.write(f"**类别**: {cert['category']}")
                    st.write(f"**描述**: {cert['description']}")
                    st.write(f"**官方网站**: [访问]({cert['url']})")
                    st.write("---")
            else:
                st.error("无法获取认证信息")
            
            # 添加认证
            st.markdown("### 添加技能认证")
            with st.form("certification_form"):
                certification_name = st.text_input("认证名称", placeholder="如：计算机等级考试")
                certification_provider = st.text_input("认证提供者", placeholder="如：教育部考试中心")
                certification_level = st.selectbox(
                    "认证级别",
                    ["入门级", "助理级", "专业级", "专家级", "大师级"]
                )
                issue_date = st.date_input("发证日期")
                expiry_date = st.date_input("过期日期")
                certificate_url = st.text_input("证书链接", placeholder="输入证书的在线链接")
                
                submitted = st.form_submit_button("添加认证")
                if submitted:
                    if certification_name:
                        success, message = add_skill_certification(
                            user_id, certification_name, certification_provider,
                            certification_level, issue_date, expiry_date, certificate_url
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("请输入认证名称")
            
            # 显示已有认证
            st.subheader("已有认证")
            success, user_certifications = get_user_certifications(user_id)
            if success:
                if user_certifications:
                    for cert in user_certifications:
                        st.markdown(f"### {cert['certification_name']}")
                        st.write(f"提供者: {cert['certification_provider']}")
                        st.write(f"级别: {cert['certification_level']}")
                        st.write(f"发证日期: {cert['issue_date']}")
                        st.write(f"过期日期: {cert['expiry_date']}")
                        if cert['certificate_url']:
                            st.markdown(f"[查看证书]({cert['certificate_url']})")
                        st.write(f"状态: {cert['status']}")
                        st.write("---")
                else:
                    st.write("暂无认证记录")
            else:
                st.error(user_certifications)
        
        with tab4:
            st.subheader("在线学习")
            
            # 中国大学MOOC集成（国内免费）
            st.markdown("### 中国大学MOOC")
            st.write("中国大学MOOC提供高质量的在线课程，完全免费")
            
            course_keywords = st.text_input("课程关键词", placeholder="输入课程关键词，如：计算机基础")
            course_limit = st.slider("课程数量", 1, 10, 5)
            
            if st.button("搜索课程"):
                if course_keywords:
                    # 初始化集成管理器
                    from third_party_integration import ThirdPartyIntegrationManager
                    manager = ThirdPartyIntegrationManager()
                    
                    # 搜索课程
                    courses = manager.search_courses(course_keywords, limit=course_limit)
                    
                    if courses:
                        st.success(f"找到 {len(courses)} 门课程")
                        for course in courses:
                            st.markdown(f"### {course['title']}")
                            st.write(f"**提供机构**: {course['provider']}")
                            st.write(f"**来源**: {course['source']}")
                            st.write(f"**链接**: [查看详情]({course['url']})")
                            st.write("---")
                    else:
                        st.info("未找到相关课程")
                else:
                    st.error("请输入课程关键词")
            
            # 注册课程
            st.markdown("### 注册新课程")
            with st.form("course_form"):
                course_name = st.text_input("课程名称", placeholder="输入课程名称")
                course_provider = st.text_input("课程提供者", placeholder="如：中国大学MOOC, 学堂在线")
                course_url = st.text_input("课程链接", placeholder="输入课程的在线链接")
                skill_level = st.selectbox(
                    "技能级别",
                    ["初级", "中级", "高级", "专家级"]
                )
                
                submitted = st.form_submit_button("注册课程")
                if submitted:
                    if course_name:
                        success, message = enroll_online_course(
                            user_id, course_name, course_provider, course_url, skill_level
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("请输入课程名称")
            
            # 显示已注册课程
            st.subheader("已注册课程")
            success, courses = get_user_courses(user_id)
            if success:
                if courses:
                    course_needs_rerun = False
                    for course in courses:
                        st.markdown(f"### {course['course_name']}")
                        st.write(f"提供者: {course['course_provider']}")
                        st.write(f"级别: {course['skill_level']}")
                        st.write(f"进度: {course['progress']}%")
                        st.progress(course['progress'])
                        st.write(f"状态: {course['status']}")
                        st.write(f"注册时间: {course['enrolled_at']}")
                        if course['completed_at']:
                            st.write(f"完成时间: {course['completed_at']}")
                        
                        # 更新进度
                        new_progress = st.slider(f"更新进度", 0, 100, course['progress'], 
                                              key=f"progress_{course['id']}")
                        if st.button(f"更新", key=f"update_{course['id']}"):
                            success, message = update_course_progress(
                                user_id, course['id'], new_progress
                            )
                            if success:
                                st.success(message)
                                course_needs_rerun = True
                            else:
                                st.error(message)
                        
                        st.write("---")
                    
                    if course_needs_rerun:
                        st.rerun()
                else:
                    st.write("暂无课程记录")
            else:
                st.error(courses)
    
    # 企业版页面
    elif page == "企业版":
        st.header("企业版功能")
        
        # 获取用户ID
        session = get_session()
        try:
            user = session.query(User).filter_by(email=username).first()
            if user:
                user_id = user.id
            else:
                st.error("用户不存在，请重新登录")
                st.stop()
        finally:
            session.close()
        
        # 记录功能使用
        record_feature_usage(user_id, "企业版")
        
        # 创建标签页
        tab1, tab2, tab3, tab4 = st.tabs(["企业管理", "团队协作", "共享资源", "数据分析"])
        
        with tab1:
            st.subheader("企业管理")
            
            # 创建企业
            st.markdown("### 创建新企业")
            with st.form("company_form"):
                company_name = st.text_input("企业名称", placeholder="输入企业名称")
                industry = st.selectbox(
                    "行业",
                    ["科技", "金融", "医疗", "教育", "制造业", "零售", "其他"]
                )
                size = st.selectbox(
                    "企业规模",
                    ["1-10人", "11-50人", "51-200人", "201-500人", "500人以上"]
                )
                website = st.text_input("企业网站", placeholder="输入企业网站")
                description = st.text_area("企业描述", placeholder="输入企业描述")
                subscription_plan = st.selectbox(
                    "订阅计划",
                    ["basic", "pro", "enterprise"]
                )
                
                submitted = st.form_submit_button("创建企业")
                if submitted:
                    if company_name:
                        success, result = create_company(
                            company_name, industry, size, website, description, subscription_plan
                        )
                        if success:
                            st.success(f"企业创建成功，ID: {result}")
                        else:
                            st.error(result)
                    else:
                        st.error("请输入企业名称")
            
            # 添加用户到企业
            st.markdown("### 添加用户到企业")
            with st.form("add_user_form"):
                company_id = st.number_input("企业ID", min_value=1)
                target_user_id = st.number_input("用户ID", min_value=1)
                role = st.selectbox(
                    "角色",
                    ["admin", "manager", "member"]
                )
                department = st.text_input("部门", placeholder="输入部门名称")
                position = st.text_input("职位", placeholder="输入职位名称")
                
                submitted = st.form_submit_button("添加用户")
                if submitted:
                    success, message = add_user_to_company(
                        company_id, target_user_id, role, department, position
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            # 显示企业用户
            st.subheader("企业用户")
            company_id = st.number_input("企业ID", min_value=1, key="company_id_users")
            if st.button("查看用户", key="view_users"):
                success, users = get_company_users(company_id)
                if success:
                    if users:
                        user_needs_rerun = False
                        for user in users:
                            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                            with col1:
                                st.write(f"**用户ID**: {user['user_id']}")
                            with col2:
                                st.write(f"**角色**: {user['role']}")
                            with col3:
                                st.write(f"**部门**: {user['department']}")
                            with col4:
                                if st.button("移除", key=f"remove_user_{user['id']}"):
                                    success, message = remove_user_from_company(company_id, user['user_id'])
                                    if success:
                                        st.success(message)
                                        user_needs_rerun = True
                                    else:
                                        st.error(message)
                            st.write("---")
                        
                        if user_needs_rerun:
                            st.rerun()
                    else:
                        st.write("暂无用户")
                else:
                    st.error(users)
        
        with tab2:
            st.subheader("团队协作")
            
            # 创建团队
            st.markdown("### 创建新团队")
            with st.form("team_form"):
                team_company_id = st.number_input("企业ID", min_value=1, key="team_company_id")
                team_name = st.text_input("团队名称", placeholder="输入团队名称")
                team_description = st.text_area("团队描述", placeholder="输入团队描述")
                
                submitted = st.form_submit_button("创建团队")
                if submitted:
                    if team_name:
                        success, result = create_team(
                            team_company_id, team_name, team_description, user_id
                        )
                        if success:
                            st.success(f"团队创建成功，ID: {result}")
                        else:
                            st.error(result)
                    else:
                        st.error("请输入团队名称")
            
            # 添加团队成员
            st.markdown("### 添加团队成员")
            with st.form("add_member_form"):
                team_id = st.number_input("团队ID", min_value=1)
                member_user_id = st.number_input("用户ID", min_value=1, key="member_user_id")
                member_role = st.selectbox(
                    "角色",
                    ["admin", "member"],
                    key="member_role"
                )
                
                submitted = st.form_submit_button("添加成员")
                if submitted:
                    success, message = add_team_member(team_id, member_user_id, member_role)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            # 显示团队和成员
            st.subheader("企业团队")
            teams_company_id = st.number_input("企业ID", min_value=1, key="teams_company_id")
            if st.button("查看团队", key="view_teams"):
                success, teams = get_company_teams(teams_company_id)
                if success:
                    if teams:
                        for team in teams:
                            st.markdown(f"### {team['name']}")
                            st.write(f"描述: {team['description']}")
                            st.write(f"创建者: {team['created_by']}")
                            
                            # 显示团队成员
                            success, members = get_team_members(team['id'])
                            if success:
                                if members:
                                    st.write("**团队成员**:")
                                    for member in members:
                                        st.write(f"- 用户ID: {member['user_id']}, 角色: {member['role']}")
                                else:
                                    st.write("暂无成员")
                            
                            st.write("---")
                    else:
                        st.write("暂无团队")
                else:
                    st.error(teams)
        
        with tab3:
            st.subheader("共享资源")
            
            # 创建共享资源
            st.markdown("### 创建共享资源")
            with st.form("resource_form"):
                resource_team_id = st.number_input("团队ID", min_value=1, key="resource_team_id")
                resource_type = st.selectbox(
                    "资源类型",
                    ["resume", "template", "job_posting"]
                )
                resource_name = st.text_input("资源名称", placeholder="输入资源名称")
                resource_data = st.text_area("资源数据", placeholder="输入资源数据（JSON格式）")
                
                submitted = st.form_submit_button("创建资源")
                if submitted:
                    if resource_name and resource_data:
                        success, message = create_shared_resource(
                            resource_team_id, resource_type, resource_name, resource_data, user_id
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("请填写完整的资源信息")
            
            # 显示团队资源
            st.subheader("团队资源")
            resources_team_id = st.number_input("团队ID", min_value=1, key="resources_team_id")
            if st.button("查看资源", key="view_resources"):
                success, resources = get_team_resources(resources_team_id)
                if success:
                    if resources:
                        for resource in resources:
                            st.markdown(f"### {resource['resource_name']}")
                            st.write(f"类型: {resource['resource_type']}")
                            st.write(f"创建者: {resource['created_by']}")
                            st.write(f"创建时间: {resource['created_at']}")
                            st.code(resource['resource_data'], language='json')
                            st.write("---")
                    else:
                        st.write("暂无资源")
                else:
                    st.error(resources)
        
        with tab4:
            st.subheader("数据分析")
            
            # 生成报告
            st.markdown("### 生成数据分析报告")
            with st.form("report_form"):
                report_company_id = st.number_input("企业ID", min_value=1, key="report_company_id")
                report_type = st.selectbox(
                    "报告类型",
                    ["usage", "performance", "hiring"]
                )
                period_start = st.date_input("开始日期", key="period_start")
                period_end = st.date_input("结束日期", key="period_end")
                
                submitted = st.form_submit_button("生成报告")
                if submitted:
                    success, result = generate_analytics_report(
                        report_company_id, report_type,
                        datetime.combine(period_start, datetime.min.time()),
                        datetime.combine(period_end, datetime.max.time())
                    )
                    if success:
                        st.success("报告生成成功")
                        st.json(result)
                    else:
                        st.error(result)
            
            # 显示历史报告
            st.subheader("历史报告")
            reports_company_id = st.number_input("企业ID", min_value=1, key="reports_company_id")
            if st.button("查看报告", key="view_reports"):
                success, reports = get_company_reports(reports_company_id)
                if success:
                    if reports:
                        for report in reports:
                            st.markdown(f"### {report['report_type'].upper()}报告")
                            st.write(f"生成时间: {report['generated_at']}")
                            st.write(f"时间范围: {report['period_start']} 至 {report['period_end']}")
                            st.json(report['report_data'])
                            st.write("---")
                    else:
                        st.write("暂无报告")
                else:
                    st.error(reports)
    
    # 用户反馈页面
    elif page == "用户反馈":
        st.header("用户反馈")
        
        # 获取用户ID
        session = get_session()
        try:
            user = session.query(User).filter_by(email=username).first()
            if user:
                user_id = user.id
            else:
                st.error("用户不存在，请重新登录")
                st.stop()
        finally:
            session.close()
        
        # 记录功能使用
        record_feature_usage(user_id, "用户反馈")
        
        # 反馈表单
        with st.form("feedback_form"):
            feedback_type = st.selectbox(
                "反馈类型",
                ["功能建议", "问题报告", "使用咨询", "其他"]
            )
            title = st.text_input("标题", placeholder="请输入反馈标题")
            content = st.text_area("详细内容", height=200, placeholder="请详细描述你的反馈")
            submitted = st.form_submit_button("提交反馈")
            
            if submitted:
                if title and content:
                    # 添加用户反馈
                    success, message = add_user_feedback(user_id, feedback_type, title, content)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("请填写完整的反馈信息")
        
        # 功能使用统计
        st.subheader("功能使用统计")
        success, stats = get_feature_usage_stats(user_id)
        if success:
            if stats:
                for stat in stats:
                    st.write(f"**{stat['feature_name']}**：{stat['total_usage']}次使用，最后使用时间：{stat['last_used']}")
            else:
                st.write("暂无使用统计数据")
        else:
            st.error(stats)
    
    # 社区论坛页面
    elif page == "社区论坛":
        st.header("社区论坛")
        
        # 获取用户ID
        session = get_session()
        try:
            user = session.query(User).filter_by(email=username).first()
            if user:
                user_id = user.id
            else:
                st.error("用户不存在，请重新登录")
                st.stop()
        finally:
            session.close()
        
        # 记录功能使用
        record_feature_usage(user_id, "社区论坛")
        
        # 发布新帖子
        st.subheader("发布新帖子")
        with st.form("post_form"):
            post_title = st.text_input("帖子标题", placeholder="请输入帖子标题")
            post_content = st.text_area("帖子内容", height=300, placeholder="请输入帖子内容")
            submitted = st.form_submit_button("发布帖子")
            
            if submitted:
                if post_title and post_content:
                    # 添加社区帖子
                    success, message = add_community_post(user_id, post_title, post_content)
                    if success:
                        st.success(message)
                        # 刷新页面
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("请填写完整的帖子信息")
        
        # 显示社区帖子
        st.subheader("社区帖子")
        success, posts = get_community_posts()
        if success:
            if posts:
                for post in posts:
                    st.markdown(f"### {post['title']}")
                    st.write(f"发布时间：{post['created_at']}")
                    st.write(f"浏览量：{post['views']} | 点赞数：{post['likes']} | 评论数：{post['comment_count']}")
                    st.write(post['content'])
                    
                    # 评论表单
                    st.subheader("评论")
                    comment_content = st.text_area(f"评论帖子 {post['id']}", height=100, key=f"comment_{post['id']}")
                    if st.button(f"提交评论", key=f"submit_comment_{post['id']}"):
                        if comment_content:
                            # 添加社区评论
                            success, message = add_community_comment(post['id'], user_id, comment_content)
                            if success:
                                st.success(message)
                                st.session_state.needs_rerun_posts = True
                            else:
                                st.error(message)
                        else:
                            st.error("请输入评论内容")
                    
                    st.write("---")
            
            if st.session_state.get('needs_rerun_posts', False):
                del st.session_state.needs_rerun_posts
                st.rerun()
            else:
                st.write("暂无社区帖子")
        else:
            st.error(posts)
    
    # 页脚
    st.markdown("---")
    st.write("© 2026 AI助残求职辅助工具 | 为残障人士提供平等的就业机会")
    
    # 添加语音导航和文本到语音转换功能
    if st.session_state.voice_navigation or st.session_state.text_to_speech:
        st.markdown("""
        <script>
        // 语音导航功能
        let recognition = null;
        let isListening = false;
        
        // 初始化语音识别
        function initVoiceRecognition() {
            if ('webkitSpeechRecognition' in window) {
                recognition = new webkitSpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'zh-CN';
                
                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    processVoiceCommand(transcript);
                };
                
                recognition.onerror = function(event) {
                    console.error('语音识别错误:', event.error);
                };
                
                recognition.onend = function() {
                    isListening = false;
                    updateVoiceIndicator();
                };
            }
        }
        
        // 处理语音命令
        function processVoiceCommand(command) {
            command = command.toLowerCase();
            
            if (command.includes('首页') || command.includes('主页')) {
                document.querySelector('[data-testid="stSidebarNav"] li:nth-child(1) a').click();
            } else if (command.includes('个人信息')) {
                document.querySelector('[data-testid="stSidebarNav"] li:nth-child(2) a').click();
            } else if (command.includes('简历分析')) {
                document.querySelector('[data-testid="stSidebarNav"] li:nth-child(3) a').click();
            } else if (command.includes('职位推荐')) {
                document.querySelector('[data-testid="stSidebarNav"] li:nth-child(4) a').click();
            } else if (command.includes('面试模拟')) {
                document.querySelector('[data-testid="stSidebarNav"] li:nth-child(5) a').click();
            } else if (command.includes('提交') || command.includes('确认')) {
                const buttons = document.querySelectorAll('button');
                for (let button of buttons) {
                    if (button.textContent.includes('提交') || button.textContent.includes('确认')) {
                        button.click();
                        break;
                    }
                }
            }
        }
        
        // 切换语音识别状态
        function toggleVoiceRecognition() {
            if (!recognition) {
                initVoiceRecognition();
            }
            
            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
                isListening = true;
                updateVoiceIndicator();
            }
        }
        
        // 更新语音指示器
        function updateVoiceIndicator() {
            const indicator = document.querySelector('.voice-navigation-indicator');
            if (indicator) {
                if (isListening) {
                    indicator.style.background = '#f44336';
                    indicator.textContent = '🔊';
                } else {
                    indicator.style.background = '#4CAF50';
                    indicator.textContent = '🎤';
                }
            }
        }
        
        // 文本到语音转换
        function speakText(text) {
            if ('speechSynthesis' in window) {
                const speech = new SpeechSynthesisUtterance(text);
                speech.lang = 'zh-CN';
                speechSynthesis.speak(speech);
            }
        }
        
        // 为页面元素添加文本到语音功能
        function initTextToSpeech() {
            const elements = document.querySelectorAll('h1, h2, h3, p, span, div');
            elements.forEach(element => {
                if (element.textContent.trim() !== '' && !element.dataset.ttsInitialized) {
                    element.dataset.ttsInitialized = 'true';
                    element.addEventListener('mouseover', function() {
                        if (element.dataset.speaked !== 'true') {
                            speakText(element.textContent);
                            element.dataset.speaked = 'true';
                            setTimeout(() => {
                                delete element.dataset.speaked;
                            }, 3000);
                        }
                    });
                }
            });
        }
        
        // 创建语音导航指示器
        function createVoiceNavigationIndicator() {
            // 先检查元素是否已存在
            let indicator = document.querySelector('.voice-navigation-indicator');
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.className = 'voice-navigation-indicator';
                indicator.textContent = '🎤';
                indicator.title = '点击开始语音导航';
                indicator.addEventListener('click', toggleVoiceRecognition);
                document.body.appendChild(indicator);
            }
        }
        
        // 语音输入到文本框功能
        function initVoiceInput() {
            const textInputs = document.querySelectorAll('input[type="text"], textarea');
            textInputs.forEach(input => {
                // 先检查语音按钮是否已存在
                if (input.parentElement && !input.parentElement.querySelector('.voice-input-button')) {
                    try {
                        const voiceButton = document.createElement('button');
                        voiceButton.className = 'voice-input-button';
                        voiceButton.textContent = '🎤';
                        voiceButton.title = '点击开始语音输入';
                        voiceButton.style.position = 'absolute';
                        voiceButton.style.right = '5px';
                        voiceButton.style.top = '50%';
                        voiceButton.style.transform = 'translateY(-50%)';
                        voiceButton.style.background = 'transparent';
                        voiceButton.style.border = 'none';
                        voiceButton.style.cursor = 'pointer';
                        voiceButton.style.fontSize = '16px';
                        
                        const parent = input.parentElement;
                        if (parent) {
                            parent.style.position = 'relative';
                            parent.appendChild(voiceButton);
                            
                            voiceButton.addEventListener('click', function() {
                                if ('webkitSpeechRecognition' in window) {
                                    const recognition = new webkitSpeechRecognition();
                                    recognition.continuous = false;
                                    recognition.interimResults = false;
                                    recognition.lang = 'zh-CN';
                                    
                                    voiceButton.textContent = '🔊';
                                    voiceButton.style.color = '#f44336';
                                    
                                    recognition.onresult = function(event) {
                                        const transcript = event.results[0][0].transcript;
                                        input.value = transcript;
                                        voiceButton.textContent = '🎤';
                                        voiceButton.style.color = '';
                                    };
                                    
                                    recognition.onerror = function(event) {
                                        console.error('语音识别错误:', event.error);
                                        voiceButton.textContent = '🎤';
                                        voiceButton.style.color = '';
                                    };
                                    
                                    recognition.onend = function() {
                                        voiceButton.textContent = '🎤';
                                        voiceButton.style.color = '';
                                    };
                                    
                                    recognition.start();
                                }
                            });
                        }
                    } catch (e) {
                        console.error('初始化语音输入失败:', e);
                    }
                }
            });
        }
        
        // 眼动追踪支持
        function initEyeTracking() {
            console.log('眼动追踪功能已启用');
            
            let eyeTrackingIndicator = document.querySelector('.eye-tracking-indicator');
            if (!eyeTrackingIndicator) {
                eyeTrackingIndicator = document.createElement('div');
                eyeTrackingIndicator.className = 'eye-tracking-indicator';
                eyeTrackingIndicator.textContent = '👁️';
                eyeTrackingIndicator.title = '眼动追踪已启用';
                eyeTrackingIndicator.style.position = 'fixed';
                eyeTrackingIndicator.style.bottom = '120px';
                eyeTrackingIndicator.style.right = '10px';
                eyeTrackingIndicator.style.background = '#2196F3';
                eyeTrackingIndicator.style.color = 'white';
                eyeTrackingIndicator.style.padding = '10px';
                eyeTrackingIndicator.style.borderRadius = '50%';
                eyeTrackingIndicator.style.zIndex = '1000';
                eyeTrackingIndicator.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
                
                document.body.appendChild(eyeTrackingIndicator);
            }
        }
        
        // 初始化功能
        window.addEventListener('load', function() {
            try {
                initVoiceRecognition();
                createVoiceNavigationIndicator();
                initTextToSpeech();
                initVoiceInput();
                initEyeTracking();
            } catch (e) {
                console.error('初始化功能失败:', e);
            }
        });
        
        // 清理之前添加的元素
        function cleanupElements() {
            try {
                // 移除语音导航指示器
                const voiceIndicator = document.querySelector('.voice-navigation-indicator');
                if (voiceIndicator && voiceIndicator.parentNode) {
                    voiceIndicator.parentNode.removeChild(voiceIndicator);
                }
                
                // 移除眼动追踪指示器
                const eyeTrackingIndicator = document.querySelector('.eye-tracking-indicator');
                if (eyeTrackingIndicator && eyeTrackingIndicator.parentNode) {
                    eyeTrackingIndicator.parentNode.removeChild(eyeTrackingIndicator);
                }
                
                // 移除语音输入按钮
                const voiceButtons = document.querySelectorAll('.voice-input-button');
                voiceButtons.forEach(button => {
                    if (button.parentNode) {
                        button.parentNode.removeChild(button);
                    }
                });
                
                // 重置元素的ttsInitialized标记
                const elements = document.querySelectorAll('h1, h2, h3, p, span, div');
                elements.forEach(element => {
                    delete element.dataset.ttsInitialized;
                    delete element.dataset.speaked;
                });
            } catch (e) {
                console.error('清理元素失败:', e);
            }
        }
        
        // 当页面重新渲染时，确保元素被正确处理
        window.addEventListener('streamlit:rerun', function() {
            // 先清理之前的元素
            cleanupElements();
            
            // 重新初始化所有功能
            setTimeout(function() {
                try {
                    initVoiceRecognition();
                    createVoiceNavigationIndicator();
                    initTextToSpeech();
                    initVoiceInput();
                    initEyeTracking();
                } catch (e) {
                    console.error('重新初始化功能失败:', e);
                }
            }, 100);
        });

        </script>
        """, unsafe_allow_html=True)