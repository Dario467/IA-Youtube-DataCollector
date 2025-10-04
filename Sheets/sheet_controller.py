from Services.sheet_service import sheet1
from Sheets.sheet_fuctions import to_a1_notation
import streamlit as st


def update_cell_by_column_name(column_name: str, content: list[list], header_row: int):
    st.write("Filling sheet...")
    # Obtaining all values in the row 1
    headers_row = sheet1.row_values(header_row)
    try:
        # Obtaining the index of the specific column with the specific name
        col_index = headers_row.index(column_name)
        # Obtaining all the values of the column with the index proportionate in a list
        col_values = sheet1.col_values(col_index+1)
        # By the length of the list we obtain the next row
        next_index = len(col_values)
        # Obtain the last index
        last_index = next_index + len(content)
        # If the next row index pass the sheet row limit we add +1000 rows
        if last_index >= sheet1.row_count - 5:
            sheet1.add_rows(1000)
            st.warning("1000 empty rows were added into the sheets")
        # Update the sheet
        # sheet1.update_cell(next_index, col_index, content)
        start_cell = to_a1_notation(next_index, col_index)
        sheet1.update(start_cell, content)
    except ValueError:
        # if the  column name did not exist we send this message in the console
        st.error(f"The column header {column_name} was not found")
