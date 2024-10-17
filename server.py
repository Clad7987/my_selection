import os
from random import choice
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from main import main as loader

# Inicializa a aplicação Flask
app = Flask(__name__)
templates = os.listdir("templates")

# Define a pasta para salvar os arquivos
UPLOAD_FOLDER = "imgs"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Verifica se a pasta de uploads existe, se não, cria ela
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Lista para armazenar o histórico de arquivos enviados
uploaded_files = []


# Rota principal para cada framework
@app.route("/")
def index():
    return render_template(
        choice(templates), items={"name": "", "date": ""}
    )  # Redireciona para Materialize por padrão


# Rota para upload de arquivos
@app.route("/upload", methods=["POST"])
def upload_file():
    # Verifica se existe a chave 'file' no request e se arquivos foram selecionados
    if "file" not in request.files:
        return "Nenhum arquivo selecionado!", 400

    # Obtém a lista de arquivos enviados
    files = request.files.getlist("file")

    # Verifica se a lista de arquivos está vazia
    if len(files) == 0 or all(f.filename == "" for f in files):
        return "Nenhum arquivo selecionado!", 400

    for file in files:
        if file and file.filename != "":
            # Salva cada arquivo na pasta 'uploads'
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            print(f"Saved {file}")

            # Armazena as informações de cada arquivo enviado
            uploaded_files.append(
                {
                    "filename": file.filename,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    loader(uploaded_files, is_first_run=False)

    return render_template(
        choice(templates), items=uploaded_files
    )  # redirect(request.referrer)  # Redireciona de volta para a página atual


# Executa a aplicação
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
