from groq import Groq
import os
import json
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Inicializa el cliente de Groq con la API key definida en las variables de entorno
cliente = Groq(
   api_key=os.getenv("GROQ_API_KEY")
)


def sugerir_recetas(productos: list[dict]):
   """
   Genera sugerencias de recetas a partir de los productos disponibles en el inventario.

   Construye un prompt estructurado y lo envía al modelo LLaMA via Groq.
   La respuesta esperada es un JSON con exactamente 4 recetas.

   - **productos**: Lista de diccionarios con las claves `id_producto`, `nombre` y `cantidad`.
   - Retorna un diccionario con la clave `recetas` si el modelo responde correctamente.
   - Retorna un diccionario con `error` y `respuesta` si el JSON devuelto no es válido.
   """

   # Convierte la lista de productos en texto plano para incluirlo en el prompt
   lista_texto = ""
   for p in productos:
       lista_texto += (
           f"- id_producto: {p['id_producto']}, "
           f"nombre: {p['nombre']}, "
           f"cantidad disponible: {p['cantidad']}\n"
       )

   # Prompt enviado al modelo con instrucciones estrictas sobre formato y consistencia de IDs
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

   # Envía el prompt al modelo LLaMA con temperatura baja para respuestas más deterministas
   respuesta = cliente.chat.completions.create(
       model="llama-3.1-8b-instant",
       messages=[
           {
               "role": "user",
               "content": prompt
           }
       ],
       temperature=0.2  # Valor bajo para reducir variabilidad en la respuesta
   )

   # Extrae el contenido de texto de la primera opción de respuesta del modelo
   contenido = respuesta.choices[0].message.content

   try:
       # Intenta parsear la respuesta como JSON válido
       return json.loads(contenido)
   except json.JSONDecodeError:
       # Si el modelo no devuelve JSON válido, retorna el error junto con la respuesta cruda
       return {
           "error": "La IA no devolvió un JSON válido",
           "respuesta": contenido
       }