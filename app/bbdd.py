import psycopg2
from psycopg2 import OperationalError, Error
from datetime import datetime

def EjecutarConsultaSqlGeneral(query):
    conn = psycopg2.connect(
        dbname="ChatBot",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432",
        options="-c client_encoding=utf8"
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(str(query))
            resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error ejecutando la consulta: {e}")
        return []


def obtener_fecha_actual():
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    return fecha_actual

def obtener_hora_actual():
    hora_actual = datetime.now().strftime("%H:%M:%S")
    return hora_actual


def obtener_ultimas_preguntas_usuario(usuario_id):
    try:
        conn = psycopg2.connect(
            dbname="ChatBot",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432",
            options="-c client_encoding=utf8"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT Pregunta 
            FROM HISTORIAL 
            WHERE UsuarioID = %s 
            ORDER BY Fecha DESC, Hora DESC 
            LIMIT 5;
        """, (usuario_id,))
        preguntas = cur.fetchall()
        cur.close()
        conn.close()
        preguntas_lista = [pregunta[0] for pregunta in preguntas]  # Extrae solo las preguntas de los resultados
        return tuple(preguntas_lista)  # Retorna una tupla con las últimas 5 preguntas
        
    except (OperationalError, Error) as e:
        print(f"Error al obtener últimas preguntas del usuario: {e}")
        return ()

def obtener_ultimas_respuestas_usuario(usuario_id):
    try:
        conn = psycopg2.connect(
            dbname="ChatBot",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432",
            options="-c client_encoding=utf8"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT Respuesta 
            FROM HISTORIAL 
            WHERE UsuarioID = %s 
            ORDER BY Fecha DESC, Hora DESC 
            LIMIT 5;
        """, (usuario_id,))
        preguntas = cur.fetchall()
        cur.close()
        conn.close()
        preguntas_lista = [pregunta[0] for pregunta in preguntas]  # Extrae solo las preguntas de los resultados
        return tuple(preguntas_lista)  # Retorna una tupla con las últimas 5 preguntas
        
    except (OperationalError, Error) as e:
        print(f"Error al obtener últimas preguntas del usuario: {e}")
        return ()


def obtener_nombre_usuario(telefono):
    try:
        conn = psycopg2.connect(
            dbname="ChatBot",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432",
            options="-c client_encoding=latin1"
        )
        with conn.cursor() as cur:
            cur.execute("SELECT nombre FROM usuario WHERE telefono = %s", (telefono,))
            nombre = cur.fetchone()
            return nombre[0] if nombre else ""
    except (OperationalError, Error) as e:
        print(f"Error al obtener nombre del usuario: {e}")
        return ""
    finally:
        if conn:
            conn.close()

def obtener_id_usuario(telefono):
    try:
        conn = psycopg2.connect(
            dbname="ChatBot",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432",
            options="-c client_encoding=latin1"
        )
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM usuario WHERE telefono = %s", (telefono,))
            id = cur.fetchone()
            return id[0] if id else -1
    except (OperationalError, Error) as e:
        print(f"Error al obtener ID del usuario: {e}")
        return -1
    finally:
        if conn:
            conn.close()


def insertar_conversacion(pregunta, respuesta, fecha, hora, usuario_id):
    try:
        conn = psycopg2.connect(
            dbname="ChatBot",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432",
            options="-c client_encoding=utf8"
        )
        with conn.cursor() as cur:
            cur.execute("INSERT INTO HISTORIAL (Pregunta, Respuesta, Fecha, Hora, UsuarioID) VALUES (%s, %s, %s, %s, %s)", 
                        (pregunta, respuesta, fecha, hora, usuario_id))
            conn.commit()
            print("Pregunta insertada correctamente.")
    except (OperationalError, Error) as e:
        print(f"Error al insertar pregunta: {e}")
    finally:
        if conn:
            conn.close()
