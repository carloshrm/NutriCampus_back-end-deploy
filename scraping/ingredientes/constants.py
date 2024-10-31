import re

# Conversões de unidades
CONVERSOES = {
    'xicara': ('ml', 240),
    'xicara (cha)': ('ml', 240),
    'colher (sopa)': ('ml', 15),
    'colher (cha)': ('ml', 5),
    'colher': ('ml', 15),  # Assumindo colher como colher de sopa
    'grama': ('g', 1),
    'kg': ('g', 1000),
    'g': ('g', 1),
    'ml': ('ml', 1),
    'litro': ('ml', 1000),
    'folha': ('unitario', 1),
    'dente': ('unitario', 1),
    'pitada': ('unitario', 1),
    'gota': ('unitario', 1),
    'lata': ('unitario', 1),
    'copo': ('ml', 250),
    'unidade': ('unitario', 1),
    'unitario': ('unitario', 1)
}

# Substituições de frações unicode por texto
SUBSTITUICOES_FRACOES = {
    '½': '1/2',
    '⅓': '1/3',
    '⅔': '2/3',
    '¼': '1/4',
    '¾': '3/4',
    '⅛': '1/8',
}

# Plurais para singular
PLURAIS_PARA_SINGULAR = {
    'xícaras': 'xicara',
    'colheres': 'colher',
    'colheres de chá': 'colher (cha)',
    'colheres de sopa': 'colher (sopa)',
    'colher de chás': 'colher (cha)',
    'colher de sopas': 'colher (sopa)',
    'gramas': 'grama',
    'kgs': 'kg',
    'mls': 'ml',
    'litros': 'litro',
    'folhas': 'folha',
    'dentes': 'dente',
    'pitadas': 'pitada',
    'gotas': 'gota',
    'latas': 'lata',
    'copos': 'copo',
    'unidades': 'unidade'
}

# Expressões regulares compiladas
PATTERN_INGREDIENTE = re.compile(
    r'^(\d+\s+\d+/\d+|\d+/\d+|\d+(?:[\.,]\d+)?)\s+([^\d]+?)\s+de\s+(.*)$', re.IGNORECASE)
PATTERN_INGREDIENTE_SEM_UNIDADE = re.compile(
    r'^(\d+\s+\d+/\d+|\d+/\d+|\d+(?:[\.,]\d+)?)(.*)$', re.IGNORECASE)