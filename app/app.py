<<<<<<< HEAD
from librerias import *

historial = ""
id_usuario = 0
register_llm_provider("groq", ChatGroq)
chat = ChatGroq(temperature=0.5, groq_api_key="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", model_name="llama3-8b-8192")

def actualizar_prompt():
    global prompt1
    global prompt2
    prompt1 = ChatPromptTemplate.from_messages([
    ("system", """Eres un asistente virtual que determina que tipo de hongo hay en una superficie como pared, techo, etc. y sobre que 
    producto sirve para eliminar un hongo"""),
    
    ("system", """Si te preguntan que productos vendes o conoces, de la lista que te van a dar busca los productos y precios (los precios estan en bolivianos bs), luego respondele"""),
    ("system", "Previamente te hice estas preguntas: "+historial),
    ("human", "Responde a esta pregunta: {pregunta}, quiero que respondas usando estos datos: {datos}")
    ])
    prompt2 = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente virtual que convierte preguntas a su equivalente en una consulta en postgress usando el lenguaje sql, solo respondes la consulta sql, sin mas texto extra"),
    ("system", "Conveierte las preguntas a su equivalente en una consulta en postgress, guiandote de esta base de datos: "+prompt_bbdd),
    ("system", "Los hongos que conoces son los aquellos que estan insertados en la tabla HONGO"),
    ("system", "El id de este usuario es: " +str(id_usuario)),
    ("system", "Los productos que vendes para eliminar algun hongo o conoces son todos aquellos que estan insertados en la tabla PRODUCTO, cada vez que te pidan un producto mostra su precio tambien"),
    ("system", "Previamente te hice estas preguntas: "+historial),
    ("human", "Esta pregunta: {pregunta}, convertilo a una consulta SQL en postgress."),
    ])




prompt1 = ChatPromptTemplate.from_messages([
    ("system", """Eres un asistente virtual que determina que tipo de hongo hay en una superficie como pared, techo, etc. y sobre que 
               producto sirve para eliminar un hongo"""),
    ("system", """Si te preguntan que productos vendes o conoces, de la lista que te van a dar busca los productos y precios (los precios estan en bolivianos bs), luego respondele"""),
    ("human", "Previamente te hice estas preguntas: "+historial + "Responde a esta pregunta: {pregunta}, quiero que respondas usando estos datos: {datos}")
])
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente virtual que convierte preguntas a su equivalente en una consulta en postgress usando el lenguaje sql, solo respondes la consulta sql, sin mas texto extra"),
    ("system", "Conveierte las preguntas a su equivalente en una consulta en postgress, guiandote de esta base de datos: "+prompt_bbdd),
    ("system", "Los hongos que conoces son los aquellos que estan insertados en la tabla HONGO"),
    ("system", "El id de este usuario es: " +str(id_usuario)),
    ("system", "Los productos que vendes para eliminar algun hongo o conoces son todos aquellos que estan insertados en la tabla PRODUCTO, cada vez que te pidan un producto mostra su precio tambien"),
    ("human", "Previamente te hice estas preguntas: "+historial + "Esta pregunta: {pregunta}, convertilo a una consulta SQL en postgress."),
])


def ObtenetRespuestaIA(mensaje):
    actualizar_prompt()
    chain = prompt2 | chat
    response = chain.invoke({"pregunta": mensaje})
    #enviar_pregunta_auxiliar(response.content)
    sql = EjecutarConsultaSqlGeneral(response.content)
    print(str(sql))
    chain = prompt1 | chat
    response = chain.invoke({"pregunta": mensaje,"datos": sql})
=======
from config import *


register_llm_provider("groq", ChatGroq)
chat = ChatGroq(temperature=1, groq_api_key="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", model_name="llama3-70b-8192")


prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente virtual que responde a preguntas sobre hongos"),
    ("human", "{text}")
])
#chain = prompt | chat
chain = chat
def chatbot(mensaje):
    global historial
    historial.append({"role": "user", "content": mensaje})
    #response = chain.invoke({"text": mensaje})
    response = chain.invoke(historial)
>>>>>>> 2711317a02654b8e7783c0477da2812f88316273
    return response.content




app = Flask(__name__)
@app.route("/webhook", methods=["POST"])
def webhook():
<<<<<<< HEAD
    global historial
    global id_usuario
    pregunta = request.form.get("Body")
    telefono_usuario = request.form.get("From")
    if pregunta.lower() == "confirm":
        id_usuario = obtener_id_usuario(telefono_usuario)
        nombre_usuario = obtener_nombre_usuario(telefono_usuario)
        respuesta_chat = mensaje_presentacion(nombre_usuario) 
    else:
        id_usuario = obtener_id_usuario(telefono_usuario)
        historial = obtener_historial_preguntas(id_usuario)
        respuesta_chat = ObtenetRespuestaIA(pregunta)  
        insertar_conversacion(pregunta,respuesta_chat,obtener_fecha_actual(),obtener_hora_actual(),id_usuario) 
    respuesta = MessagingResponse()
    respuesta.message(respuesta_chat)
    print(respuesta_chat)
    return str(respuesta)
=======
    message_body = request.form.get("Body")
    from_number = request.form.get("From")
    nombre = obtener_nombre_usuario(from_number)
    if message_body.lower() == "confirm":
        respuesta = mensaje_presentacion(nombre) 
    else:
        id_usuario = obtener_id_usuario(from_number)
        cargar_historial(nombre)
        agregar_preguntas_respuestas_al_historial(id_usuario)     
        respuesta = chatbot(message_body)  
        insertar_conversacion(message_body,respuesta,obtener_fecha_actual(),obtener_hora_actual(),id_usuario) 
    resp = MessagingResponse()
    resp.message(respuesta)
    print(message_body)
    print(respuesta)
    return str(resp)


>>>>>>> 2711317a02654b8e7783c0477da2812f88316273


if __name__ == "__main__":
    app.run(debug=True, port=5000)