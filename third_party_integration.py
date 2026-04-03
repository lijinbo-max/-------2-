import requests
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class LinkedInIntegration:
    """LinkedIn API集成"""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.base_url = "https://api.linkedin.com/v2"
    
    def get_authorization_url(self) -> str:
        """获取授权URL"""
        scopes = ["r_liteprofile", "r_emailaddress", "w_member_social"]
        auth_url = (
            f"https://www.linkedin.com/oauth/v2/authorization"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={' '.join(scopes)}"
        )
        return auth_url
    
    def get_access_token(self, authorization_code: str) -> Tuple[bool, str]:
        """获取访问令牌"""
        try:
            url = "https://www.linkedin.com/oauth/v2/accessToken"
            data = {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                return True, "访问令牌获取成功"
            else:
                return False, f"获取访问令牌失败: {response.text}"
        except Exception as e:
            return False, f"获取访问令牌异常: {str(e)}"
    
    def get_profile(self) -> Tuple[bool, Dict]:
        """获取用户资料"""
        try:
            if not self.access_token:
                return False, {"error": "未授权"}
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{self.base_url}/me",
                headers=headers
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def search_jobs(self, keywords: str, location: str = None, limit: int = 10) -> Tuple[bool, List[Dict]]:
        """搜索职位"""
        try:
            if not self.access_token:
                return False, []
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            params = {
                "keywords": keywords,
                "count": limit
            }
            if location:
                params["location"] = location
            
            response = requests.get(
                f"{self.base_url}/jobSearch",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                return True, response.json().get("elements", [])
            else:
                return False, []
        except Exception as e:
            return False, []
    
    def apply_job(self, job_id: str, application_data: Dict) -> Tuple[bool, str]:
        """申请职位"""
        try:
            if not self.access_token:
                return False, "未授权"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            response = requests.post(
                f"{self.base_url}/jobApplications",
                headers=headers,
                json=application_data
            )
            
            if response.status_code == 201:
                return True, "申请成功"
            else:
                return False, f"申请失败: {response.text}"
        except Exception as e:
            return False, f"申请异常: {str(e)}"


class IndeedIntegration:
    """Indeed API集成"""
    
    def __init__(self, publisher_id: str, api_key: str):
        self.publisher_id = publisher_id
        self.api_key = api_key
        self.base_url = "https://api.indeed.com/v2"
    
    def search_jobs(self, query: str, location: str = None, 
                   salary_min: int = None, salary_max: int = None,
                   job_type: str = None, limit: int = 10) -> Tuple[bool, List[Dict]]:
        """搜索职位"""
        try:
            params = {
                "q": query,
                "publisher": self.publisher_id,
                "v": "2",
                "format": "json",
                "limit": limit
            }
            
            if location:
                params["l"] = location
            if salary_min:
                params["salary_min"] = salary_min
            if salary_max:
                params["salary_max"] = salary_max
            if job_type:
                params["jt"] = job_type
            
            response = requests.get(
                f"{self.base_url}/jobs/search",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                return True, data.get("results", [])
            else:
                return False, []
        except Exception as e:
            return False, []
    
    def get_job_details(self, job_key: str) -> Tuple[bool, Dict]:
        """获取职位详情"""
        try:
            params = {
                "jobkeys": job_key,
                "publisher": self.publisher_id,
                "v": "2",
                "format": "json"
            }
            
            response = requests.get(
                f"{self.base_url}/jobs/details",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("results", [])
                if jobs:
                    return True, jobs[0]
                return False, {"error": "职位不存在"}
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}


class CareerAssessmentIntegration:
    """职业测评服务集成"""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.career-assessment.com/v1"
    
    def create_assessment(self, user_id: int, assessment_type: str) -> Tuple[bool, Dict]:
        """创建测评"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "user_id": user_id,
                "assessment_type": assessment_type,
                "created_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.base_url}/assessments",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                return True, response.json()
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def submit_answers(self, assessment_id: str, answers: List[Dict]) -> Tuple[bool, Dict]:
        """提交测评答案"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "answers": answers,
                "submitted_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.base_url}/assessments/{assessment_id}/submit",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def get_assessment_results(self, assessment_id: str) -> Tuple[bool, Dict]:
        """获取测评结果"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            response = requests.get(
                f"{self.base_url}/assessments/{assessment_id}/results",
                headers=headers
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}


class SkillCertificationIntegration:
    """技能认证服务集成"""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.skill-certification.com/v1"
    
    def get_available_certifications(self, skill_category: str = None) -> Tuple[bool, List[Dict]]:
        """获取可用的认证"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            params = {}
            
            if skill_category:
                params["category"] = skill_category
            
            response = requests.get(
                f"{self.base_url}/certifications",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                return True, response.json().get("certifications", [])
            else:
                return False, []
        except Exception as e:
            return False, []
    
    def register_for_certification(self, user_id: int, certification_id: str) -> Tuple[bool, Dict]:
        """注册认证考试"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "user_id": user_id,
                "certification_id": certification_id,
                "registered_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.base_url}/registrations",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                return True, response.json()
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def get_user_certifications(self, user_id: int) -> Tuple[bool, List[Dict]]:
        """获取用户认证"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            response = requests.get(
                f"{self.base_url}/users/{user_id}/certifications",
                headers=headers
            )
            
            if response.status_code == 200:
                return True, response.json().get("certifications", [])
            else:
                return False, []
        except Exception as e:
            return False, []


class OnlineLearningIntegration:
    """在线学习平台集成"""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.online-learning.com/v1"
    
    def search_courses(self, keywords: str, skill_level: str = None, 
                     language: str = None, limit: int = 10) -> Tuple[bool, List[Dict]]:
        """搜索课程"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            params = {
                "q": keywords,
                "limit": limit
            }
            
            if skill_level:
                params["skill_level"] = skill_level
            if language:
                params["language"] = language
            
            response = requests.get(
                f"{self.base_url}/courses/search",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                return True, response.json().get("courses", [])
            else:
                return False, []
        except Exception as e:
            return False, []
    
    def enroll_course(self, user_id: int, course_id: str) -> Tuple[bool, Dict]:
        """注册课程"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "user_id": user_id,
                "course_id": course_id,
                "enrolled_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.base_url}/enrollments",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                return True, response.json()
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}
    
    def get_user_courses(self, user_id: int) -> Tuple[bool, List[Dict]]:
        """获取用户课程"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            response = requests.get(
                f"{self.base_url}/users/{user_id}/courses",
                headers=headers
            )
            
            if response.status_code == 200:
                return True, response.json().get("courses", [])
            else:
                return False, []
        except Exception as e:
            return False, []
    
    def get_course_progress(self, user_id: int, course_id: str) -> Tuple[bool, Dict]:
        """获取课程进度"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            response = requests.get(
                f"{self.base_url}/users/{user_id}/courses/{course_id}/progress",
                headers=headers
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {"error": response.text}
        except Exception as e:
            return False, {"error": str(e)}


class ThirdPartyIntegrationManager:
    """第三方服务集成管理器"""
    
    def __init__(self):
        self.linkedin = None
        self.indeed = None
        self.career_assessment = None
        self.skill_certification = None
        self.online_learning = None
    
    def init_linkedin(self, client_id: str, client_secret: str, redirect_uri: str):
        """初始化LinkedIn集成"""
        self.linkedin = LinkedInIntegration(client_id, client_secret, redirect_uri)
    
    def init_indeed(self, publisher_id: str, api_key: str):
        """初始化Indeed集成"""
        self.indeed = IndeedIntegration(publisher_id, api_key)
    
    def init_career_assessment(self, api_key: str, base_url: str = None):
        """初始化职业测评集成"""
        self.career_assessment = CareerAssessmentIntegration(api_key, base_url)
    
    def init_skill_certification(self, api_key: str, base_url: str = None):
        """初始化技能认证集成"""
        self.skill_certification = SkillCertificationIntegration(api_key, base_url)
    
    def init_online_learning(self, api_key: str, base_url: str = None):
        """初始化在线学习集成"""
        self.online_learning = OnlineLearningIntegration(api_key, base_url)
    
    def search_jobs_all_platforms(self, keywords: str, location: str = None, 
                                 limit: int = 10) -> List[Dict]:
        """在所有平台搜索职位"""
        all_jobs = []
        
        # 从LinkedIn搜索
        if self.linkedin:
            success, jobs = self.linkedin.search_jobs(keywords, location, limit)
            if success:
                all_jobs.extend([{"source": "LinkedIn", **job} for job in jobs])
        
        # 从Indeed搜索
        if self.indeed:
            success, jobs = self.indeed.search_jobs(keywords, location, limit=limit)
            if success:
                all_jobs.extend([{"source": "Indeed", **job} for job in jobs])
        
        return all_jobs