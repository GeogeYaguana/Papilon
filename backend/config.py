import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600')))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://ubasg72abi62gl:pe57b2ca8503d9cbd58763ac4a87e1ae4ea39ae84c8ff769f0e87c490647e3472@c9pv5s2sq0i76o.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddpb2lu396gu31')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
