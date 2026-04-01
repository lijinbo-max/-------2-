from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.app.auth.auth_service import AuthService
from src.database import get_session
from sqlalchemy.orm import Session
from src.database.models import User, PersonalInfo, Education, WorkExperience, Resume, Job, JobPreference, JobApplication, Notification, Feedback, AccessibilitySetting, SystemSetting
from datetime import datetime
import os
import uuid

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保响应使用UTF-8编码
@app.middleware("http")
async def add_utf8_encoding(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str

class PersonalInfoRequest(BaseModel):
    gender: str = None
    age: int = None
    disability_type: str = None
    disability_level: str = None
    phone: str = None
    address: str = None

class EducationRequest(BaseModel):
    school: str = None
    degree: str = None
    major: str = None
    start_date: str = None
    end_date: str = None
    description: str = None

class WorkExperienceRequest(BaseModel):
    company: str = None
    position: str = None
    start_date: str = None
    end_date: str = None
    description: str = None

class UpdatePersonalInfoRequest(BaseModel):
    personal_info: PersonalInfoRequest
    education: EducationRequest
    work_experience: WorkExperienceRequest

class ResumeAnalysisResponse(BaseModel):
    score: int
    strengths: list
    improvements: list

class JobPreferenceRequest(BaseModel):
    industry: str = None
    position: str = None
    salary_min: int = None
    salary_max: int = None
    location: str = None
    work_type: str = None

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    industry: str
    location: str
    salary_min: int
    salary_max: int
    description: str
    requirements: str

class InterviewQuestionRequest(BaseModel):
    interview_type: str

class InterviewAnswerRequest(BaseModel):
    interview_type: str
    question_index: int
    answer: str

class InterviewFeedbackResponse(BaseModel):
    feedback: list
    next_question: str = None

class JobApplicationRequest(BaseModel):
    job_id: int
    resume_id: int

class FeedbackRequest(BaseModel):
    content: str

class AccessibilitySettingRequest(BaseModel):
    font_size: int = 16
    contrast: str = 'normal'
    text_to_speech: bool = False
    screen_reader: bool = False

class SystemSettingRequest(BaseModel):
    key: str
    value: str

@app.post("/api/login")
async def login(request: LoginRequest):
    success, result = AuthService.login(request.email, request.password)
    if success:
        return {"success": True, "user": result}
    else:
        raise HTTPException(status_code=401, detail=result)

@app.post("/api/register")
async def register(request: RegisterRequest):
    success, result = AuthService.register(request.email, request.name, request.password)
    if success:
        return {"success": True, "user": result}
    else:
        raise HTTPException(status_code=400, detail=result)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/user/{email}")
async def get_user_info(email: str, session: Session = Depends(get_session)):
    """获取用户信息"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 获取个人信息
    personal_info = session.query(PersonalInfo).filter_by(user_id=user.id).first()
    # 获取教育背景
    education = session.query(Education).filter_by(user_id=user.id).first()
    # 获取工作经验
    work_experience = session.query(WorkExperience).filter_by(user_id=user.id).first()
    
    return {
        "user": {
            "email": user.email,
            "name": user.name
        },
        "personal_info": personal_info.__dict__ if personal_info else None,
        "education": education.__dict__ if education else None,
        "work_experience": work_experience.__dict__ if work_experience else None
    }

@app.put("/api/user/{email}")
async def update_user_info(email: str, request: UpdatePersonalInfoRequest, session: Session = Depends(get_session)):
    """更新用户信息"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新个人信息
    personal_info = session.query(PersonalInfo).filter_by(user_id=user.id).first()
    if not personal_info:
        personal_info = PersonalInfo(user_id=user.id)
        session.add(personal_info)
    
    for key, value in request.personal_info.model_dump().items():
        if value is not None:
            setattr(personal_info, key, value)
    
    # 更新教育背景
    education = session.query(Education).filter_by(user_id=user.id).first()
    if not education:
        education = Education(user_id=user.id)
        session.add(education)
    
    for key, value in request.education.model_dump().items():
        if value is not None:
            # 处理日期类型
            if key in ['start_date', 'end_date'] and value:
                try:
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                except:
                    value = None
            setattr(education, key, value)
    
    # 更新工作经验
    work_experience = session.query(WorkExperience).filter_by(user_id=user.id).first()
    if not work_experience:
        work_experience = WorkExperience(user_id=user.id)
        session.add(work_experience)
    
    for key, value in request.work_experience.model_dump().items():
        if value is not None:
            # 处理日期类型
            if key in ['start_date', 'end_date'] and value:
                try:
                    value = datetime.strptime(value, '%Y-%m-%d').date()
                except:
                    value = None
            setattr(work_experience, key, value)
    
    session.commit()
    return {"success": True, "message": "个人信息更新成功"}

@app.post("/api/resume/upload")
async def upload_resume(email: str, file: UploadFile = File(...), session: Session = Depends(get_session)):
    """上传简历"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 创建上传目录
    upload_dir = "uploads/resumes"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # 保存到数据库
    resume = Resume(
        user_id=user.id,
        file_name=file.filename,
        file_path=file_path
    )
    session.add(resume)
    session.commit()
    
    return {"success": True, "resume_id": resume.id, "file_name": file.filename}

@app.post("/api/resume/analyze")
async def analyze_resume(email: str, resume_id: int, session: Session = Depends(get_session)):
    """分析简历"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    resume = session.query(Resume).filter_by(id=resume_id, user_id=user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    # 模拟简历分析
    analysis_result = {
        "score": 85,
        "strengths": [
            "教育背景完整，专业对口",
            "工作经验丰富，有相关行业经验",
            "技能清单全面，符合职位要求"
        ],
        "improvements": [
            "增加具体的工作成果和量化指标",
            "优化简历格式，提高可读性",
            "突出与目标职位相关的技能和经验"
        ]
    }
    
    return analysis_result

@app.post("/api/job/preference")
async def save_job_preference(email: str, request: JobPreferenceRequest, session: Session = Depends(get_session)):
    """保存职位偏好"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 查找或创建职位偏好
    job_preference = session.query(JobPreference).filter_by(user_id=user.id).first()
    if not job_preference:
        job_preference = JobPreference(user_id=user.id)
        session.add(job_preference)
    
    # 更新职位偏好
    for key, value in request.model_dump().items():
        if value is not None:
            setattr(job_preference, key, value)
    
    session.commit()
    return {"success": True, "message": "职位偏好保存成功"}

@app.get("/api/job/recommendations")
async def get_job_recommendations(email: str, session: Session = Depends(get_session)):
    """获取职位推荐"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 获取用户职位偏好
    job_preference = session.query(JobPreference).filter_by(user_id=user.id).first()
    
    # 模拟职位推荐
    jobs = [
        {
            "id": 1,
            "title": "软件工程师",
            "company": "科技公司A",
            "industry": "IT/互联网",
            "location": "北京",
            "salary_min": 15000,
            "salary_max": 25000,
            "description": "负责公司产品的设计和开发，与团队合作完成项目目标。",
            "requirements": "熟悉Python、Java等编程语言，有相关工作经验。"
        },
        {
            "id": 2,
            "title": "数据分析师",
            "company": "互联网公司B",
            "industry": "IT/互联网",
            "location": "上海",
            "salary_min": 12000,
            "salary_max": 20000,
            "description": "负责数据分析和挖掘，为业务决策提供支持。",
            "requirements": "熟悉SQL、Python，有数据分析经验。"
        },
        {
            "id": 3,
            "title": "产品经理",
            "company": "创业公司C",
            "industry": "IT/互联网",
            "location": "深圳",
            "salary_min": 18000,
            "salary_max": 28000,
            "description": "负责产品的规划和设计，与开发团队合作实现产品功能。",
            "requirements": "有产品经理经验，熟悉产品开发流程。"
        }
    ]
    
    return {"jobs": jobs}

@app.get("/api/job/{job_id}")
async def get_job_detail(job_id: int, session: Session = Depends(get_session)):
    """获取职位详情"""
    job = session.query(Job).filter_by(id=job_id).first()
    if not job:
        # 模拟职位详情
        return {
            "id": job_id,
            "title": "软件工程师",
            "company": "科技公司A",
            "industry": "IT/互联网",
            "location": "北京",
            "salary_min": 15000,
            "salary_max": 25000,
            "description": "负责公司产品的设计和开发，与团队合作完成项目目标。",
            "requirements": "熟悉Python、Java等编程语言，有相关工作经验。"
        }
    return job.__dict__

@app.post("/api/interview/questions")
async def get_interview_questions(request: InterviewQuestionRequest):
    """获取面试问题"""
    # 面试问题
    questions = {
        "技术面试": [
            "请介绍一下你最熟悉的编程语言",
            "你如何解决遇到的技术难题？",
            "请解释一下什么是面向对象编程"
        ],
        "行为面试": [
            "请描述一次你面对挑战的经历",
            "你如何与团队成员合作？",
            "请分享一次你解决冲突的经历"
        ],
        "情景面试": [
            "如果你的项目延期了，你会怎么做？",
            "如果客户对你的方案不满意，你会如何处理？",
            "如果团队成员意见分歧，你会如何协调？"
        ]
    }
    
    if request.interview_type not in questions:
        raise HTTPException(status_code=400, detail="无效的面试类型")
    
    return {"questions": questions[request.interview_type]}

@app.post("/api/interview/answer")
async def submit_interview_answer(request: InterviewAnswerRequest):
    """提交面试回答并获取反馈"""
    # 面试问题
    questions = {
        "技术面试": [
            "请介绍一下你最熟悉的编程语言",
            "你如何解决遇到的技术难题？",
            "请解释一下什么是面向对象编程"
        ],
        "行为面试": [
            "请描述一次你面对挑战的经历",
            "你如何与团队成员合作？",
            "请分享一次你解决冲突的经历"
        ],
        "情景面试": [
            "如果你的项目延期了，你会怎么做？",
            "如果客户对你的方案不满意，你会如何处理？",
            "如果团队成员意见分歧，你会如何协调？"
        ]
    }
    
    if request.interview_type not in questions:
        raise HTTPException(status_code=400, detail="无效的面试类型")
    
    if request.question_index < 0 or request.question_index >= len(questions[request.interview_type]):
        raise HTTPException(status_code=400, detail="无效的问题索引")
    
    # 模拟反馈
    feedback = [
        "回答结构清晰，逻辑连贯",
        "提供了具体的例子，增强了说服力",
        "可以更详细地说明你是如何解决问题的"
    ]
    
    # 检查是否有下一个问题
    next_question = None
    if request.question_index < len(questions[request.interview_type]) - 1:
        next_question = questions[request.interview_type][request.question_index + 1]
    
    return {
        "feedback": feedback,
        "next_question": next_question
    }

# 职位申请相关接口
@app.post("/api/job/apply")
async def apply_for_job(email: str, request: JobApplicationRequest, session: Session = Depends(get_session)):
    """申请职位"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查职位是否存在
    job = session.query(Job).filter_by(id=request.job_id).first()
    if not job:
        # 模拟职位存在
        pass
    
    # 检查简历是否存在
    resume = session.query(Resume).filter_by(id=request.resume_id, user_id=user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    # 创建职位申请
    job_application = JobApplication(
        user_id=user.id,
        job_id=request.job_id,
        resume_id=request.resume_id
    )
    session.add(job_application)
    session.commit()
    
    return {"success": True, "application_id": job_application.id, "message": "职位申请成功"}

@app.get("/api/job/applications")
async def get_job_applications(email: str, session: Session = Depends(get_session)):
    """获取申请记录"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    applications = session.query(JobApplication).filter_by(user_id=user.id).all()
    
    # 模拟职位信息
    job_info = {
        1: {"title": "软件工程师", "company": "科技公司A"},
        2: {"title": "数据分析师", "company": "互联网公司B"},
        3: {"title": "产品经理", "company": "创业公司C"}
    }
    
    result = []
    for app in applications:
        job = job_info.get(app.job_id, {"title": "未知职位", "company": "未知公司"})
        result.append({
            "id": app.id,
            "job_title": job["title"],
            "company": job["company"],
            "application_date": app.application_date,
            "status": app.status
        })
    
    return {"applications": result}

@app.get("/api/job/application/{id}")
async def get_application_detail(id: int, email: str, session: Session = Depends(get_session)):
    """获取申请详情"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    application = session.query(JobApplication).filter_by(id=id, user_id=user.id).first()
    if not application:
        raise HTTPException(status_code=404, detail="申请记录不存在")
    
    # 模拟职位详情
    job_detail = {
        "id": application.job_id,
        "title": "软件工程师",
        "company": "科技公司A",
        "industry": "IT/互联网",
        "location": "北京",
        "salary_min": 15000,
        "salary_max": 25000,
        "description": "负责公司产品的设计和开发，与团队合作完成项目目标。",
        "requirements": "熟悉Python、Java等编程语言，有相关工作经验。"
    }
    
    return {
        "id": application.id,
        "job": job_detail,
        "application_date": application.application_date,
        "status": application.status
    }

# 简历管理相关接口
@app.get("/api/resume/list")
async def get_resume_list(email: str, session: Session = Depends(get_session)):
    """获取简历列表"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    resumes = session.query(Resume).filter_by(user_id=user.id).all()
    
    result = []
    for resume in resumes:
        result.append({
            "id": resume.id,
            "file_name": resume.file_name,
            "uploaded_date": resume.uploaded_date
        })
    
    return {"resumes": result}

@app.get("/api/resume/{id}")
async def get_resume_detail(id: int, email: str, session: Session = Depends(get_session)):
    """获取简历详情"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    resume = session.query(Resume).filter_by(id=id, user_id=user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    return {
        "id": resume.id,
        "file_name": resume.file_name,
        "file_path": resume.file_path,
        "uploaded_date": resume.uploaded_date
    }

@app.delete("/api/resume/{id}")
async def delete_resume(id: int, email: str, session: Session = Depends(get_session)):
    """删除简历"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    resume = session.query(Resume).filter_by(id=id, user_id=user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    # 删除文件
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    # 删除数据库记录
    session.delete(resume)
    session.commit()
    
    return {"success": True, "message": "简历删除成功"}

# 通知系统相关接口
@app.get("/api/notifications")
async def get_notifications(email: str, session: Session = Depends(get_session)):
    """获取通知列表"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    notifications = session.query(Notification).filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()
    
    result = []
    for notification in notifications:
        result.append({
            "id": notification.id,
            "title": notification.title,
            "content": notification.content,
            "is_read": notification.is_read,
            "created_at": notification.created_at
        })
    
    return {"notifications": result}

@app.get("/api/notification/{id}")
async def get_notification_detail(id: int, email: str, session: Session = Depends(get_session)):
    """获取通知详情"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    notification = session.query(Notification).filter_by(id=id, user_id=user.id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    # 标记为已读
    if not notification.is_read:
        notification.is_read = True
        session.commit()
    
    return {
        "id": notification.id,
        "title": notification.title,
        "content": notification.content,
        "is_read": notification.is_read,
        "created_at": notification.created_at
    }

@app.put("/api/notification/{id}/read")
async def mark_notification_as_read(id: int, email: str, session: Session = Depends(get_session)):
    """标记通知为已读"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    notification = session.query(Notification).filter_by(id=id, user_id=user.id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    notification.is_read = True
    session.commit()
    
    return {"success": True, "message": "通知已标记为已读"}

@app.delete("/api/notification/{id}")
async def delete_notification(id: int, email: str, session: Session = Depends(get_session)):
    """删除通知"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    notification = session.query(Notification).filter_by(id=id, user_id=user.id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    session.delete(notification)
    session.commit()
    
    return {"success": True, "message": "通知删除成功"}

# 用户反馈相关接口
@app.post("/api/feedback")
async def submit_feedback(email: str, request: FeedbackRequest, session: Session = Depends(get_session)):
    """提交反馈"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    feedback = Feedback(
        user_id=user.id,
        content=request.content
    )
    session.add(feedback)
    session.commit()
    
    return {"success": True, "message": "反馈提交成功"}

@app.get("/api/feedback/list")
async def get_feedback_list(email: str, session: Session = Depends(get_session)):
    """获取反馈历史"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    feedbacks = session.query(Feedback).filter_by(user_id=user.id).order_by(Feedback.created_at.desc()).all()
    
    result = []
    for feedback in feedbacks:
        result.append({
            "id": feedback.id,
            "content": feedback.content,
            "created_at": feedback.created_at
        })
    
    return {"feedbacks": result}

# 数据统计相关接口
@app.get("/api/stats/user")
async def get_user_stats(email: str, session: Session = Depends(get_session)):
    """获取用户统计信息"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 模拟统计数据
    stats = {
        "total_applications": 5,
        "pending_applications": 2,
        "interview_applications": 1,
        "rejected_applications": 2,
        "total_resumes": 2,
        "total_notifications": 8,
        "unread_notifications": 3
    }
    
    return stats

@app.get("/api/stats/jobs")
async def get_job_stats():
    """获取职位统计信息"""
    # 模拟统计数据
    stats = {
        "total_jobs": 100,
        "jobs_by_industry": {
            "IT/互联网": 45,
            "金融": 20,
            "教育": 15,
            "医疗": 10,
            "其他": 10
        },
        "jobs_by_location": {
            "北京": 30,
            "上海": 25,
            "广州": 15,
            "深圳": 20,
            "其他": 10
        },
        "average_salary": 18000
    }
    
    return stats

@app.get("/api/stats/applications")
async def get_application_stats(email: str, session: Session = Depends(get_session)):
    """获取申请统计信息"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 模拟统计数据
    stats = {
        "application_trend": [
            {"month": "1月", "count": 2},
            {"month": "2月", "count": 1},
            {"month": "3月", "count": 2}
        ],
        "application_by_industry": {
            "IT/互联网": 3,
            "金融": 1,
            "教育": 1
        },
        "application_success_rate": 20
    }
    
    return stats

# 无障碍功能设置相关接口
@app.get("/api/accessibility/settings")
async def get_accessibility_settings(email: str, session: Session = Depends(get_session)):
    """获取无障碍设置"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    setting = session.query(AccessibilitySetting).filter_by(user_id=user.id).first()
    if not setting:
        # 创建默认设置
        setting = AccessibilitySetting(user_id=user.id)
        session.add(setting)
        session.commit()
    
    return {
        "font_size": setting.font_size,
        "contrast": setting.contrast,
        "text_to_speech": setting.text_to_speech,
        "screen_reader": setting.screen_reader
    }

@app.put("/api/accessibility/settings")
async def update_accessibility_settings(email: str, request: AccessibilitySettingRequest, session: Session = Depends(get_session)):
    """更新无障碍设置"""
    user = session.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    setting = session.query(AccessibilitySetting).filter_by(user_id=user.id).first()
    if not setting:
        setting = AccessibilitySetting(user_id=user.id)
        session.add(setting)
    
    # 更新设置
    setting.font_size = request.font_size
    setting.contrast = request.contrast
    setting.text_to_speech = request.text_to_speech
    setting.screen_reader = request.screen_reader
    
    session.commit()
    
    return {"success": True, "message": "无障碍设置更新成功"}

# 系统管理相关接口
@app.get("/api/system/settings")
async def get_system_settings():
    """获取系统设置"""
    # 模拟系统设置
    settings = {
        "system_name": "AI助残求职辅助工具",
        "version": "1.0.0",
        "maintenance_mode": False,
        "max_resume_size": 10485760  # 10MB
    }
    
    return settings

@app.put("/api/system/settings")
async def update_system_settings(request: SystemSettingRequest, session: Session = Depends(get_session)):
    """更新系统设置"""
    setting = session.query(SystemSetting).filter_by(key=request.key).first()
    if not setting:
        setting = SystemSetting(key=request.key, value=request.value)
        session.add(setting)
    else:
        setting.value = request.value
    
    session.commit()
    
    return {"success": True, "message": "系统设置更新成功"}

@app.get("/api/system/version")
async def get_system_version():
    """获取系统版本信息"""
    return {
        "version": "1.0.0",
        "release_date": "2026-04-01",
        "features": [
            "职位推荐",
            "简历分析",
            "面试模拟",
            "无障碍功能"
        ]
    }
