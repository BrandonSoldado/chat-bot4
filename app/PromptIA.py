from bbdd import *

historial = []

def agregar_preguntas_respuestas_al_historial(usuario_id):
    global historial
    preguntas = obtener_ultimas_preguntas_usuario(usuario_id)
    respuestas = obtener_ultimas_respuestas_usuario(usuario_id)
    preguntas = list(reversed(preguntas))
    respuestas = list(reversed(respuestas))
    for pregunta, respuesta in zip(preguntas, respuestas):
        historial.append({"role": "user", "content": pregunta})
        historial.append({"role": "assistant", "content": respuesta})

def cargar_historial(nombre):
    global historial
    historial.clear()
    historial.append({"role": "user", "content": """podes simular ser un chat bot asistente que determina que tipo de hongo hay en una superficie como la pared, techo, ect., quiero que en tu presentacion saludes a este nombre: """+nombre})
    historial.append({"role": "assistant", "content": mensaje_presentacion(nombre)})
    
    historial.append({"role": "user", "content": "Los datos que te doy son inserciones de esta bbdd: " +prompt_bbdd})
    historial.append({"role": "assistant", "content": "Entendido."})

    historial.append({"role": "user", "content": "En tus respuestas quiero que no menciones a la base de datos, ni me saludes"})
    historial.append({"role": "assistant", "content": "Entendido."})
    
    historial.append({"role": "user", "content": "Solo respondes preguntas relacionadas sobre hongos,sea producto, compras,etc., responde que no tenes informacion sobre ese tema"})
    historial.append({"role": "assistant", "content": "Entendido."})
    
    historial.append({"role": "user", "content": "Si te preguntan con que producto puedo eliminar un hongo o que producto vendes, quiero que le mostres los productos que se relacionan con ese hongo que te preguntaron, queiro que mostres el producto y su precio que esta en la bbdd, el precio mostralo en bolivianos (bs)"})
    historial.append({"role": "assistant", "content": "Entendido."})
    
    historial.append({"role": "user", "content": "Si los datos que te doy para responder no coinciden con la pregunta que te doy, responde usando tus conocimientos"})
    historial.append({"role": "assistant", "content": "Entendido."})

    historial.append({"role": "user", "content": "No quiero que me mostres los id de los datos que te doy para responder"})
    historial.append({"role": "assistant", "content": "Entendido."})







def mensaje_presentacion(nombre):
    return "¡Hola "+ nombre+"""! Soy el asistente de detección de hongos, aquí para ayudarte a identificar el tipo de hongo que se encuentra en una superficie. Estoy listo para trabajar contigo.

Por favor, dime más sobre la superficie donde crees que hay un hongo. ¿Es una pared interior o exterior, un techo, un suelo, o algo más? ¿Cuál es el aspecto del hongo? ¿Es blanco, verde, negro, o de algún otro color? ¿Tiene un olor desagradable o algún otro detalle notable?

Cuanto más información me proporciones, mejor podré ayudarte a identificar el tipo de hongo que estás viendo. ¡Empecemos!"""


prompt_bbdd= """
CREATE TABLE HONGO (ID INT PRIMARY KEY, Nombre VARCHAR(50), Descripcion TEXT);
CREATE TABLE USUARIO (ID INT PRIMARY KEY, Nombre VARCHAR(60), Ci INT, Direccion VARCHAR(60), Email VARCHAR(60), FechaNacimiento DATE, Telefono VARCHAR(20));
CREATE TABLE COMPRA (ID INT PRIMARY KEY, Fecha DATE, Total NUMERIC(10, 2),  UsuarioID INT REFERENCES USUARIO(ID));
CREATE TABLE SUPERFICIE (SitioHongo VARCHAR(60) NOT NULL, UsuarioID INT, HongoID INT, PRIMARY KEY (UsuarioID, HongoID), FOREIGN KEY (UsuarioID) REFERENCES USUARIO(ID) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (HongoID) REFERENCES HONGO(ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE AMBIENTE_FAVORABLE (ID SERIAL PRIMARY KEY, Nombre VARCHAR(100));
CREATE TABLE DESARROLLA (HongoID INT,AmbienteID INT, Descripcion TEXT, PRIMARY KEY (HongoID, AmbienteID), FOREIGN KEY (HongoID) REFERENCES HONGO(ID) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (AmbienteID) REFERENCES AMBIENTE_FAVORABLE(ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE SINTOMA (ID SERIAL PRIMARY KEY, Nombre VARCHAR(100));
CREATE TABLE PRODUCE (HongoID INT, SintomaID INT, PRIMARY KEY (HongoID, SintomaID), FOREIGN KEY (HongoID) REFERENCES HONGO(ID) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (SintomaID) REFERENCES SINTOMA(ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE PRODUCTO (ID INT PRIMARY KEY, Nombre VARCHAR(255), Descripcion TEXT, Precio NUMERIC(10, 2), EsNuevo BOOLEAN);
CREATE TABLE DETALLE_COMPRA (Cantidad INT, CompraID INT, ProductoID INT, PRIMARY KEY (CompraID, ProductoID), FOREIGN KEY (CompraID) REFERENCES COMPRA(ID) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (ProductoID) REFERENCES PRODUCTO(ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE OFERTA (ID SERIAL PRIMARY KEY, PrecioOferta NUMERIC(10, 2), Descripcion TEXT, ProductoID INT REFERENCES PRODUCTO(ID));
CREATE TABLE ANTIBIOTICO (PRODUCTOID INT, HongoID INT, PRIMARY KEY (PRODUCTOID, HongoID), FOREIGN KEY (PRODUCTOID) REFERENCES PRODUCTO(ID) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (HongoID) REFERENCES HONGO(ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE PATRON_CRECIENTO (ID SERIAL PRIMARY KEY, Nombre VARCHAR(60));
CREATE TABLE FORMA (Descripcion TEXT, HongoID INT, PATRON_CRECIENTOID INT, PRIMARY KEY (HongoID, PATRON_CRECIENTOID), FOREIGN KEY (HongoID) REFERENCES HONGO(ID) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (PATRON_CRECIENTOID) REFERENCES PATRON_CRECIENTO(ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE TEXTURA (ID SERIAL PRIMARY KEY, Nombre VARCHAR(100));
CREATE TABLE PRESENTA (HongoID INT, TexturaID INT, PRIMARY KEY (HongoID, TexturaID), FOREIGN KEY (HongoID) REFERENCES HONGO(ID) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (TexturaID) REFERENCES TEXTURA(ID) ON UPDATE CASCADE ON DELETE CASCADE);
CREATE TABLE COLOR (ID SERIAL PRIMARY KEY, Nombre VARCHAR(100));
CREATE TABLE CORRESPONDE (ColorID INT, EtapaDesarrollo VARCHAR(100), HongoID INT, PRIMARY KEY (HongoID, ColorID), FOREIGN KEY (HongoID) REFERENCES HONGO(ID) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (ColorID) REFERENCES COLOR(ID) ON UPDATE CASCADE ON DELETE CASCADE);"""
