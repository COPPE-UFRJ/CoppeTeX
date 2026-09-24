# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, Anexo A e Anexo B) a folha de rosto repetia a linha de logotipos da capa; o Anexo A poe os dois logotipos na CAPA, e o Anexo B -- o modelo da folha de rosto -- nao traz imagem nenhuma (#130).

O Anexo A do Manual UFRJ/SiBI mostra, no alto da capa, "Logo da UFRJ" e "Logo do
Programa", os dois marcados como opcionais. O Anexo B, que e o modelo da folha
de rosto, comeca pelo nome do autor: nao ha logotipo nenhum nele, nem nas duas
folhas do modelo que o SiBI distribui (specs/Folha adicional T&D Coleta+
CAPES.pdf). A secao 1 da Norma COPPE punha os dois logotipos nas duas folhas e
citava o Anexo A como apoio -- mas o Anexo A e sobre a capa.

Os logotipos sao vetoriais, e o `pdfimages' nao os enxerga: este teste mede
TINTA. Rende cada folha em tons de cinza e olha a faixa de cima, da borda ate
4 cm -- onde a linha de logotipos ficava, e acima da primeira linha de texto das
duas folhas (a margem superior e de 3 cm, e o que vem depois comeca mais abaixo).

Cobra-se, com o estilo da COPPE carregado, que e quem declara os logotipos:
  1. a capa (folha 1) tem tinta nessa faixa -- os logotipos;
  2. a folha de rosto (folha 2) nao tem nenhuma.
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medidas import Documento, relatar  # noqa: E402

DPI = 50
FAIXA_CM = 4.0


def pgm(pdf, pagina):
    """A folha renderizada em tons de cinza: (largura, altura, bytes).

    O pdftoppm escreve num arquivo, e nao na saida padrao: nesta versao o `-'
    devolve vazio."""
    pasta = tempfile.mkdtemp(prefix="ufrj-rt71-")
    try:
        prefixo = os.path.join(pasta, "folha")
        p = subprocess.run(["pdftoppm", "-gray", "-singlefile", "-r", str(DPI),
                            "-f", str(pagina), "-l", str(pagina), pdf, prefixo],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        arq = prefixo + ".pgm"
        d = io.open(arq, "rb").read() if os.path.exists(arq) else b""
    finally:
        shutil.rmtree(pasta, ignore_errors=True)
    if not d.startswith(b"P5"):
        raise SystemExit("pdftoppm nao devolveu um PGM na folha %d: %r"
                         % (pagina, p.stderr.decode("utf-8", "replace")[:200]))
    campos = []
    i = 2
    while len(campos) < 3:
        while i < len(d) and d[i:i + 1].isspace():
            i += 1
        if d[i:i + 1] == b"#":
            while i < len(d) and d[i:i + 1] != b"\n":
                i += 1
            continue
        j = i
        while j < len(d) and not d[j:j + 1].isspace():
            j += 1
        campos.append(int(d[i:j]))
        i = j
    larg, alt, _ = campos
    return larg, alt, d[i + 1:]


def tinta_no_alto(pdf, pagina):
    """Quantos pixels escuros ha na faixa de cima da folha."""
    larg, alt, px = pgm(pdf, pagina)
    linhas = int(FAIXA_CM / 2.54 * DPI)
    escuros = 0
    for y in range(min(linhas, alt)):
        linha = px[y * larg:(y + 1) * larg]
        escuros += sum(1 for b in linha if b < 200)
    return escuros


problemas = []
with Documento(corpo=r"\chapter{Um}Texto.") as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    capa = tinta_no_alto(d.pdf, 1)
    if capa < 100:
        problemas.append("a capa (folha 1) esta sem tinta nos %.1f cm de cima (%d pixels): "
                         "o Anexo A poe os dois logotipos nela" % (FAIXA_CM, capa))
    rosto = tinta_no_alto(d.pdf, 2)
    if rosto > 0:
        problemas.append("a folha de rosto (folha 2) tem tinta nos %.1f cm de cima "
                         "(%d pixels escuros); o Anexo B nao traz logotipo nenhum"
                         % (FAIXA_CM, rosto))

relatar(problemas)
