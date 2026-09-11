@echo off
setlocal
rem ===========================================================================
rem  coppetex.bat -- o bat central da CoppeTeX.
rem
rem  Sem argumento, abre o painel do desenvolvedor e PERGUNTA o que fazer.
rem  Com argumento, faz o que foi pedido e nao pergunta nada:
rem
rem      coppetex.bat                       abre a janela
rem      coppetex.bat --regerar             so regera o src a partir do .dtx
rem      coppetex.bat --testes              so a primeira camada de testes
rem      coppetex.bat --adversativo         so os documentos adversativos
rem      coppetex.bat --regressivo          so a suite de regressao
rem      coppetex.bat --tudo --dist         a prova inteira e a copia para dist
rem      coppetex.bat --versao 2            sobe 4.1 para 4.2
rem      coppetex.bat --ajuda               a lista completa
rem
rem  O manual esta em PAINEL.md, na raiz.
rem
rem  Este arquivo e so o lancador. Quem faz e tools\painel.py, e quem compila e
rem  tools\build-check.ps1 -- que ja existia e continua sendo o unico lugar do
rem  projeto que sabe o ciclo de compilacao de cada documento.
rem ===========================================================================

where python >nul 2>nul
if errorlevel 1 goto sempython

python "%~dp0tools\painel.py" %*
exit /b %errorlevel%

:sempython
echo.
echo   Nao achei o python no PATH, e o painel e escrito em Python.
echo.
echo   Instale o Python 3 (python.org) ou rode o harness direto, que e
echo   PowerShell e nao depende de Python nenhum:
echo.
echo       powershell -File tools\build-check.ps1 -Scope prova
echo       powershell -File tools\build-check.ps1 -Scope class
echo.
echo   A suite de regressao, essa sim, precisa do Python.
echo.
exit /b 1
