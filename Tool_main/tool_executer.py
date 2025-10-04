import streamlit as st
import Sheets.sheet_controller as shc
import Sheets.channel_list_manager as chlm
import Youtube.YT_info_searcher
import Gemini.AI_channel_generation as Channels_ai


def get_in_prompt_list() -> list[str]:
    return st.session_state.in_prompt


def del_in_prompt_list():
    del st.session_state.in_prompt


def tool_discard_execution(channel_name_list: list[str]) -> list[str]:
    st.write("Checking that the AI did not suggest duplicate channels")
    if chlm.is_first_time():
        channel_set = chlm.get_column_data("ChannelsData")
        chlm.update_channel_set(channel_set)
        return chlm.discard_repeat_data(st.session_state.in_prompt, channel_name_list)
    else:
        return chlm.discard_repeat_data(st.session_state.in_prompt, channel_name_list)


def execute_tool(channel_prompt: str):
    st.write("Generating request...")
    channel_name_list = Channels_ai.ia_google_search_request(channel_prompt)
    if not channel_name_list:
        st.warning("Not valid response")
    else:
        st.write("Channel's to process:")
        st.write(channel_name_list)
        channel_name_list = tool_discard_execution(channel_name_list)
        if channel_name_list:
            for channel_name in channel_name_list:
                videos = Youtube.YT_info_searcher.most_view_videos(channel_name)
                if not videos:
                    continue
                Youtube.YT_info_searcher.videos_info(videos, st.session_state.video_info)
            shc.update_cell_by_column_name("Titulo", st.session_state.video_info, 1)
        else:
            st.error('''Todos los canales sugeridos por la IA coinciden con entradas ya analizadas.
            Para obtener nuevos resultados, considera refinar el prompt con mayor detalle, modificar la 
            categoría/subcategoría, o cambiar de enfoque temático. ''')
