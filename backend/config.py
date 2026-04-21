import os
from dotenv import load_dotenv

load_dotenv()

# 服务配置
PORT = int(os.getenv("PORT", "8765"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# AI配置
AI_PROVIDER = os.getenv("AI_PROVIDER", "minimax")  # minimax / stepfun / ollama
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.minimax.chat/v1")
AI_MODEL = os.getenv("AI_MODEL", "MiniMax-Text-01")

# Ollama本地配置（可选）
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# 数据库配置
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/data.db")

# 前端静态文件路径
FRONTEND_PATH = os.getenv("FRONTEND_PATH", "../web")
