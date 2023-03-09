import streamlit as st
import openai
import os

st.title("ChatGPT聊天机器人")
st.markdown(
    """
    使用 Openai chatgpt gpt-3.5-turbo 模型创建的聊天机器人
    """
)

api_key = os.environ.get("OPENAI_API_KEY", None)
error_block = st.empty()
if not api_key:
    error_block.error(
        "Please input your api_key from openai https://platform.openai.com/account/api-keys or this app won't work"
    )
    api_key = st.text_input("Api Key", key="api_key_input")
    if api_key:
        error_block.empty()

openai.api_key = api_key
# create role selection
role = st.selectbox("选择AI角色", ["默认机器人", "中英翻译", "心理咨询师"])
prompt_dict = {
    # You are a friendly and helpful assistant.
    "默认机器人": "",
    "中英翻译": "你现在是一个中英翻译机器人，翻译用户输入的每一句话，如果输入是中文，翻译成英文，如果输入是英文，翻译成中文",
    "心理咨询师": "你现在是一个心理咨询师，请友好，耐心，详细地帮助客户解答疑惑",
}
default_prompt = prompt_dict.get(role, '') # type: ignore
# create prompt input box, default value is role_prompt

with st.expander("自定义提示词", expanded=False):
    st.markdown("这个[网站](https://newzone.top/chatgpt/) 有很多有趣的AI角色（或者说prompt/shortcut），可以试试，也可以输入自定义的 prompt提示词")
    role_prompt = st.text_input("输入自定义prompt", value=default_prompt, key="prompt_input")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "system", "content": f"{role_prompt}"}]

# user input
user_input = st.text_input("用户输入", key="user_input")

# create a clear history button
clear_history = st.button("清空历史记录")

if clear_history or role_prompt != st.session_state["chat_history"][0]["content"]:
    # reset chat history with role
    st.session_state["chat_history"] = [{"role": "system", "content": f"{role_prompt}"}]
    user_input = None
    st.session_state["chat_history"] = [{"role": "system", "content": f"{role_prompt}"}]
    user_input = None

with st.expander("聊天记录", expanded=True):
    spin = st.container()
    stream_block = st.empty()
    history_block = st.container()

    rename_dict = {"user": "User   ", "assistant": "Chatgpt", "system": "Prompt"}


    if user_input:
        st.session_state["chat_history"].append(
            {"role": "user", "content": f"{user_input}"}
        )
        with history_block:
            for message in st.session_state["chat_history"][::-1]:
                name = rename_dict.get(message["role"], message["role"])
                st.markdown(f"{name}: {message['content']}")

        with spin:
            with st.spinner("生成中..."):
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state["chat_history"],
                    temperature=1,
                    stream=True,
                )

                # 流式（实时）显示chatgpt的返回信息
                chat_response = ""
                for res in completion:
                    word = res.choices[0].delta.get("content", "")
                    chat_response += word
                    stream_block.markdown("chatGPT: " + chat_response)
                st.session_state["chat_history"].append(
                    {"role": "assistant", "content": chat_response}
                )
