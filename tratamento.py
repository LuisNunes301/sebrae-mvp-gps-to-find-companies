import json

import pandas as pd


def converter_csv_para_json(arquivo_csv, arquivo_saida):
    # 1. Lê o arquivo
    df = pd.read_csv(arquivo_csv, encoding='cp1252', sep=None, engine='python')
    
    # 2. Corrigindo o problema da vírgula
    for col in ['Latitude', 'Longitude']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.')
    
    # 3. Mapeamento
    mapeamento = {
        'Nome Fantasia': 'nome',
        'Razão Social': 'razao',
        'CNPJ': 'cnpj',
        'Telefones': 'tel',
        'CNAE Fiscal Descrição': 'cnae',
        'Município': 'cidade',
        'Endereço': 'endereco',
        'Latitude': 'lat',
        'Longitude': 'lng'
    }
    
    # Tratamento de campos vazios
    if 'Nome Fantasia' in df.columns and 'Razão Social' in df.columns:
        df['Nome Fantasia'] = df['Nome Fantasia'].fillna(df['Razão Social'])
    
    df = df.rename(columns=mapeamento)
    colunas_necessarias = ['nome', 'razao', 'cnpj', 'tel', 'cnae', 'cidade', 'endereco', 'lat', 'lng']
    df = df[[c for c in colunas_necessarias if c in df.columns]]

    # 4. Limpeza final
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lng'] = pd.to_numeric(df['lng'], errors='coerce')
    df = df.dropna(subset=['lat', 'lng'])
    
    # ID sequencial
    df.insert(0, 'id', range(1, 1 + len(df)))
    
    # A LINHA MÁGICA: Preenche qualquer buraco restante com "Não informado"
    df = df.fillna("Não informado")
    
    # 5. Salvar
    dados = df.to_dict(orient='records')
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Sucesso! {len(df)} empresas processadas e salvas em {arquivo_saida}.")

if __name__ == "__main__":
    converter_csv_para_json('teste.csv', 'dados.json')