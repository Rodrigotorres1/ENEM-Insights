"""Funções utilitárias compartilhadas entre os notebooks."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ---------------------------------------------------------------------------
# Configurações globais de visualização
# ---------------------------------------------------------------------------

PALETTE = "Blues_r"
FIGSIZE_DEFAULT = (10, 6)

MAPA_RENDA = {
    "A": "Nenhuma renda",
    "B": "Até R$ 1.320",
    "C": "R$ 1.320 – R$ 1.980",
    "D": "R$ 1.980 – R$ 2.640",
    "E": "R$ 2.640 – R$ 3.300",
    "F": "R$ 3.300 – R$ 3.960",
    "G": "R$ 3.960 – R$ 5.280",
    "H": "R$ 5.280 – R$ 6.600",
    "I": "R$ 6.600 – R$ 7.920",
    "J": "R$ 7.920 – R$ 9.240",
    "K": "R$ 9.240 – R$ 10.560",
    "L": "R$ 10.560 – R$ 13.200",
    "M": "R$ 13.200 – R$ 19.800",
    "N": "R$ 19.800 – R$ 26.400",
    "O": "R$ 26.400 – R$ 39.600",
    "P": "Acima de R$ 39.600",
}

MAPA_ESCOLA = {
    1: "Não respondeu",
    2: "Pública",
    3: "Privada",
    4: "Exterior",
}

MAPA_COR_RACA = {
    0: "Não declarado",
    1: "Branca",
    2: "Preta",
    3: "Parda",
    4: "Amarela",
    5: "Indígena",
    6: "Não dispõe",
}

NOTAS_COLS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
NOTAS_LABELS = {
    "NU_NOTA_CN": "Ciências da Natureza",
    "NU_NOTA_CH": "Ciências Humanas",
    "NU_NOTA_LC": "Linguagens e Códigos",
    "NU_NOTA_MT": "Matemática",
    "NU_NOTA_REDACAO": "Redação",
}


def configurar_estilo():
    """Aplica o estilo padrão do projeto a todos os gráficos."""
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
    plt.rcParams.update({
        "figure.dpi": 120,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def salvar_figura(fig: plt.Figure, nome: str, pasta: str = "../reports/figures") -> None:
    """Salva a figura em PNG na pasta de relatórios."""
    caminho = f"{pasta}/{nome}.png"
    fig.savefig(caminho, bbox_inches="tight")
    print(f"Figura salva: {caminho}")


def nota_media(df: pd.DataFrame) -> pd.Series:
    """Retorna a média das 5 notas por linha (ignora NaN)."""
    return df[NOTAS_COLS].mean(axis=1)


def formatar_eixo_mil(ax, eixo: str = "y") -> None:
    """Formata eixo numérico com separador de milhar em PT-BR."""
    fmt = mticker.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", "."))
    if eixo == "y":
        ax.yaxis.set_major_formatter(fmt)
    else:
        ax.xaxis.set_major_formatter(fmt)
