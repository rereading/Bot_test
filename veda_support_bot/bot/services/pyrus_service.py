import httpx
from typing import Dict, Any, Optional
import logging
from bot.config import settings

logger = logging.getLogger(__name__)


class PyrusService:
    def __init__(self):
        self.api_url = settings.PYRUS_API_URL
        self.api_key = settings.PYRUS_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_task(self, data: Dict[str, Any]) -> Optional[str]:
        """Создать задачу в Pyrus"""
        payload = {
            "subject": "Заявка техподдержки",
            "description": data["description"],
            "fields": [
                {"name": "Группа", "value": data["group_name"]},
                {"name": "Язык", "value": data["language"]},
                {"name": "Премиум", "value": "Да" if data["is_premium"] else "Нет"},
            ]
        }
        
        if data.get("filial"):
            payload["fields"].append({"name": "Филиал", "value": data["filial"]})
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/tasks",
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                result = response.json()
                task_id = result.get("task", {}).get("id")
                logger.info(f"Создана задача Pyrus: {task_id}")
                return task_id
                
        except httpx.HTTPError as e:
            logger.error(f"Ошибка создания задачи Pyrus: {e}")
            return None
    
    async def add_comment(self, task_id: str, text: str) -> bool:
        """Добавить комментарий к задаче"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/tasks/{task_id}/comments",
                    json={"text": text},
                    headers=self.headers
                )
                response.raise_for_status()
                return True
        except httpx.HTTPError as e:
            logger.error(f"Ошибка добавления комментария: {e}")
            return False


pyrus_service = PyrusService()