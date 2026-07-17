import pandas as pd
import json

def processar_dados(arquivo_csv, arquivo_saida):
    # Lendo com o encoding correto e delimitador automático
    df = pd.read_csv(arquivo_csv, encoding='cp1252', sep=None, engine='python')
    
    # Mapeamento baseado exatamente nos nomes das colunas da sua imagem
    mapeamento = {
        'Nome Fantasia': 'nome',
        'Razão Social': 'razao',
        'CNPJ': 'cnpj',
        'Telefones': 'tel',
        'CNAE Fiscal': 'cnae',
        'CNAE Fiscal Descrição': 'cnae_descricao',
        'Município': 'cidade',
        'Bairro': 'bairro',
        'Endereço': 'endereco',
        'Latitude': 'lat',
        'Longitude': 'lng'
    }
    
    df = df.rename(columns=mapeamento)
    
    # Garantir tratamento de coordenadas (substituir vírgula por ponto)
    for col in ['lat', 'lng']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.')
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remover linhas sem localização
    df = df.dropna(subset=['lat', 'lng'])
    
    # Preencher vazios
    df = df.fillna("Não informado")
    
    # Salvar
    df.to_json(arquivo_saida, orient='records', force_ascii=False, indent=4)
    print(f"✅ JSON gerado com {len(df)} empresas.")

if __name__ == "__main__":
    processar_dados('teste.csv', 'dados.json')