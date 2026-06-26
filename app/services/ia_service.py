from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

cliente = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def sugerir_recetas(productos: list[dict]):

    lista_texto = ""

    for p in productos:
        lista_texto += (
            f"- id_producto: {p['id_producto']}, "
            f"nombre: {p['nombre']}, "
            f"cantidad disponible: {p['cantidad']}\n"
        )

    prompt = f"""
        Tengo disponibles los siguientes productos del inventario.

        Cada producto tiene un id_producto que NO debes modificar.

        Productos disponibles:

        {lista_texto}

        Sugiere exactamente 4 recetas utilizando únicamente estos productos.

        Para cada ingrediente debes conservar exactamente el mismo id_producto que aparece en la lista anterior.pero no se necesita mostrar los id_producto

        Nunca inventes ids.
        Nunca cambies un id.
        Si utilizas "Pollo", debes devolver el id_producto correspondiente al pollo.
        Si utilizas "Queso", debes devolver el id_producto correspondiente al queso.

        Responde únicamente un JSON válido con este formato:

        {{
        "recetas":[
            {{
            "titulo":"",
            "descripcion":"",
            "ingredientes":[
                {{
                "id_producto":0,
                "nombre":"",
                "cantidad":""
                }}
            ]
            }}
        ]
        }}

        La descripción los pasos a pasos para preparar la receta

        No escribas explicaciones.
        No escribas markdown.
        No escribas ```json.
        Devuelve solamente el objeto JSON.
        """
    respuesta = cliente.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    contenido = respuesta.choices[0].message.content

    try:
        return json.loads(contenido)
    except json.JSONDecodeError:
        return {
            "error": "La IA no devolvió un JSON válido",
            "respuesta": contenido
        }