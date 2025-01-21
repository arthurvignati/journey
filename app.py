import requests
from datetime import datetime
import numpy as np
import json
import copy 

get_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"

#Faça uma requisição GET para a URL da API Alpha Vantage para IBM usando a chave demo:
def get_alpha_json(url):
    r = requests.get(url)
    return r.json()

#Extraia os dados diários de fechamento do ativo a partir da resposta da API.
def extrair_dados_diarios(response):
    time_series_daily = response["Time Series (Daily)"]
    close = []
    for data, dados in time_series_daily.items():
        close.append({
            "data": data,
            "close": dados["4. close"]
        })
    return close


#Ordene os dados cronologicamente.
def ordenar_dados(close):
    close_ordenado = sorted(close, key=lambda x: datetime.strptime(x["data"], "%Y-%m-%d"))
    return close_ordenado


#Calcule
#1) Retorno diário: variação percentual do fechamento de um dia para o próximo
def retorno_diario(anterior, atual):
    var = ((atual/anterior) - 1)*100
    return var

def calculo_retorno_diario(close_ordenado_diario):
    for i in range(len(close_ordenado_diario)):
        if i == 0:
            close_ordenado_diario[i]["daily_return"] = 0
        else:
            anterior = float(close_ordenado_diario[i-1]["close"])
            atual = float(close_ordenado_diario[i]["close"])
            close_ordenado_diario[i]["daily_return"] = retorno_diario(anterior, atual)
    return close_ordenado_diario
        

#2) Retorno acumulado: soma cumulativa dos retornos diários ao longo do tempo
def calculo_retorno_acumulado(close_ordenado_acumulado):
    for i in range(len(close_ordenado_acumulado)):
        if i == 0:
            close_ordenado_acumulado[i]["cumulative_return"] = 0
        else:
            atual = float(close_ordenado_acumulado[i]["daily_return"])
            anterior = float(close_ordenado_acumulado[i-1]["daily_return"])
            cumulative_return = atual + anterior
            close_ordenado_acumulado[i]["cumulative_return"] = cumulative_return
    return close_ordenado_acumulado


#3) Volatilidade média: média dos desvios padrões dos retornos diários calculados em janelas móveis ao longo do tempo.
def desvio_padrao(dados):
    return float(np.std(dados))

def calculo_volatilidade_media(close_ordenado_volatilidade):
    dados = []
    for i in range(len(close_ordenado_volatilidade)):
        if i < 20:
            close_ordenado_volatilidade[i]["desvio_padrao"] = 0
        else:
            for j in range(i-20,i+1):
                dados.append(close_ordenado_volatilidade[j]["daily_return"])
            close_ordenado_volatilidade[i]["desvio_padrao"] = desvio_padrao(dados)
    return close_ordenado_volatilidade


#Salve as datas e os valores de retorno acumulado e volatilidade em um arquivo JSON
def salvar_json(close_ordenado_acumulado, close_ordenado_volatilidade):
    json_str = json.dumps(close_ordenado_acumulado)
    json_str1 = json.dumps(close_ordenado_volatilidade)

    with open("retorno_acumulado.json", "w") as arquivo:
        arquivo.write(json_str)

    with open("volatilidade.json", "w") as arquivo:
        arquivo.write(json_str1)

def main():
    response = get_alpha_json(get_url)
    close = extrair_dados_diarios(response)
    close_ordenado = ordenar_dados(close)
    close_ordenado_diario = calculo_retorno_diario(close_ordenado)
    close_ordenado_cumulative = copy.deepcopy(close_ordenado_diario)
    close_ordenado_acumulado = calculo_retorno_acumulado(close_ordenado_cumulative)
    close_ordenado_volatilidade = calculo_volatilidade_media(close_ordenado_diario)
    salvar_json(close_ordenado_acumulado, close_ordenado_volatilidade)


if __name__ == '__main__':
    main()