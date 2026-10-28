import os
import sqlite3
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "troque-esta-chave-secreta-antes-de-publicar"
)

PASTA = os.path.abspath(os.path.dirname(__file__))
BANCO = os.path.join(PASTA, "mensagens.db")
SENHA_ADMIN = os.environ.get("ADMIN_PASSWORD", "Caio123!")


def conectar_banco():
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    with conectar_banco() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS mensagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)


def exige_login(funcao):
    @wraps(funcao)
    def verificar_login(*args, **kwargs):
        if not session.get("administrador_logado"):
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return verificar_login


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/enviar-mensagem", methods=["POST"])
def enviar_mensagem():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    mensagem = request.form.get("mensagem", "").strip()
    consentimento = request.form.get("consentimento")

    if not consentimento:
        flash("Marque a opção de consentimento.")
    elif len(nome) < 2 or len(nome) > 100:
        flash("Digite um nome válido.")
    elif (
        len(email) > 254
        or "@" not in email
        or "." not in email.rsplit("@", 1)[-1]
    ):
        flash("Digite um e-mail válido.")
    elif len(mensagem) < 10 or len(mensagem) > 5000:
        flash("A mensagem deve ter entre 10 e 5000 caracteres.")
    else:
        data = datetime.now().strftime("%d/%m/%Y às %H:%M")

        with conectar_banco() as conexao:
            conexao.execute(
                """INSERT INTO mensagens
                (nome, email, mensagem, data)
                VALUES (?, ?, ?, ?)""",
                (nome, email, mensagem, data)
            )

        flash("Mensagem enviada com sucesso!")

    return redirect(url_for("index") + "#contato")


@app.route("/caixa-de-correio", methods=["GET", "POST"])
def login():
    erro = None

    if request.method == "POST":
        senha = request.form.get("senha", "")

        if senha and senha == SENHA_ADMIN:
            session["administrador_logado"] = True
            return redirect(url_for("caixa_entrada"))

        erro = "Senha incorreta. Tente novamente."

    return render_template("login.html", erro=erro)


@app.route("/caixa-de-entrada")
@exige_login
def caixa_entrada():
    with conectar_banco() as conexao:
        mensagens = conexao.execute(
            "SELECT * FROM mensagens ORDER BY id DESC"
        ).fetchall()

    return render_template("inbox.html", mensagens=mensagens)


@app.route("/excluir-mensagem/<int:mensagem_id>", methods=["POST"])
@exige_login
def excluir_mensagem(mensagem_id):
    with conectar_banco() as conexao:
        conexao.execute(
            "DELETE FROM mensagens WHERE id = ?",
            (mensagem_id,)
        )

    return redirect(url_for("caixa_entrada"))


@app.route("/sair")
def logout():
    session.clear()
    return redirect(url_for("index"))


criar_banco()

if __name__ == "__main__":
    app.run(debug=True)