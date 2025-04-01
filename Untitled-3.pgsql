-- Таблица Cipher
CREATE TABLE IF NOT EXISTS Cipher (
    cipher_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cipher_type VARCHAR(50),        -- Caesar, Substitution, Vigenere, ...
    historical_period VARCHAR(100),
    origin VARCHAR(100),
    encryption_principles TEXT,
    encrypted_text TEXT,
    discovery_date DATE
);

-- Таблица Model
CREATE TABLE IF NOT EXISTS Model (
    model_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,      -- Например, GPT-2, GPT-Neo
    specialization VARCHAR(100),
    version VARCHAR(20),
    usage_date DATE
);

-- Таблица DecryptionAttempt
CREATE TABLE IF NOT EXISTS DecryptionAttempt (
    attempt_id SERIAL PRIMARY KEY,
    cipher_id INT,
    model_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    success BOOLEAN,                -- 1/0 заменяем на true/false
    percent_correct DECIMAL(5,2),
    FOREIGN KEY (cipher_id) REFERENCES Cipher(cipher_id),
    FOREIGN KEY (model_id) REFERENCES Model(model_id)
);

-- Таблица DecryptionResult
CREATE TABLE IF NOT EXISTS DecryptionResult (
    result_id SERIAL PRIMARY KEY,
    cipher_id INT,
    model_output TEXT,
    similarity DECIMAL(5,2),
    readability DECIMAL(5,2),
    FOREIGN KEY (cipher_id) REFERENCES Cipher(cipher_id)
);

-- Таблица ManualCorrection
CREATE TABLE IF NOT EXISTS ManualCorrection (
    correction_id SERIAL PRIMARY KEY,
    result_id INT,
    corrected_by VARCHAR(100),
    percent_changed DECIMAL(5,2),
    final_text TEXT,
    FOREIGN KEY (result_id) REFERENCES DecryptionResult(result_id)
);
