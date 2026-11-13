import streamlit as st
import frontmatter
from pathlib import Path

st.set_page_config(page_title="Справочник макросов", layout="wide")
st.title("📚 Справочник макросов VBA & Apps Script")

content_dir = Path("content")
cards = []
if content_dir.exists():
    for md_file in sorted(content_dir.rglob("*.md")):
        post = frontmatter.load(md_file)
        cards.append(post)

if not cards:
    st.warning("Карточки не найдены. Добавьте `.md` файлы в папку `content/`.")
else:
    st.sidebar.header("🔍 Фильтры")
    categories = sorted({card.metadata.get("category", md_file.parent.name) for card, md_file in zip(cards, sorted(content_dir.rglob("*.md")))})
    selected_category = st.sidebar.multiselect("Категория", categories, default=categories)

    for card, md_file in zip(cards, sorted(content_dir.rglob("*.md"))):
        category = card.metadata.get("category", md_file.parent.name)
        if selected_category and category not in selected_category:
            continue

        with st.expander(f"**{card.metadata.get('title', md_file.stem)}** — {card.metadata.get('description', '')}", expanded=False):
            for warning in card.metadata.get("warnings", []):
                st.warning(f"⚠️ {warning}")
            st.markdown(card.content)
