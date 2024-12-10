import pandas as pd

def transformar_texto_em_classes(csv_file, coluna_texto, output_file=None):
    """
    Transforma uma coluna de texto em várias colunas representando classes usando 0 e 1.

    Args:
        csv_file (str): Caminho para o arquivo CSV de entrada.
        coluna_texto (str): Nome da coluna no CSV que contém o texto a ser transformado.
        output_file (str, optional): Caminho para salvar o CSV processado. Se None, o arquivo não será salvo.

    Returns:
        pd.DataFrame: DataFrame com as classes representadas como colunas.
    """
    # Ler o arquivo CSV
    df = pd.read_csv(csv_file)

    if coluna_texto not in df.columns:
        raise ValueError(f"A coluna '{coluna_texto}' não foi encontrada no arquivo CSV.")

    # Aplicar one-hot encoding à coluna de texto e converter de True/False para 1/0
    one_hot_encoded = pd.get_dummies(df[coluna_texto], prefix=coluna_texto)
    one_hot_encoded = one_hot_encoded.astype(int)  # Convertendo de booleano para inteiro

    # Combinar o DataFrame original com as novas colunas
    df = pd.concat([df.drop(columns=[coluna_texto]), one_hot_encoded], axis=1)

    # Salvar o novo DataFrame em um arquivo CSV, se especificado
    if output_file:
        df.to_csv(output_file, index=False)

    return df

# Exemplo de uso
csv_file = "heart_expandido.csv"  # Substitua pelo caminho do seu arquivo CSV
coluna_texto = "classe"  # Nome da coluna com texto a ser transformado
output_file = "heart_expandido_processado.csv"  # Nome do arquivo de saída

# Transformar o CSV
df_processado = transformar_texto_em_classes(csv_file, coluna_texto, output_file)

print("CSV processado com sucesso!")
print(df_processado.head())
