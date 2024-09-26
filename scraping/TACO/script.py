import os
import camelot
import locale
import unicodedata
import scraping.TACO.modelo_tabelas as modelo_tabelas
import requests
from database import engine
from sqlalchemy.orm import Session
from model.alimento import Alimento, Alimento_AcidosGraxos, Alimento_Aminoacidos, Alimento_Centesimal

NOME_ARQ_PDF = "./scraping/TACO/tabela.pdf"

def _baixar_pdf():
  if os.path.isfile(NOME_ARQ_PDF):
     return

  URL = "https://www.cfn.org.br/wp-content/uploads/2017/03/taco_4_edicao_ampliada_e_revisada.pdf"
  with open(NOME_ARQ_PDF, "wb") as arq:
    respPDF = requests.get(URL, stream=True)
    if respPDF.status_code != 200:
       raise Exception("Erro ao baixar a tabela TACO")
    else:
      arq.write(respPDF.content)  


def _limpar_nome(nome):
    return [_remover_acentos(parte).strip().lower() for parte in nome.split(",")]


def _remover_acentos(nome):
    return "".join(
        ch
        for ch in unicodedata.normalize("NFKD", nome)
        if unicodedata.category(ch) != "Mn"
    )


def _preencher_info_alimento(lista_alimentos, linha_pdf, conteudo_categoria):
    if not lista_alimentos[linha_pdf[0]]["nome"]:
        lista_alimentos[linha_pdf[0]]["nome"] = _limpar_nome(linha_pdf[1])

    for n_coluna, nome_info in enumerate(conteudo_categoria["lista"]):
        if nome_info[0] == "_":
            continue
        else:
            lista_alimentos[linha_pdf[0]][conteudo_categoria["categoria"]][
                nome_info
            ] = _processar_valor(linha_pdf[n_coluna])


def _processar_valor(val):
    if val.replace(",", "").isnumeric():
        return locale.atof(val) / 100
    else:
        return 0


def _ler_tabela(lista_alimentos, valores_tabela, modelo):
    for linha in valores_tabela:
        if linha[0].isnumeric():
            _preencher_info_alimento(lista_alimentos, linha, modelo)


def _preparar_colecao():
  colecao_preparada = {}
  for n in range(600):
      colecao_preparada[str(n)] = {
          "nome": [],
          modelo_tabelas.Categorias.CENTESIMAL.value: {},
          modelo_tabelas.Categorias.ACIDOS_GRAXOS.value: {},
          modelo_tabelas.Categorias.AMINOACIDOS.value: {},
      }
  return colecao_preparada;


def _reconhecer_centesimal(colecao_info):
  tabelas_reconhecidas = camelot.read_pdf(
      NOME_ARQ_PDF, pages="29-68,103,104", flavor="stream"
  )
  centesimal = tabelas_reconhecidas[:-2]
  for i in range(0, len(centesimal) - 1, 2):
      _ler_tabela(
          colecao_info,
          centesimal[i].df.values,
          modelo_tabelas.info_centesimal_um,
      )
      _ler_tabela(
          colecao_info,
          centesimal[i + 1].df.values,
          modelo_tabelas.info_centesimal_dois,
      )
  aminoacidos = tabelas_reconhecidas[-2:]
  _ler_tabela(colecao_info, aminoacidos[0].df.values, modelo_tabelas.info_amino_um)
  _ler_tabela(colecao_info, aminoacidos[1].df.values, modelo_tabelas.info_amino_dois)


def _reconhecer_graxos(colecao_info):
  graxos_parte_um = camelot.read_pdf(
      NOME_ARQ_PDF,
      pages=("".join(str(c) + "," for c in range(71, 100, 2))[:-1]),
      flavor="stream",
      columns=["114.7,351.02,425.24,476.42,524.24,561.80,598.64,634.04,669.44,704.84,740.24"],
  )
  graxos_parte_dois = camelot.read_pdf(
      NOME_ARQ_PDF,
      pages=("".join(str(c) + "," for c in range(72, 101, 2))[:-1]),
      flavor="stream",
      columns=["118.22,172.52,227.12,281.72,336.32,390.92,445.52,502.167,54.78,607.34,663.90,718.46"]
  )
  a = 1
  for tabela_g1 in graxos_parte_um:
      a += 1
      _ler_tabela(colecao_info, tabela_g1.df.values, modelo_tabelas.info_graxos_um)

  a = 1
  for tabela_g2 in graxos_parte_dois:
      a += 1
      _ler_tabela(colecao_info, tabela_g2.df.values, modelo_tabelas.info_graxos_dois)


def _preencher_banco(info):  
  with Session(engine) as db:
    db.query(Alimento_Centesimal).delete()
    db.query(Alimento_AcidosGraxos).delete()
    db.query(Alimento_Aminoacidos).delete()
    db.query(Alimento).delete()
    db.commit()
    
    for al in info.items():
      if al[1]['nome'] == []:
        continue

      novoAlim = Alimento(_id=al[0], _nome=";".join(al[1]['nome']) ,**dict(list(al[1]['centesimal'].items())[:11]))
      novoAlim.centesimal = Alimento_Centesimal(_id=al[0], **dict(list(al[1]['centesimal'].items())[11:]))
      novoAlim.graxos = Alimento_AcidosGraxos(_id=al[0], **dict(list(al[1]['acidos_graxos'].items())))
      novoAlim.aminoacidos = Alimento_Aminoacidos(_id=al[0], **dict(list(al[1]['aminoacidos'].items())))
      
      db.add(novoAlim)
      
      db.commit()


def executar_scraping(force=False):
  with Session(engine) as db:
    if (db.query(Alimento).count() != 0) and not force:
       return
  print("Iniciando scraping da tabela TACO...")
  locale.setlocale(locale.LC_NUMERIC, "pt-br")
  _baixar_pdf()
  colecao_info = _preparar_colecao()
  _reconhecer_centesimal(colecao_info)
  _reconhecer_graxos(colecao_info)
  _preencher_banco(colecao_info)
  print("Scraping da tabela TACO finalizado.")
