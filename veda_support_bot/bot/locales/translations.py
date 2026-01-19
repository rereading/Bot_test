"""
Полная система локализации для бота
Все тексты на 3 языках: русский, узбекский, английский
"""

TRANSLATIONS = {
    "ru": {
        # Общие
        "cancel": "❌ Отмена",
        "cancel_success": "❌ Создание заявки отменено",
        
        # Welcome сообщение
        "welcome_title": "👋 <b>Добро пожаловать!</b>",
        "welcome_text": (
            "Я бот технической поддержки компании VedaVector.\n\n"
            "<b>Как создать заявку:</b>\n"
            "1. Напишите команду /help\n"
            "2. Выберите язык\n"
            "3. Опишите вашу проблему\n\n"
            "⚠️ <i>Пожалуйста, заполняйте заявку максимально подробно</i>"
        ),
        
        # Выбор языка
        "choose_language": "🌐 <b>Выберите язык:</b>",
        
        # Описание проблемы
        "describe_problem": "📝 Опишите вашу проблему подробно:",
        "description_too_short": "⚠️ Описание слишком короткое. Пожалуйста, опишите проблему подробнее (минимум 10 символов).",
        "description_too_long": "⚠️ Описание слишком длинное (максимум {max_length} символов)",
        
        # Филиалы
        "choose_filial": "🏢 Выберите филиал:",
        "filial_not_found": "❌ Филиал не найден",
        
        # Успех
        "ticket_created": (
            "✅ <b>Заявка успешно создана!</b>\n\n"
            "Номер заявки: <code>{task_id}</code>\n"
            "Мы свяжемся с вами в ближайшее время."
        ),
        
        # Ошибки
        "error_creating_ticket": "❌ Произошла ошибка при создании заявки. Попробуйте позже.",
        "error_group_not_found": "❌ Ошибка: группа не найдена в базе данных",
        "private_chat_only": "⚠️ Эта команда работает только в групповых чатах",
        
        # Админ
        "no_admin_rights": "⛔ У вас нет прав администратора",
        "admin_premium_format": "⚠️ Формат: /admin_set_premium <group_id> <true/false>",
        "admin_premium_success": "✅ Премиум статус для группы {group_id}: {status}",
        "admin_premium_not_found": "❌ Группа {group_id} не найдена",
        "admin_filial_format": "⚠️ Формат: /admin_add_filial <group_id> <название>",
        "admin_filial_success": "✅ Филиал '{name}' добавлен группе {group_id}",
        "admin_invalid_id": "❌ Некорректный group_id",
        "admin_error": "❌ Ошибка: {error}",
    },
    
    "uz": {
        # Общие
        "cancel": "❌ Bekor qilish",
        "cancel_success": "❌ Murojaat yaratish bekor qilindi",
        
        # Welcome сообщение
        "welcome_title": "👋 <b>Xush kelibsiz!</b>",
        "welcome_text": (
            "Men VedaVector kompaniyasining texnik qo'llab-quvvatlash botiman.\n\n"
            "<b>Murojaat yaratish:</b>\n"
            "1. /help buyrug'ini yozing\n"
            "2. Tilni tanlang\n"
            "3. Muammoingizni tasvirlab bering\n\n"
            "⚠️ <i>Iltimos, murojaatnomani to'liq to'ldiring</i>"
        ),
        
        # Выбор языка
        "choose_language": "🌐 <b>Tilni tanlang:</b>",
        
        # Описание проблемы
        "describe_problem": "📝 Muammoingizni batafsil tasvirlab bering:",
        "description_too_short": "⚠️ Tavsif juda qisqa. Iltimos, muammoni batafsil tasvirlab bering (kamida 10 belgi).",
        "description_too_long": "⚠️ Tavsif juda uzun (maksimal {max_length} belgi)",
        
        # Филиалы
        "choose_filial": "🏢 Filialni tanlang:",
        "filial_not_found": "❌ Filial topilmadi",
        
        # Успех
        "ticket_created": (
            "✅ <b>Murojaat muvaffaqiyatli yaratildi!</b>\n\n"
            "Murojaat raqami: <code>{task_id}</code>\n"
            "Yaqin orada siz bilan bog'lanamiz."
        ),
        
        # Ошибки
        "error_creating_ticket": "❌ Murojaat yaratishda xatolik yuz berdi. Keyinroq urinib ko'ring.",
        "error_group_not_found": "❌ Xato: guruh ma'lumotlar bazasida topilmadi",
        "private_chat_only": "⚠️ Bu buyruq faqat guruh chatlarida ishlaydi",
        
        # Админ
        "no_admin_rights": "⛔ Sizda administrator huquqlari yo'q",
        "admin_premium_format": "⚠️ Format: /admin_set_premium <group_id> <true/false>",
        "admin_premium_success": "✅ {group_id} guruh uchun premium status: {status}",
        "admin_premium_not_found": "❌ {group_id} guruh topilmadi",
        "admin_filial_format": "⚠️ Format: /admin_add_filial <group_id> <nomi>",
        "admin_filial_success": "✅ '{name}' filiali {group_id} guruhga qo'shildi",
        "admin_invalid_id": "❌ Noto'g'ri group_id",
        "admin_error": "❌ Xato: {error}",
    },
    
    "en": {
        # Общие
        "cancel": "❌ Cancel",
        "cancel_success": "❌ Request creation cancelled",
        
        # Welcome сообщение
        "welcome_title": "👋 <b>Welcome!</b>",
        "welcome_text": (
            "I am VedaVector's technical support bot.\n\n"
            "<b>How to create a request:</b>\n"
            "1. Type /help command\n"
            "2. Choose your language\n"
            "3. Describe your problem\n\n"
            "⚠️ <i>Please fill in the request form completely</i>"
        ),
        
        # Выбор языка
        "choose_language": "🌐 <b>Choose language:</b>",
        
        # Описание проблемы
        "describe_problem": "📝 Describe your problem in detail:",
        "description_too_short": "⚠️ Description is too short. Please describe the problem in more detail (minimum 10 characters).",
        "description_too_long": "⚠️ Description is too long (maximum {max_length} characters)",
        
        # Филиалы
        "choose_filial": "🏢 Choose branch:",
        "filial_not_found": "❌ Branch not found",
        
        # Успех
        "ticket_created": (
            "✅ <b>Request created successfully!</b>\n\n"
            "Request ID: <code>{task_id}</code>\n"
            "We will contact you soon."
        ),
        
        # Ошибки
        "error_creating_ticket": "❌ An error occurred while creating the request. Please try again later.",
        "error_group_not_found": "❌ Error: group not found in database",
        "private_chat_only": "⚠️ This command only works in group chats",
        
        # Админ
        "no_admin_rights": "⛔ You don't have administrator rights",
        "admin_premium_format": "⚠️ Format: /admin_set_premium <group_id> <true/false>",
        "admin_premium_success": "✅ Premium status for group {group_id}: {status}",
        "admin_premium_not_found": "❌ Group {group_id} not found",
        "admin_filial_format": "⚠️ Format: /admin_add_filial <group_id> <name>",
        "admin_filial_success": "✅ Branch '{name}' added to group {group_id}",
        "admin_invalid_id": "❌ Invalid group_id",
        "admin_error": "❌ Error: {error}",
    }
}