import pandas as pd
import os
import glob


folder_path = 'src/data/raw' # caminho dos arquivos
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx')) # lista todos os arquivos excel

df_list = []

try:
    if len(excel_files) == 0:
        raise FileNotFoundError('Nenhum arquivo encontrado na pasta {}'.format(folder_path))

    for file in excel_files:
        df = pd.read_excel(file) # Dataframe tabela na memoria para guardar os arquivos        
        file_name = os.path.basename(file)

        df['file'] = file_name        

        # Adiciona a coluna 'location' baseada no nome do arquivo
        if 'brasil' in file_name.lower():
            df['location'] = 'br'
        elif 'france' in file_name.lower():
            df['location'] = 'fr'
        elif 'italian' in file_name.lower():
            df['location'] = 'it'
        else:
            raise ValueError('Arquivo nao identificado: {}'.format(file_name))

        
        # Adiciona a coluna 'campaign' baseada no nome do arquivo
        df['campaign'] = df['utm_link'].str.extract(r"utm_campaign=(.*)")

        df_list.append(df)  # guarda os dataframes na memoria 

except FileNotFoundError as e: # Exceção para arquivos não encontrados
    print(e)

if df_list:
    result = pd.concat(df_list, ignore_index=True) # concatena os dataframes
    output_file = os.path.join('src', 'data', 'ready', 'cleaned_data.xlsx')
    output_csv = os.path.join('src', 'data', 'ready', 'cleaned_data.csv')

    writer = pd.ExcelWriter(output_file, engine='xlsxwriter') # configura o motor de escrita
    result.to_excel(writer, index=False) # leva os dados para o excel
    result.to_csv(output_csv, index=False) # leva os dados para o csv

    writer.close() # fecha o motor de escrita
elif not excel_files:
    print("Nenhum arquivo encontrado na pasta {}".format(folder_path))