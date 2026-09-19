from html import escape


def messages(attempt):
    return [
        *attempt.get("prompt_messages", []),
        {"role": "assistant", "content": attempt.get("response_text", "")},
    ]


def render(attempt):
    import streamlit as st

    for msg in messages(attempt):
        role = msg.get("role", "?")
        klass = {
            "user": "msg msg-user",
            "assistant": "msg msg-assistant",
            "system": "msg msg-system",
        }.get(role, "msg")
        body = escape(str(msg.get("content", "")))
        st.markdown(
            f'<div class="{klass}"><div class="role">{escape(role)}</div>'
            f'<div class="body">{body}</div></div>',
            unsafe_allow_html=True,
        )
