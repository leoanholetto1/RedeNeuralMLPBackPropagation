import pandas as pd


def dividir_colunas_strings(csv_path, coluna_classe):
    """
    Divide colunas do tipo string em várias colunas com base na codificação One-Hot Encoding
    e preserva a coluna de classe, movendo-a para a última posição.

    Parâmetros:
    - csv_path (str): Caminho para o arquivo CSV.
    - coluna_classe (str): Nome da coluna que é a classe (a ser preservada).

    Retorna:
    - DataFrame com as colunas divididas e a coluna de classe no final.
    """
    # Carregar o arquivo CSV
    df = pd.read_csv(csv_path)

    # Identificar colunas do tipo string
    colunas_strings = df.select_dtypes(include=['object', 'string']).columns.tolist()

    # Remover a coluna de classe das colunas de strings, se ela estiver incluída
    if coluna_classe in colunas_strings:
        colunas_strings.remove(coluna_classe)

    # Aplicar One-Hot Encoding às colunas de strings
    df_expandido = pd.get_dummies(df, columns=colunas_strings, drop_first=True).astype(int)

    # Garantir que a coluna de classe seja mantida
    if coluna_classe in df.columns:
        df_expandido[coluna_classe] = df[coluna_classe]

    # Reorganizar para colocar a coluna de classe no final
    colunas = [col for col in df_expandido.columns if col != coluna_classe]  # Lista de colunas sem a classe
    colunas.append(coluna_classe)  # Adiciona a classe ao final
    df_expandido = df_expandido[colunas]  # Reorganiza as colunas

    return df_expandido


# Exemplo de uso
if __name__ == "__main__":
    caminho_csv = "heart.csv"  # Substitua pelo caminho do seu arquivo CSV
    coluna_classe = "HeartDisease"  # Substitua pelo nome da coluna de classe

    try:
        # Dividir as colunas automaticamente e preservar a coluna de classe no final
        df_expandido = dividir_colunas_strings(caminho_csv, coluna_classe)
        print("CSV processado com sucesso:")
        print(df_expandido)

        # Salvar o DataFrame processado em um novo arquivo
        df_expandido.to_csv("heart_expandido.csv", index=False)
    except Exception as e:
        print(f"Erro: {e}")
