from enum import Enum

class Categorias(str, Enum):
    CENTESIMAL = "centesimal"
    ACIDOS_GRAXOS = "acidos_graxos"
    AMINOACIDOS = "aminoacidos"

info_centesimal_um = {
    "categoria": Categorias.CENTESIMAL,
    "lista": [
        "_id",
        "_nome",
        "umidade",
        "energia_kcal",
        "energia_kj",
        "proteina",
        "lipideos",
        "colesterol",
        "carboidrato",
        "fibra_alimentar",
        "cinzas",
        "calcio",
        "magnesio",
    ],
}

info_centesimal_dois = {
    "categoria": Categorias.CENTESIMAL,
    "lista": [
        "_id",
        "manganes",
        "fosforo",
        "ferro",
        "sodio",
        "potassio",
        "cobre",
        "zinco",
        "retinol",
        "re",
        "rae",
        "tiamina",
        "riboflavina",
        "piridoxina",
        "niacina",
        "vitamina_c",
    ],
}

info_graxos_um = {
    "categoria": Categorias.ACIDOS_GRAXOS,
    "lista": [
        "_id",
        "_nome",
        "saturados",
        "mono_insaturados",
        "poli_insaturados",
        "_12_0",
        "_14_0",
        "_16_0",
        "_18_0",
        "_20_0",
        "_22_0",
        "_24_0",
    ],
}

info_graxos_dois = {
    "categoria": Categorias.ACIDOS_GRAXOS,
    "lista": [
        "_id",
        "_14_1",
        "_16_1",
        "_18_1",
        "_20_1",
        "_18_2n6",
        "_18_3n3",
        "_20_4",
        "_20_5",
        "_22_5",
        "_22_6",
        "_18_1t",
        "_18_2t",
    ],
}

info_amino_um = {
    "categoria": Categorias.AMINOACIDOS,  
    "lista": [
        "_id",
        "_nome",
        "triptofano",
        "treonina",
        "isoleucina",
        "leucina",
        "lisina",
        "metionina",
        "cistina",
        "fenilalanina",
        "tirosina",
    ],
}

info_amino_dois = {
    "categoria": Categorias.AMINOACIDOS,
    "lista": [
        "_id",
        "valina",
        "arginina",
        "histidina",
        "alanina",
        "acido_aspartico",
        "acido_glutamico",
        "glicina",
        "prolina",
        "serina",
    ],
}

modelo_JSON = {
    "ID_Alimento": {
        "Nome": [],
        Categorias.CENTESIMAL: {},
        Categorias.ACIDOS_GRAXOS: {},
        Categorias.AMINOACIDOS: {},
    }
}
