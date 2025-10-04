def to_a1_notation(row, col):
    col_str = ""
    while col >= 0:
        col_str = chr(ord('A') + col % 26) + col_str
        col = col // 26 - 1
    return f"{col_str}{row + 1}"
