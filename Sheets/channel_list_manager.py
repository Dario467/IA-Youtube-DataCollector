from Services.sheet_service import sheet2
from Sheets.sheet_fuctions import to_a1_notation
import streamlit as st


def get_channel_set() -> set:
    return st.session_state.channel_set


def update_channel_set(_set: set[str]):
    if not st.session_state.channel_set:
        st.session_state.channel_set.update(_set)


def is_first_time() -> bool:
    if not st.session_state.channel_set:
        return True
    return False


def get_column_data(column_name: str) -> set[str]:
    # Getting first row values
    headers_row = sheet2.row_values(1)
    # Obtaining the index of the specific column with the specific name
    col_index = headers_row.index(column_name)
    # Obtaining all the values of the column with the index proportionate in a list
    col_values = sheet2.col_values(col_index + 1)
    # Converting the list into a set
    data_set = set(col_values)
    return data_set


def discard_repeat_data(in_prompt: list[str], channels_to_add: list[str]) -> list[str]:
    total_discard = 0
    data_row_index = len(st.session_state.channel_set)
    data_index = to_a1_notation(data_row_index, 0)
    added_channels = []
    filtered_channel_list = []
    in_prompt_list = []
    for channel in channels_to_add:
        if channel not in st.session_state.channel_set:
            st.session_state.channel_set.add(channel)
            added_channels.append([channel])
            filtered_channel_list.append(channel)
            if len(in_prompt_list) <= 10:
                in_prompt_list.append(channel)
        else:
            total_discard += 1
    if in_prompt_list:
        in_prompt.clear()
        in_prompt.extend(in_prompt_list)
    if added_channels:
        sheet2.update(added_channels, data_index)
        st.warning(f"Se descartaron {total_discard} canales que ya fueron analizaados previamente por la herramienta.")
        return filtered_channel_list
    else:
        st.warning(f"Se descartaron {total_discard} canales que ya fueron analizaados previamente por la herramienta.")
        return []
