

def get_prompt(languages: str, categories: str, video_types: str, subcategories: str, total_channel:  int) -> str:
    if not subcategories:
        return f"""Investiga a fondo, devuelve únicamente una lista con los nombres de {total_channel} canales de 
        YouTube que sean muy reconocidos y virales {languages} que se especializan en {categories}. Prioriza los que 
        hagan {video_types}. Devuélve solo una lista de Python con los nombres exactos de los canales como 
        strings sin texto extra.No uses markdown ni etiquetas como ```python., solo la lista. Si no encuentras 
        exactamente lo pedido, da solo canales similares."""
    else:
        return f"""Investiga a fondo, devuelve únicamente una lista con los nombres de {total_channel} canales de 
        YouTube que sean muy reconocidos y virales {languages} que se especializan en {categories} y {subcategories}. 
        Prioriza los que hagan {video_types}. Devuélve solo una lista de Python con los nombres exactos de los 
        canales como strings no texto extra. No uses markdown ni etiquetas como ```python., solo la lista. 
        Si no encuentras exactamente lo pedido, da solo canales similares."""


def get_prompt_again(languages: str, categories: str, types: str, subcategories: str, total: int, exclusion: list[str]):
    no_include_string = ",".join(exclusion)
    if not subcategories:
        return f"""Investiga a fondo, devuelve únicamente una lista con los nombres de {total} canales de 
        YouTube que sean muy reconocidos y virales {languages} que se especializan en {categories}. Prioriza los que 
        hagan {types}. que no sean {no_include_string}. Devuélve solo una lista de Python con los nombres exactos 
        de los canales como strings sin texto extra. No uses markdown ni etiquetas como ```python., solo la lista. 
        Si no encuentras exactamente lo pedido, da solo canales similares.n"""
    else:
        return f"""Investiga a fondo, devuelve únicamente una lista con los nombres de {total} canales de 
        YouTube que sean muy reconocidos y virales {languages} que se especializan en {categories} y {subcategories}. 
        Prioriza los que hagan {types}. que no sean {no_include_string}. Devuélve solo una lista de Python con 
        los nombres exactos de los canales como strings sin texto extra.No uses markdown ni etiquetas como ```python., 
        solo la lista. Si no encuentras exactamente lo pedido, da solo canales similares."""
