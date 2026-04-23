"""
BabyGrow AI Service
支持多AI Provider：MiniMax / StepFun / Ollama
"""
import httpx
import json
import os
from typing import Optional, Dict, Any, List
from config import AI_PROVIDER, AI_API_KEY, AI_BASE_URL, AI_MODEL, OLLAMA_BASE_URL, OLLAMA_MODEL


class AIService:
    """AI服务封装，支持多Provider"""

    def __init__(self):
        self.provider = AI_PROVIDER
        self.api_key = AI_API_KEY or os.getenv("MINIMAX_API_KEY", "")
        self.base_url = AI_BASE_URL
        self.model = AI_MODEL

    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        通用对话接口

        Args:
            messages: [{"role": "user", "content": "..."}]
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            {"content": str, "usage": dict, "reasoning": str}
        """
        if self.provider == "ollama":
            return await self._chat_ollama(messages, system_prompt, temperature, max_tokens)
        elif self.provider == "stepfun":
            return await self._chat_stepfun(messages, system_prompt, temperature, max_tokens)
        else:
            # 默认MiniMax
            return await self._chat_minimax(messages, system_prompt, temperature, max_tokens)

    async def _chat_minimax(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """MiniMax API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": full_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/text/chatcompletion_v2",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            return {
                "content": data["choices"][0]["message"]["content"],
                "usage": data.get("usage", {}),
                "reasoning": data.get("choices")[0].get("thinking", "")
            }

    async def _chat_stepfun(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """StepFun API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": full_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            return {
                "content": data["choices"][0]["message"]["content"],
                "usage": data.get("usage", {}),
                "reasoning": ""
            }

    async def _chat_ollama(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Ollama本地API"""
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        payload = {
            "model": OLLAMA_MODEL,
            "messages": full_messages,
            "temperature": temperature,
            "options": {
                "num_predict": max_tokens
            }
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            return {
                "content": data["message"]["content"],
                "usage": {},
                "reasoning": ""
            }


# 全局单例
ai_service = AIService()


async def generate_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> str:
    """简单对话生成"""
    messages = [{"role": "user", "content": prompt}]

    if context:
        context_str = f"\n\nContext:\n{json.dumps(context, ensure_ascii=False)}"
        messages[0]["content"] = prompt + context_str

    result = await ai_service.chat(messages, system_prompt)
    return result["content"]
