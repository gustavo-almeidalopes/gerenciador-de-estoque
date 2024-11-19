import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def criar_tabela_produtos():
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            descricao TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

def adicionar_produto(nome, quantidade, preco, descricao, tabela, status_label):
    try:
        if not nome or quantidade <= 0 or preco <= 0:
            raise ValueError("Preencha todos os campos corretamente!")

        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute(
            'INSERT INTO produtos (nome, quantidade, preco, descricao) VALUES (?, ?, ?, ?)', 
            (nome, quantidade, preco, descricao)
        )
        conexao.commit()
        conexao.close()
        atualizar_lista_produtos(tabela)
        status_label.config(text="Produto adicionado com sucesso!", fg="green")
    except ValueError as erro:
        status_label.config(text=f"Erro: {erro}", fg="red")

def remover_produto(produto_id, tabela, status_label):
    try:
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        conexao.commit()
        conexao.close()
        atualizar_lista_produtos(tabela)
        status_label.config(text="Produto removido com sucesso!", fg="green")
    except ValueError:
        status_label.config(text="Erro: ID inválido!", fg="red")

def passar_no_caixa(produto_id, tabela, status_label):
    try:
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (produto_id,))
        produto = cursor.fetchone()

        if produto:
            quantidade = produto[0]
            if quantidade > 1:
                cursor.execute('UPDATE produtos SET quantidade = quantidade - 1 WHERE id = ?', (produto_id,))
            else:
                cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
            conexao.commit()
            status_label.config(text="Produto passado no caixa!", fg="green")
        else:
            status_label.config(text="Erro: Produto não encontrado!", fg="red")

        conexao.close()
        atualizar_lista_produtos(tabela)
    except ValueError:
        status_label.config(text="Erro: ID inválido!", fg="red")

def atualizar_lista_produtos(tabela):
    conexao = sqlite3.connect('estoque.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conexao.close()

    tabela.delete(*tabela.get_children())
    for produto in produtos:
        tabela.insert("", "end", values=produto)

def mostrar_sobre():
    messagebox.showinfo("Sobre", "Gerenciamento de Estoque v2.0\nDesenvolvido por Você!")

def sair_aplicativo(janela):
    janela.destroy()

criar_tabela_produtos()

janela_principal = tk.Tk()
janela_principal.title("Gerenciamento de Estoque")
janela_principal.geometry("800x600")
janela_principal.configure(bg="#f7f7f7")

menu_principal = tk.Menu(janela_principal)
janela_principal.config(menu=menu_principal)

menu_opcoes = tk.Menu(menu_principal, tearoff=0)
menu_opcoes.add_command(label="Sobre", command=mostrar_sobre)
menu_opcoes.add_separator()
menu_opcoes.add_command(label="Sair", command=lambda: sair_aplicativo(janela_principal))
menu_principal.add_cascade(label="Opções", menu=menu_opcoes)

titulo = tk.Label(janela_principal, text="Gerenciamento de Estoque", font=("Helvetica", 18, "bold"), bg="#f7f7f7")
titulo.pack(pady=10)

frame_adicionar_produto = ttk.LabelFrame(janela_principal, text="Adicionar Produto", padding=10)
frame_adicionar_produto.pack(fill="x", padx=20, pady=10)

frame_caixa_produto = ttk.LabelFrame(janela_principal, text="Caixa", padding=10)
frame_caixa_produto.pack(fill="x", padx=20, pady=10)

frame_tabela_produtos = ttk.Frame(janela_principal)
frame_tabela_produtos.pack(fill="both", expand=True, padx=20, pady=10)

nome_produto_var = tk.StringVar()
ttk.Label(frame_adicionar_produto, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(frame_adicionar_produto, textvariable=nome_produto_var, width=30).grid(row=0, column=1, padx=5, pady=5)

quantidade_produto_var = tk.StringVar()
ttk.Label(frame_adicionar_produto, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(frame_adicionar_produto, textvariable=quantidade_produto_var, width=30).grid(row=1, column=1, padx=5, pady=5)

preco_produto_var = tk.StringVar()
ttk.Label(frame_adicionar_produto, text="Preço:").grid(row=2, column=0, padx=5, pady=5)
ttk.Entry(frame_adicionar_produto, textvariable=preco_produto_var, width=30).grid(row=2, column=1, padx=5, pady=5)

descricao_produto_var = tk.StringVar()
ttk.Label(frame_adicionar_produto, text="Descrição:").grid(row=3, column=0, padx=5, pady=5)
ttk.Entry(frame_adicionar_produto, textvariable=descricao_produto_var, width=30).grid(row=3, column=1, padx=5, pady=5)

status_label = tk.Label(janela_principal, text="", font=("Helvetica", 12), bg="#f7f7f7", fg="blue")
status_label.pack(pady=5)

ttk.Button(
    frame_adicionar_produto, 
    text="Adicionar Produto", 
    command=lambda: adicionar_produto(
        nome_produto_var.get(),
        int(quantidade_produto_var.get()),
        float(preco_produto_var.get()),
        descricao_produto_var.get(),
        tabela_produtos,
        status_label
    )
).grid(row=4, column=0, columnspan=2, pady=10)

id_produto_var = tk.StringVar()
ttk.Label(frame_caixa_produto, text="ID do Produto:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(frame_caixa_produto, textvariable=id_produto_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Button(
    frame_caixa_produto, 
    text="Remover Produto", 
    command=lambda: remover_produto(
        int(id_produto_var.get()), 
        tabela_produtos, 
        status_label
    )
).grid(row=1, column=0, pady=10, padx=5)

ttk.Button(
    frame_caixa_produto, 
    text="Passar no Caixa", 
    command=lambda: passar_no_caixa(
        int(id_produto_var.get()), 
        tabela_produtos, 
        status_label
    )
).grid(row=1, column=1, pady=10, padx=5)

colunas_tabela = ("ID", "Nome", "Quantidade", "Preço", "Descrição")
tabela_produtos = ttk.Treeview(frame_tabela_produtos, columns=colunas_tabela, show="headings", selectmode="browse")
for coluna in colunas_tabela:
    tabela_produtos.heading(coluna, text=coluna)
    tabela_produtos.column(coluna, width=150)
tabela_produtos.pack(fill="both", expand=True, side="left")

scrollbar_tabela = ttk.Scrollbar(frame_tabela_produtos, orient="vertical", command=tabela_produtos.yview)
tabela_produtos.configure(yscrollcommand=scrollbar_tabela.set)
scrollbar_tabela.pack(side="right", fill="y")

atualizar_lista_produtos(tabela_produtos)

janela_principal.mainloop()
