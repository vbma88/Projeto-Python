import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from fpdf import FPDF
import webbrowser

# Caminhos de diretórios
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
CONFIG_FILE = os.path.join(BASE_DIR, 'config_empresa.json')

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Carregar configuração da empresa
def carregar_config_empresa():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "nome_empresa": "",
        "telefone": "",
        "email": "",
        "endereco": "",
        "site": ""
    }

# Salvar configuração da empresa
def salvar_config_empresa(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Tela de cadastro da empresa
def tela_config_empresa():
    def salvar():
        config = {
            "nome_empresa": entry_nome.get(),
            "telefone": entry_telefone.get(),
            "email": entry_email.get(),
            "endereco": entry_endereco.get(),
            "site": entry_site.get()
        }
        salvar_config_empresa(config)
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        janela.destroy()

    janela = tk.Toplevel()
    janela.title("Cadastro da Empresa")
    janela.geometry("400x300")

    ttk.Label(janela, text="Nome da Empresa").pack(pady=5)
    entry_nome = ttk.Entry(janela)
    entry_nome.pack(fill='x', padx=20)

    ttk.Label(janela, text="Telefone").pack(pady=5)
    entry_telefone = ttk.Entry(janela)
    entry_telefone.pack(fill='x', padx=20)

    ttk.Label(janela, text="Email").pack(pady=5)
    entry_email = ttk.Entry(janela)
    entry_email.pack(fill='x', padx=20)

    ttk.Label(janela, text="Endereço").pack(pady=5)
    entry_endereco = ttk.Entry(janela)
    entry_endereco.pack(fill='x', padx=20)

    ttk.Label(janela, text="Site").pack(pady=5)
    entry_site = ttk.Entry(janela)
    entry_site.pack(fill='x', padx=20)

    config = carregar_config_empresa()
    entry_nome.insert(0, config["nome_empresa"])
    entry_telefone.insert(0, config["telefone"])
    entry_email.insert(0, config["email"])
    entry_endereco.insert(0, config["endereco"])
    entry_site.insert(0, config["site"])

    ttk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

# Tela de orçamento
def tela_orcamento():
    def calcular():
        try:
            largura = float(entry_largura.get())
            altura = float(entry_altura.get())
            preco_custo = float(entry_preco_custo.get())
            tipo = tipo_instalacao.get()
            instalacao = float(entry_instalacao.get())

            m2 = largura * altura
            medida_sem_acrescimo = largura
            medida_com_acrescimo = largura + 0.40 if tipo == 'Parede' else largura
            preco_parcial = preco_custo * medida_com_acrescimo if tipo == 'Parede' else preco_custo * medida_sem_acrescimo
            preco_arredondado = round(preco_parcial)
            medida_bando = medida_com_acrescimo if tipo == 'Parede' else medida_sem_acrescimo
            valor_total = preco_arredondado + medida_bando + instalacao

            resultado_m2.set(f"{m2:.2f}")
            resultado_medida.set(f"{medida_com_acrescimo:.2f}" if tipo == 'Parede' else f"{medida_sem_acrescimo:.2f}")
            resultado_parcial.set(f"{preco_parcial:.2f}")
            resultado_arredondado.set(f"{preco_arredondado:.2f}")
            resultado_bando.set(f"{medida_bando:.2f}")
            resultado_total.set(f"{valor_total:.2f}")
        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

    janela = tk.Toplevel()
    janela.title("Novo Orçamento")
    janela.geometry("600x600")

    ttk.Label(janela, text="Nome do Cliente").pack()
    entry_nome = ttk.Entry(janela)
    entry_nome.pack(fill='x', padx=20)

    ttk.Label(janela, text="Telefone").pack()
    entry_telefone = ttk.Entry(janela)
    entry_telefone.pack(fill='x', padx=20)

    ttk.Label(janela, text="Email").pack()
    entry_email = ttk.Entry(janela)
    entry_email.pack(fill='x', padx=20)

    ttk.Label(janela, text="Endereço").pack()
    entry_endereco = ttk.Entry(janela)
    entry_endereco.pack(fill='x', padx=20)

    ttk.Label(janela, text="Largura (m)").pack()
    entry_largura = ttk.Entry(janela)
    entry_largura.pack(fill='x', padx=20)

    ttk.Label(janela, text="Altura (m)").pack()
    entry_altura = ttk.Entry(janela)
    entry_altura.pack(fill='x', padx=20)

    tipo_instalacao = tk.StringVar(value='Parede')
    ttk.Radiobutton(janela, text='Instalação na Parede', variable=tipo_instalacao, value='Parede').pack()
    ttk.Radiobutton(janela, text='Instalação na Janela', variable=tipo_instalacao, value='Janela').pack()

    ttk.Label(janela, text="Preço de Custo da Persiana (por metro)").pack()
    entry_preco_custo = ttk.Entry(janela)
    entry_preco_custo.pack(fill='x', padx=20)

    ttk.Label(janela, text="Valor da Instalação").pack()
    entry_instalacao = ttk.Entry(janela)
    entry_instalacao.pack(fill='x', padx=20)

    ttk.Button(janela, text="Calcular", command=calcular).pack(pady=10)

    resultado_m2 = tk.StringVar()
    resultado_medida = tk.StringVar()
    resultado_parcial = tk.StringVar()
    resultado_arredondado = tk.StringVar()
    resultado_bando = tk.StringVar()
    resultado_total = tk.StringVar()

    ttk.Label(janela, textvariable=resultado_m2).pack()
    ttk.Label(janela, textvariable=resultado_medida).pack()
    ttk.Label(janela, textvariable=resultado_parcial).pack()
    ttk.Label(janela, textvariable=resultado_arredondado, foreground='red').pack()
    ttk.Label(janela, textvariable=resultado_bando).pack()
    ttk.Label(janela, textvariable=resultado_total, font=("Helvetica", 12, "bold")).pack()

# Janela principal
def main():
    root = tk.Tk()
    root.title("Sistema de Orçamento de Persiana")
    root.geometry("500x400")

    ttk.Label(root, text="Sistema de Orçamento", font=("Helvetica", 18, "bold")).pack(pady=20)

    ttk.Button(root, text="Cadastrar Dados da Empresa", command=tela_config_empresa).pack(pady=10)
    ttk.Button(root, text="Novo Orçamento", command=tela_orcamento).pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()