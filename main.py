import math
import tkinter as tk
from tkinter import ttk, filedialog
import random


# Variáveis globais
selected_files = []
file_option = None

def calcula(net,funcao):
    print(funcao)
    return net/10

def rede_neural(treinamento, erro, iter, N, camada, funcao, entrada, saida):
    print(treinamento)
    camada = int(camada)
    entrada = int(entrada)
    saida = int(saida)
    erro = float(erro)
    iter = int(iter)
    N = float(N)
    erroRede = 100.0

    # Inicializando camada de entrada com valores aleatórios
    camada_entrada = [[random.uniform(0, 1) for _ in range(entrada)] for _ in range(camada)]

    # Inicializando camada de saída com valores aleatórios
    camada_saida = [[random.uniform(0, 1) for _ in range(camada)] for _ in range(saida)]
    print("Camada Entrada:")
    print(camada_entrada)
    print("Camada Saida:")
    print(camada_saida)
    entrada_valor = [[0] * entrada for _ in range(len(treinamento))]
    saida_valor = [[0] * saida for _ in range(len(treinamento))]
    for i in range(entrada):
        for j in range(len(treinamento)):
            entrada_valor[j][i] = treinamento[j][i]
    for i in range(entrada,entrada+saida):
        for j in range(len(treinamento)):
            saida_valor[j][i-entrada] = treinamento[j][i]
    print(entrada_valor)
    print(saida_valor)
    while iter > 0 and erroRede > erro:
        for linha in range(len(entrada_valor)):
            funca_neuro = []
            for i in range(camada):
                net = 0.0
                for j in range(entrada):
                    net+=camada_entrada[i][j]*linha[j]
                funca_neuro.add(calcula(net,funcao))
            saida_neuro = []
            for i in range(saida):
                net = 0.0
                for j in range(camada):
                    net+=camada_saida[i][j]*funca_neuro[j]
                saida_neuro.add(calcula(net,funcao))
            #calcula erro e volta
        break

    return []

def show_values():
    value1 = entry1.get()
    value2 = entry2.get()
    value3 = entry3.get()
    hidden_layer = entry_hidden.get()
    selected_option = option_var.get()
    result_label.config(
        text=f"Erro: {value1}, Iterações: {value2}, N: {value3}, Camada Oculta: {hidden_layer}, Opção: {selected_option}"
    )
    open_new_window(value1, value2, value3, hidden_layer, selected_option)

def normalizacao(teste, treinamento):
    testeN = [[0] * len(teste[0]) for _ in range(len(teste))]
    treinamentoN = [[0] * len(treinamento[0]) for _ in range(len(treinamento))]

    for dataset, normalized in [(teste, testeN), (treinamento, treinamentoN)]:
        for i in range(len(dataset[0])):
            coluna = [float(dataset[j][i]) for j in range(len(dataset))]
            menor, maior = min(coluna), max(coluna)
            if 0 <= menor <= 1 and 0 <= maior <= 1:
                for j in range(len(dataset)):
                    normalized[j][i] = float(dataset[j][i])
            else:
                for j in range(len(dataset)):
                    normalized[j][i] = (float(dataset[j][i]) - menor) / (maior - menor)
    return testeN, treinamentoN

def open_new_window(erro, iter, N, camada, funcao):
    global result_label, file_option
    root.destroy()

    new_window = tk.Tk()
    new_window.title("Seleção de Arquivos")
    new_window.geometry("450x300")
    new_window.config(bg="#f0f0f5")

    file_option = tk.IntVar(value=1)

    tk.Radiobutton(new_window, text="Inserir um arquivo", variable=file_option, value=1, bg="#f0f0f5").pack(anchor="w", padx=20, pady=5)
    tk.Radiobutton(new_window, text="Inserir dois arquivos", variable=file_option, value=2, bg="#f0f0f5").pack(anchor="w", padx=20, pady=5)

    tk.Button(new_window, text="Selecionar Arquivo(s)", command=open_file_dialog, bg="#007acc", fg="white", font=("Arial", 10)).pack(pady=10)
    tk.Button(new_window, text="Processar Arquivo(s)",
              command=lambda: process_files(erro, iter, N, camada, funcao),
              bg="#28a745", fg="white", font=("Arial", 10)).pack(pady=10)

    result_label = tk.Label(new_window, text="", font=("Arial", 10, "italic"), foreground="#333", bg="#f0f0f5", wraplength=300)
    result_label.pack(pady=10)

def open_file_dialog():
    global selected_files
    selected_files.clear()

    if file_option.get() == 1:
        file_path = filedialog.askopenfilename(title="Selecione um arquivo")
        if file_path:
            selected_files.append(file_path)
    else:
        file_paths = filedialog.askopenfilenames(title="Selecione dois arquivos")
        selected_files.extend(file_paths)


def process_files(erro, iter, N, camada, funcao):
    global selected_files
    teste, treinamento = [], []
    processed_text = ""

    if not selected_files:
        result_label.config(text="Nenhum arquivo selecionado.\n")
        return

    try:
        # Contagem de X e classes a partir da primeira linha
        with open(selected_files[0], 'r', encoding='utf-8') as file:
            header = file.readline().strip().split(',')
        count_x = sum(1 for col in header if col.startswith('X'))
        count_classes = sum(1 for col in header if col.startswith('classe_'))

        # Leitura dos arquivos
        if len(selected_files) == 2:
            with open(selected_files[0], 'r', encoding='utf-8') as file:
                treinamento = [line.strip().split(',') for line in file.readlines()[1:]]
            with open(selected_files[1], 'r', encoding='utf-8') as file:
                teste = [line.strip().split(',') for line in file.readlines()[1:]]
            processed_text = f"Arquivos lidos com sucesso.\nColunas X: {count_x}, Classes: {count_classes}.\n"
        elif len(selected_files) == 1:
            with open(selected_files[0], 'r', encoding='utf-8') as file:
                aux = [line.strip().split(',') for line in file.readlines()[1:]]
            split_index = math.floor(len(aux) * 0.7)
            treinamento, teste = aux[:split_index], aux[split_index:]
            processed_text = f"Arquivo único lido e dividido em treinamento e teste.\nColunas X: {count_x}, Classes: {count_classes}.\n"
        else:
            processed_text = "Mais de dois arquivos selecionados. Não suportado.\n"
    except Exception as e:
        processed_text = f"Erro ao processar arquivo(s): {e}\n"

    # Atualiza a interface com o resultado
    result_label.config(text=processed_text)

    # Normaliza os dados

    teste, treinamento = normalizacao(teste, treinamento)
    random.shuffle(treinamento)
    print("Camadas Ocultas:", camada)
    print("Função:", funcao)
    print(f"X: {count_x}, Classes: {count_classes}")

    resultado = rede_neural(treinamento, erro, iter, N, camada, funcao, count_x, count_classes)




root = tk.Tk()
root.title("Interface de Entrada e Seleção")
root.geometry("350x350")
root.config(bg="#f0f0f5")

style = ttk.Style()
style.configure("TLabel", font=("Arial", 10), foreground="#333")
style.configure("TEntry", padding=5)
style.configure("TFrame", background="#f0f0f5")

frame1 = ttk.Frame(root)
frame1.pack(pady=10, padx=10, fill="x")

frame2 = ttk.Frame(root)
frame2.pack(pady=10, padx=10, fill="x")

label1 = ttk.Label(frame1, text="Erro:")
label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry1 = ttk.Entry(frame1, width=25)
entry1.grid(row=0, column=1, padx=5, pady=5)

label2 = ttk.Label(frame1, text="Iterações:")
label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry2 = ttk.Entry(frame1, width=25)
entry2.grid(row=1, column=1, padx=5, pady=5)

label3 = ttk.Label(frame1, text="N:")
label3.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry3 = ttk.Entry(frame1, width=25)
entry3.grid(row=2, column=1, padx=5, pady=5)

label_hidden = ttk.Label(frame1, text="Camada Oculta:")
label_hidden.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_hidden = ttk.Entry(frame1, width=25)
entry_hidden.grid(row=3, column=1, padx=5, pady=5)

option_var = tk.StringVar(value="Linear")
options = ["Linear", "Logistica", "Hiperbolica"]
option_menu = ttk.OptionMenu(frame2, option_var, *options)
option_label = ttk.Label(frame2, text="Escolha uma opção:")
option_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
option_menu.grid(row=0, column=1, padx=5, pady=5)

show_button = tk.Button(root, text="Avançar", command=show_values, bg="#007acc", fg="white", font=("Arial", 10))
show_button.pack(pady=10)

result_label = ttk.Label(root, text="", font=("Arial", 10, "italic"), foreground="#333")
result_label.pack(pady=10)

root.mainloop()
