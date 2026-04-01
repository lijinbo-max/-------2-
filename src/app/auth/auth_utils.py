import hashlib

# 密码哈希
def hash_password(password):
    # 使用 SHA-256 哈希，避免 bcrypt 的长度限制
    return hashlib.sha256(password.encode()).hexdigest()

# 密码验证
def verify_password(password, hashed_password):
    return hash_password(password) == hashed_password
