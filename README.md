# AI助残求职辅助工具

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://empowered-by-technology-epkz76rmbhk5ccwflhtxla.streamlit.app/)
[![Deploy to Streamlit Cloud](https://github.com/lijinbo-max/Empowered-by-technology/actions/workflows/deploy.yml/badge.svg)](https://github.com/lijinbo-max/Empowered-by-technology/actions/workflows/deploy.yml)
[![Visitors](https://visitor-badge.laobi.icu/badge?page_id=lijinbo-max.Empowered-by-technology)](https://empowered-by-technology-epkz76rmbhk5ccwflhtxla.streamlit.app/)

## 项目概述

AI助残求职辅助工具是一款专为残障人士设计的求职辅助应用，旨在帮助残障人士更有效地寻找工作机会，提供平等的就业机会。该应用集成了AI技术，为用户提供简历分析、职位推荐和面试模拟等功能，同时注重无障碍设计，确保所有用户都能便捷使用。

## 功能特点

- **个人信息管理**：填写和管理个人基本信息、教育背景和工作经验
- **简历分析**：上传简历文件（支持txt和PDF格式），获取AI分析和优化建议
- **PDF文件预览**：支持PDF文件内容预览和提取
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
- **PDF处理**：PyPDF2
- **AI API**：GLM-4-Flash
- **AI SDK**：zai-sdk
- **部署**：Docker, GitHub Actions

## 安装和运行

### 方法一：本地运行

1. **克隆项目**
   ```bash
   git clone https://github.com/lijinbo-max/Empowered-by-technology.git
   cd AI
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   - 复制 `.env.example` 文件为 `.env`
   - 在 `.env` 文件中配置GLM-4-Flash API密钥

4. **运行应用**
   ```bash
   streamlit run app.py
   ```

### 方法二：Docker运行

1. **构建镜像**
   ```bash
   docker build -t ai-job-helper .
   ```

2. **运行容器**
   ```bash
   docker run -p 8501:8501 -e GLM4_API_KEY=<your-api-key> ai-job-helper
   ```

3. **或使用docker-compose**
   ```bash
   docker-compose up
   ```

## 在线部署

本项目已部署到Streamlit Cloud，您可以直接访问使用：
- **Streamlit Cloud**: https://empowered-by-technology-epkz76rmbhk5ccwflhtxla.streamlit.app/

## 登录测试

- **邮箱**：test@example.com
- **密码**：123456

## 项目结构

```
AI/
├── src/                          # 源代码目录
│   ├── ai_job_helper/            # Python包主目录
│   │   ├── __init__.py           # 包初始化文件
│   │   └── main.py               # 包入口文件
│   ├── app/                      # 应用代码
│   │   ├── auth/                 # 认证相关代码
│   │   │   ├── auth_service.py   # 认证服务
│   │   │   └── auth_utils.py     # 认证工具
│   │   ├── utils/                # 工具函数
│   │   │   ├── logger.py         # 日志工具
│   │   │   └── style.css         # 样式文件
│   │   └── main.py               # 主应用文件
│   ├── database/                 # 数据库相关代码
│   │   ├── migrations/           # 数据库迁移文件
│   │   │   ├── env.py            # 迁移环境配置
│   │   │   └── script.py.mako    # 迁移脚本模板
│   │   ├── __init__.py           # 数据库包初始化
│   │   └── models.py             # 数据库模型
├── tests/                        # 测试代码
│   ├── run_tests.py              # 运行测试的脚本
│   ├── test_auth_service.py      # 认证服务测试
│   └── test_auth_utils.py        # 认证工具测试
├── .github/                      # GitHub Actions配置
│   └── workflows/                # 工作流配置
│       ├── ci-cd.yml             # CI/CD配置
│       └── deploy.yml            # 部署配置
├── .postman/                     # Postman配置
│   └── resources.yaml            # Postman资源配置
├── postman/                      # Postman配置
│   └── globals/                  # 全局变量配置
│       └── workspace.globals.yaml # 工作区全局变量
├── Dockerfile                    # Docker配置
├── docker-compose.yml            # Docker Compose配置
├── pyproject.toml                # Python包配置
├── requirements.txt              # 依赖文件
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git忽略文件
├── alembic.ini                   # Alembic配置
├── api.py                        # API文件
├── app.py                        # 主应用入口
├── database.py                   # 数据库配置
├── LICENSE                       # 许可证文件
├── README.md                     # 项目说明
├── test_glm4.py                  # GLM-4-Flash API测试脚本
├── test_glm4.ps1                 # PowerShell测试脚本
└── test_glm4_fixed.ps1           # 修复后的测试脚本
```

## 依赖说明

项目依赖项已在 `requirements.txt` 文件中定义，包括：
- streamlit：用于构建Web应用
- sqlalchemy：ORM框架
- dotenv：环境变量管理
- passlib：密码加密
- pandas：数据处理
- numpy：数值计算
- requests：HTTP请求
- pyyaml：YAML配置解析
- alembic：数据库迁移
- streamlit-authenticator：身份验证
- PyPDF2：PDF文件处理
- zai-sdk：GLM-4-Flash API调用

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

## 贡献

欢迎提交Issue和Pull Request，共同改进这个项目。

## 联系方式

如果您有任何问题或建议，欢迎联系我们。