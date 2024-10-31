from typing import Optional, Dict
from unidecode import unidecode
from utils import avaliar_quantidade, converter_para_singular, converter_para_unidade_padrao
from constants import SUBSTITUICOES_FRACOES, PATTERN_INGREDIENTE, PATTERN_INGREDIENTE_SEM_UNIDADE
import re


def processar_ingrediente(texto_limpo: str) -> Optional[Dict]:
    """
    Processa uma linha de texto representando um ingrediente e extrai seus componentes.

    Args:
        texto_limpo (str): Linha de texto com o ingrediente.

    Returns:
        dict ou None: Dicionário com os componentes do ingrediente ou None se não for válido.
    """
    # Verificar se o ingrediente é "opcional" e descartar se for
    if 'opcional' in texto_limpo.lower():
        return None

    # Verificar se o ingrediente é "a gosto"
    if 'a gosto' in texto_limpo.lower():
        return {
            'nome_ingrediente': texto_limpo.replace('a gosto', '').strip(),
            'quantidade': None,
            'unidade_original': None,
            'a_gosto': True
        }

    # Substituir frações unicode por texto
    for k, v in SUBSTITUICOES_FRACOES.items():
        texto_limpo = texto_limpo.replace(k, v)

    # Tentar corresponder com padrão completo
    match = PATTERN_INGREDIENTE.match(texto_limpo)
    if match:
        quantidade_str = match.group(1)
        unidade_raw = match.group(2).strip()
        nome_ingrediente = match.group(3).strip()
    else:
        # Tentar outra expressão regular sem unidade
        match_sem_unidade = PATTERN_INGREDIENTE_SEM_UNIDADE.match(texto_limpo)
        if match_sem_unidade:
            quantidade_str = match_sem_unidade.group(1)
            unidade_raw = ''
            nome_ingrediente = match_sem_unidade.group(2).strip()
        else:
            # Se não houver correspondência, assumir que é apenas o nome do ingrediente
            quantidade_str = None
            unidade_raw = None
            nome_ingrediente = texto_limpo.strip()

    # Converter quantidade para float
    quantidade = avaliar_quantidade(quantidade_str) if quantidade_str else None

    # Limpar e padronizar a unidade
    if unidade_raw is not None:
        unidade_clean = unidade_raw.lower().strip()

        # Remover parênteses da unidade
        unidade_clean = unidade_clean.replace('(', '').replace(')', '')

        # Padronizar colheres
        if 'colher' in unidade_clean or 'colheres' in unidade_clean:
            if 'chá' in unidade_clean or 'cha' in unidade_clean:
                unidade_original = 'colher (cha)'
            elif 'sopa' in unidade_clean:
                unidade_original = 'colher (sopa)'
            else:
                # Se não especificado, assumir colher de sopa
                unidade_original = 'colher (sopa)'
        elif 'xícara' in unidade_clean or 'xicara' in unidade_clean:
            unidade_original = 'xicara (cha)'  # Assumindo que xícaras são geralmente de chá
        else:
            # Converter para singular outras unidades
            unidade_original = converter_para_singular(unidade_clean)
    else:
        unidade_original = None

    # Se não houver unidade, mas houver quantidade, definir 'unitario' como unidade
    if quantidade is not None and (unidade_original is None or unidade_original == ''):
        unidade_original = 'unitario'

    # Converter a unidade para algo padronizado
    quantidade_normalizada, unidade_normalizada = converter_para_unidade_padrao(quantidade, unidade_original)

    # Remover parênteses e seu conteúdo do nome do ingrediente
    nome_ingrediente = re.sub(r'\s*\(.*?\)', '', nome_ingrediente).strip()
    return {
        'nome_ingrediente': nome_ingrediente.strip(),
        'quantidade': quantidade,
        'unidade_original': unidade_original,
        'a_gosto': False,
        'quantidade_normalizada': quantidade_normalizada,
        'unidade_normalizada': unidade_normalizada
    }
