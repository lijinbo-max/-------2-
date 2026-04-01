from src.database import get_session, User
from .auth_utils import hash_password, verify_password
from src.app.utils.logger import get_logger

logger = get_logger(__name__)

class AuthService:
    @staticmethod
    def login(email, password):
        """用户登录"""
        logger.info(f"Login attempt for email: {email}")
        session = get_session()
        try:
            user = session.query(User).filter_by(email=email).first()
            if user:
                if verify_password(password, user.password):
                    logger.info(f"Login successful for user: {email}")
                    # 在会话关闭前提取属性
                    user_data = {"email": user.email, "name": user.name}
                    return True, user_data
                else:
                    logger.warning(f"Login failed: incorrect password for email: {email}")
                    return False, "密码错误"
            else:
                # 如果用户不存在，创建默认测试用户
                if email == "test@example.com" and password == "123456":
                    new_user = User(
                        email="test@example.com",
                        name="测试用户",
                        password=hash_password("123456"),
                        disabled=False
                    )
                    session.add(new_user)
                    session.commit()
                    logger.info(f"Created test user: {email}")
                    # 在会话关闭前提取属性
                    user_data = {"email": new_user.email, "name": new_user.name}
                    return True, user_data
                else:
                    logger.warning(f"Login failed: user not found for email: {email}")
                    return False, "用户不存在"
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False, f"登录失败: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def register(email, name, password):
        """用户注册"""
        logger.info(f"Registration attempt for email: {email}")
        session = get_session()
        try:
            # 检查用户是否已存在
            existing_user = session.query(User).filter_by(email=email).first()
            if existing_user:
                logger.warning(f"Registration failed: email already exists: {email}")
                return False, "邮箱已被注册"
            
            # 创建新用户
            new_user = User(
                email=email,
                name=name,
                password=hash_password(password),
                disabled=False
            )
            session.add(new_user)
            session.commit()
            logger.info(f"Registration successful for user: {email}")
            # 在会话关闭前提取属性
            user_data = {"email": new_user.email, "name": new_user.name}
            return True, user_data
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return False, f"注册失败: {str(e)}"
        finally:
            session.close()
