import os
import pandas as pd
from datetime import datetime
from time import time
from scraping import fuel_price_diesel_gnv, fuel_price_gasoline_ethanol
from notebooks import bronze_ingestion, silver_transformation, gold_product


def salvar_csv(df, caminho_saida_csv, nome_arquivo):
    # Garante que o diretório de saída exista antes de salvar
    diretorio_saida = os.path.dirname(caminho_saida_csv)
    if diretorio_saida and not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
        print(f"Diretório de saída '{diretorio_saida}' criado.")

    # Salva o DataFrame final no caminho especificado '/database_fuel_price_br.csv'
    try:
        df.to_csv(caminho_saida_csv + nome_arquivo, index=False, sep=';', encoding='latin1')
        print(f"DataFrame final salvo em '{caminho_saida_csv}'")
    except Exception as e:
        print(f"Erro ao salvar o arquivo '{caminho_saida_csv}': {e}")

def salvar_parquet(df, caminho_saida_parquet, nome_arquivo):
    # Garante que o diretório de saída exista antes de salvar
    diretorio_saida = os.path.dirname(caminho_saida_parquet)
    if diretorio_saida and not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
        print(f"Diretório de saída '{diretorio_saida}' criado.")

    # Salva o DataFrame final no caminho especificado '/database_fuel_price_br.csv'
    try:
        df.to_parquet(caminho_saida_parquet + nome_arquivo, index=False)
        print(f"DataFrame final salvo em '{caminho_saida_parquet}'")
    except Exception as e:
        print(f"Erro ao salvar o arquivo '{caminho_saida_parquet}': {e}")


if __name__ == "__main__":
    # Início
    start_time = time()

    # Definir Datas
    ANO_INICIO = 2023
    ANO_FIM = datetime.now().year
    
    # Scraping
    print(f"Iniciando o processo de download de dados para os anos de {ANO_INICIO} a {ANO_FIM}...")
    fuel_price_gasoline_ethanol.baixar_arquivos(ANO_INICIO, ANO_FIM,'db_raw/gasoline_ethanol')
    fuel_price_diesel_gnv.baixar_arquivos(ANO_INICIO, ANO_FIM,'db_raw/diesel_gnv')
    print("Processo de download concluído.")

    # Bronze Layer
    print('Iniciando Camada Bronze...')
    df_bronze = bronze_ingestion.empilhar_csv('db_raw')
    #salvar_csv(df_bronze, 'db', '/bronze_fuel_price_br.csv')
    salvar_parquet(df_bronze, 'db', '/bronze_fuel_price_br.parquet')
    print('Camada Bronze finalizada com sucesso!')
    #print(df_bronze)

    # Silver Layer
    print('Iniciando Camada Silver...')
    df_silver = silver_transformation.ajustar_df(df_bronze)
    salvar_csv(df_silver, 'db', '/silver_fuel_price_br.csv')
    salvar_parquet(df_silver, 'db', '/silver_fuel_price_br.parquet')
    print('Camada Silver finalizada com sucesso!')
    #print(df_silver)

    # Gold Layer
    print('Iniciando Camada Gold...')
    df_gold = gold_product.criar_produto(df_silver)
    salvar_csv(df_gold, 'db', '/gold_fuel_price_br.csv')
    salvar_parquet(df_gold, 'db', '/gold_fuel_price_br.parquet')
    print('Camada Gold finalizada com sucesso!')
    #print(df_gold)

    # Fim
    end_time = time()
    tempo = end_time - start_time
    print(f'\nTempo de execução: {tempo:.4f} s')