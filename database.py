from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# 创建数据库引擎
engine = create_engine('sqlite:///job_helper.db', echo=True)

# 创建会话工厂
Session = sessionmaker(bind=engine)

# 创建基类
Base = declarative_base()

# 用户模型
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(200), nullable=False)
    disabled = Column(Boolean, default=False)
    
    # 关系
    personal_info = relationship('PersonalInfo', back_populates='user', uselist=False)
    education = relationship('Education', back_populates='user')
    work_experience = relationship('WorkExperience', back_populates='user')
    job_preferences = relationship('JobPreference', back_populates='user', uselist=False)
    feedback = relationship('Feedback', back_populates='user')
    community_posts = relationship('CommunityPost', back_populates='user')

# 个人信息模型
class PersonalInfo(Base):
    __tablename__ = 'personal_info'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone = Column(String(20))
    disability_type = Column(String(50))
    disability_level = Column(String(20))
    
    # 关系
    user = relationship('User', back_populates='personal_info')

# 教育背景模型
class Education(Base):
    __tablename__ = 'education'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    education_level = Column(String(50), nullable=False)
    school = Column(String(100), nullable=False)
    major = Column(String(100))
    graduation_year = Column(Integer)
    
    # 关系
    user = relationship('User', back_populates='education')

# 工作经验模型
class WorkExperience(Base):
    __tablename__ = 'work_experience'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    responsibilities = Column(Text)
    
    # 关系
    user = relationship('User', back_populates='work_experience')

# 职位偏好模型
class JobPreference(Base):
    __tablename__ = 'job_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_category = Column(String(50))
    location = Column(String(100))
    salary_range = Column(String(50))
    work_type = Column(String(50))
    
    # 关系
    user = relationship('User', back_populates='job_preferences')

# 职位模型
class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100))
    salary = Column(String(50))
    description = Column(Text)
    category = Column(String(50))
    work_type = Column(String(50))

# 简历模型
class Resume(Base):
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    file_name = Column(String(100))
    upload_date = Column(Date)

# 用户反馈模型
class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String(50), nullable=False)  # 反馈类型：bug, suggestion, question, etc.
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String(50), default='pending')  # 状态：pending, processing, resolved
    
    # 关系
    user = relationship('User', back_populates='feedback')

# 社区帖子模型
class CommunityPost(Base):
    __tablename__ = 'community_posts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    
    # 关系
    user = relationship('User', back_populates='community_posts')
    comments = relationship('CommunityComment', back_populates='post')

# 社区评论模型
class CommunityComment(Base):
    __tablename__ = 'community_comments'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('community_posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    post = relationship('CommunityPost', back_populates='comments')
    user = relationship('User')

# 功能使用统计模型
class FeatureUsage(Base):
    __tablename__ = 'feature_usage'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    feature_name = Column(String(100), nullable=False)
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime, default=datetime.now)
    
    # 关系
    user = relationship('User')

# 第三方服务集成模型
class ThirdPartyIntegration(Base):
    __tablename__ = 'third_party_integrations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    platform = Column(String(50), nullable=False)  # 平台名称：linkedin, indeed, etc.
    access_token = Column(Text)  # 访问令牌
    refresh_token = Column(Text)  # 刷新令牌
    token_expires_at = Column(DateTime)  # 令牌过期时间
    integration_data = Column(Text)  # 其他集成数据（JSON格式）
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    user = relationship('User')

# 职业测评记录模型
class CareerAssessment(Base):
    __tablename__ = 'career_assessments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assessment_type = Column(String(50), nullable=False)  # 测评类型
    assessment_data = Column(Text)  # 测评数据（JSON格式）
    results = Column(Text)  # 测评结果（JSON格式）
    status = Column(String(50), default='pending')  # 状态：pending, completed, failed
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    
    # 关系
    user = relationship('User')

# 技能认证记录模型
class SkillCertification(Base):
    __tablename__ = 'skill_certifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    certification_name = Column(String(200), nullable=False)
    certification_provider = Column(String(100))  # 认证提供者
    certification_level = Column(String(50))  # 认证级别
    issue_date = Column(Date)
    expiry_date = Column(Date)
    certificate_url = Column(String(500))  # 证书链接
    status = Column(String(50), default='active')  # 状态：active, expired, revoked
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    user = relationship('User')

# 在线学习课程记录模型
class OnlineCourse(Base):
    __tablename__ = 'online_courses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_name = Column(String(200), nullable=False)
    course_provider = Column(String(100))  # 课程提供者
    course_url = Column(String(500))  # 课程链接
    skill_level = Column(String(50))  # 技能级别
    progress = Column(Integer, default=0)  # 进度百分比
    status = Column(String(50), default='enrolled')  # 状态：enrolled, in_progress, completed
    enrolled_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    
    # 关系
    user = relationship('User')

# 企业模型
class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    industry = Column(String(100))
    size = Column(String(50))  # 企业规模
    website = Column(String(200))
    description = Column(Text)
    subscription_plan = Column(String(50), default='basic')  # 订阅计划：basic, pro, enterprise
    subscription_expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    users = relationship('CompanyUser', back_populates='company')
    teams = relationship('Team', back_populates='company')

# 企业用户关联模型
class CompanyUser(Base):
    __tablename__ = 'company_users'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String(50), default='member')  # 角色：admin, manager, member
    department = Column(String(100))
    position = Column(String(100))
    joined_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # 关系
    company = relationship('Company', back_populates='users')
    user = relationship('User')

# 团队模型
class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    company = relationship('Company', back_populates='teams')
    members = relationship('TeamMember', back_populates='team')
    shared_resources = relationship('SharedResource', back_populates='team')

# 团队成员模型
class TeamMember(Base):
    __tablename__ = 'team_members'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String(50), default='member')  # 角色：admin, member
    joined_at = Column(DateTime, default=datetime.now)
    
    # 关系
    team = relationship('Team', back_populates='members')
    user = relationship('User')

# 共享资源模型
class SharedResource(Base):
    __tablename__ = 'shared_resources'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    resource_type = Column(String(50), nullable=False)  # 资源类型：resume, template, job_posting
    resource_name = Column(String(200), nullable=False)
    resource_data = Column(Text)  # 资源数据（JSON格式）
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    team = relationship('Team', back_populates='shared_resources')
    creator = relationship('User')

# 数据分析报告模型
class AnalyticsReport(Base):
    __tablename__ = 'analytics_reports'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    report_type = Column(String(50), nullable=False)  # 报告类型：usage, performance, hiring
    report_data = Column(Text)  # 报告数据（JSON格式）
    generated_at = Column(DateTime, default=datetime.now)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    
    # 关系
    company = relationship('Company')

# 用户活动日志模型
class ActivityLog(Base):
    __tablename__ = 'activity_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    activity_type = Column(String(50), nullable=False)  # 活动类型：login, resume_analysis, job_search, etc.
    activity_data = Column(Text)  # 活动数据（JSON格式）
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    user = relationship('User')
    company = relationship('Company')

# 创建所有表
def init_db():
    Base.metadata.create_all(engine)

# 获取数据库会话
def get_session():
    return Session()

# 数据备份功能
def backup_database(backup_path='backup_job_helper.db'):
    """备份数据库到指定路径"""
    import shutil
    import os
    
    try:
        # 复制数据库文件
        shutil.copy('job_helper.db', backup_path)
        return True, f"数据库备份成功，保存到: {backup_path}"
    except Exception as e:
        return False, f"数据库备份失败: {str(e)}"

# 数据恢复功能
def restore_database(backup_path='backup_job_helper.db'):
    """从指定路径恢复数据库"""
    import shutil
    import os
    
    try:
        # 检查备份文件是否存在
        if not os.path.exists(backup_path):
            return False, f"备份文件不存在: {backup_path}"
        
        # 复制备份文件到数据库位置
        shutil.copy(backup_path, 'job_helper.db')
        return True, f"数据库恢复成功，从: {backup_path}"
    except Exception as e:
        return False, f"数据库恢复失败: {str(e)}"

# 优化数据库查询性能的函数
def optimize_database():
    """优化数据库性能"""
    try:
        # 对于SQLite，执行VACUUM命令来优化数据库
        from sqlalchemy import text
        session = get_session()
        session.execute(text('VACUUM'))
        session.commit()
        session.close()
        return True, "数据库优化成功"
    except Exception as e:
        return False, f"数据库优化失败: {str(e)}"

# 切换到PostgreSQL数据库的函数
def switch_to_postgresql(db_url):
    """切换到PostgreSQL数据库"""
    global engine, Session
    try:
        # 创建PostgreSQL引擎
        from sqlalchemy import create_engine
        engine = create_engine(db_url, echo=True)
        Session = sessionmaker(bind=engine)
        
        # 创建所有表
        Base.metadata.create_all(engine)
        return True, "成功切换到PostgreSQL数据库"
    except Exception as e:
        return False, f"切换到PostgreSQL数据库失败: {str(e)}"

# 云服务集成功能
class CloudStorage:
    """云存储服务类"""
    def __init__(self, provider='aws', **kwargs):
        """初始化云存储服务"""
        self.provider = provider
        self.kwargs = kwargs
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化云存储客户端"""
        try:
            if self.provider == 'aws':
                import boto3
                self.client = boto3.client('s3', 
                                         aws_access_key_id=self.kwargs.get('aws_access_key_id'),
                                         aws_secret_access_key=self.kwargs.get('aws_secret_access_key'),
                                         region_name=self.kwargs.get('region_name', 'us-east-1'))
            elif self.provider == 'google':
                from google.cloud import storage
                self.client = storage.Client.from_service_account_json(self.kwargs.get('service_account_file'))
            elif self.provider == 'azure':
                from azure.storage.blob import BlobServiceClient
                connection_string = self.kwargs.get('connection_string')
                self.client = BlobServiceClient.from_connection_string(connection_string)
        except Exception as e:
            print(f"初始化云存储客户端失败: {str(e)}")
    
    def upload_file(self, local_path, bucket_name, cloud_path):
        """上传文件到云存储"""
        try:
            if self.provider == 'aws':
                self.client.upload_file(local_path, bucket_name, cloud_path)
            elif self.provider == 'google':
                bucket = self.client.get_bucket(bucket_name)
                blob = bucket.blob(cloud_path)
                blob.upload_from_filename(local_path)
            elif self.provider == 'azure':
                blob_client = self.client.get_blob_client(container=bucket_name, blob=cloud_path)
                with open(local_path, "rb") as data:
                    blob_client.upload_blob(data)
            return True, f"文件上传成功: {cloud_path}"
        except Exception as e:
            return False, f"文件上传失败: {str(e)}"
    
    def download_file(self, bucket_name, cloud_path, local_path):
        """从云存储下载文件"""
        try:
            if self.provider == 'aws':
                self.client.download_file(bucket_name, cloud_path, local_path)
            elif self.provider == 'google':
                bucket = self.client.get_bucket(bucket_name)
                blob = bucket.blob(cloud_path)
                blob.download_to_filename(local_path)
            elif self.provider == 'azure':
                blob_client = self.client.get_blob_client(container=bucket_name, blob=cloud_path)
                with open(local_path, "wb") as data:
                    data.write(blob_client.download_blob().readall())
            return True, f"文件下载成功: {local_path}"
        except Exception as e:
            return False, f"文件下载失败: {str(e)}"
    
    def list_files(self, bucket_name, prefix=''):
        """列出云存储中的文件"""
        try:
            files = []
            if self.provider == 'aws':
                response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
                if 'Contents' in response:
                    files = [obj['Key'] for obj in response['Contents']]
            elif self.provider == 'google':
                bucket = self.client.get_bucket(bucket_name)
                blobs = bucket.list_blobs(prefix=prefix)
                files = [blob.name for blob in blobs]
            elif self.provider == 'azure':
                container_client = self.client.get_container_client(bucket_name)
                blobs = container_client.list_blobs(name_starts_with=prefix)
                files = [blob.name for blob in blobs]
            return True, files
        except Exception as e:
            return False, f"列出文件失败: {str(e)}"

# 云备份和恢复功能
def backup_to_cloud(cloud_provider, bucket_name, **kwargs):
    """备份数据库到云存储"""
    try:
        # 先备份到本地
        backup_path = 'backup_job_helper.db'
        success, message = backup_database(backup_path)
        if not success:
            return success, message
        
        # 上传到云存储
        cloud = CloudStorage(provider=cloud_provider, **kwargs)
        cloud_path = f'backups/job_helper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        success, message = cloud.upload_file(backup_path, bucket_name, cloud_path)
        return success, message
    except Exception as e:
        return False, f"云备份失败: {str(e)}"

# 从云存储恢复数据库
def restore_from_cloud(cloud_provider, bucket_name, cloud_path, **kwargs):
    """从云存储恢复数据库"""
    try:
        # 从云存储下载备份文件
        local_path = 'temp_backup.db'
        cloud = CloudStorage(provider=cloud_provider, **kwargs)
        success, message = cloud.download_file(bucket_name, cloud_path, local_path)
        if not success:
            return success, message
        
        # 恢复数据库
        success, message = restore_database(local_path)
        return success, message
    except Exception as e:
        return False, f"云恢复失败: {str(e)}"

# 列出云存储中的备份文件
def list_cloud_backups(cloud_provider, bucket_name, **kwargs):
    """列出云存储中的备份文件"""
    try:
        cloud = CloudStorage(provider=cloud_provider, **kwargs)
        success, files = cloud.list_files(bucket_name, prefix='backups/')
        if not success:
            return success, files
        
        # 过滤出数据库备份文件
        backup_files = [f for f in files if f.endswith('.db')]
        return True, backup_files
    except Exception as e:
        return False, f"列出云备份失败: {str(e)}"

# 记录功能使用统计
def record_feature_usage(user_id, feature_name):
    """记录功能使用情况"""
    session = get_session()
    try:
        # 查找是否已有该功能的使用记录
        usage = session.query(FeatureUsage).filter_by(user_id=user_id, feature_name=feature_name).first()
        
        if usage:
            # 更新使用次数和最后使用时间
            usage.usage_count += 1
            usage.last_used = datetime.now()
        else:
            # 创建新的使用记录
            usage = FeatureUsage(
                user_id=user_id,
                feature_name=feature_name,
                usage_count=1,
                last_used=datetime.now()
            )
            session.add(usage)
        
        session.commit()
        return True, "功能使用记录成功"
    except Exception as e:
        session.rollback()
        return False, f"功能使用记录失败: {str(e)}"
    finally:
        session.close()

# 获取功能使用统计
def get_feature_usage_stats():
    """获取功能使用统计数据"""
    session = get_session()
    try:
        # 获取所有功能的使用统计
        usage_stats = session.query(FeatureUsage).all()
        
        # 转换为字典列表
        stats = []
        for usage in usage_stats:
            stats.append({
                'feature_name': usage.feature_name,
                'total_usage': usage.usage_count,
                'last_used': usage.last_used
            })
        
        # 按使用次数排序
        stats.sort(key=lambda x: x['total_usage'], reverse=True)
        
        return True, stats
    except Exception as e:
        return False, f"获取功能使用统计失败: {str(e)}"
    finally:
        session.close()

# 获取用户反馈
def get_user_feedback():
    """获取用户反馈"""
    session = get_session()
    try:
        # 获取所有反馈
        feedbacks = session.query(Feedback).order_by(Feedback.created_at.desc()).all()
        
        # 转换为字典列表
        feedback_list = []
        for feedback in feedbacks:
            feedback_list.append({
                'id': feedback.id,
                'user_id': feedback.user_id,
                'type': feedback.type,
                'title': feedback.title,
                'content': feedback.content,
                'created_at': feedback.created_at,
                'status': feedback.status
            })
        
        return True, feedback_list
    except Exception as e:
        return False, f"获取用户反馈失败: {str(e)}"
    finally:
        session.close()

# 添加用户反馈
def add_user_feedback(user_id, feedback_type, title, content):
    """添加用户反馈"""
    session = get_session()
    try:
        # 创建新的反馈记录
        feedback = Feedback(
            user_id=user_id,
            type=feedback_type,
            title=title,
            content=content,
            status='pending'
        )
        session.add(feedback)
        session.commit()
        return True, "反馈提交成功"
    except Exception as e:
        session.rollback()
        return False, f"反馈提交失败: {str(e)}"
    finally:
        session.close()

# 添加社区帖子
def add_community_post(user_id, title, content):
    """添加社区帖子"""
    session = get_session()
    try:
        # 创建新的帖子
        post = CommunityPost(
            user_id=user_id,
            title=title,
            content=content
        )
        session.add(post)
        session.commit()
        return True, "帖子发布成功"
    except Exception as e:
        session.rollback()
        return False, f"帖子发布失败: {str(e)}"
    finally:
        session.close()

# 获取社区帖子
def get_community_posts():
    """获取社区帖子"""
    session = get_session()
    try:
        # 获取所有帖子，按创建时间降序排序
        posts = session.query(CommunityPost).order_by(CommunityPost.created_at.desc()).all()
        
        # 转换为字典列表
        post_list = []
        for post in posts:
            post_list.append({
                'id': post.id,
                'user_id': post.user_id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'views': post.views,
                'likes': post.likes,
                'comment_count': len(post.comments)
            })
        
        return True, post_list
    except Exception as e:
        return False, f"获取社区帖子失败: {str(e)}"
    finally:
        session.close()

# 添加社区评论
def add_community_comment(post_id, user_id, content):
    """添加社区评论"""
    session = get_session()
    try:
        # 创建新的评论
        comment = CommunityComment(
            post_id=post_id,
            user_id=user_id,
            content=content
        )
        session.add(comment)
        session.commit()
        return True, "评论发布成功"
    except Exception as e:
        session.rollback()
        return False, f"评论发布失败: {str(e)}"
    finally:
        session.close()

# 获取社区帖子详情
def get_community_post_detail(post_id):
    """获取社区帖子详情"""
    session = get_session()
    try:
        # 获取帖子
        post = session.query(CommunityPost).filter_by(id=post_id).first()
        if not post:
            return False, "帖子不存在"
        
        # 增加浏览量
        post.views += 1
        session.commit()
        
        # 获取评论
        comments = []
        for comment in post.comments:
            comments.append({
                'id': comment.id,
                'user_id': comment.user_id,
                'content': comment.content,
                'created_at': comment.created_at
            })
        
        # 构建帖子详情
        post_detail = {
            'id': post.id,
            'user_id': post.user_id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'views': post.views,
            'likes': post.likes,
            'comments': comments
        }
        
        return True, post_detail
    except Exception as e:
        return False, f"获取帖子详情失败: {str(e)}"
    finally:
        session.close()

# 第三方服务集成相关函数
def add_third_party_integration(user_id, platform, access_token=None, refresh_token=None, 
                             token_expires_at=None, integration_data=None):
    """添加第三方服务集成"""
    session = get_session()
    try:
        integration = ThirdPartyIntegration(
            user_id=user_id,
            platform=platform,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires_at=token_expires_at,
            integration_data=integration_data,
            is_active=True
        )
        session.add(integration)
        session.commit()
        return True, "第三方服务集成成功"
    except Exception as e:
        session.rollback()
        return False, f"第三方服务集成失败: {str(e)}"
    finally:
        session.close()

def get_user_integrations(user_id):
    """获取用户的第三方服务集成"""
    session = get_session()
    try:
        integrations = session.query(ThirdPartyIntegration).filter_by(user_id=user_id, is_active=True).all()
        integration_list = []
        for integration in integrations:
            integration_list.append({
                'id': integration.id,
                'platform': integration.platform,
                'is_active': integration.is_active,
                'created_at': integration.created_at,
                'updated_at': integration.updated_at
            })
        return True, integration_list
    except Exception as e:
        return False, f"获取第三方服务集成失败: {str(e)}"
    finally:
        session.close()

def update_integration_token(user_id, platform, access_token, refresh_token=None, token_expires_at=None):
    """更新第三方服务集成令牌"""
    session = get_session()
    try:
        integration = session.query(ThirdPartyIntegration).filter_by(
            user_id=user_id, platform=platform, is_active=True
        ).first()
        if integration:
            integration.access_token = access_token
            if refresh_token:
                integration.refresh_token = refresh_token
            if token_expires_at:
                integration.token_expires_at = token_expires_at
            integration.updated_at = datetime.now()
            session.commit()
            return True, "令牌更新成功"
        else:
            return False, "未找到对应的集成"
    except Exception as e:
        session.rollback()
        return False, f"令牌更新失败: {str(e)}"
    finally:
        session.close()

def remove_integration(user_id, platform):
    """移除第三方服务集成"""
    session = get_session()
    try:
        integration = session.query(ThirdPartyIntegration).filter_by(
            user_id=user_id, platform=platform, is_active=True
        ).first()
        if integration:
            integration.is_active = False
            integration.updated_at = datetime.now()
            session.commit()
            return True, "集成已移除"
        else:
            return False, "未找到对应的集成"
    except Exception as e:
        session.rollback()
        return False, f"集成移除失败: {str(e)}"
    finally:
        session.close()

# 职业测评相关函数
def create_career_assessment(user_id, assessment_type, assessment_data):
    """创建职业测评"""
    session = get_session()
    try:
        assessment = CareerAssessment(
            user_id=user_id,
            assessment_type=assessment_type,
            assessment_data=assessment_data,
            status='pending'
        )
        session.add(assessment)
        session.commit()
        return True, assessment.id
    except Exception as e:
        session.rollback()
        return False, f"创建职业测评失败: {str(e)}"
    finally:
        session.close()

def update_assessment_results(assessment_id, results):
    """更新测评结果"""
    session = get_session()
    try:
        assessment = session.query(CareerAssessment).filter_by(id=assessment_id).first()
        if assessment:
            assessment.results = results
            assessment.status = 'completed'
            assessment.completed_at = datetime.now()
            session.commit()
            return True, "测评结果更新成功"
        else:
            return False, "未找到对应的测评"
    except Exception as e:
        session.rollback()
        return False, f"测评结果更新失败: {str(e)}"
    finally:
        session.close()

def get_user_assessments(user_id):
    """获取用户的职业测评"""
    session = get_session()
    try:
        assessments = session.query(CareerAssessment).filter_by(user_id=user_id).order_by(
            CareerAssessment.created_at.desc()
        ).all()
        assessment_list = []
        for assessment in assessments:
            assessment_list.append({
                'id': assessment.id,
                'assessment_type': assessment.assessment_type,
                'status': assessment.status,
                'created_at': assessment.created_at,
                'completed_at': assessment.completed_at
            })
        return True, assessment_list
    except Exception as e:
        return False, f"获取职业测评失败: {str(e)}"
    finally:
        session.close()

# 技能认证相关函数
def add_skill_certification(user_id, certification_name, certification_provider=None, 
                         certification_level=None, issue_date=None, expiry_date=None, 
                         certificate_url=None):
    """添加技能认证"""
    session = get_session()
    try:
        certification = SkillCertification(
            user_id=user_id,
            certification_name=certification_name,
            certification_provider=certification_provider,
            certification_level=certification_level,
            issue_date=issue_date,
            expiry_date=expiry_date,
            certificate_url=certificate_url,
            status='active'
        )
        session.add(certification)
        session.commit()
        return True, "技能认证添加成功"
    except Exception as e:
        session.rollback()
        return False, f"技能认证添加失败: {str(e)}"
    finally:
        session.close()

def get_user_certifications(user_id):
    """获取用户的技能认证"""
    session = get_session()
    try:
        certifications = session.query(SkillCertification).filter_by(user_id=user_id).order_by(
            SkillCertification.issue_date.desc()
        ).all()
        certification_list = []
        for certification in certifications:
            certification_list.append({
                'id': certification.id,
                'certification_name': certification.certification_name,
                'certification_provider': certification.certification_provider,
                'certification_level': certification.certification_level,
                'issue_date': certification.issue_date,
                'expiry_date': certification.expiry_date,
                'certificate_url': certification.certificate_url,
                'status': certification.status
            })
        return True, certification_list
    except Exception as e:
        return False, f"获取技能认证失败: {str(e)}"
    finally:
        session.close()

# 在线学习课程相关函数
def enroll_online_course(user_id, course_name, course_provider=None, course_url=None, 
                      skill_level=None):
    """注册在线学习课程"""
    session = get_session()
    try:
        course = OnlineCourse(
            user_id=user_id,
            course_name=course_name,
            course_provider=course_provider,
            course_url=course_url,
            skill_level=skill_level,
            status='enrolled',
            progress=0
        )
        session.add(course)
        session.commit()
        return True, "课程注册成功"
    except Exception as e:
        session.rollback()
        return False, f"课程注册失败: {str(e)}"
    finally:
        session.close()

def update_course_progress(user_id, course_id, progress, status=None):
    """更新课程进度"""
    session = get_session()
    try:
        course = session.query(OnlineCourse).filter_by(id=course_id, user_id=user_id).first()
        if course:
            course.progress = progress
            if status:
                course.status = status
            if status == 'completed' and not course.completed_at:
                course.completed_at = datetime.now()
            session.commit()
            return True, "课程进度更新成功"
        else:
            return False, "未找到对应的课程"
    except Exception as e:
        session.rollback()
        return False, f"课程进度更新失败: {str(e)}"
    finally:
        session.close()

def get_user_courses(user_id):
    """获取用户的在线学习课程"""
    session = get_session()
    try:
        courses = session.query(OnlineCourse).filter_by(user_id=user_id).order_by(
            OnlineCourse.enrolled_at.desc()
        ).all()
        course_list = []
        for course in courses:
            course_list.append({
                'id': course.id,
                'course_name': course.course_name,
                'course_provider': course.course_provider,
                'course_url': course.course_url,
                'skill_level': course.skill_level,
                'progress': course.progress,
                'status': course.status,
                'enrolled_at': course.enrolled_at,
                'completed_at': course.completed_at
            })
        return True, course_list
    except Exception as e:
        return False, f"获取在线学习课程失败: {str(e)}"
    finally:
        session.close()

# 企业版功能相关函数
def create_company(name, industry=None, size=None, website=None, description=None, 
                  subscription_plan='basic'):
    """创建企业"""
    session = get_session()
    try:
        company = Company(
            name=name,
            industry=industry,
            size=size,
            website=website,
            description=description,
            subscription_plan=subscription_plan
        )
        session.add(company)
        session.commit()
        return True, company.id
    except Exception as e:
        session.rollback()
        return False, f"创建企业失败: {str(e)}"
    finally:
        session.close()

def add_user_to_company(company_id, user_id, role='member', department=None, position=None):
    """添加用户到企业"""
    session = get_session()
    try:
        company_user = CompanyUser(
            company_id=company_id,
            user_id=user_id,
            role=role,
            department=department,
            position=position
        )
        session.add(company_user)
        session.commit()
        return True, "用户添加到企业成功"
    except Exception as e:
        session.rollback()
        return False, f"添加用户到企业失败: {str(e)}"
    finally:
        session.close()

def get_company_users(company_id):
    """获取企业用户"""
    session = get_session()
    try:
        company_users = session.query(CompanyUser).filter_by(
            company_id=company_id, is_active=True
        ).all()
        user_list = []
        for company_user in company_users:
            user_list.append({
                'id': company_user.id,
                'user_id': company_user.user_id,
                'role': company_user.role,
                'department': company_user.department,
                'position': company_user.position,
                'joined_at': company_user.joined_at
            })
        return True, user_list
    except Exception as e:
        return False, f"获取企业用户失败: {str(e)}"
    finally:
        session.close()

def update_user_role(company_id, user_id, new_role):
    """更新用户角色"""
    session = get_session()
    try:
        company_user = session.query(CompanyUser).filter_by(
            company_id=company_id, user_id=user_id, is_active=True
        ).first()
        if company_user:
            company_user.role = new_role
            session.commit()
            return True, "用户角色更新成功"
        else:
            return False, "未找到对应的用户"
    except Exception as e:
        session.rollback()
        return False, f"用户角色更新失败: {str(e)}"
    finally:
        session.close()

def remove_user_from_company(company_id, user_id):
    """从企业移除用户"""
    session = get_session()
    try:
        company_user = session.query(CompanyUser).filter_by(
            company_id=company_id, user_id=user_id, is_active=True
        ).first()
        if company_user:
            company_user.is_active = False
            session.commit()
            return True, "用户已从企业移除"
        else:
            return False, "未找到对应的用户"
    except Exception as e:
        session.rollback()
        return False, f"从企业移除用户失败: {str(e)}"
    finally:
        session.close()

def create_team(company_id, name, description=None, created_by=None):
    """创建团队"""
    session = get_session()
    try:
        team = Team(
            company_id=company_id,
            name=name,
            description=description,
            created_by=created_by
        )
        session.add(team)
        session.commit()
        return True, team.id
    except Exception as e:
        session.rollback()
        return False, f"创建团队失败: {str(e)}"
    finally:
        session.close()

def get_company_teams(company_id):
    """获取企业团队"""
    session = get_session()
    try:
        teams = session.query(Team).filter_by(company_id=company_id).all()
        team_list = []
        for team in teams:
            team_list.append({
                'id': team.id,
                'name': team.name,
                'description': team.description,
                'created_by': team.created_by,
                'created_at': team.created_at
            })
        return True, team_list
    except Exception as e:
        return False, f"获取企业团队失败: {str(e)}"
    finally:
        session.close()

def add_team_member(team_id, user_id, role='member'):
    """添加团队成员"""
    session = get_session()
    try:
        team_member = TeamMember(
            team_id=team_id,
            user_id=user_id,
            role=role
        )
        session.add(team_member)
        session.commit()
        return True, "团队成员添加成功"
    except Exception as e:
        session.rollback()
        return False, f"添加团队成员失败: {str(e)}"
    finally:
        session.close()

def get_team_members(team_id):
    """获取团队成员"""
    session = get_session()
    try:
        team_members = session.query(TeamMember).filter_by(team_id=team_id).all()
        member_list = []
        for team_member in team_members:
            member_list.append({
                'id': team_member.id,
                'user_id': team_member.user_id,
                'role': team_member.role,
                'joined_at': team_member.joined_at
            })
        return True, member_list
    except Exception as e:
        return False, f"获取团队成员失败: {str(e)}"
    finally:
        session.close()

def create_shared_resource(team_id, resource_type, resource_name, resource_data, created_by):
    """创建共享资源"""
    session = get_session()
    try:
        shared_resource = SharedResource(
            team_id=team_id,
            resource_type=resource_type,
            resource_name=resource_name,
            resource_data=resource_data,
            created_by=created_by
        )
        session.add(shared_resource)
        session.commit()
        return True, "共享资源创建成功"
    except Exception as e:
        session.rollback()
        return False, f"创建共享资源失败: {str(e)}"
    finally:
        session.close()

def get_team_resources(team_id):
    """获取团队共享资源"""
    session = get_session()
    try:
        resources = session.query(SharedResource).filter_by(team_id=team_id).all()
        resource_list = []
        for resource in resources:
            resource_list.append({
                'id': resource.id,
                'resource_type': resource.resource_type,
                'resource_name': resource.resource_name,
                'resource_data': resource.resource_data,
                'created_by': resource.created_by,
                'created_at': resource.created_at
            })
        return True, resource_list
    except Exception as e:
        return False, f"获取团队共享资源失败: {str(e)}"
    finally:
        session.close()

def generate_analytics_report(company_id, report_type, period_start, period_end):
    """生成数据分析报告"""
    session = get_session()
    try:
        # 根据报告类型生成不同的数据
        if report_type == 'usage':
            report_data = _generate_usage_report(company_id, period_start, period_end)
        elif report_type == 'performance':
            report_data = _generate_performance_report(company_id, period_start, period_end)
        elif report_type == 'hiring':
            report_data = _generate_hiring_report(company_id, period_start, period_end)
        else:
            return False, "不支持的报告类型"
        
        report = AnalyticsReport(
            company_id=company_id,
            report_type=report_type,
            report_data=json.dumps(report_data),
            period_start=period_start,
            period_end=period_end
        )
        session.add(report)
        session.commit()
        return True, report_data
    except Exception as e:
        session.rollback()
        return False, f"生成数据分析报告失败: {str(e)}"
    finally:
        session.close()

def _generate_usage_report(company_id, period_start, period_end):
    """生成使用情况报告"""
    session = get_session()
    try:
        # 获取活动日志
        activities = session.query(ActivityLog).filter(
            ActivityLog.company_id == company_id,
            ActivityLog.created_at >= period_start,
            ActivityLog.created_at <= period_end
        ).all()
        
        # 统计数据
        total_activities = len(activities)
        active_users = len(set(activity.user_id for activity in activities))
        
        # 按活动类型统计
        activity_types = {}
        for activity in activities:
            activity_types[activity.activity_type] = activity_types.get(activity.activity_type, 0) + 1
        
        return {
            'total_activities': total_activities,
            'active_users': active_users,
            'activity_types': activity_types,
            'period_start': period_start.isoformat(),
            'period_end': period_end.isoformat()
        }
    finally:
        session.close()

def _generate_performance_report(company_id, period_start, period_end):
    """生成性能报告"""
    session = get_session()
    try:
        # 获取活动日志
        activities = session.query(ActivityLog).filter(
            ActivityLog.company_id == company_id,
            ActivityLog.created_at >= period_start,
            ActivityLog.created_at <= period_end
        ).all()
        
        # 统计简历分析次数
        resume_analyses = len([a for a in activities if a.activity_type == 'resume_analysis'])
        
        # 统计职位搜索次数
        job_searches = len([a for a in activities if a.activity_type == 'job_search'])
        
        # 统计面试模拟次数
        interview_simulations = len([a for a in activities if a.activity_type == 'interview_simulation'])
        
        return {
            'resume_analyses': resume_analyses,
            'job_searches': job_searches,
            'interview_simulations': interview_simulations,
            'period_start': period_start.isoformat(),
            'period_end': period_end.isoformat()
        }
    finally:
        session.close()

def _generate_hiring_report(company_id, period_start, period_end):
    """生成招聘报告"""
    session = get_session()
    try:
        # 获取企业用户
        company_users = session.query(CompanyUser).filter_by(
            company_id=company_id, is_active=True
        ).all()
        
        # 统计用户数量
        total_users = len(company_users)
        
        # 按部门统计
        departments = {}
        for company_user in company_users:
            dept = company_user.department or '未分配'
            departments[dept] = departments.get(dept, 0) + 1
        
        # 按角色统计
        roles = {}
        for company_user in company_users:
            role = company_user.role
            roles[role] = roles.get(role, 0) + 1
        
        return {
            'total_users': total_users,
            'departments': departments,
            'roles': roles,
            'period_start': period_start.isoformat(),
            'period_end': period_end.isoformat()
        }
    finally:
        session.close()

def get_company_reports(company_id):
    """获取企业报告"""
    session = get_session()
    try:
        reports = session.query(AnalyticsReport).filter_by(company_id=company_id).order_by(
            AnalyticsReport.generated_at.desc()
        ).all()
        report_list = []
        for report in reports:
            report_list.append({
                'id': report.id,
                'report_type': report.report_type,
                'report_data': json.loads(report.report_data),
                'generated_at': report.generated_at,
                'period_start': report.period_start,
                'period_end': report.period_end
            })
        return True, report_list
    except Exception as e:
        return False, f"获取企业报告失败: {str(e)}"
    finally:
        session.close()

def log_activity(user_id, company_id, activity_type, activity_data=None, ip_address=None, user_agent=None):
    """记录用户活动"""
    session = get_session()
    try:
        activity_log = ActivityLog(
            user_id=user_id,
            company_id=company_id,
            activity_type=activity_type,
            activity_data=json.dumps(activity_data) if activity_data else None,
            ip_address=ip_address,
            user_agent=user_agent
        )
        session.add(activity_log)
        session.commit()
        return True, "活动记录成功"
    except Exception as e:
        session.rollback()
        return False, f"活动记录失败: {str(e)}"
    finally:
        session.close()
