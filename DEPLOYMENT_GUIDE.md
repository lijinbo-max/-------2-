# Streamlit Cloud 部署指南

## 🔧 部署准备

### 1. 检查项目状态
- ✅ 所有代码已提交到 GitHub
- ✅ `requirements.txt` 包含所有必要依赖
- ✅ `.env.example` 配置了必要的环境变量

### 2. 部署步骤

**步骤 1: 访问 Streamlit Cloud**
- 打开浏览器，访问 [https://streamlit.io/cloud](https://streamlit.io/cloud)
- 点击 "Get started for free" 或 "Sign in"
- 使用 GitHub 账号登录

**步骤 2: 创建新应用**
- 登录后，点击右上角的 "New app" 按钮
- 或在仪表板页面点击 "Deploy an app"

**步骤 3: 配置应用**

| 配置项 | 值 |
|-------|-----|
| Repository | `lijinbo-max/Empowered-by-technology` |
| Branch | `main` |
| Main file path | `app.py` |
| App name | `empowered-by-technology` (或自定义名称) |

**步骤 4: 配置环境变量**
- 展开 "Advanced settings"
- 在 "Secrets" 部分，添加以下环境变量：
  ```
  GLM4_API_KEY=your-actual-api-key-here
  ```
- 点击 "Save"

**步骤 5: 部署应用**
- 点击 "Deploy!" 按钮
- Streamlit Cloud 会自动克隆仓库、安装依赖、启动应用
- 部署过程需要 1-5 分钟，耐心等待

## 📊 部署状态

**部署过程中**：
- 您会看到 "Deploying..." 状态
- 可以查看实时部署日志

**部署成功**：
- 状态会变为 "Running"
- 您会收到部署成功的通知
- 应用 URL 会显示在页面上（例如：`https://empowered-by-technology.streamlit.app`）

## 🔍 验证部署

1. **访问应用**：点击生成的 URL 访问部署的应用
2. **测试功能**：
   - 尝试注册/登录
   - 测试简历分析功能
   - 查看职位推荐
   - 测试无障碍功能
3. **检查日志**：如果遇到问题，查看部署日志了解详情

## ⚠️ 常见问题

### 1. 依赖安装失败
- **原因**：`requirements.txt` 中可能有缺失的依赖
- **解决**：确保所有依赖都正确列出，包括版本号

### 2. 环境变量未配置
- **原因**：`GLM4_API_KEY` 未设置
- **解决**：在 Secrets 中添加正确的 API 密钥

### 3. 应用崩溃
- **原因**：代码中可能有错误
- **解决**：查看部署日志，修复代码问题后重新部署

### 4. 数据库连接问题
- **原因**：SQLite 数据库在 Streamlit Cloud 上是临时的
- **解决**：对于生产环境，建议使用 PostgreSQL 等外部数据库

## 📝 部署后管理

### 更新应用
- 每次推送到 `main` 分支，Streamlit Cloud 会自动重新部署
- 无需手动操作，实现 CI/CD 自动部署

### 查看使用统计
- 在 Streamlit Cloud 仪表板查看应用访问量和使用情况
- 监控应用健康状态

### 自定义域名
- 升级到付费计划后，可以设置自定义域名
- 提升品牌形象

## 🎯 部署成功标准

- ✅ 应用成功启动并运行
- ✅ 所有核心功能正常工作
- ✅ 无障碍功能可用
- ✅ AI 模型集成正常
- ✅ 数据持久化正常（如适用）

## 📞 支持

如果部署过程中遇到问题：
1. 查看 [Streamlit Cloud 文档](https://docs.streamlit.io/streamlit-cloud)
2. 检查应用日志获取详细错误信息
3. 联系 Streamlit 支持团队
4. 或在项目 GitHub 仓库提交 Issue

---

**祝您部署成功！🚀**

应用部署完成后，您就可以通过生成的 URL 访问和使用 AI助残求职辅助工具了！