from flask import Flask, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Функция для установки соединения с базой данных
def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="llm",
            user="y0ta",
            password="4572"
        )
        return conn
    except Exception as e:
        print("Ошибка подключения к БД:", e)
        abort(500)

# Эндпоинт для получения всех шифров
@app.route('/api/ciphers', methods=['GET'])
def get_ciphers():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM Cipher;")
            ciphers = cur.fetchall()
            return jsonify(ciphers)
    except Exception as e:
        print("Ошибка при получении шифров:", e)
        abort(500)
    finally:
        conn.close()

# Эндпоинт для получения данных по конкретному шифру по его ID
@app.route('/api/ciphers/<int:cipher_id>', methods=['GET'])
def get_cipher(cipher_id):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM Cipher WHERE cipher_id = %s;", (cipher_id,))
            cipher = cur.fetchone()
            if cipher is None:
                abort(404)
            return jsonify(cipher)
    except Exception as e:
        print("Ошибка при получении шифра:", e)
        abort(500)
    finally:
        conn.close()

# Эндпоинт для получения всех моделей
@app.route('/api/models', methods=['GET'])
def get_models():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM Model;")
            models = cur.fetchall()
            return jsonify(models)
    except Exception as e:
        print("Ошибка при получении моделей:", e)
        abort(500)
    finally:
        conn.close()

# Эндпоинт для получения всех попыток дешифрования
@app.route('/api/decryption-attempts', methods=['GET'])
def get_decryption_attempts():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM DecryptionAttempt;")
            attempts = cur.fetchall()
            return jsonify(attempts)
    except Exception as e:
        print("Ошибка при получении попыток дешифрования:", e)
        abort(500)
    finally:
        conn.close()

if __name__ == '__main__':
    # Запуск сервера на локальном хосте, порт 5000, в режиме отладки
    app.run(debug=True)
