import pandas as pd
from bs4 import BeautifulSoup
import os
import re
from dotenv import load_dotenv

load_dotenv()

masp = os.getenv('MASP')

directory = masp
files = os.listdir(directory)

#print(files)
df_final = None

for html in files:
    datas = (re.findall(r'\d+', html))
    
    table = BeautifulSoup(open(f"{directory}/{html}",'r').read()).find('table')

    parsed_tables = pd.read_html(str(table)) 
                
    df_folhas = parsed_tables[6]
    df_folhas = df_folhas.dropna(how='all')
    df_folhas['Arquivo'] = html
    df_folhas['Mes'] = datas[1]
    df_folhas['Ano'] = datas[0]
    df_folhas = df_folhas[1:]
    if df_final is None:
        df_final = df_folhas
    else:
        df_final = pd.concat([df_final, df_folhas])
df_final.columns = ['Nº ADM','TR','DESCRIÇÃO','PARCELA','VANTAGENS','DESCONTOS','ARQUIVO','Mes','Ano']
print(df_final)
df_final.to_csv(f"{masp}/Resultado_compilado_{masp}.csv")