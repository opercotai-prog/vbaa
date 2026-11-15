"""Интерактивный демо-стенд: таблица + список операций сбоку.

Без загрузки файлов, без LLM. Пользователь применяет операции кнопками
из сайдбара, видит результат в таблице, может отменить или сбросить.
"""

import streamlit as st
import pandas as pd

from demo_data import get_demo_table
from operations import OPERATIONS, Operation, ParamSpec


st.set_page_config(page_title="Демо-стенд: операции с таблицей", layout="wide")


# ─── Состояние сессии ─────────────────────────────────────────────────

def init_state() -> None:
    if "df" not in st.session_state:
        st.session_state.df = get_demo_table()
    if "history" not in st.session_state:
        st.session_state.history: list[pd.DataFrame] = []
    if "op_count" not in st.session_state:
        st.session_state.op_count = 0
    if "last_msg" not in st.session_state:
        st.session_state.last_msg = "Исходные данные. Выберите операцию сбоку."
    if "last_op_title" not in st.session_state:
        st.session_state.last_op_title = "—"


def apply_op(op: Operation, params: dict) -> None:
    """Сохраняет снимок, применяет операцию, обновляет состояние."""
    st.session_state.history.append(st.session_state.df.copy())
    new_df, msg = op.func(st.session_state.df, params)
    st.session_state.df = new_df
    st.session_state.op_count += 1
    st.session_state.last_msg = msg
    st.session_state.last_op_title = op.title
    st.rerun()


def undo() -> None:
    if not st.session_state.history:
        return
    st.session_state.df = st.session_state.history.pop()
    st.session_state.op_count = max(0, st.session_state.op_count - 1)
    st.session_state.last_msg = "Последняя операция отменена."
    st.session_state.last_op_title = "Отмена"
    st.rerun()


def reset() -> None:
    st.session_state.df = get_demo_table()
    st.session_state.history = []
    st.session_state.op_count = 0
    st.session_state.last_msg = "Таблица сброшена к исходным данным."
    st.session_state.last_op_title = "Сброс"
    st.rerun()


# ─── Форма параметров ─────────────────────────────────────────────────

def render_param_input(spec: ParamSpec, op_id: str, columns: list[str]):
    """Возвращает значение одного параметра из виджета."""
    widget_key = f"{op_id}__{spec.key}"

    if spec.kind == "column":
        return st.selectbox(spec.label, columns, key=widget_key)

    if spec.kind == "columns_multi":
        chosen = st.multiselect(spec.label, columns, key=widget_key)
        return chosen if chosen else None

    if spec.kind == "value":
        return st.text_input(spec.label, key=widget_key)

    if spec.kind == "choice":
        labels = [label for label, _ in spec.options]
        values = [val for _, val in spec.options]
        default_val = spec.default if spec.default is not None else values[0]
        default_idx = values.index(default_val) if default_val in values else 0
        idx = st.radio(
            spec.label,
            range(len(labels)),
            index=default_idx,
            format_func=lambda i: labels[i],
            key=widget_key,
        )
        return values[idx]

    raise ValueError(f"Неизвестный тип параметра: {spec.kind}")


def render_op_with_params(op: Operation) -> None:
    """Операция с параметрами: expander + форма."""
    with st.expander(op.title):
        st.caption(op.description)
        columns = list(st.session_state.df.columns)
        with st.form(key=f"form__{op.id}"):
            params = {}
            for spec in op.params:
                params[spec.key] = render_param_input(spec, op.id, columns)
            submitted = st.form_submit_button("Применить")
        if submitted:
            apply_op(op, params)


# ─── Сайдбар ──────────────────────────────────────────────────────────

def render_sidebar() -> None:
    with st.sidebar:
        st.header("Операции")

        groups: dict[str, list[Operation]] = {}
        for op in OPERATIONS.values():
            groups.setdefault(op.group, []).append(op)

        for group_name, ops in groups.items():
            st.subheader(group_name)
            for op in ops:
                if not op.params:
                    if st.button(op.title, key=f"btn__{op.id}", help=op.description, use_container_width=True):
                        apply_op(op, {})
                else:
                    render_op_with_params(op)

        st.divider()
        st.subheader("Управление")

        can_undo = len(st.session_state.history) > 0
        col1, col2 = st.columns(2)
        with col1:
            if st.button("↩️ Отменить", disabled=not can_undo, use_container_width=True):
                undo()
        with col2:
            if st.button("🔄 Сбросить", use_container_width=True):
                reset()

        st.caption(f"В истории: {len(st.session_state.history)} шаг(ов)")


# ─── Основная область ────────────────────────────────────────────────

def render_main() -> None:
    st.title("📊 Демо-стенд: операции с таблицей")
    st.caption(
        "Демо-таблица «Продажи». Выбирайте операции в сайдбаре — таблица меняется. "
        "Любую операцию можно отменить."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Строк в таблице", len(st.session_state.df))
    col2.metric("Операций выполнено", st.session_state.op_count)
    col3.metric("Можно отменить", len(st.session_state.history))

    st.info(f"**{st.session_state.last_op_title}** — {st.session_state.last_msg}")

    if len(st.session_state.df) == 0:
        st.warning("Таблица пуста. Нажмите «Сбросить», чтобы вернуть исходные данные.")
    else:
        st.dataframe(st.session_state.df, use_container_width=True, height=500)


# ─── Точка входа ──────────────────────────────────────────────────────

def main() -> None:
    init_state()
    render_sidebar()
    render_main()


if __name__ == "__main__":
    main()
