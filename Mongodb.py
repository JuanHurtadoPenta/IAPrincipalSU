from pymongo import MongoClient

def agregar_item(codigo_emp,codigo_cliente,hilo, asistente):
    item = {
    "codigo_emp": codigo_emp,
    "codigo_cliente": codigo_cliente,
    "hilo": hilo,
    "asistente": asistente
    }
    try:
        # Conectar al cliente de MongoDB usando la URI proporcionada
        client = MongoClient('mongodb://corp_usr:corp2021@192.168.193.5:27017/')
         # Seleccionar la base de datos
        db = client['bot_db_core_dev']
         # Seleccionar la colección
        collection = db['InfoAsistenteIA']
        # Insertar el documento
        result = collection.insert_one(item)
        # Confirmar la inserción
        print(f"Documento insertado con el ID: {result.inserted_id}")
    
    except Exception as e:
        print(f"Error al conectar o insertar el documento: {e}")

def obtener_hilo_y_asistente( codigo_emp, codigo_cliente):
    try:
        # Conectar al cliente de MongoDB usando la URI proporcionada
        client = MongoClient('mongodb://corp_usr:corp2021@192.168.193.5:27017/')
        # Seleccionar la base de datos
        db = client['bot_db_core_dev']
        # Seleccionar la colección
        collection = db['InfoAsistenteIA']
        # Consultar el documento
        query = {
            "codigo_emp": codigo_emp,
            "codigo_cliente": codigo_cliente
        }
        documento = collection.find_one(query, {"hilo": 1, "asistente": 1, "_id": 0})
        if documento:
            return documento['asistente'],documento['hilo']
        else:
            return None,None
    
    except Exception as e:
        print (e)
        return "Ninguno","Ninguno"


