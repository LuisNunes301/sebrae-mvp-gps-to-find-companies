import pandas as pd
import json

def processar_dados(arquivo_csv, arquivo_saida):
    df = pd.read_csv(arquivo_csv, encoding='cp1252', sep=None, engine='python')
    
    # Mapeamento ajustado: Razão Social vira o 'nome' principal
    mapeamento = {
        'Razão Social': 'nome',
        'CNPJ': 'cnpj',
        'Telefones': 'tel',
        'Email': 'email',
        'CNAE Fiscal Descrição': 'cnae_descricao',
        'Município': 'cidade',
        'Bairro': 'bairro',
        'Endereço': 'endereco',
        'Latitude': 'lat',
        'Longitude': 'lng'
    }
    
    df = df.rename(columns=mapeamento)
    
    # Limpeza básica
    df['lat'] = pd.to_numeric(df['lat'].astype(str).str.replace(',', '.'), errors='coerce')
    df['lng'] = pd.to_numeric(df['lng'].astype(str).str.replace(',', '.'), errors='coerce')
    df = df.dropna(subset=['lat', 'lng'])
    df = df.fillna("Não informado")
    
    # Salvar
    df.to_json(arquivo_saida, orient='records', force_ascii=False, indent=4)
    print(f"✅ JSON gerado com {len(df)} empresas.")

if __name__ == "__main__":
    processar_dados('teste.csv', 'dados.json')