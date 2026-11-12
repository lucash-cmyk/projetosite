import html

import streamlit as st

from dto.posts.request.post_requests import CATEGORIES, normalize_tags


def _reset_page() -> None:
    st.session_state["feed_page"] = 0


def render_sidebar(container, user, cookies=None) -> dict:
    """Desenha a barra lateral e devolve os filtros do feed."""
    with st.sidebar:
        st.markdown(f"**{html.escape(user['name'])}**")
        if user.get("headline"):
            st.caption(user["headline"])
        if st.button("Sair", use_container_width=True):
            container.sessions.logout(st.session_state.get("token"))
            if cookies is not None:
                cookies.remove("session_token")
            container.presence.delete(user["id"])
            st.session_state.clear()
            st.rerun()
        online=container.presence.get_paginated(0,100)
        if online.status:
            st.caption(f"🟢 {len(online.data)} usuário(s) com presença registrada")

        st.divider()
        st.subheader("Filtrar feed")
        category = st.selectbox(
            "Categoria", ["Todas", *CATEGORIES], key="filter_category", on_change=_reset_page
        )
        tag_text = st.text_input(
            "Tag (ex.: python)", key="filter_tag", on_change=_reset_page
        )

    filters = {}
    if category != "Todas":
        filters["category"] = category
    try:
        tags = normalize_tags(tag_text)
    except ValueError:
        tags = []
        st.sidebar.warning("Tag inválida no filtro.")
    if tags:
        filters["tag"] = tags[0]
    return filters
