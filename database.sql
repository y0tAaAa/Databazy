-- Создаём базу данных, если она ещё не существует
CREATE DATABASE IF NOT EXISTS CryptanalysisDB;
USE CryptanalysisDB;

-- Таблица с информацией о шифрах
CREATE TABLE Cipher (
    cipher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cipher_type VARCHAR(50),           -- Тип шифра: Caesar, Substitution, Vigenere, Transposition и т.д.
    historical_period VARCHAR(100),
    origin VARCHAR(100),
    encryption_principles TEXT,
    encrypted_text TEXT,
    discovery_date DATE
);

-- Таблица с информацией о LLM-моделях, используемых для дешифрования
CREATE TABLE Model (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,           -- Например, GPT-2, GPT-Neo и т.д.
    specialization VARCHAR(100),
    version VARCHAR(20),
    usage_date DATE
);

-- Таблица для истории попыток дешифрования
CREATE TABLE DecryptionAttempt (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    cipher_id INT,
    model_id INT,
    start_time DATETIME,
    end_time DATETIME,
    success BOOLEAN,                     -- 1: успешная, 0: неуспешная попытка
    percent_correct DECIMAL(5,2),        -- Процент правильно расшифрованных символов
    FOREIGN KEY (cipher_id) REFERENCES Cipher(cipher_id),
    FOREIGN KEY (model_id) REFERENCES Model(model_id)
);

-- Таблица для хранения результатов дешифрования (выход модели)
CREATE TABLE DecryptionResult (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    cipher_id INT,
    model_output TEXT,
    similarity DECIMAL(5,2),             -- Степень схожести с ожидаемым текстом
    readability DECIMAL(5,2),            -- Оценка читаемости полученного текста
    FOREIGN KEY (cipher_id) REFERENCES Cipher(cipher_id)
);

-- Таблица для записей о ручных корректировках результатов дешифрования
CREATE TABLE ManualCorrection (
    correction_id INT AUTO_INCREMENT PRIMARY KEY,
    result_id INT,
    corrected_by VARCHAR(100),           -- Кто проводил корректировку
    percent_changed DECIMAL(5,2),          -- Процент символов, изменённых вручную
    final_text TEXT,
    FOREIGN KEY (result_id) REFERENCES DecryptionResult(result_id)
);
