"""Демо-таблица "Продажи" для интерактивного стенда.

Данные намеренно "грязные": содержат дубликаты, пропуски в amount
и полностью пустые строки, чтобы каждая операция давала видимый результат.
"""

import pandas as pd


DEMO_TABLE = [
    # ─── Уникальные заказы (35) ───────────────────────────────────────
    {"order_id": "A-001", "region": "Москва",         "month": "Янв", "amount": 12500, "manager": "Иванов"},
    {"order_id": "A-002", "region": "Москва",         "month": "Фев", "amount":  9800, "manager": "Петрова"},
    {"order_id": "A-003", "region": "СПб",            "month": "Янв", "amount": 15200, "manager": "Сидоров"},
    {"order_id": "A-004", "region": "СПб",            "month": "Фев", "amount": 11300, "manager": "Кузнецова"},
    {"order_id": "A-005", "region": "Казань",         "month": "Мар", "amount":  None, "manager": "Смирнов"},   # ← пропуск
    {"order_id": "A-006", "region": "Казань",         "month": "Апр", "amount":  8900, "manager": "Иванов"},
    {"order_id": "A-007", "region": "Новосибирск",    "month": "Мар", "amount": 13400, "manager": "Петрова"},
    {"order_id": "A-008", "region": "Новосибирск",    "month": "Апр", "amount": 10100, "manager": "Сидоров"},
    {"order_id": "A-009", "region": "Екатеринбург",   "month": "Май", "amount":  7800, "manager": "Кузнецова"},
    {"order_id": "A-010", "region": "Екатеринбург",   "month": "Июн", "amount":  9600, "manager": "Смирнов"},
    {"order_id": "A-011", "region": "Москва",         "month": "Мар", "amount":  None, "manager": "Иванов"},   # ← пропуск
    {"order_id": "A-012", "region": "СПб",            "month": "Апр", "amount": 14300, "manager": "Петрова"},
    {"order_id": "A-013", "region": "Казань",         "month": "Май", "amount":  8200, "manager": "Сидоров"},
    {"order_id": "A-014", "region": "Новосибирск",    "month": "Июн", "amount": 11900, "manager": "Кузнецова"},
    {"order_id": "A-015", "region": "Екатеринбург",   "month": "Янв", "amount": 10500, "manager": "Смирнов"},
    {"order_id": "A-016", "region": "Москва",         "month": "Апр", "amount": 13100, "manager": "Иванов"},
    {"order_id": "A-017", "region": "СПб",            "month": "Май", "amount":  9900, "manager": "Петрова"},
    {"order_id": "A-018", "region": "Казань",         "month": "Июн", "amount":  7600, "manager": "Сидоров"},
    {"order_id": "A-019", "region": "Новосибирск",    "month": "Янв", "amount":  None, "manager": "Кузнецова"}, # ← пропуск
    {"order_id": "A-020", "region": "Екатеринбург",   "month": "Фев", "amount": 11200, "manager": "Смирнов"},
    {"order_id": "A-021", "region": "Москва",         "month": "Май", "amount": 14800, "manager": "Иванов"},
    {"order_id": "A-022", "region": "СПб",            "month": "Июн", "amount": 12300, "manager": "Петрова"},
    {"order_id": "A-023", "region": "Казань",         "month": "Фев", "amount":  8600, "manager": "Сидоров"},
    {"order_id": "A-024", "region": "Новосибирск",    "month": "Фев", "amount": 10800, "manager": "Кузнецова"},
    {"order_id": "A-025", "region": "Екатеринбург",   "month": "Мар", "amount":  9400, "manager": "Смирнов"},
    {"order_id": "A-026", "region": "Москва",         "month": "Июн", "amount": 13700, "manager": "Иванов"},
    {"order_id": "A-027", "region": "СПб",            "month": "Мар", "amount":  None, "manager": "Петрова"},   # ← пропуск
    {"order_id": "A-028", "region": "Казань",         "month": "Апр", "amount":  9100, "manager": "Сидоров"},
    {"order_id": "A-029", "region": "Новосибирск",    "month": "Апр", "amount": 11600, "manager": "Кузнецова"},
    {"order_id": "A-030", "region": "Екатеринбург",   "month": "Апр", "amount":  8700, "manager": "Смирнов"},
    {"order_id": "A-031", "region": "Москва",         "month": "Янв", "amount": 12900, "manager": "Иванов"},
    {"order_id": "A-032", "region": "СПб",            "month": "Фев", "amount": 10700, "manager": "Петрова"},
    {"order_id": "A-033", "region": "Казань",         "month": "Мар", "amount":  8300, "manager": "Сидоров"},
    {"order_id": "A-034", "region": "Новосибирск",    "month": "Май", "amount": 12100, "manager": "Кузнецова"},
    {"order_id": "A-035", "region": "Екатеринбург",   "month": "Июн", "amount": 10200, "manager": "Смирнов"},

    # ─── Дубликаты (полные копии, 6 шт.) ──────────────────────────────
    {"order_id": "A-003", "region": "СПб",            "month": "Янв", "amount": 15200, "manager": "Сидоров"},    # ← дубликат
    {"order_id": "A-007", "region": "Новосибирск",    "month": "Мар", "amount": 13400, "manager": "Петрова"},   # ← дубликат
    {"order_id": "A-012", "region": "СПб",            "month": "Апр", "amount": 14300, "manager": "Петрова"},   # ← дубликат
    {"order_id": "A-018", "region": "Казань",         "month": "Июн", "amount":  7600, "manager": "Сидоров"},   # ← дубликат
    {"order_id": "A-025", "region": "Екатеринбург",   "month": "Мар", "amount":  9400, "manager": "Смирнов"},   # ← дубликат
    {"order_id": "A-030", "region": "Екатеринбург",   "month": "Апр", "amount":  8700, "manager": "Смирнов"},   # ← дубликат

    # ─── Полностью пустые строки (3 шт.) ──────────────────────────────
    {"order_id": None, "region": None, "month": None, "amount": None, "manager": None},  # ← пустая
    {"order_id": None, "region": None, "month": None, "amount": None, "manager": None},  # ← пустая
    {"order_id": None, "region": None, "month": None, "amount": None, "manager": None},  # ← пустая
]


def get_demo_table() -> pd.DataFrame:
    """Возвращает свежую копию демо-таблицы.

    Копия нужна, чтобы любое изменение (удаление строк, заполнение пропусков)
    не портило исходные данные — это важно для кнопки "Сбросить к исходным".
    """
    return pd.DataFrame(DEMO_TABLE).copy()
