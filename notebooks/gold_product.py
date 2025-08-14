import pandas as pd
import numpy as np

def criar_produto(df):
    region_map = {
        'AC': 'NORTE', 'AP': 'NORTE', 'AM': 'NORTE', 'PA': 'NORTE', 'RO': 'NORTE', 'RR': 'NORTE', 'TO': 'NORTE',
        'AL': 'NORDESTE', 'BA': 'NORDESTE', 'CE': 'NORDESTE', 'MA': 'NORDESTE', 'PB': 'NORDESTE', 'PE': 'NORDESTE', 'PI': 'NORDESTE', 'RN': 'NORDESTE', 'SE': 'NORDESTE',
        'ES': 'SUDESTE', 'MG': 'SUDESTE', 'RJ': 'SUDESTE', 'SP': 'SUDESTE',
        'PR': 'SUL', 'RS': 'SUL', 'SC': 'SUL',
        'DF': 'CENTRO-OESTE', 'GO': 'CENTRO-OESTE', 'MS': 'CENTRO-OESTE', 'MT': 'CENTRO-OESTE'
    }
    df['regiao'] = df['uf'].map(region_map)
    df['produto_grupo'] = np.where(
        df['produto'].str.contains('DIESEL', na=False), 
        'DIESEL',
        np.where(                                       
        df['produto'].str.contains('GASOLINA', na=False),
        'GASOLINA',
        df['produto']
        )
    )
    return df