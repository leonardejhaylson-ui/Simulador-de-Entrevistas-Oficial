import sqlite3

def iniciar_banco():
    conexao = sqlite3.connect("entrevistas.db")
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            user_id INTEGER PRIMARY KEY,
            tecnologia_atual TEXT,
            entrevista_ativa INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_entrevistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            papel TEXT, 
            conteudo TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES usuarios(user_id)
        )
    """)
    conexao.commit()
    conexao.close()

def atualizar_estado_usuario(user_id, tecnologia, ativa):
    conexao = sqlite3.connect("entrevistas.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO usuarios (user_id, tecnologia_atual, entrevista_ativa)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET 
            tecnologia_atual = excluded.tecnologia_atual,
            entrevista_ativa = excluded.entrevista_ativa
    """, (user_id, tecnologia, ativa))
    conexao.commit()
    conexao.close()

def obter_estado_usuario(user_id):
    conexao = sqlite3.connect("entrevistas.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT tecnologia_atual, entrevista_ativa FROM usuarios WHERE user_id = ?", (user_id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado if resultado else (None, 0)

def salvar_mensagem_historico(user_id, papel, conteudo):
    conexao = sqlite3.connect("entrevistas.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO historico_entrevistas (user_id, papel, conteudo) VALUES (?, ?, ?)", (user_id, papel, conteudo))
    conexao.commit()
    conexao.close()

def limpar_historico_usuario(user_id):
    conexao = sqlite3.connect("entrevistas.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM historico_entrevistas WHERE user_id = ?", (user_id,))
    conexao.commit()
    conexao.close()
