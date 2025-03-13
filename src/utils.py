import pandas as pd

def carregar_dados(caminho_arquivo):
    """
    Carrega os dados do cronograma do projeto a partir de um arquivo Excel.
    Retorna um DataFrame com os dados carregados.
    """
    # O cabeçalho correto está na linha 2 (índice 1 para o pandas)
    df = pd.read_excel(caminho_arquivo, header=0)

    colunas_datas = ['Início Previsto', 'Término Previsto', 'Início Real', 'Término Real']

    for coluna in colunas_datas:
        df[coluna] = pd.to_datetime(df[coluna], errors='coerce', dayfirst=True)

    return df
    
def limpar_dados(df):
    """Remove linhas inválidas do DataFrame."""
    df = df.dropna(subset=['Descrição dos Serviços']).reset_index(drop=True)
    # Remover colunas "Unnamed" que aparecem devido ao Excel
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

def calcular_duracao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona colunas de duração prevista e real (dias).
    """
    df["Duração Prevista"] = (df["Término Previsto"] - df["Início Previsto"]).dt.days
    df["Duração Real"] = (df["Término Real"] - df["Início Real"]).dt.days

    # Coluna principal que será exibida no gráfico (real se existir, senão previsto)
    df["Duração (dias)"] = df["Duração Real"].combine_first(df["Duração Prevista"])

    return df
