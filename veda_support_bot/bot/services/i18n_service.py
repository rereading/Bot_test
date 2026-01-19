"""
Сервис локализации
Предоставляет переводы на разные языки
"""

from typing import Optional
from bot.locales.translations import TRANSLATIONS


class I18nService:
    """Сервис локализации"""
    
    DEFAULT_LANGUAGE = "ru"
    
    @staticmethod
    def get_text(key: str, language: str = "ru", **kwargs) -> str:
        """
        Получить переведённый текст
        
        Args:
            key: Ключ перевода (например, "cancel", "choose_language")
            language: Код языка (ru, uz, en)
            **kwargs: Параметры для форматирования строки
        
        Returns:
            Переведённый текст
        
        Example:
            i18n.get_text("cancel", "uz")  # → "Bekor qilish"
            i18n.get_text("ticket_created", "en", task_id="12345")
        """
        # Получаем словарь языка, fallback на русский
        lang_dict = TRANSLATIONS.get(
            language,
            TRANSLATIONS[I18nService.DEFAULT_LANGUAGE]
        )
        
        # Получаем текст, fallback на русский если ключ не найден
        text = lang_dict.get(
            key,
            TRANSLATIONS[I18nService.DEFAULT_LANGUAGE].get(key, f"[Missing: {key}]")
        )
        
        # Форматируем с параметрами если есть
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        
        return text
    
    @staticmethod
    def get_available_languages() -> dict[str, str]:
        """Получить список доступных языков"""
        return {
            "ru": "🇷🇺 Русский",
            "uz": "🇺🇿 O'zbekcha",
            "en": "🇬🇧 English"
        }


# Создаём глобальный экземпляр для использования в других модулях
i18n = I18nService()