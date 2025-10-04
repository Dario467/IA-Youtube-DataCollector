import time
import streamlit as st


def split_text_time(text: str):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)


def response_generator(index: int):
    text_list = [
        '''¡Hola! Estoy aquí para ayudarte a recolectar datos sobre los videos más virales''',
        '''Para iniciar el proceso, por favor, ingrese un prompt detallando los criterios de los canales 
        que desea localizar.''',
        '''Perfecto, para poder continuar rellena los siguientes cuadros de texto: ''',
        '''¡Listo! Por favor, revise que su selección sea correcta. ¿Desea continuar con esta información o prefiere 
        volver para hacer algún cambio?''',
        '''Tu Google sheet ha sido rellenada con exito'''
    ]
    return split_text_time(text_list[index])


def get_input_text(index: int) -> str:
    text_list = ['''Indique el idioma o región usando el formato (en [su preferencia]). Por ejemplo:
     en español, en Argentina, en inglés y japonés, en el mundo...''',
                 '''Por favor, especifique la categoría principal que definirán los parámetros para la búsqueda de 
                 canales. Ejemplo: Emprendimiento''',
                 '''Para mayor precisión, puede complementar su prompt especificando una subcategoría o 
                 añadiendo detalles adicionales. **(Este campo es opcional)**.''',
                 '''Indique un numero entero de canales que quieres que te recomiende la IA''',
                 "Seleccione el formato de video deseado: "]
    return text_list[index]


def get_warning_text(index: int) -> str:
    text_list = ['''**Aviso:** Un número elevado de canales consumira mas rapido los limites de requests de la 
    herramienta, tambien puede incrementar la probabilidad de que la IA genere resultados imprecisos o no entregue la 
    cantidad exacta solicitada. **Cantidad recomendada y por defecto: 10**. Si la categoria es amplia se recomienda
    escribir un numero mayor''',
                 "no puedes dejar cuadros de texto vacíos."]
    return text_list[index]


def reset_process():
    # Clean the session state
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
