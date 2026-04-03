# AI助残求职辅助工具

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://empowered-by-technology-epkz76rmbhk5ccwflhtxla.streamlit.app/)
[![Deploy to Streamlit Cloud](https://github.com/lijinbo-max/Empowered-by-technology/actions/workflows/deploy.yml/badge.svg)](https://github.com/lijinbo-max/Empowered-by-technology/actions/workflows/deploy.yml)
[![Visitors](https://visitor-badge.laobi.icu/badge?page_id=lijinbo-max.Empowered-by-technology)](https://empowered-by-technology-epkz76rmbhk5ccwflhtxla.streamlit.app/)

## 项目概述

AI助残求职辅助工具是一款专为残障人士设计的求职辅助应用，旨在帮助残障人士更有效地寻找工作机会，提供平等的就业机会。该应用集成了AI技术，为用户提供简历分析、职位推荐和面试模拟等功能，同时注重无障碍设计，确保所有用户都能便捷使用。

## 功能特点

### 核心功能
- **个人信息管理**：填写和管理个人基本信息、教育背景和工作经验
- **简历分析**：上传简历文件（支持txt和PDF格式），获取AI分析和优化建议
- **PDF文件预览**：支持PDF文件内容预览和提取
- **职位推荐**：根据用户技能和偏好推荐合适的职位
- **面试模拟**：选择面试类型，进行模拟面试并获取反馈

### 无障碍功能
- **屏幕阅读器支持**：优化页面结构和标签，提高屏幕阅读器兼容性
- **语音导航**：集成Web Speech API，实现语音导航功能
- **文本到语音转换**：实现文本到语音的转换功能
- **语音输入**：支持语音输入，方便操作
- **键盘导航增强**：实现鼠标替代方案，增强键盘导航
- **眼动追踪支持**：添加眼动追踪支持框架
- **字体调整**：提供多种字体大小和样式选项
- **高对比度模式**：实现高对比度显示模式
- **自定义快捷键**：添加自定义快捷键设置
- **深色模式**：实现深色/浅色主题切换功能

### 技术改进
- **数据库优化**：
  - 实现数据备份和恢复功能
  - 优化数据库查询性能（VACUUM）
  - 支持切换到PostgreSQL数据库
- **云服务集成**：
  - 创建CloudStorage类，支持AWS S3、Google Cloud Storage和Azure Blob Storage
  - 实现云备份和恢复功能
- **API优化**：
  - 创建api_manager.py模块，实现错误重试机制（指数退避策略）
  - 添加API使用统计和监控功能
  - 实现API密钥安全管理
- **部署优化**：
  - 优化Dockerfile，减小镜像大小并提高构建速度
  - 添加CI/CD流程自动化（GitHub Actions）
  - 实现多环境部署支持（开发、测试、生产）

### 用户体验改进
- **界面设计改进**：
  - 实现现代卡片式布局
  - 优化移动端适配
  - 添加主题切换功能
  - 实现渐进式加载和动画效果
- **用户反馈机制**：
  - 添加用户反馈表单
  - 实现功能使用统计和分析
  - 建立用户社区和论坛功能

### 第三方服务集成
- **招聘平台集成**：
  - LinkedIn API集成（用户资料、职位搜索、职位申请）
  - Indeed API集成（职位搜索、职位详情）
- **职业测评服务**：
  - 创建职业测评（性格测试、职业兴趣测试、能力测试、价值观测试）
  - 提交测评答案并获取结果
  - 查看历史测评记录
- **技能认证服务**：
  - 获取可用的技能认证
  - 注册认证考试
  - 管理用户认证记录
- **在线学习平台**：
  - 搜索在线课程
  - 注册课程并跟踪学习进度
  - 管理用户课程记录

### 移动应用
- **跨平台开发**：使用Flutter框架开发iOS和Android应用
- **数据同步**：实现与Web版本的无缝同步
- **离线支持**：支持离线使用和数据同步
- **推送通知**：集成Firebase推送通知
- **无障碍功能**：移动端无障碍功能支持

### 企业版功能
- **企业管理**：
  - 创建和管理企业信息
  - 添加和管理企业用户
  - 用户角色管理（admin、manager、member）
- **团队协作**：
  - 创建和管理团队
  - 添加和管理团队成员
  - 团队成员角色管理
- **共享资源**：
  - 创建和管理共享资源（简历、模板、职位发布）
  - 团队资源共享
- **数据分析**：
  - 生成使用情况报告
  - 生成性能报告
  - 生成招聘报告
  - 查看历史报告

### 数据安全
- **密码哈希存储**：使用Passlib进行密码加密
- **API密钥管理**：安全的API密钥存储和管理
- **数据加密**：敏感数据加密存储
- **会话管理**：安全的用户会话管理

### 响应式设计
- **多设备适配**：适配不同屏幕尺寸的设备
- **移动端优化**：优化移动端用户体验
- **无障碍设计**：遵循WCAG无障碍标准

## 技术栈

### 前端
- **Streamlit**：Web应用框架
- **Flutter**：移动应用开发框架
- **React Native**：备选移动应用框架

### 后端
- **Python**：主要编程语言
- **SQLAlchemy**：ORM框架
- **Passlib**：密码加密

### 数据库
- **SQLite**：默认数据库
- **PostgreSQL**：可选数据库

### AI服务
- **GLM-4-Flash**：AI模型
- **zai-sdk**：AI SDK

### 云服务
- **AWS S3**：云存储
- **Google Cloud Storage**：云存储
- **Azure Blob Storage**：云存储
- **Firebase**：推送通知和实时数据库

### 第三方服务
- **LinkedIn API**：招聘平台集成
- **Indeed API**：招聘平台集成

### 部署
- **Docker**：容器化部署
- **GitHub Actions**：CI/CD自动化
- **Streamlit Cloud**：云部署平台

### 其他工具
- **PyPDF2**：PDF文件处理
- **dotenv**：环境变量管理
- **pandas**：数据处理
- **numpy**：数值计算
- **requests**：HTTP请求

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

### 方法三：多环境部署

1. **开发环境**
   ```bash
   docker-compose -f docker-compose.yml --profile development up
   ```

2. **测试环境**
   ```bash
   docker-compose -f docker-compose.yml --profile test up
   ```

3. **生产环境**
   ```bash
   docker-compose -f docker-compose.yml --profile production up
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
├── mobile_app/                   # 移动应用代码
│   ├── lib/                     # Flutter应用代码
│   ├── android/                 # Android平台代码
│   ├── ios/                     # iOS平台代码
│   └── pubspec.yaml             # Flutter依赖配置
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
├── api_manager.py                # API管理模块
├── app.py                        # 主应用入口
├── database.py                   # 数据库配置
├── third_party_integration.py     # 第三方服务集成
├── mobile_app_development.md     # 移动应用开发计划
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
- boto3：AWS S3 SDK
- google-cloud-storage：Google Cloud Storage SDK
- azure-storage-blob：Azure Blob Storage SDK

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

## 未来规划

### 已完成功能
- ✅ 无障碍功能增强（屏幕阅读器、语音导航、文本到语音、语音输入、键盘导航、眼动追踪）
- ✅ 个性化无障碍设置（字体调整、高对比度模式、自定义快捷键、深色模式）
- ✅ 数据库优化（数据备份恢复、查询优化、PostgreSQL支持）
- ✅ 云服务集成（AWS S3、Google Cloud Storage、Azure Blob Storage）
- ✅ API优化（错误重试、使用统计、密钥管理）
- ✅ 部署优化（Docker优化、CI/CD、多环境部署）
- ✅ 界面设计改进（卡片式布局、移动端适配、主题切换、动画效果）
- ✅ 用户反馈机制（反馈表单、功能统计、社区论坛）
- ✅ 第三方服务集成（LinkedIn、Indeed、职业测评、技能认证、在线学习）
- ✅ 移动应用开发计划（Flutter框架、完整功能模块）
- ✅ 企业版功能（企业管理、团队协作、共享资源、数据分析）

### 未来扩展方向
- **多语言支持**：实现国际化和本地化，支持多语言界面和内容
- **社交功能**：添加用户分享功能，实现简历和职位的社交分享
- **AI能力增强**：
  - 实现简历与职位的智能匹配
  - 添加行业趋势分析和技能需求预测
  - 提供个性化的职业发展建议
- **移动应用开发**：完成iOS和Android应用的开发和发布
- **企业版增强**：
  - 添加更多数据分析维度
  - 实现企业级安全审计
  - 提供API接口供企业集成

## 更新日志

### v2.0.0 (2026-04-03)
- 新增无障碍功能增强
- 新增第三方服务集成
- 新增企业版功能
- 新增移动应用开发计划
- 优化数据库和API性能
- 改进用户界面和体验
- 添加用户反馈和社区功能

### v1.0.0 (2026-03-01)
- 初始版本发布
- 实现核心求职功能
- 支持简历分析和职位推荐
- 添加面试模拟功能