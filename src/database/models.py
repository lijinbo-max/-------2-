from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 创建数据库引擎
engine = create_engine('sqlite:///ai_job_helper.db', echo=True)

# 创建会话工厂
Session = sessionmaker(bind=engine)

# 创建基类
Base = declarative_base()

# 用户模型
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)
    
    # 关系
    personal_info = relationship('PersonalInfo', back_populates='user', uselist=False)
    education = relationship('Education', back_populates='user')
    work_experience = relationship('WorkExperience', back_populates='user')
    job_preferences = relationship('JobPreference', back_populates='user')
    resumes = relationship('Resume', back_populates='user')

# 个人信息模型
class PersonalInfo(Base):
    __tablename__ = 'personal_info'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    gender = Column(String(10))
    age = Column(Integer)
    disability_type = Column(String(100))
    disability_level = Column(String(50))
    phone = Column(String(20))
    address = Column(Text)
    
    # 关系
    user = relationship('User', back_populates='personal_info')

# 教育背景模型
class Education(Base):
    __tablename__ = 'education'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    school = Column(String(255), nullable=False)
    degree = Column(String(100), nullable=False)
    major = Column(String(255), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    
    # 关系
    user = relationship('User', back_populates='education')

# 工作经验模型
class WorkExperience(Base):
    __tablename__ = 'work_experience'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    company = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    
    # 关系
    user = relationship('User', back_populates='work_experience')

# 职位偏好模型
class JobPreference(Base):
    __tablename__ = 'job_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    industry = Column(String(255))
    position = Column(String(255))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    location = Column(String(255))
    work_type = Column(String(100))
    
    # 关系
    user = relationship('User', back_populates='job_preferences')

# 职位模型
class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    industry = Column(String(255))
    location = Column(String(255))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    description = Column(Text)
    requirements = Column(Text)
    posted_date = Column(Date, default=datetime.utcnow)

# 简历模型
class Resume(Base):
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    uploaded_date = Column(Date, default=datetime.utcnow)
    
    # 关系
    user = relationship('User', back_populates='resumes')

# 职位申请模型
class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    resume_id = Column(Integer, ForeignKey('resumes.id'), nullable=False)
    application_date = Column(Date, default=datetime.utcnow)
    status = Column(String(50), default='申请中')  # 申请中、已通过、已拒绝
    
    # 关系
    user = relationship('User', backref='job_applications')
    job = relationship('Job', backref='job_applications')
    resume = relationship('Resume', backref='job_applications')

# 通知模型
class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(Date, default=datetime.utcnow)
    
    # 关系
    user = relationship('User', backref='notifications')

# 用户反馈模型
class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(Date, default=datetime.utcnow)
    
    # 关系
    user = relationship('User', backref='feedback')

# 无障碍设置模型
class AccessibilitySetting(Base):
    __tablename__ = 'accessibility_settings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    font_size = Column(Integer, default=16)
    contrast = Column(String(50), default='normal')  # normal, high
    text_to_speech = Column(Boolean, default=False)
    screen_reader = Column(Boolean, default=False)
    
    # 关系
    user = relationship('User', backref='accessibility_settings')

# 系统设置模型
class SystemSetting(Base):
    __tablename__ = 'system_settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text)

# 初始化数据库
def init_db():
    Base.metadata.create_all(engine)

# 获取数据库会话
def get_session():
    return Session()
