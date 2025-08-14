import pandas as pd

def ajustar_df(df):
    colunas_renomear = {
        'regiao_-_sigla': 'regiao',
        'estado_-_sigla': 'uf',
        'municipio': 'municipio',
        'revenda': 'revenda',
        'cnpj_da_revenda': 'cnpj',
        'nome_da_rua': 'rua',
        'numero_rua': 'numero',
        'complemento': 'complemento',
        'bairro': 'bairro',
        'cep': 'cep',
        'produto': 'produto',
        'data_da_coleta': 'data_coleta',
        'valor_de_venda': 'valor_venda',
        'valor_de_compra': 'valor_compra',
        'unidade_de_medida': 'unidade_medida',
        'bandeira': 'bandeira'
    }
    colunas_drop = [
        'regiao',
        'cnpj',
        'rua',
        'numero',
        'complemento',
        'bairro',
        'cep',
        'valor_compra',
        'unidade_medida'
    ]
    colunas_agrupar = [
        'uf',
        'municipio',
        'revenda',
        'produto',
        'bandeira',
        'data_ref'
    ]
    df = df.rename(columns=colunas_renomear)
    df = df.drop(columns=colunas_drop)
    df['data_coleta'] = pd.to_datetime(df['data_coleta'], format='%d/%m/%Y')
    df['data_ref'] = df['data_coleta'].dt.to_period('M').dt.start_time
    df = df.drop(columns=['data_coleta'])
    df['valor_venda'] = df['valor_venda'].str.replace(',', '.', regex=False).astype(float)
    df = df.groupby(by=colunas_agrupar)['valor_venda'].mean().reset_index()
    return df