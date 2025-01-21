# Extração com Python e Visualização de Dados

## Objetivo
Desenvolver uma aplicação simples que consome dados da **API Alpha Vantage** para o ativo IBM, realiza o cálculo de retorno acumulado, volatilidade média e disponibiliza esses dados em um arquivo JSON, que é utilizado em uma página HTML para plotar gráficos interativos com Plotly.

## 1. Visão Geral
A aplicação principal é um **script Python** que:

1. **Faz requisição** à API Alpha Vantage para obter dados diários do ativo IBM.  
2. **Extrai e processa** dados de fechamento para calcular:
   - **Retorno diário** (variação percentual dia a dia)  
   - **Retorno acumulado** (soma cumulativa dos retornos diários)  
   - **Volatilidade média** (desvios padrão em janelas móveis, depois tirando a média das volatilidades)  
3. **Salva** esses resultados em arquivos JSON (por exemplo, `retorno_acumulado.json` e `volatilidade.json`).


Em seguida, temos uma **página HTML** que utiliza **Plotly.js** para ler os arquivos JSON e exibir **gráficos de linhas** interativos:
- Um gráfico para **Retorno Acumulado** ao longo do tempo.
- Um gráfico para **Volatilidade** (média dos desvios padrão) ao longo do tempo.

# 2. Pré Requisitos
- **Python 3.8+** (ou superior)
- Biblioteca Requests (para fazer a requisição à API)
- Instale via pip install requests
- Recomendo a utilização de um ambiente virtual venv.
- Um servidor local (ou outro ambiente) para servir o index.html e permitir o fetch dos JSON, por exemplo:
  - **python -m http.server 8000**


# 3. Passo a Passo de Execução
- Clonar ou baixar este repositório.
- Criar ambiente virtual:
  - **python -m venv venv**
  - **venv\Scripts\activate (Windows)**
  - ou
  - **source venv/bin/activate (Linux/Mac)**
- Instalar as dependências através do requirements.txt:
  - **pip install requirements.txt**
- Instalar a biblioteca requests
   - **pip install requests**
- Executar o script Python para baixar e processar os dados:
  - **py app.py**
  - Isso vai gerar ou atualizar os arquivos retorno_acumulado.json e volatilidade.json.
- Iniciar um servidor local para servir a página HTML:
  - **python -m http.server 8000**
- Abrir o navegador em http://localhost:8000/index.html para visualizar os gráficos.

# 4. Visualização 

- Após iniciar o servidor e acessar a página, você deve ver dois gráficos interativos:
1. **Retorno Acumulado**
2. **Volatilidade ao longo do tempo**

![image](https://github.com/user-attachments/assets/24e7bcd2-94b8-4cc3-b531-55278b61648c)
![image](https://github.com/user-attachments/assets/9967338b-20e3-49dd-9858-179fbd02a194)
