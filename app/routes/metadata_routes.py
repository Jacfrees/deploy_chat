import uuid
import json
from datetime import datetime

from flask import Blueprint, jsonify, request

from app.database.db import create_connection

metadata_bp = Blueprint('metadata', __name__)


def get_metadata_by_project(id):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM T_PROJECT_METADATA WHERE project = %s", (id,))
    obj = cursor.fetchone()
    cursor.close()
    db.close()
    return obj


def get_metadata_by_code(code):
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT * 
    FROM T_PROJECT_METADATA TPM
    LEFT OUTER JOIN T_PROJECT TP ON TP.id = TPM.project
    WHERE TP.code = %s
    """
    cursor.execute(query, (code,))
    obj = cursor.fetchone()
    cursor.close()
    db.close()
    return obj



def create_metadata(data):
    try:
        new = data

        print("nuevo metadata ===>  ", new)

        db = create_connection()
        cursor = db.cursor()
        id = uuid.uuid4()
        date_creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ventas_to_save = json.dumps(new.get('ventas', []))
        gastos_to_save = json.dumps(new.get('gastos', []))
        print("ventas_to_save ===>  ", ventas_to_save)

        queryInsert = '''
            INSERT INTO T_CUSTOMER_METADATA (id, customer_id, ventas, gastos)
            VALUES (%s, %s, %s, %s)
            '''
        cursor.execute(queryInsert, (
            str(id),
            new['customer_id'],
            ventas_to_save,
            gastos_to_save
        ))
        db.commit()
        print("metadata creado con éxito")
        return True
    except Exception as e:
        print("Error al crear el metadata: ", str(e))
        return False
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def update_metadata(data):
    try:
        new = data

        print("nuevo metadata ===>  ", new)

        db = create_connection()
        cursor = db.cursor()
        ventas_to_save = json.dumps(new.get('ventas', []))
        gastos_to_save = json.dumps(new.get('gastos', []))
        print("ventas_to_save ===>  ", ventas_to_save)
        print("gastos_to_save ===>  ", gastos_to_save)

        queryUpdate = '''
            UPDATE T_CUSTOMER_METADATA
            SET ventas = %s, gastos = %s
            WHERE customer_id = %s
            '''
        cursor.execute(queryUpdate, (
            ventas_to_save,
            gastos_to_save,
            new['customer_id']
        ))
        db.commit()
        print("metadata actualizado con éxito")
        return True
    except Exception as e:
        print("Error al actualizar el metadata: ", str(e))
        return False
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
