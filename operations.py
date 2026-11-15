"""Реестр операций над таблицей.

Каждая операция описана один раз: id, название, параметры, функция.
Из этого реестра UI автоматически строит кнопки и формы.
Позже — LLM сможет вызывать те же операции (tool calling) без переписывания.
"""

from dataclasses import dataclass, field
from typing import Any, Callable
import pandas as pd


# ─── Схемы ────────────────────────────────────────────────────────────

@dataclass
class ParamSpec:
    """Описание одного параметра операции.

    kind:
      - "column"        — выбор одной колонки из таблицы
      - "columns_multi" — выбор нескольких колонок (может быть пустым)
      - "value"         — произвольная строка
      - "choice"        — выбор из фиксированного списка options
    """
    key: str
    label: str
    kind: str
    required: bool = True
    default: Any = None
    options: list[tuple[str, Any]] = field(default_factory=list)


@dataclass
class Operation:
    id: str
    title: str
    description: str
    group: str
    params: list[ParamSpec]
    func: Callable[[pd.DataFrame, dict], tuple[pd.DataFrame, str]]


# ─── Функции-исполнители ──────────────────────────────────────────────
# Каждая возвращает (новый_df, сообщение_пользователю).
# Никогда не мутирует входной df — работает с копией.

def _op_drop_duplicates(df: pd.DataFrame, params: dict) -> tuple[pd.DataFrame, str]:
    subset = params.get("subset") or None  # None = все колонки
    before = len(df)
    out = df.drop_duplicates(subset=subset).reset_index(drop=True)
    removed = before - len(out)
    if removed == 0:
        return out, f"Дубликатов не найдено (было {before} строк)"
    where = "по всем колонкам" if subset is None else f"по колонкам: {', '.join(subset)}"
    return out, f"Удалено {removed} дубликатов {where} (было {before} → стало {len(out)})"


def _op_filter(df: pd.DataFrame, params: dict) -> tuple[pd.DataFrame, str]:
    col = params["column"]
    val = params["value"]
    before = len(df)
    mask = df[col].astype(str) == str(val)
    out = df[mask].reset_index(drop=True)
    if len(out) == 0:
        return df, f"Ничего не найдено: {col} = «{val}». Таблица не изменена."
    return out, f"Осталось {len(out)} из {before} строк (фильтр: {col} = «{val}»)"


def _op_sort(df: pd.DataFrame, params: dict) -> tuple[pd.DataFrame, str]:
    col = params["column"]
    ascending = params.get("direction", True)
    out = df.sort_values(by=col, ascending=ascending, na_position="last").reset_index(drop=True)
    direction = "возрастанию" if ascending else "убыванию"
    return out, f"Отсортировано по «{col}» ({direction})"


def _op_drop_empty(df: pd.DataFrame, params: dict) -> tuple[pd.DataFrame, str]:
    before = len(df)
    out = df.dropna(how="all").reset_index(drop=True)
    removed = before - len(out)
    if removed == 0:
        return out, f"Пустых строк не найдено (было {before})"
    return out, f"Удалено {removed} пустых строк (было {before} → стало {len(out)})"


def _op_fill_na(df: pd.DataFrame, params: dict) -> tuple[pd.DataFrame, str]:
    col = params["column"]
    raw = params["value"]
    before_na = int(df[col].isna().sum())
    out = df.copy()
    if pd.api.types.is_numeric_dtype(out[col]):
        try:
            value = float(raw) if "." in str(raw) else int(raw)
        except (ValueError, TypeError):
            return df, f"Значение «{raw}» не похоже на число для колонки «{col}». Таблица не изменена."
    else:
        value = str(raw)
    out[col] = out[col].fillna(value)
    if before_na == 0:
        return out, f"В колонке «{col}» не было пропусков"
    return out, f"Заполнено {before_na} пропусков в «{col}» значением {value}"


# ─── Реестр ───────────────────────────────────────────────────────────

OPERATIONS: dict[str, Operation] = {
    "drop_duplicates": Operation(
        id="drop_duplicates",
        title="Удалить дубликаты",
        description="Удаляет повторяющиеся строки. Без параметров — ищет полные дубликаты по всем колонкам.",
        group="Очистка",
        params=[
            ParamSpec(
                key="subset",
                label="По каким колонкам (пусто = по всем)",
                kind="columns_multi",
                required=False,
            ),
        ],
        func=_op_drop_duplicates,
    ),
    "filter": Operation(
        id="filter",
        title="Фильтр по значению",
        description="Оставляет только строки, где выбранная колонка равна указанному значению.",
        group="Преобразование",
        params=[
            ParamSpec(key="column", label="Колонка", kind="column"),
            ParamSpec(key="value",  label="Значение", kind="value"),
        ],
        func=_op_filter,
    ),
    "sort": Operation(
        id="sort",
        title="Сортировать",
        description="Сортирует строки по выбранной колонке.",
        group="Преобразование",
        params=[
            ParamSpec(key="column", label="Колонка", kind="column"),
            ParamSpec(
                key="direction",
                label="Направление",
                kind="choice",
                default=True,
                options=[("По возрастанию", True), ("По убыванию", False)],
            ),
        ],
        func=_op_sort,
    ),
    "drop_empty": Operation(
        id="drop_empty",
        title="Удалить пустые строки",
        description="Удаляет строки, где все ячейки пустые.",
        group="Очистка",
        params=[],
        func=_op_drop_empty,
    ),
    "fill_na": Operation(
        id="fill_na",
        title="Заполнить пропуски",
        description="Заполняет пустые ячейки в выбранной колонке указанным значением.",
        group="Очистка",
        params=[
            ParamSpec(key="column", label="Колонка", kind="column"),
            ParamSpec(key="value",  label="Чем заполнить", kind="value"),
        ],
        func=_op_fill_na,
    ),
}
