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
        "ag12_0",
        "ag14_0",
        "ag16_0",
        "ag18_0",
        "ag20_0",
        "ag22_0",
        "ag24_0",
    ],
}

info_graxos_dois = {
    "categoria": Categorias.ACIDOS_GRAXOS,
    "lista": [
        "_id",
        "ag14_1",
        "ag16_1",
        "ag18_1",
        "ag20_1",
        "ag18_2n6",
        "ag18_3n3",
        "ag20_4",
        "ag20_5",
        "ag22_5",
        "ag22_6",
        "ag18_1t",
        "ag18_2t",
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
