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
            cur.execute("SELECT * FROM Ciphers;")
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
            cur.execute("SELECT * FROM Ciphers WHERE cipher_id = %s;", (cipher_id,))
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
            cur.execute("SELECT * FROM Models;")
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
            cur.execute("SELECT * FROM Decryption_Attempts;")
            attempts = cur.fetchall()
            return jsonify(attempts)
    except Exception as e:
        print("Ошибка при получении попыток дешифрования:", e)
        abort(500)
    finally:
        conn.close()

# Эндпоинт для получения всех результатов дешифрования
@app.route('/api/decryption-results', methods=['GET'])
def get_decryption_results():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM Decryption_Results;")
            results = cur.fetchall()
            return jsonify(results)
    except Exception as e:
        print("Ошибка при получении результатов дешифрования:", e)
        abort(500)
    finally:
        conn.close()

# Эндпоинт для получения всех ручных правок
@app.route('/api/manual-corrections', methods=['GET'])
def get_manual_corrections():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM Manual_Corrections;")
            corrections = cur.fetchall()
            return jsonify(corrections)
    except Exception as e:
        print("Ошибка при получении ручных правок:", e)
        abort(500)
    finally:
        conn.close()

# Эндпоинт для обязательного запроса 1: Успешно дешифрованные шифры
@app.route('/api/successful-ciphers', methods=['GET'])
def get_successful_ciphers():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT c.*
                FROM Ciphers c
                JOIN Decryption_Attempts da ON c.cipher_id = da.cipher_id
                WHERE da.success = TRUE
                ORDER BY c.discovery_date DESC;
            """)
            ciphers = cur.fetchall()
            return jsonify(ciphers)
    except Exception as e:
        print("Ошибка при получении успешно дешифрованных шифров:", e)
        abort(500)
    finally:
        conn.close()

# Эндпоинт для обязательного запроса 2: Шифры с самым долгим дешифрованием
@app.route('/api/longest-decryption-ciphers', methods=['GET'])
def get_longest_decryption_ciphers():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT c.cipher_id, c.name,
                       MAX(EXTRACT(EPOCH FROM (da.end_time - da.start_time))) AS duration_seconds
                FROM Ciphers c
                JOIN Decryption_Attempts da ON c.cipher_id = da.cipher_id
                GROUP BY c.cipher_id, c.name
                ORDER BY duration_seconds ASC;
            """)
            ciphers = cur.fetchall()
            return jsonify(ciphers)
    except Exception as e:
        print("Ошибка при получении шифров с долгим дешифрованием:", e)
        abort(500)
    finally:
        conn.close()

# Эндпоинт для обязательного запроса 3: Сравнение символов до и после правок
@app.route('/api/correction-stats', methods=['GET'])
def get_correction_stats():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT char_before, COUNT(*) AS correction_freq
                FROM (
                    SELECT SUBSTRING(dr.model_output FROM n FOR 1) AS char_before,
                           SUBSTRING(mc.final_text FROM n FOR 1) AS char_after
                    FROM Decryption_Results dr
                    JOIN Manual_Corrections mc ON dr.result_id = mc.result_id,
                    GENERATE_SERIES(1, LEAST(LENGTH(dr.model_output), LENGTH(mc.final_text))) AS n
                    WHERE SUBSTRING(dr.model_output FROM n FOR 1) <> SUBSTRING(mc.final_text FROM n FOR 1)
                ) AS changes
                GROUP BY char_before
                ORDER BY correction_freq DESC;
            """)
            stats = cur.fetchall()
            return jsonify(stats)
    except Exception as e:
        print("Ошибка при получении статистики правок:", e)
        abort(500)
    finally:
        conn.close()

if __name__ == '__main__':
    # Запуск сервера на локальном хосте, порт 5000, в режиме отладки
    app.run(debug=True)