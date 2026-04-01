# AI助残求职辅助工具

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://empowered-by-technology-epkz76rmbhk5ccwflhtxla.streamlit.app/)
[![Deploy to Streamlit Cloud](https://github.com/lijinbo-max/Empowered-by-technology/actions/workflows/deploy.yml/badge.svg)](https://github.com/lijinbo-max/Empowered-by-technology/actions/workflows/deploy.yml)
[![Visitors](https://visitor-badge.laobi.icu/badge?page_id=lijinbo-max.Empowered-by-technology)](https://empowered-by-technology-epkz76rmbhk5ccwflhtxla.streamlit.app/)

## 项目概述

AI助残求职辅助工具是一款专为残障人士设计的求职辅助应用，旨在帮助残障人士更有效地寻找工作机会，提供平等的就业机会。

## 功能特点

- **个人信息管理**：填写和管理个人基本信息、教育背景和工作经验
- **简历分析**：上传简历文件，获取AI分析和优化建议
- **职位推荐**：根据用户技能和偏好推荐合适的职位
- **面试模拟**：选择面试类型，进行模拟面试并获取反馈
- **无障碍功能**：调整字体大小、对比度和其他无障碍选项
- **数据安全**：使用密码哈希存储，确保用户数据安全
- **响应式设计**：适配不同屏幕尺寸的设备

## 技术栈

- **前端**：Streamlit
- **后端**：Python
- **数据库**：SQLite
- **ORM**：SQLAlchemy
- **密码加密**：Passlib
- **AI API**：通义千问
- **部署**：Docker, GitHub Actions

## 安装和运行

### 方法一：本地运行

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd ai-job-helper
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   - 复制 `.env.example` 文件为 `.env`
   - 在 `.env` 文件中配置通义千问API密钥

4. **运行应用**
   ```bash
   streamlit run src/app/main.py
   ```

### 方法二：Docker运行

1. **构建镜像**
   ```bash
   docker build -t ai-job-helper .
   ```

2. **运行容器**
   ```bash
   docker run -p 8501:8501 -e QIANWEN_API_KEY=<your-api-key> ai-job-helper
   ```

3. **或使用docker-compose**
   ```bash
   docker-compose up
   ```

### 方法三：安装为Python包

1. **安装包**
   ```bash
   pip install -e .
   ```

2. **运行应用**
   ```bash
   ai-job-helper
   ```

## 在线部署

本项目已部署到Streamlit Cloud，您可以直接访问使用：
- **Streamlit Cloud**: https://share.streamlit.io/lijinbo-max/-------2-

## 登录测试

- **邮箱**：test@example.com
- **密码**：123456

## 项目结构

```
ai-job-helper/
├── src/
│   ├── ai_job_helper/     # Python包主目录
│   │   ├── __init__.py    # 包初始化文件
│   │   └── main.py        # 包入口文件
│   ├── app/
│   │   ├── auth/          # 认证相关代码
│   │   ├── utils/         # 工具函数
│   │   ├── pages/         # 页面代码
│   │   └── main.py        # 主应用文件
│   ├── database/          # 数据库相关代码
│   │   ├── migrations/    # 数据库迁移文件
│   │   └── models.py      # 数据库模型
├── tests/                 # 测试代码
├── logs/                  # 日志文件
├── .github/               # GitHub Actions配置
├── Dockerfile             # Docker配置
├── docker-compose.yml     # Docker Compose配置
├── pyproject.toml         # Python包配置
├── requirements.txt       # 依赖文件
├── .env                   # 环境变量
├── LICENSE                # 许可证文件
└── README.md              # 项目说明
```

## 发布包

### 构建包
```bash
# 安装构建工具
pip install build

# 构建包
python -m build
```

### 发布到PyPI
```bash
# 安装发布工具
pip install twine

# 上传到PyPI
python -m twine upload dist/*
```

## 许可证

MIT License
