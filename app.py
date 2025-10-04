import streamlit as st
import interface_text as inf
import Tool_main.prompt_maker as app_prompt
import Tool_main.tool_executer as te

st.title("Youtube data collector Tool")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_info" not in st.session_state:
    st.session_state.video_info = []

if 'channel_set' not in st.session_state:
    st.session_state.channel_set = set()

if 'in_prompt' not in st.session_state:
    st.session_state.in_prompt = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if 'step' not in st.session_state:
    st.session_state.step = "Get_User_input"
    st.session_state.language = ""
    st.session_state.category = ""
    st.session_state.subcategory = ""
    st.session_state.video_type = ""
    st.session_state.channel_number = 10


def reset_session_state():
    te.del_in_prompt_list()
    del st.session_state.messages
    del st.session_state.step
    st.rerun()


if st.session_state.step == "Get_User_input":
    with st.chat_message("assistant"):
        message = st.write_stream(inf.response_generator(0))
    st.session_state.messages.append({"role": "assistant", "content": message})

    with st.chat_message("assistant"):
        message = st.write_stream(inf.response_generator(1))
    st.session_state.messages.append({"role": "assistant", "content": message})

    st.session_state.step = "Prompt_mode_selection"
    st.rerun()
elif st.session_state.step == "Prompt_mode_selection":
    if st.button("Prompt guiado"):
        st.session_state.step = "Guide_prompt"
        st.rerun()

elif st.session_state.step == "Guide_prompt":
    with st.chat_message("user"):
        st.write("Prompt Guiado")
    st.session_state.messages.append({"role": "user", "content": "Prompt Guiado"})
    with st.chat_message("assistant"):
        message = st.write_stream(inf.response_generator(2))
    st.session_state.messages.append({"role": "assistant", "content": message})

    st.session_state.step = "Guide_prompt_2"
    st.rerun()

elif st.session_state.step == "Guide_prompt_2":
    language = st.text_input(inf.get_input_text(0))
    category = st.text_input(inf.get_input_text(1))
    subcategory = st.text_input(inf.get_input_text(2))
    total_channels = st.number_input(inf.get_input_text(3), min_value=1, value=10, step=1)
    st.warning(inf.get_warning_text(0))
    video_type = st.radio(inf.get_input_text(4), ('Videos y shorts', 'Shorts', 'Videos'), index=0)
    if st.button("Continuar"):
        if language and category and video_type:
            st.session_state.language = language
            st.session_state.category = category
            st.session_state.video_type = video_type
            st.session_state.channel_number = total_channels
            if subcategory:
                st.session_state.subcategory = subcategory
            else:
                st.session_state.subcategory = ""
            st.session_state.step = "Guide_prompt_3"
            st.rerun()
        else:
            st.warning(inf.get_warning_text(1))

elif st.session_state.step == "Guide_prompt_3":
    with st.chat_message("assistant"):
        message = st.write_stream(inf.response_generator(3))
    st.session_state.messages.append({"role": "assistant", "content": message})
    text = (f"Categoria: {st.session_state.category}, \tLugar o idioma: {st.session_state.language}, "
            f"\tTipo de video a buscar: {st.session_state.video_type}")
    with st.chat_message("user"):
        st.write(text)
    st.session_state.messages.append({"role": "user", "content": text})
    st.session_state.step = "Guide_prompt_4"
    st.rerun()

elif st.session_state.step == "Guide_prompt_4":
    if st.button("Volver"):
        st.session_state.step = "Prompt_mode_selection"
        st.rerun()
    if st.button("Ejecutar herramienta"):
        st.session_state.step = "Tool_execution"
        st.rerun()

elif st.session_state.step == "Tool_execution":
    # Get prompt
    prompt = app_prompt.get_prompt(st.session_state.language, st.session_state.category, st.session_state.video_type,
                                   st.session_state.subcategory, st.session_state.channel_number)
    # Tool execution
    te.execute_tool(prompt)

    st.session_state.step = "End_question"
    st.rerun()

elif st.session_state.step == "End_question":
    st.balloons()
    with st.chat_message("assistant"):
        message = st.write_stream(inf.response_generator(4))
    st.session_state.messages.append({"role": "assistant", "content": message})
    st.session_state.step = "End_selection"
    st.rerun()
elif st.session_state.step == "End_selection":
    if st.button("Seguir buscando canales"):
        st.session_state.step = "Tool_execution_again"
        st.rerun()
    if st.button("Buscar canales con otro prompt"):
        reset_session_state()
elif st.session_state.step == "Tool_execution_again":
    # Get the past list
    discard_in_prompt = te.get_in_prompt_list()
    # Get prompt
    prompt = app_prompt.get_prompt_again(st.session_state.language, st.session_state.category,
                                         st.session_state.video_type, st.session_state.subcategory,
                                         st.session_state.channel_number, discard_in_prompt)
    # Tool execution
    te.execute_tool(prompt)

    st.session_state.step = "End_question"
    st.rerun()
