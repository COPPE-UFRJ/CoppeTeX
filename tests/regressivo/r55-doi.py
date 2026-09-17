# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.2.3.5) o DOI saia como "doi: 10.1234/..." em versalete -- que a Latin Modern Sans nao tem, e o LaTeX avisava "Font shape T1/lmss/m/sc not available" --, sem o endereco https://doi.org/ (#136).
ABERTO: #136

Os exemplos da 4.2.3.5 e da 4.2.4.3 do Manual UFRJ/SiBI registram o DOI como
"DOI: https://doi.org/<doi>", antes do "Disponivel em:". O coppe.bbx usa o
formato de campo doi do biblatex padrao, que poe a sigla em \\mkbibacro
(versalete) e so o identificador.

Cobra-se:
  1. o texto traz "DOI: https://doi.org/10.1234/teste.5678" (caixa exata);
  2. o .log nao traz o aviso de versalete indisponivel.
"""
from medidas import Documento, relatar, compacta

BIB = r"""@article{doi,
  author = {Costa, Lúcia},
  title = {Um artigo identificado},
  journaltitle = {Revista de Teste},
  location = {Manaus},
  volume = {5},
  number = {1},
  pages = {1-8},
  year = {2020},
  doi = {10.1234/teste.5678},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Costa")
    texto = compacta(d.texto(pg))
    if "DOI: https://doi.org/10.1234/teste.5678" not in texto.replace("doi. org", "doi.org"):
        trecho = texto[texto.upper().find("DOI") - 5:texto.upper().find("DOI") + 45] if "DOI" in texto.upper() else texto[-80:]
        problemas.append("o DOI nao saiu como 'DOI: https://doi.org/...': %r" % trecho)
    if "T1/lmss/m/sc" in d.log:
        problemas.append("o .log avisa versalete indisponivel (T1/lmss/m/sc)")

relatar(problemas)
