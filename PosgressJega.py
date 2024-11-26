import psycopg2
from psycopg2 import sql
from datetime import datetime

# Datos de conexión
DB_HOST = "10.124.0.5"#"192.168.193.5"#"10.124.0.5"#
DB_NAME = "dbcorp"
DB_USER = "dev_jhurtado" 
DB_PASSWORD = "Pka12msE1b2qO@1"#"Pka12msE1b2qO%401"#"Pka12msE1b2qO@1"#
DB_PORT = "5432"  # Por defecto, PostgreSQL utiliza el puerto 5432
SCHEMA_NAME = 'jega'  # Nombre del esquema donde están tus tablas

def connect_db():
    """Conectar a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None


def create_user(usu_id, nombres, apellidos, correo, celular, cargo,rol):
    """Crear un nuevo usuario en la tabla jega_usuario."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}."jega_usuario" (usu_id, usu_nombres, usu_apellidos, usu_correo, usu_celular, usu_cargo,usu_rol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (usu_id, nombres, apellidos, correo, celular, cargo,rol))
                conn.commit()
                print(f"Usuario {nombres} {apellidos} creado con éxito.")
            except Exception as e:
                print(f"Error al crear usuario: {e}")
            finally:
                cur.close()
                conn.close()

def create_role(rol_tipo):
    """Crear un nuevo rol en la tabla jega_roles."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}."jega_roles" (rol_tipo)
                    VALUES (%s);
                """, (rol_tipo,))
                conn.commit()
                print(f"Rol '{rol_tipo}' creado con éxito.")
            except Exception as e:
                print(f"Error al crear rol: {e}")
            finally:
                cur.close()
                conn.close()

def add_question(pre_canal_id, pre_cliente, pre_pregunta):
    """Agregar una nueva pregunta en la tabla jega_preguntas y retornar el ID de la pregunta creada."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}."jega_preguntas" (pre_canal_id, pre_id_usuario, pre_fecha, pre_pregunta)
                    VALUES (%s, %s, %s, %s)
                    RETURNING pre_id;  -- Devuelve el ID de la pregunta creada
                """, (pre_canal_id, pre_cliente, datetime.now(), pre_pregunta))
                
                # Obtener el ID de la pregunta creada
                pregunta_id = cur.fetchone()[0]  # fetchone() devuelve una tupla, así que obtenemos el primer elemento
                conn.commit()
                print(f"Pregunta '{pre_pregunta}' agregada con éxito. ID: {pregunta_id}")
                return pregunta_id  # Retorna el ID de la pregunta
            except Exception as e:
                print(f"Error al agregar pregunta: {e}")
            finally:
                cur.close()
                conn.close()

def add_channel(can_descripcion_canal):
    """Agregar un nuevo canal en la tabla jega_canal."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}."jega_canal" (can_descripcion_canal)
                    VALUES (%s);
                """, (can_descripcion_canal,))
                conn.commit()
                print(f"Canal '{can_descripcion_canal}' agregado con éxito.")
            except Exception as e:
                print(f"Error al agregar canal: {e}")
            finally:
                cur.close()
                conn.close()
def add_response_id(res_respuesta, res_id_pregunta, res_modulo):
    """Agregar una nueva respuesta en la tabla jega_respuestas y retornar el ID."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                # Ejecutar la inserción con la cláusula RETURNING para obtener el ID
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}."jega_respuestas" (res_respuesta, res_id_pregunta, res_modulo, res_fecha)
                    VALUES (%s, %s, %s, %s) RETURNING res_id;
                """, (res_respuesta, res_id_pregunta, res_modulo, datetime.now()))
                
                # Obtener el ID retornado
                res_id = cur.fetchone()[0]
                conn.commit()
                
                print(f"Respuesta agregada con éxito, ID: {res_id}")
                return res_id  # Retornar el ID de la respuesta insertada

            except Exception as e:
                print(f"Error al agregar respuesta: {e}")
                return None
            finally:
                cur.close()
                conn.close()
def add_response(res_respuesta, res_id_pregunta, res_modulo):
    """Agregar una nueva respuesta en la tabla jega_respuestas."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}."jega_respuestas" (res_respuesta, res_id_pregunta, res_modulo, res_fecha)
                    VALUES (%s, %s, %s, %s);
                """, (res_respuesta, res_id_pregunta, res_modulo, datetime.now()))
                conn.commit()
                print(f"Respuesta agregada con éxito.")
            except Exception as e:
                print(f"Error al agregar respuesta: {e}")
            finally:
                cur.close()
                conn.close()

def add_sql_query(con_id_pregunta, con_consulta_sql, con_modulo):
    """Agregar una nueva consulta SQL en la tabla jega_Consulta_sql."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    INSERT INTO {SCHEMA_NAME}."jega_consulta_sql" (con_id_pregunta, con_consulta_sql, con_modulo)
                    VALUES (%s, %s, %s);
                """, (con_id_pregunta, con_consulta_sql, con_modulo))
                conn.commit()
                print(f"Consulta SQL agregada con éxito.")
            except Exception as e:
                print(f"Error al agregar consulta SQL: {e}")
            finally:
                cur.close()
                conn.close()
def add_module(mod_descricion_modulo):
    """Agregar un nuevo módulo en la tabla jega_modulo."""
    # Conectar a la base de datos
    conn = connect_db()
    if conn:
        # Crear un cursor para ejecutar consultas
        with conn.cursor() as cur:
            try:
                # Ejecutar la consulta para insertar un nuevo módulo
                cur.execute(f"""
                    INSERT INTO "{SCHEMA_NAME}"."jega_modulo" (mod_descripcion_modulo)
                    VALUES (%s)
                    RETURNING mod_id;  -- Devuelve el ID del módulo creado
                """, (mod_descricion_modulo,))
                
                # Obtener el ID del módulo creado
                modulo_id = cur.fetchone()[0]  # fetchone() devuelve una tupla, así que obtenemos el primer elemento
                conn.commit()
                print(f"Módulo '{mod_descricion_modulo}' agregado con éxito. ID: {modulo_id}")
                return modulo_id  # Retorna el ID del módulo
            except Exception as e:
                # Manejar errores durante la inserción
                print(f"Error al agregar módulo: {e}")
            finally:
                # Cerrar el cursor y la conexión a la base de datos
                cur.close()
                conn.close()

def list_tables(schema_name):
    """Listar todas las tablas en un esquema específico."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                query = sql.SQL("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = %s
                """)
                cur.execute(query, (schema_name,))
                tables = cur.fetchall()
                print(f"Tablas en el esquema '{schema_name}':")
                for table in tables:
                    print(f"- {table[0]}")
            except Exception as e:
                print(f"Error al listar tablas: {e}")
            finally:
                cur.close()
                conn.close()

def get_user_id_by_channel(canal_id, value):
    """Obtener el ID del usuario en función del canal (1: correo, 2: celular)."""
    # Conectar a la base de datos
    conn = connect_db()
    if conn:
        # Crear un cursor para ejecutar consultas
        with conn.cursor() as cur:
            try:
                if canal_id == 1:
                    print(value)
                    # Si el canal es 1, buscar el ID del usuario por correo electrónico
                    cur.execute(f"""
                        SELECT usu_id
                        FROM "{SCHEMA_NAME}"."jega_usuario"
                        WHERE usu_correo = %s;
                    """, (value,))
                elif canal_id == 2:
                    # Si el canal es 2, buscar el ID del usuario por celular
                    cur.execute(f"""
                        SELECT usu_id
                        FROM "{SCHEMA_NAME}"."jega_usuario"
                        WHERE usu_celular = %s;
                    """, (value,))
                else:
                    # Si el canal no es válido, imprimir un mensaje y retornar None
                    print("ID de canal no válido. Debe ser 1 o 2.")
                    return None
                
                # Obtener el ID del usuario de la consulta
                print(cur)
                user_id = cur.fetchone()  # fetchone() devuelve una tupla
                print(user_id)
                if user_id:
                    # Si se encontró un usuario, retornar su ID
                    return user_id[0]
                else:
                    # Si no se encontró ningún usuario, imprimir un mensaje y retornar None
                    print("No se encontró un usuario con el valor proporcionado.")
                    return None
            
            except Exception as e:
                # Manejar errores durante la consulta
                print(f"Error al obtener ID de usuario: {e}")
            finally:
                # Cerrar el cursor y la conexión a la base de datos
                cur.close()
                conn.close()

def get_modulos_by_cliente(codigo_cliente):
    """Obtener los módulos a los que un cliente tiene acceso mediante su ID."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    SELECT m.mod_descricion_modulo
                    FROM {SCHEMA_NAME}."jega_modulo" m
                    JOIN {SCHEMA_NAME}."jega_usuario_modulo" um ON m.mod_id = um.mod_id
                    WHERE um.codigo_cliente = %s;
                """, (codigo_cliente,))
                
                modulos = cur.fetchall()  # Obtener todos los módulos asociados al cliente
                if modulos:
                    return [mod[0] for mod in modulos]  # Retorna una lista de nombres de módulos
                else:
                    print("El cliente no tiene acceso a ningún módulo.")
                    return None
            except Exception as e:
                print(f"Error al obtener módulos para el cliente: {e}")
                return None
            finally:
                cur.close()
                conn.close()

def get_modulos_ids_by_user_id(usuario_id):
    """Obtener los IDs de los módulos a los que un usuario tiene acceso mediante su ID."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                query = f"""
                    SELECT rm.rom_id_modulo
                    FROM {SCHEMA_NAME}."jega_usuario" u
                    JOIN {SCHEMA_NAME}."jega_roles" r ON u.usu_rol = r.rol_id
                    JOIN {SCHEMA_NAME}."jega_rol_modulo" rm ON r.rol_id = rm.rom_rol_id
                    WHERE u.usu_id = %s;
                """
                cur.execute(query, (usuario_id,))
                modulos_ids = cur.fetchall()  # Obtener todos los IDs de módulos asociados al usuario
                if modulos_ids:
                    return [mod[0] for mod in modulos_ids]  # Retorna una lista de IDs de módulos
                else:
                    print("El usuario no tiene acceso a ningún módulo.")
                    return None
            except Exception as e:
                print(f"Error al obtener módulos para el usuario: {e}")
                return None
            finally:
                cur.close()
                conn.close()

def get_user_assistant_and_thread(usuario_id):
    """Obtener el asistente y hilo del usuario mediante su ID."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                query = f"""
                    SELECT usu_asistente, usu_hilo
                    FROM {SCHEMA_NAME}."jega_usuario"
                    WHERE usu_id = %s;
                """
                cur.execute(query, (usuario_id,))
                result = cur.fetchone()  # Obtener el resultado de la consulta

                if result:
                    asistente, hilo = result
                    return asistente if asistente is not None else None, hilo if hilo is not None else None
                else:
                    print("No se encontró el usuario.")
                    return None, None
            except Exception as e:
                print(f"Error al obtener asistente y hilo para el usuario: {e}")
                return None, None
            finally:
                cur.close()
                conn.close()

def update_user_assistant_and_thread(usuario_id, nuevo_asistente, nuevo_hilo):
    """Actualizar el asistente y el hilo del usuario mediante su ID."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                query = f"""
                    UPDATE {SCHEMA_NAME}."jega_usuario"
                    SET usu_asistente = %s, usu_hilo = %s
                    WHERE usu_id = %s;
                """
                print(f"ID del usuario: {usuario_id}, Asistente: {nuevo_asistente}, Hilo: {nuevo_hilo}")
                cur.execute(query, (nuevo_asistente, nuevo_hilo, usuario_id))
                try:
                    conn.commit()
                    print("Commit realizado con éxito")
                except Exception as e:
                    print(f"Error al hacer commit: {e}")
                
                if cur.rowcount > 0:
                    print(cur.rowcount)
                    print(f"Asistente y hilo actualizados para el usuario con ID {usuario_id}.")
                else:
                    print(f"No se encontró un usuario con ID {usuario_id}.")
            except Exception as e:
                print(f"Error al actualizar asistente y hilo para el usuario: {e}")
            finally:
                cur.close()
                conn.close()

def assistant_and_thread_to_null(usuario_id):
    """Actualizar los valores de asistente y hilo a NULL para el usuario mediante su ID."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cur:
            try:
                query = f"""
                    UPDATE {SCHEMA_NAME}."jega_usuario"
                    SET usu_asistente = NULL, usu_hilo = NULL
                    WHERE usu_id = %s;
                """
                print(f"ID del usuario: {usuario_id}, Asistente: NULL, Hilo: NULL")
                cur.execute(query, (usuario_id,))
                
                try:
                    conn.commit()
                    print("Commit realizado con éxito")
                except Exception as e:
                    print(f"Error al hacer commit: {e}")
                
                if cur.rowcount > 0:
                    print(f"Asistente y hilo actualizados a NULL para el usuario con ID {usuario_id}.")
                else:
                    print(f"No se encontró un usuario con ID {usuario_id}.")
            except Exception as e:
                print(f"Error al actualizar asistente y hilo para el usuario: {e}")
            finally:
                cur.close()
                conn.close()

def agregar_rank(id_respuesta,valor):
    if valor==1:
      valor=True
    elif valor==2:
        valor=False

    """Agregar un registro en jega_rank_respuesta con id_pregunta y rank = True."""
    conn = connect_db()  # Asumo que tienes una función connect_db() para obtener la conexión
    if conn:
        with conn.cursor() as cur:
            try:
                query = f"""
                    INSERT INTO {SCHEMA_NAME}."jega_rank_respuesta" (id_respuesta, rank)
                    VALUES (%s, %s);
                """
                print(f"Insertando id_pregunta: {id_respuesta}, rank: True")
                cur.execute(query, (id_respuesta, valor))
                
                try:
                    conn.commit()
                    print("Commit realizado con éxito")
                except Exception as e:
                    print(f"Error al hacer commit: {e}")

                if cur.rowcount > 0:
                    print(f"Registro agregado con éxito en jega_rank_respuesta con id_pregunta={id_respuesta}.")
                else:
                    print(f"No se insertó el registro correctamente.")
            except Exception as e:
                print(f"Error al insertar en jega_rank_respuesta: {e}")
            finally:
                cur.close()
                conn.close()

def obtener_preguntas(pre_id_usuario):
    """Obtener los pre_id, pre_pregunta y pre_fecha de las preguntas según el pre_id_usuario dado."""
    conn = connect_db()  # Asegúrate de que esta función esté definida y conecte a tu base de datos
    preguntas = []  # Lista para almacenar los datos de cada pregunta
    
    if conn:
        with conn.cursor() as cur:
            try:
                query =f"""
                    SELECT pre_id, pre_pregunta, pre_fecha
                    FROM {SCHEMA_NAME}.jega_preguntas
                    WHERE pre_canal_id = 1
                      AND pre_id_usuario = %s
                      AND pre_padre_id IS NULL
                    ORDER BY pre_id DESC
                    LIMIT 16;
                """
                cur.execute(query, (pre_id_usuario,))
                resultados = cur.fetchall()
                
                # Guardar cada pregunta en forma de diccionario en la lista preguntas
                preguntas = [{"pre_id": fila[0], "pre_pregunta": fila[1], "pre_fecha": fila[2]} for fila in resultados]
                
                #print("Lista de preguntas obtenidas:", preguntas)
            except Exception as e:
                print(f"Error al obtener preguntas: {e}")
            finally:
                cur.close()
                conn.close()
    
    return preguntas  # Retorna la lista de preguntas
    
    return pre_ids  # Retorna la lista de pre_ids
def obtener_respuestas(preguntas):
    """Obtener res_respuesta y res_fecha de jega_respuestas para cada pre_id en preguntas."""
    conn = connect_db()  # Asegúrate de que esta función esté definida y conecte a tu base de datos
    respuestas = []  # Lista para almacenar los resultados de cada consulta
    
    if conn:
        with conn.cursor() as cur:
            try:
                for pregunta in preguntas:
                    pre_id = pregunta["pre_id"]
                    query = f"""
                        SELECT res_respuesta, res_fecha,res_id
                        FROM  {SCHEMA_NAME}.jega_respuestas
                        WHERE res_id_pregunta = %s;
                    """
                    cur.execute(query, (pre_id,))
                    resultados = cur.fetchall()
                    
                    # Añadir los resultados a la lista respuestas
                    for respuesta in resultados:
                        respuestas.append({
                            "pre_id": pre_id,
                            "pre_pregunta": pregunta["pre_pregunta"],
                            "pre_fecha_pregunta": pregunta["pre_fecha"],
                            "res_respuesta": respuesta[0],
                            "res_fecha_respuesta": respuesta[1],
                            "res_id":respuesta[2]
                        })
                
                #print("Respuestas obtenidas:", respuestas)
            except Exception as e:
                print(f"Error al obtener respuestas: {e}")
            finally:
                cur.close()
                conn.close()
    
    return respuestas
#print(list_tables(SCHEMA_NAME))
#print(get_modulos_by_cliente(1))
#add_module("Financiero")
#create_role("Desarrollador")
#create_user(1, "Juan Jose", "Hurtado Ordoñez", "jhurtado@pentalab.tech","0983340250", "Desarrollador", 1)
#print(get_modulos_ids_by_user_id(1))
#add_channel("Teams")
#print(get_user_assistant_and_thread(1))
