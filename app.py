import requests
from datetime import datetime
import numpy as np

#Faça uma requisição GET para a URL da API Alpha Vantage para IBM usando a chave demo:
def get_alpha_json(url):
    r = requests.get(url)
    return r.json()
get_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = get_alpha_json(get_url)

#Extraia os dados diários de fechamento do ativo a partir da resposta da API.
time_series_daily = response["Time Series (Daily)"]
close = []
for data, dados in time_series_daily.items():
    close.append({
        "data": data,
        "close": dados["4. close"]
    })

#Ordene os dados cronologicamente.
close_ordenado = sorted(close, key=lambda x: datetime.strptime(x["data"], "%Y-%m-%d"))

#Calcule
#1) Retorno diário: variação percentual do fechamento de um dia para o próximo
def retorno_diario(anterior, atual):
    var = ((atual/anterior) - 1)*100
    return var

for i in range(len(close_ordenado)):
    if i == 0:
        close_ordenado[i]["daily_return"] = 0
    else:
        anterior = float(close_ordenado[i-1]["close"])
        atual = float(close_ordenado[i]["close"])
        close_ordenado[i]["daily_return"] = retorno_diario(anterior, atual)
        
#2) Retorno acumulado: soma cumulativa dos retornos diários ao longo do tempo

for i in range(len(close_ordenado)):
    if i == 0:
        close_ordenado[i]["cumulative_return"] = 0
    else:
        atual = float(close_ordenado[i]["daily_return"])
        anterior = float(close_ordenado[i-1]["daily_return"])
        cumulative_return = atual + anterior
        close_ordenado[i]["cumulative_return"] = cumulative_return

#3) Volatilidade média: média dos desvios padrões dos retornos diários calculados em janelas móveis ao longo do tempo.

def desvio_padrao(dados):
    return float(np.std(dados))

dados = []

for i in range(len(close_ordenado)):
    if i < 20:
        close_ordenado[i]["desvio_padrão"] = None
    else:
        for j in range(i-20,i+1):
            dados.append(close_ordenado[j]["daily_return"])
        close_ordenado[i]["desvio_padrão"] = desvio_padrao(dados)

print(close_ordenado)