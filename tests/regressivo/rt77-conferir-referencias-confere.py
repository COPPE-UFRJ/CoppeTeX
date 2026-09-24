# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (ferramentas) o tools/conferir-referencias.py separava as referencias do PDF pela marca [n]; desde a #140 a lista numerica sai sem colchetes, ele achava zero referencias, dava o documento como "pulado" e passava -- de 17 a 21/09/2026 nenhuma referencia foi conferida. E o gabarito nao era o Manual: 12 das 34 referencias tinham sido ajustadas ao que a classe compoe, e a divergencia aceita de uma entrada escondia qualquer outra dela (#167).

Uma virgula errada da classe antes das paginas -- "1996, p. 7-16" -- passou
assim: a entrada tinha nota de divergencia aceita por outro motivo, e a nota
aceitava a entrada inteira.

Cobra-se, sem compilar:
  1. a separacao das referencias no texto extraido: com e sem colchetes, so o
     numero SEGUINTE da sequencia abre referencia -- a linha de continuacao que
     comeca por "156 p." nao parte a anterior --, o folio sozinho na linha nao
     entra, e o apendice fecha a lista;
  2. a comparacao: a divergencia aceita so passa quando a classe compoe a forma
     do @comment{Classe: ...}; sem essa forma, com outra saida, ou com a nota
     velha (a classe ja compoe o Manual), e divergencia;
  3. os 35 gabaritos de cada base sao o texto do Manual, lido do PDF de specs/
     (as 34 categorias da 4.2, e o segundo exemplo da 4.2.6.2, que e o que segue
     o texto da norma);
  4. toda divergencia aceita das duas bases traz a forma da classe.
"""
import importlib.util
import os
import shutil
from medidas import relatar

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))

spec = importlib.util.spec_from_file_location(
    "conferir_referencias", os.path.join(RAIZ, "tools", "conferir-referencias.py"))
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)

problemas = []

# 1. a separacao
TEXTO = """Fim do ultimo capitulo.

                                  REFERÊNCIAS

1  CASTRO, C. M. A prática da pesquisa. São Paulo: Mc Graw-Hill do Brasil,
   1978. 156 p.

2  SILVA, José. Um título qualquer. Rio de Janeiro: Editora, 2000.
156 p.

                                  12

[3]  SOUZA, Maria. Outro título. São Paulo: Outra, 1979.
1979. Nota.
4 LEITE, Sonia. Memória. 1997.
APÊNDICE A – NADA
5 NAO E REFERENCIA
"""
ESPERADO = [
    (1, "CASTRO, C. M. A prática da pesquisa. São Paulo: Mc Graw-Hill do Brasil, 1978. 156 p."),
    (2, "SILVA, José. Um título qualquer. Rio de Janeiro: Editora, 2000. 156 p."),
    (3, "SOUZA, Maria. Outro título. São Paulo: Outra, 1979. 1979. Nota."),
    (4, "LEITE, Sonia. Memória. 1997."),
]
obtido = cr.separa_referencias(TEXTO)
if obtido != ESPERADO:
    problemas.append("a separacao das referencias saiu errada:\n  esperado %r\n  obtido   %r"
                     % (ESPERADO, obtido))
if cr.separa_referencias(TEXTO.replace("REFERÊNCIAS", "BIBLIOGRAFIA")):
    problemas.append("sem o titulo REFERENCIAS a separacao devia achar nada")

# 2. a comparacao
GAB = {
    "ok":      ("X. Titulo. 2000.", None, None),
    "difere":  ("X. Titulo. 2000.", None, None),
    "aceita":  ("X, Y. 2000.", "errata", "X; Y. 2000."),
    "semfor":  ("X, Y. 2000.", "errata", None),
    "velha":   ("X, Y. 2000.", "errata", "X; Y. 2000."),
    "fora":    ("X, Y. 2000.", "errata", "X; Y. 2000."),
    "ausente": ("Z. 2001.", None, None),
}
COMPOSTAS = {
    "ok": "X. Titulo. 2000.",
    "difere": "X. Titulo, 2000.",
    "aceita": "X; Y. 2000.",
    "semfor": "X; Y. 2000.",
    "velha": "X, Y. 2000.",
    "fora": "X; Y, 2000.",
}
dif, aceitas, linhas = cr.compara(GAB, COMPOSTAS)
relato = "\n".join(linhas)
if (dif, aceitas) != (5, 1):
    problemas.append("a comparacao contou %d divergencia(s) e %d aceita(s); sao 5 e 1:\n%s"
                     % (dif, aceitas, relato))
for marca in ("DIFERE   difere", "SEM FORMA semfor", "NOTA VELHA velha",
              "DIFERE   fora (fora da divergencia aceita)", "AUSENTE  ausente"):
    if marca not in relato:
        problemas.append("o relato da comparacao nao diz %r:\n%s" % (marca, relato))
for chave in ("ok", "aceita"):
    if any(l.split()[1:2] == [chave] for l in linhas):
        problemas.append("o relato acusa %r, que passa:\n%s" % (chave, relato))

# 3. os gabaritos sao o texto do Manual
if not shutil.which("pdftotext"):
    print("AVISO: sem o pdftotext, os gabaritos nao foram conferidos contra o Manual")
elif not os.path.exists(cr.MANUAL):
    problemas.append("o PDF do Manual nao esta em specs/: %s" % cr.MANUAL)
else:
    texto = cr._saida(["pdftotext", "-enc", "UTF-8", "-layout", cr.MANUAL, "-"])
    for base in cr.BASES:
        gab = cr.gabaritos(base)
        if len(gab) != 35:
            problemas.append("%s: %d gabaritos lidos, e sao 35" % (os.path.basename(base), len(gab)))
        fora = cr.fora_do_manual(gab, texto)
        if fora:
            problemas.append("%s: gabarito que nao e o texto do Manual: %s"
                             % (os.path.basename(base), ", ".join(fora)))

# 4. toda divergencia aceita traz a forma da classe
for base in cr.BASES:
    for chave, (manual, motivo, classe) in cr.gabaritos(base).items():
        if motivo and not classe:
            problemas.append("%s: %s tem divergencia aceita sem o @comment{Classe: ...}"
                             % (os.path.basename(base), chave))
        if classe and not motivo:
            problemas.append("%s: %s tem @comment{Classe: ...} sem divergencia aceita"
                             % (os.path.basename(base), chave))

relatar(problemas)
