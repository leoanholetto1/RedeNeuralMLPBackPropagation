import math
import tkinter as tk
from tkinter import ttk, filedialog
import random

import numpy as np

selected_files = []
file_option = None

def calcula(net,funcao):
    if funcao == "Linear":
        return net/10
    elif funcao == "Logistica":
        return 1 / (1 +np.exp(-net))
    else:
        return (1 - np.exp(-2*net)) / (1 + np.exp(-2*net))

def calculaDerivada(net,funcao):
    if funcao == "Linear":
        return 1/10.0
    elif funcao == "Logistica":
        return calcula(net,funcao)*(1-calcula(net,funcao))
    else:
        return 1 - float(calcula(net,funcao))*float(calcula(net,funcao))

def calculaDerivada(net, funcao):
    if funcao == "Linear":
        return 1 / 10.0
    elif funcao == "Logistica":
        return calcula(net, funcao) * (1 - calcula(net, funcao))
    else:  # Derivada da função hiperbólica tangente
        return 1 - float(calcula(net, funcao))**2

def prompt_continue_training(current_n):
    result = []

    def choose_continue():
        result.extend(["continuar"])
        window.destroy()

    def choose_stop():
        result.extend(["parar"])
        window.destroy()

    def choose_change_n():
        try:
            new_n = float(entry_n.get())
            result.extend(["alterar_n", new_n])
            window.destroy()
        except ValueError:
            error_label.config(text="Por favor, insira um valor válido para N.")

    def on_close():
        result.extend(["continuar"])
        window.destroy()

    window = tk.Toplevel()  # Use Toplevel para abrir uma nova janela em vez de Tk()
    window.title("Ação no Treinamento")
    window.geometry("400x200")
    window.config(bg="#f0f0f5")
    window.protocol("WM_DELETE_WINDOW", on_close)

    tk.Label(window, text="O treinamento está em progresso.\nO que você gostaria de fazer?", font=("Arial", 12), bg="#f0f0f5", wraplength=350, pady=10).pack()

    button_frame = tk.Frame(window, bg="#f0f0f5")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Continuar", command=choose_continue, bg="#28a745", fg="white", font=("Arial", 10), padx=20, pady=5).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Parar", command=choose_stop, bg="#e74c3c", fg="white", font=("Arial", 10), padx=20, pady=5).grid(row=0, column=1, padx=10)

    tk.Label(window, text="Alterar N:", font=("Arial", 10), bg="#f0f0f5").pack(pady=5)
    entry_n = tk.Entry(window, width=10)
    entry_n.insert(0, str(current_n))
    entry_n.pack()

    tk.Button(window, text="Confirmar Novo N", command=choose_change_n, bg="#007acc", fg="white", font=("Arial", 10), padx=20, pady=5).pack(pady=10)

    error_label = tk.Label(window, text="", font=("Arial", 10), fg="red", bg="#f0f0f5")
    error_label.pack()

    window.wait_window()  # Aguarda a janela ser fechada
    return result


def rede_neural(treinamento, erro, iter, N, camada, funcao, entrada, saida):
    print(funcao)
    print(treinamento)
    camada = int(camada)
    entrada = int(entrada)
    saida = int(saida)
    erro = float(erro)
    iter = int(iter)
    N = float(N)
    erroRede = 100.0

    camada_entrada = [[random.uniform(0, 1) for _ in range(entrada)] for _ in range(camada)]

    camada_saida = [[random.uniform(0, 1) for _ in range(camada)] for _ in range(saida)]
    entrada_valor = [[0] * entrada for _ in range(len(treinamento))]
    saida_valor = [[0] * saida for _ in range(len(treinamento))]
    for i in range(entrada):
        for j in range(len(treinamento)):
            entrada_valor[j][i] = treinamento[j][i]
    for i in range(entrada,entrada+saida):
        for j in range(len(treinamento)):
            saida_valor[j][i-entrada] = treinamento[j][i]
    nInter = 0
    erroEpoca = []
    sumErroEpoca = 0.0
    flag = True
    while nInter < iter and erroRede > erro and flag:
        erroLinha = []
        for linha in range(len(entrada_valor)):
            funca_neuro = []
            nets_entrada = []
            nets_saida = []
            saida_neuro = []
            erro_linha = []
            erro_camadaOculta = []

            for i in range(camada):
                net = 0.0
                for j in range(entrada):
                    net += camada_entrada[i][j] * entrada_valor[linha][j]
                nets_entrada.append(net)
                funca_neuro.append(calcula(net, funcao))

            for i in range(saida):
                net = 0.0
                for j in range(camada):
                    net += camada_saida[i][j] * funca_neuro[j]
                nets_saida.append(net)
                saida_neuro.append(calcula(net, funcao))

            for i in range(saida):
                erro_linha.append((saida_valor[linha][i] - saida_neuro[i]) * calculaDerivada(nets_saida[i], funcao))

            media = sum(e * e for e in erro_linha) / 2.0
            erroLinha.append(media)

            for i in range(camada):
                sumErros = sum(camada_saida[j][i] * erro_linha[j] for j in range(saida))
                erro_camadaOculta.append(sumErros * calculaDerivada(nets_entrada[i], funcao))

            for i in range(saida):
                for j in range(camada):
                    camada_saida[i][j] += erro_linha[i] * N * nets_entrada[j]

            for i in range(entrada):
                for j in range(camada):
                    camada_entrada[j][i] += erro_camadaOculta[j] * N * entrada_valor[linha][i]

        nInter+=1
        erroRede = sum(erroLinha) / len(erroLinha)
        sumErroEpoca+=erroRede
        if(nInter%20 == 0):
            erroEpoca.append(sumErroEpoca/20.0)
            if(len(erroEpoca) == 10):
                erroEpoca.pop(0)
                mediaErroRede = sum(erroEpoca) / len(erroEpoca)
                dif = []
                for val in erroEpoca:
                    dif.append(abs(val-mediaErroRede))
                mediaDif = sum(dif) / len(dif)
                print(mediaDif)
                if mediaDif < 1e-4:
                    resultado = prompt_continue_training(N)
                    if resultado[0] == "parar":
                        flag = False
                    elif resultado[0] == "alterar_n":
                        N = resultado[1]
                erroEpoca = []
            sumErroEpoca = 0.0
        print(N)
        #print("Erro:" + str(erroRede))
        #print("Iteração:"+str(nInter))

    return camada_entrada,camada_saida

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


def gera_matriz_confusao(previsoes, saida_valor):
    todas_listas = previsoes + saida_valor
    listas_unicas = {tuple(sublista): idx for idx, sublista in enumerate(set(map(tuple, todas_listas)))}

    n_classes = len(listas_unicas)

    matriz_confusao = [[0.0 for _ in range(n_classes)] for _ in range(n_classes)]

    for sub_previsoes, sub_saida in zip(previsoes, saida_valor):
        idx_previsto = listas_unicas[tuple(sub_previsoes)]
        idx_real = listas_unicas[tuple(sub_saida)]
        matriz_confusao[idx_real][idx_previsto] += 1
    return  matriz_confusao

def exibir_matriz_confusao(matriz):
    # Cria uma nova janela
    matriz_window = tk.Toplevel()
    matriz_window.title("Matriz de Confusão")
    matriz_window.geometry("800x600")
    matriz_window.config(bg="#2c3e50")  # Fundo escuro para contraste

    # Título
    titulo = tk.Label(
        matriz_window,
        text="Matriz de Confusão",
        font=("Arial", 16, "bold"),
        fg="#ecf0f1",
        bg="#2c3e50",
        pady=10
    )
    titulo.pack()

    frame = tk.Frame(matriz_window, bg="#2c3e50")
    frame.pack(padx=20, pady=20)

    header_font = ("Arial", 12, "bold")
    cell_font = ("Arial", 11)

    for j in range(len(matriz[0])):
        header = tk.Label(
            frame,
            text=f"Classe {j + 1}",
            font=header_font,
            bg="#34495e",
            fg="#ecf0f1",
            borderwidth=1,
            relief="solid",
            padx=10,
            pady=5
        )
        header.grid(row=0, column=j + 1)

    for i in range(len(matriz)):
        header = tk.Label(
            frame,
            text=f"Classe {i + 1}",
            font=header_font,
            bg="#34495e",
            fg="#ecf0f1",
            borderwidth=1,
            relief="solid",
            padx=10,
            pady=5
        )
        header.grid(row=i + 1, column=0)

    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            cell = tk.Label(
                frame,
                text=f"{int(valor)}",
                font=cell_font,
                borderwidth=1,
                relief="solid",
                padx=10,
                pady=5,
                bg="#ecf0f1" if (i + j) % 2 == 0 else "#bdc3c7"
            )
            cell.grid(row=i + 1, column=j + 1)

    tk.Button(
        matriz_window,
        text="Fechar",
        command=matriz_window.destroy,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5
    ).pack(pady=20)



def process_files(erro, iter, N, camada, funcao):
    global selected_files
    teste, treinamento = [], []
    processed_text = ""

    if not selected_files:
        result_label.config(text="Nenhum arquivo selecionado.\n")
        return

    try:
        with open(selected_files[0], 'r', encoding='utf-8') as file:
            header = file.readline().strip().split(',')
        count_x = sum(1 for col in header if col.startswith('X'))
        count_classes = sum(1 for col in header if col.startswith('classe_'))

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
            teste, treinamento = aux[:split_index], aux[split_index:]
            processed_text = f"Arquivo único lido e dividido em treinamento e teste.\nColunas X: {count_x}, Classes: {count_classes}.\n"
        else:
            processed_text = "Mais de dois arquivos selecionados. Não suportado.\n"
    except Exception as e:
        processed_text = f"Erro ao processar arquivo(s): {e}\n"

    result_label.config(text=processed_text)


    treinamento,teste = normalizacao(teste, treinamento)
    random.shuffle(treinamento)
    camada = int(camada)
    entrada_valor = [[0] * count_x for _ in range(len(teste))]
    saida_valor = [[0] * count_classes for _ in range(len(teste))]
    for i in range(count_x):
        for j in range(len(teste)):
            entrada_valor[j][i] = teste[j][i]
    for i in range(count_x,count_x+count_classes):
        for j in range(len(teste)):
            saida_valor[j][i-count_x] = teste[j][i]
    camada_entrada,camada_saida = rede_neural(treinamento, erro, iter, N, camada, funcao, count_x, count_classes)
    previsoes = []
    for linha in range(len(teste)):
        funca_neuro = []
        nets_entrada = []
        saida_neuro = []
        for i in range(camada):
            net = 0.0
            for j in range(count_x):
                net += camada_entrada[i][j] * entrada_valor[linha][j]
            nets_entrada.append(net)
            funca_neuro.append(calcula(net, funcao))
        for i in range(count_classes):
            net = 0.0
            for j in range(camada):
                net += camada_saida[i][j] * funca_neuro[j]
            saida_neuro.append(calcula(net, funcao))
        previsoes.append(saida_neuro)
    for linha in previsoes:
        max_index = linha.index(max(linha))
        for i in range(len(linha)):
            linha[i] = 1.0 if i == max_index else 0.0
    cont = 0
    for i  in range(len(previsoes)):
        if previsoes[i] == saida_valor[i]:
            cont+=1
    print(cont)
    print(len(previsoes))
    matriz = gera_matriz_confusao(previsoes,saida_valor)
    for linha in matriz:
        print(linha)
    exibir_matriz_confusao(matriz)

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
