from flask import Blueprint, jsonify, request
from app.database.db import create_connection

project_bp = Blueprint('project', __name__)


@project_bp.route('/getCustomers', methods=['GET'])
def get_customers():
    result = []
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM T_CUSTOMER')
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        for row in rows:
            result.append(dict(zip(column_names, row)))

        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, "error": str(e)}), 500


def get_projects():
    db = create_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM T_PROJECT order by date_created desc limit 2")
    projects = cursor.fetchall()
    cursor.close()
    db.close()
    return projects


@project_bp.route('/getCustomerByDocument', methods=['GET'])
def get_customer_by_document():
    if 'documento' not in request.form:
        return jsonify({'success': False, 'error': 'No se dio nungun numero de documento'})
    documento = request.form['documento']
    print(documento)

    result = None
    try:
        db = create_connection()
        cursor = db.cursor()
        query = 'SELECT * FROM T_CUSTOMER WHERE documento = %s'
        cursor.execute(query, (documento,))
        row = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        if row:
            result = dict(zip(column_names, row))
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'error': 'Numero de documento no encontrado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})








