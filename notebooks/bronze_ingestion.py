import pandas as pd
import os

def empilhar_csv(caminho_da_pasta):

    todos_dataframes = []

    if not os.path.isdir(caminho_da_pasta):
        print(f"Erro: O caminho '{caminho_da_pasta}' não é um diretório válido.")
        return None

    for diretorio_raiz, _, arquivos in os.walk(caminho_da_pasta):
        for nome_arquivo in arquivos:
            if nome_arquivo.endswith(".csv"):
                caminho_completo_arquivo = os.path.join(diretorio_raiz, nome_arquivo)
                try:
                    df = pd.read_csv(caminho_completo_arquivo, sep=';', encoding='latin1')

                    # --- AJUSTE AQUI: Padronizar nomes das colunas ---
                    # 1. Remover espaços em branco no início/fim
                    df.columns = df.columns.str.strip()
                    # 2. Converter para minúsculas (ou maiúsculas, consistentemente)
                    df.columns = df.columns.str.lower()
                    # 3. Substituir espaços por underscores, se desejar (opcional, mas boa prática)
                    df.columns = df.columns.str.replace(' ', '_')
                    df.columns = df.columns.str.replace('ï»¿regiao_-_sigla', 'regiao_-_sigla')
                    # --------------------------------------------------

                    todos_dataframes.append(df)
                    print(f"Arquivo '{nome_arquivo}' lido com sucesso de '{diretorio_raiz}'.")
                    #print(df.columns)
                except Exception as e:
                    print(f"Erro ao ler o arquivo '{nome_arquivo}' em '{diretorio_raiz}': {e}")

    if todos_dataframes:
        dataframe_final = pd.concat(todos_dataframes, ignore_index=True)
        print("\nTodos os arquivos CSV foram empilhados com sucesso!")
        return dataframe_final
    else:
        print("\nNenhum arquivo CSV encontrado na pasta especificada.")
        return None