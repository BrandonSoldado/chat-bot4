from librerias import *

os.environ['OPENAI_API_KEY'] = 'sk-proj-9sZ52JPDfVBk1wHNGyraT3BlbkFJPPxeTzV9ezevy9VBjA8g'
embeddings = OpenAIEmbeddings()
os.environ['PINECONE_API_KEY'] = 'cee01680-c49f-4a68-90f6-4f1a888900c7'
index_name = "asistente-virtual"
docsearch = PineconeVectorStore(index_name=index_name, embedding=embeddings)

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "Solo respondes: true o false"),
    ("system", "respondes true: solamente cuando te pida que le des o le envies una factura proforma"),
    ("system", "respondes false: cuando mencione una factura proforma o hable de cualquier otro tema"),
    ("system", "Si te preguntan (solo escriben):factura proforma, devolve false"),
    ("system", "Si te piden una factura o desean o exigen factura, devolve false"),
    ("system", "Si te piden una factura o desean o exigen proforma, devolve true"),
    ("human", "{pregunta}")
])



id_usuario = 0
register_llm_provider("groq", ChatGroq)
chat = ChatGroq(temperature=0, groq_api_key="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", model_name="llama3-8b-8192")
chat2 = ChatGroq(temperature=0, groq_api_key="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", model_name="llama3-8b-8192")
chat3 = ChatGroq(temperature=0, groq_api_key="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", model_name="llama3-8b-8192")
chat4 = ChatGroq(temperature=0, groq_api_key="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", model_name="llama3-8b-8192")

def ObtenetRespuestaIA(mensaje):
    docs = docsearch.similarity_search(mensaje)
    print(docs[0].page_content)
    datos = str(docs[0].page_content)
    global historial
    historial.append({"role": "user", "content": "esta es la pregunta: "+mensaje+", respondele usando estos datos: "+datos})
    response = chat.invoke(historial)
    return str(response.content)

def DeterminarSiEsFactura(mensaje):
    chain = prompt1 | chat2
    response = chain.invoke({"pregunta": mensaje})
    return str(response.content)

def ObtenerListaProductos(mensaje):
    chain = prompt2 | chat3
    response = chain.invoke({"pregunta": mensaje})
    return str(response.content)

def TodosProductosEstanLista(mensaje):
    chain = prompt3 | chat4
    response = chain.invoke({"pregunta": mensaje})
    return str(response.content)


app = Flask(__name__)
@app.route("/webhook", methods=["POST"])
def webhook():
    global historial
    global id_usuario
    pregunta = request.form.get("Body")
    telefono_usuario = request.form.get("From")
    nombre_usuario = obtener_nombre_usuario(telefono_usuario)
    if pregunta.lower() == "confirm":
        id_usuario = obtener_id_usuario(telefono_usuario)
        respuesta_chat = mensaje_presentacion(nombre_usuario) 
    else:
        if (DeterminarSiEsFactura(pregunta).lower()=="true"):
            pregunta22 = TodosProductosEstanLista(pregunta)
            respuesta_chat = ObtenerListaProductos(pregunta22)
            texto_limpio = respuesta_chat.replace('\n', '').replace(' ', '')
            lista_de_listas = literal_eval(texto_limpio)
            generate_proforma_invoice("factura_proforma.pdf",lista_de_listas)              
            SubirPDFazure()
            EnviarPDF(telefono_usuario,ObtenerURLpdf())
            EliminarPDFplataforma()
            respuesta_chat = "Aqui esta tu factura proforma!"
        else:
            id_usuario = obtener_id_usuario(telefono_usuario)
            cargar_historial(nombre_usuario)
            agregar_preguntas_respuestas_al_historial(id_usuario)
            respuesta_chat = ObtenetRespuestaIA(pregunta)   
            insertar_conversacion(pregunta,respuesta_chat,obtener_fecha_actual(),obtener_hora_actual(),id_usuario) 
    respuesta = MessagingResponse()
    respuesta.message(respuesta_chat)
    return str(respuesta)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
