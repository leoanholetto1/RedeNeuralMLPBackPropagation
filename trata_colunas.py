import pandas as pd
from sklearn.preprocessing import LabelEncoder


def codificar_ordinal(csv_path, colunas_codificar):
    """
    Realiza a codificação ordinal nas colunas especificadas de um arquivo CSV.

    Parâmetros:
    - csv_path (str): Caminho para o arquivo CSV.
    - colunas_codificar (list): Lista de nomes das colunas a serem codificadas.

    Retorna:
    - DataFrame codificado.
    """
    # Carregar o arquivo CSV
    df = pd.read_csv(csv_path)

    # Verificar se as colunas existem no DataFrame
    colunas_invalidas = [col for col in colunas_codificar if col not in df.columns]
    if colunas_invalidas:
        raise ValueError(f"Colunas não encontradas no CSV: {colunas_invalidas}")

    # Criar um LabelEncoder para cada coluna e aplicá-lo
    label_encoders = {}
    for coluna in colunas_codificar:
        encoder = LabelEncoder()
        df[coluna] = encoder.fit_transform(df[coluna])
        label_encoders[coluna] = encoder  # Armazenar o encoder caso seja necessário inverso

    return df, label_encoders


# Exemplo de uso
if __name__ == "__main__":
    caminho_csv = "heart.csv"  # Substitua pelo caminho do seu arquivo CSV
    colunas = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]  # Substitua pelos nomes das colunas a serem codificadas

    try:
        df_codificado, encoders = codificar_ordinal(caminho_csv, colunas)
        print("CSV codificado com sucesso:")
        print(df_codificado)

        # Salvar o DataFrame codificado em um novo arquivo
        df_codificado.to_csv("heart_codificado.csv", index=False)
    except Exception as e:
        print(f"Erro: {e}")
