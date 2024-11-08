from typing import Optional, Tuple
from scraping.ingredientes.constants import SUBSTITUICOES_FRACOES, CONVERSOES, PLURAIS_PARA_SINGULAR

def avaliar_quantidade(quantidade_str: str) -> Optional[float]:
    """
    Avalia uma string de quantidade e retorna seu valor em float.

    Args:
        quantidade_str (str): A quantidade em formato de string.

    Returns:
        float or None: O valor da quantidade em float ou None se não for possível avaliar.
    """
    quantidade_str = quantidade_str.replace(',', '.').strip()
    try:
        if ' ' in quantidade_str:
            partes = quantidade_str.split(' ')
            inteiro = float(partes[0])
            frac_str = partes[1]
            numerador, denominador = map(float, frac_str.split('/'))
            return inteiro + (numerador / denominador)
        elif '/' in quantidade_str:
            numerador, denominador = map(float, quantidade_str.split('/'))
            return numerador / denominador
        else:
            return float(quantidade_str)
    except ValueError:
        return None  # Retorna None se não for possível avaliar


def converter_para_unidade_padrao(quantidade: float, unidade_original: Optional[str]) -> Tuple[float, Optional[str]]:
    """
    Converte a quantidade para a unidade padrão.

    Args:
        quantidade (float): A quantidade a ser convertida.
        unidade_original (str): A unidade original.

    Returns:
        Tuple[float, str]: A quantidade normalizada e a unidade padrão.
    """
    unidade_original_lower = unidade_original.lower() if unidade_original else ''
    if unidade_original_lower in CONVERSOES:
        unidade_padrao, fator = CONVERSOES[unidade_original_lower]
        quantidade_normalizada = quantidade * fator
        return quantidade_normalizada, unidade_padrao
    else:
        return quantidade, unidade_original  # Unidade não reconhecida, retorna como está


def converter_para_singular(unidade: str) -> str:
    """
    Converte uma unidade no plural para o singular.

    Args:
        unidade (str): Unidade no plural.

    Returns:
        str: Unidade no singular.
    """
    unidade = unidade.strip().lower()
    unidade_singular = PLURAIS_PARA_SINGULAR.get(unidade, unidade)
    return unidade_singular
