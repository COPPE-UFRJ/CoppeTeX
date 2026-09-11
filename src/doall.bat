@echo off
setlocal
rem ===========================================================================
rem  doall.bat -- atalho historico. O bat central agora e ..\coppetex.bat.
rem
rem  Este arquivo fazia tres coisas de uma vez: gerava o src a partir do .dtx,
rem  compilava os PDFs e copiava o conjunto minimo para ..\dist. Ele continua
rem  fazendo exatamente isso, mas por intermedio do painel, e nao mais com uma
rem  lista de copias propria.
rem
rem  A razao da mudanca: a lista de arquivos que vao para dist\ estava escrita
rem  aqui E no Makefile, e as duas versoes divergiram -- uma delas copiava o
rem  README.md da raiz por cima do guia de instalacao de dist\ a cada execucao,
rem  e reintroduzia os cinco exemplos por idioma que tinham sido retirados de
rem  proposito. Agora a lista existe em um lugar so, em tools\painel.py.
rem
rem  Quem quiser escolher o que fazer, em vez de fazer tudo:
rem      ..\coppetex.bat
rem ===========================================================================

call "%~dp0..\coppetex.bat" --regerar --docs --dist
exit /b %errorlevel%
