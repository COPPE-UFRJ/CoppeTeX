@echo off
setlocal
rem ===========================================================================
rem  coppetex-novo.bat -- comeca um trabalho novo.
rem
rem  Sem argumento, abre uma janela com abas, pergunta os dados do trabalho e
rem  escreve os dois arquivos com que ele comeca: o .tex e o .bib.
rem
rem      coppetex-novo.bat                          abre a janela
rem      coppetex-novo.bat --gerar                  gera com os padroes da COPPE
rem      coppetex-novo.bat --gerar --tipo=msc --programa=PEM
rem      coppetex-novo.bat --ajuda                  a lista de todos os campos
rem
rem  Os padroes sao os da COPPE COMPLETA, como no exemplo da entrega: quem nao
rem  mexe em nada recebe um trabalho com todas as folhas que a norma preve.
rem
rem  Nao confundir com o coppetex.bat, que e o painel de quem MEXE na classe.
rem  Este aqui e para quem vai ESCREVER uma tese.
rem ===========================================================================

where python >nul 2>nul
if errorlevel 1 goto sempython

python "%~dp0tools\geradocvazio.py" %*
exit /b %errorlevel%

:sempython
echo.
echo   Nao achei o python no PATH, e o gerador e escrito em Python.
echo.
echo   Instale o Python 3 (python.org) e rode de novo. Sem ele, comece
echo   copiando o example.tex da entrega e apagando o que nao for usar.
echo.
exit /b 1
