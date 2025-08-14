import requests
import os

def gerar_urls(ano_inicio, ano_fim):
    url_base_parte1='https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan/'
    url_base_parte2='/precos-gasolina-etanol-'
    extensao='.csv/@@download/file'
    urls_geradas = []
    meses = [f'{i:02d}' for i in range(1, 13)] # Garante '01', '02', etc.

    for ano in range(ano_inicio, ano_fim + 1):
        for mes in meses:
            url_completa = f'{url_base_parte1}{ano}{url_base_parte2}{mes}{extensao}'
            urls_geradas.append(url_completa)
    return urls_geradas

def baixar_arquivos(ano_inicio, ano_fim, pasta_destino):
    urls = gerar_urls(ano_inicio, ano_fim)
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"Pasta '{pasta_destino}' criada com sucesso.")
    elif not os.listdir(pasta_destino) and not urls:
        print(f"A pasta '{pasta_destino}' está vazia e não há URLs para baixar.")
        return

    for url in urls:
        try:
            partes_url = url.split('/')
            ano = partes_url[-4]
            nome_arquivo_original = url.split('/')[-3]
            nome_arquivo_final = f"{ano}_{nome_arquivo_original}"
            caminho_completo_arquivo = os.path.join(pasta_destino, nome_arquivo_final)

            if os.path.exists(caminho_completo_arquivo):
                print(f"Arquivo já existe, pulando download: {nome_arquivo_final}")
                continue

            print(f"Baixando: {url} para {caminho_completo_arquivo}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(caminho_completo_arquivo, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Download concluído: {nome_arquivo_final}")

        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar {url}: {e}")
        except IndexError:
            print(f"Não foi possível extrair o ano ou nome do arquivo da URL: {url}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao processar {url}: {e}")