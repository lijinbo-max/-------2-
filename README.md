# AI助残求职辅助工具

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-Empowered--by--technology-blue?logo=github)](https://github.com/lijinbo-max/Empowered-by-technology)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 项目概述

AI助残求职辅助工具是一款专为残障人士设计的求职辅助应用，旨在帮助残障人士更有效地寻找工作机会，提供平等的就业机会。该应用集成了AI技术，为用户提供简历分析、职位推荐和面试模拟等功能，同时注重无障碍设计，确保所有用户都能便捷使用。

## 核心功能

### 用户管理
- **用户注册与登录**：支持邮箱注册和密码登录，使用Passlib进行密码加密
- **个人信息管理**：填写和管理个人基本信息、教育背景和工作经验
- **用户认证**：基于JWT的安全认证机制
- **自动登录**：注册成功后自动登录，提升用户体验

### 简历分析
- **简历上传**：支持txt和PDF格式文件上传
- **AI智能分析**：基于GLM-4-Flash大模型进行简历分析和优化建议
- **简历评分**：提供简历质量评分和改进建议

### 职位推荐
- **智能推荐**：根据用户技能和偏好推荐合适的职位
- **职位浏览**：查看职位详情、公司信息、薪资范围等
- **职位申请**：在线申请感兴趣的职位
- **URL参数编码**：安全的参数处理，防止特殊字符错误

### 面试模拟
- **多种面试类型**：支持技术面试、行为面试等多种类型
- **AI面试官**：基于GLM-4-Flash的AI面试官
- **面试反馈**：提供详细的面试表现分析和改进建议

### 无障碍功能
- **屏幕阅读器支持**：优化页面结构和标签，提高屏幕阅读器兼容性
- **语音导航**：集成Web Speech API，实现语音导航功能
- **文本到语音转换**：实现文本到语音的转换功能
- **语音输入**：支持语音输入，方便操作
- **键盘导航增强**：实现鼠标替代方案，增强键盘导航
- **字体调整**：提供多种字体大小和样式选项
- **高对比度模式**：实现高对比度显示模式
- **深色模式**：实现深色/浅色主题切换功能

### 企业版功能
- **企业用户管理**：支持企业用户注册和管理
- **团队协作**：创建和管理团队，共享资源
- **数据分析**：生成使用情况、性能和招聘报告
- **权限管理**：灵活的用户角色和权限控制

### 第三方服务集成
- **LinkedIn集成**：同步LinkedIn档案和职位
- **Indeed集成**：访问Indeed职位数据库
- **职业测评**：集成职业测评工具
- **技能认证**：管理技能认证记录
- **在线学习**：追踪在线学习课程进度

## 技术架构

### 后端技术栈
- **Python 3.9+**：主要编程语言
- **FastAPI**：高性能Web框架，提供RESTful API
- **SQLAlchemy**：ORM框架，支持SQLite和PostgreSQL
- **Alembic**：数据库迁移工具
- **Passlib**：密码加密库
- **PyPDF2**：PDF文件处理

### 前端技术栈
- **Streamlit**：Web应用框架，快速构建数据应用界面
- **CSS3**：自定义样式和动画效果
- **JavaScript**：无障碍功能实现

### 移动应用技术栈
- **Flutter**：跨平台移动应用开发框架
- **Provider**：状态管理
- **Dio/HTTP**：网络请求
- **SharedPreferences**：本地存储
- **环境配置**：支持开发/生产环境切换

### AI服务
- **GLM-4-Flash**：智谱AI大模型，用于简历分析、面试模拟等
- **zai-sdk**：智谱AI SDK

### 数据库
- **SQLite**：默认数据库，适合开发和轻量级部署
- **PostgreSQL**：可选数据库，适合生产环境

### 部署与运维
- **Docker**：容器化部署
- **GitHub Actions**：CI/CD自动化
- **Streamlit Cloud**：云部署平台

## 项目结构

```
AI/
├── app.py                      # Streamlit主应用入口
├── api.py                      # FastAPI RESTful API
├── api_manager.py              # API管理模块（错误重试、统计监控）
├── database.py                 # 数据库配置和模型
├── third_party_integration.py  # 第三方服务集成
├── test_glm4.py                # GLM-4-Flash API测试脚本
├── requirements.txt            # Python依赖
├── Dockerfile                  # Docker配置
├── docker-compose.yml          # Docker Compose配置
├── pyproject.toml              # Python包配置
├── alembic.ini                 # Alembic数据库迁移配置
├── .env.example                # 环境变量示例
├── .gitignore                 # Git忽略文件配置
├── src/                        # 源代码目录
│   ├── ai_job_helper/          # Python包
│   │   ├── __init__.py
│   │   └── main.py
│   ├── app/                    # 应用代码
│   │   ├── auth/               # 认证模块
│   │   │   ├── auth_service.py
│   │   │   └── auth_utils.py
│   │   ├── utils/              # 工具函数
│   │   │   ├── logger.py
│   │   │   └── style.css
│   │   └── main.py
│   └── database/               # 数据库模块
│       ├── __init__.py
│       ├── models.py           # 数据库模型定义
│       └── migrations/         # 数据库迁移文件
├── tests/                      # 测试代码
│   ├── run_tests.py
│   ├── test_auth_service.py
│   └── test_auth_utils.py
├── mobile_app/                 # Flutter移动应用
│   ├── lib/                    # Dart源代码
│   │   ├── main.dart           # 应用入口
│   │   ├── screens/            # 页面组件
│   │   │   ├── home_screen.dart
│   │   │   ├── login_screen.dart
│   │   │   ├── register_screen.dart
│   │   │   ├── profile_screen.dart
│   │   │   ├── job_recommendation_screen.dart
│   │   │   ├── interview_screen.dart
│   │   │   ├── feedback_screen.dart
│   │   │   ├── community_screen.dart
│   │   │   ├── third_party_services_screen.dart
│   │   │   └── enterprise_screen.dart
│   │   ├── models/             # 数据模型
│   │   │   ├── user.dart
│   │   │   ├── job.dart
│   │   │   ├── feedback.dart
│   │   │   ├── post.dart
│   │   │   └── third_party.dart
│   │   ├── services/           # 服务层
│   │   │   ├── auth_service.dart
│   │   │   ├── user_service.dart
│   │   │   ├── job_service.dart
│   │   │   ├── feedback_service.dart
│   │   │   ├── community_service.dart
│   │   │   └── third_party_service.dart
│   │   ├── providers/          # 状态管理
│   │   │   ├── auth_provider.dart
│   │   │   └── theme_provider.dart
│   │   ├── components/         # UI组件
│   │   │   ├── custom_card.dart
│   │   │   ├── loading_indicator.dart
│   │   │   └── message_snackbar.dart
│   │   ├── utils/              # 工具函数
│   │   │   ├── date_utils.dart
│   │   │   ├── network_utils.dart
│   │   │   └── storage_utils.dart
│   │   └── config/             # 配置文件
│   │       └── app_config.dart
│   ├── android/                # Android平台配置
│   ├── ios/                    # iOS平台配置
│   └── pubspec.yaml            # Flutter依赖配置
└── .github/workflows/          # GitHub Actions工作流
    ├── ci-cd.yml
    └── deploy.yml
```

## 数据库模型

### 核心模型
- **User**：用户基本信息（邮箱、姓名、密码等）
- **PersonalInfo**：个人详细信息（电话、残疾类型、残疾等级等）
- **Education**：教育背景（学校、专业、学历、毕业年份等）
- **WorkExperience**：工作经验（公司、职位、工作时间、职责等）
- **JobPreference**：职位偏好（行业、职位、薪资范围、工作地点等）
- **Job**：职位信息（标题、公司、地点、薪资、描述等）
- **Resume**：简历记录（内容、文件名、上传日期等）
- **Feedback**：用户反馈（类型、标题、内容、状态等）
- **CommunityPost**：社区帖子（标题、内容、浏览量、点赞数等）
- **CommunityComment**：社区评论
- **ThirdPartyIntegration**：第三方服务集成记录
- **CareerAssessment**：职业测评记录
- **SkillCertification**：技能认证记录
- **OnlineCourse**：在线学习课程记录
- **Company**：企业信息
- **CompanyUser**：企业用户关联
- **Team**：团队信息
- **TeamMember**：团队成员
- **SharedResource**：共享资源
- **AnalyticsReport**：数据分析报告
- **ActivityLog**：用户活动日志
- **FeatureUsage**：功能使用统计

## 快速开始

### 环境要求
- Python 3.9+
- pip
- Git

### 本地运行

1. **克隆项目**
   ```bash
   git clone https://github.com/lijinbo-max/Empowered-by-technology.git
   cd AI
   ```

2. **创建虚拟环境**（推荐）
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，添加GLM-4-Flash API密钥
   ```

5. **初始化数据库**
   ```bash
   # 数据库会自动初始化
   # 或使用Alembic进行迁移
   alembic upgrade head
   ```

6. **运行应用**
   ```bash
   # 运行Streamlit Web应用
   streamlit run app.py
   
   # 或运行FastAPI服务
   uvicorn api:app --reload
   ```

### Docker运行

1. **构建镜像**
   ```bash
   docker build -t ai-job-helper .
   ```

2. **运行容器**
   ```bash
   docker run -p 8501:8501 -e GLM4_API_KEY=<your-api-key> ai-job-helper
   ```

3. **使用Docker Compose**
   ```bash
   docker-compose up
   ```

## API文档

启动FastAPI服务后，访问以下地址查看API文档：
- **Swagger UI**：http://localhost:8000/docs
- **ReDoc**：http://localhost:8000/redoc

### 主要API端点

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | /api/register | 用户注册 |
| POST | /api/login | 用户登录 |
| GET | /api/user/{email} | 获取用户信息 |
| POST | /api/personal-info | 更新个人信息 |
| POST | /api/resume/analyze | 分析简历 |
| GET | /api/jobs | 获取职位列表 |
| POST | /api/jobs/apply | 申请职位 |
| POST | /api/interview/start | 开始面试模拟 |
| POST | /api/interview/answer | 提交面试答案 |
| POST | /api/feedback | 提交反馈 |
| GET | /api/community/posts | 获取社区帖子 |
| POST | /api/community/posts | 创建帖子 |
| POST | /api/community/comments | 添加评论 |
| GET | /api/third-party/integrations | 获取第三方集成 |
| POST | /api/third-party/integrate | 添加第三方集成 |
| DELETE | /api/third-party/integrate/{platform} | 删除第三方集成 |

## 移动应用开发

### 环境要求
- Flutter SDK 3.0+
- Dart SDK
- Android Studio / Xcode

### 运行移动应用

1. **进入移动应用目录**
   ```bash
   cd mobile_app
   ```

2. **安装依赖**
   ```bash
   flutter pub get
   ```

3. **运行应用**
   ```bash
   # 运行Android应用
   flutter run
   
   # 或指定设备
   flutter run -d <device_id>
   ```

### 构建发布版本

```bash
# Android APK
flutter build apk --release

# Android App Bundle
flutter build appbundle --release

# iOS
flutter build ios --release
```

## 测试

### 运行测试

```bash
# 运行所有测试
python tests/run_tests.py

# 或运行特定测试文件
python -m pytest tests/test_auth_service.py -v
python -m pytest tests/test_auth_utils.py -v
```

### 测试覆盖
- 用户认证测试
- 密码加密测试
- API接口测试

## 部署

### Streamlit Cloud部署

1. 将代码推送到GitHub仓库
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 点击 "New app" 或 "Deploy an app"
4. 选择仓库：`lijinbo-max/Empowered-by-technology`
5. 选择分支：`main`
6. 选择文件：`app.py`
7. 配置环境变量（GLM4_API_KEY）
8. 点击 "Deploy!"

**Streamlit Cloud 特点**：
- ✅ 一键部署
- ✅ 自动更新（每次git push）
- ✅ 完全免费
- ✅ HTTPS支持
- ✅ 自定义域名

### 生产环境部署

1. **使用Docker Compose**
   ```bash
   docker-compose -f docker-compose.yml --profile production up -d
   ```

2. **配置反向代理**（Nginx）
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

## 环境变量配置

创建 `.env` 文件并配置以下变量：

```env
# AI API密钥
GLM4_API_KEY=your_glm4_api_key_here

# 数据库配置
DATABASE_URL=sqlite:///job_helper.db
# 或使用PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/job_helper

# 应用配置
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your_secret_key_here

# 可选：云服务配置
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

## 安全特性

- **密码加密**：使用Passlib和bcrypt进行密码加密
- **JWT认证**：基于JWT的安全认证机制
- **空值检查**：完善的空值检查，防止空指针异常
- **参数编码**：URL参数编码，防止特殊字符错误
- **环境变量**：敏感信息存储在环境变量中
- **HTTPS支持**：生产环境强制HTTPS

## 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交Issue或联系项目维护者。

## 更新日志

### v1.1.0 (2026-04-03)
- 修复认证服务空值检查问题
- 修复调试模式检测逻辑错误
- 添加注册自动登录功能
- 完善登出状态清理
- 修复用户查询空值检查
- 优化Android签名配置
- 改进错误处理和日志记录
- 添加完整的移动应用结构
- 实现环境配置管理
- 支持URL参数编码

### v1.0.0 (2026-04-03)
- 初始版本发布
- 实现核心求职功能（简历分析、职位推荐、面试模拟）
- 添加无障碍功能支持
- 集成GLM-4-Flash大模型
- 支持Web和移动端
- 实现Docker部署和CI/CD流程
- 添加企业版功能
- 集成第三方服务
- 实现社区论坛功能
- 添加用户反馈系统

## 致谢

感谢以下技术和工具的支持：
- Streamlit - Web应用框架
- Flutter - 跨平台移动开发
- GLM-4-Flash - AI大模型服务
- SQLAlchemy - 数据库ORM
- FastAPI - Web框架
- Docker - 容器化部署