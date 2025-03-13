import os
import webbrowser
import pandas as pd
import plotly.express as px
from utils import carregar_dados, limpar_dados, calcular_duracao

if __name__ == "__main__":
    # Caminho ajustado corretamente (relativo)
    caminho_arquivo = "../dados/cronograma.xlsx"

    # Carregar, limpar e calcular duração das tarefas
    cronograma = carregar_dados(caminho_arquivo)
    cronograma = limpar_dados(cronograma)
    cronograma = calcular_duracao(cronograma)

    # Simplificando o gráfico: apenas uma barra por tarefa (usando datas reais, se existentes)
    cronograma["Data Inicial Gantt"] = cronograma["Início Real"].combine_first(cronograma["Início Previsto"])
    cronograma["Data Final Gantt"] = cronograma["Término Real"].combine_first(cronograma["Término Previsto"])

    # Formatação para exibir duração no hover do gráfico
    cronograma["Descrição com Duração"] = cronograma["Descrição dos Serviços"] + \
        " (" + cronograma["Duração (dias)"].astype(str) + " dias)"

    fig = px.timeline(cronograma, 
                      x_start="Data Inicial Gantt", 
                      x_end="Data Final Gantt", 
                      y="Descrição dos Serviços", 
                      title="Cronograma de Obra - Gráfico Gantt",
                      labels={
                          "Data Inicial Gantt": "Início",
                          "Data Final Gantt": "Término",
                          "Descrição dos Serviços": "Tarefas"
                      },
                      color="Duração (dias)",
                      opacity=0.9,
                      color_continuous_scale="Viridis")

    fig.update_yaxes(autorange="reversed")

    # Ajustes visuais
    fig.update_layout(
        xaxis_title="Datas",
        yaxis_title="Descrição dos Serviços",
        font=dict(size=13, family="Arial"),
        paper_bgcolor='rgba(248, 249, 250, 1)',
        hovermode='closest'
    )
    # Salvar e abrir gráfico
resultados_path = "resultados"
if not os.path.exists(resultados_path):
    os.makedirs(resultados_path)

caminho_grafico = os.path.join(resultados_path, "cronograma_gantt_duracao.html")
fig.write_html(caminho_grafico)

# Corrigido aqui: passando o caminho do arquivo (não da pasta)
caminho_absoluto = 'file://' + os.path.abspath(caminho_grafico)
webbrowser.open(caminho_absoluto)