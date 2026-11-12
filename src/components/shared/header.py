import streamlit as st


def render_header() -> None:
    st.markdown(
        """
        <div class="brand">
          <h1><span class="accent">&gt;_</span> Rede Social Profissional</h1>
          <p>Conecte-se, compartilhe código e evolua na área de TI.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
