@echo on
setlocal EnableExtensions EnableDelayedExpansion

rem ===========================
rem  COPPE bundle build script
rem  Windows .bat
rem  Targets: all (default) | install | doc | example | clean
rem ===========================

rem --- Change to the folder where this .bat lives
pushd "%~dp0" >nul 2>&1

rem --- Config (edit as needed)
set DOC=coppe
set EXAMPLE=example
set PDFLATEX=pdflatex
rem You can switch to lualatex/xelatex if you prefer:
rem set PDFLATEX=lualatex
set BIBER=biber
set MAKEINDEX=makeindex

rem --- PDFLATEX flags: stop on first error, non-interactive
set PDFLATEX_FLAGS=-halt-on-error -interaction=nonstopmode

rem --- Where to put logs (optional)
set LOGDIR=build-logs
if not exist "%LOGDIR%" mkdir "%LOGDIR%" >nul 2>&1

rem --- Helper: run a step and abort on error
:runstep
    rem %* = command
    echo.
    echo ================================
    echo   RUN: %*
    echo ================================
    %*
    if errorlevel 1 (
        echo.
        echo [ERROR] Step failed: %*
        echo Aborting.
        popd >nul 2>&1
        exit /b 1
    )
    goto :eof

rem --- Dispatch on target
set TARGET=%1
if "%TARGET%"=="" set TARGET=all

if /I "%TARGET%"=="install" goto :install
if /I "%TARGET%"=="doc"     goto :doc
if /I "%TARGET%"=="example" goto :example
if /I "%TARGET%"=="clean"   goto :clean
if /I "%TARGET%"=="all"     goto :all

echo Unknown target "%TARGET%".
echo Usage: build.bat [all^|install^|doc^|example^|clean]
popd >nul 2>&1
exit /b 1

:install
    echo.
    echo === [INSTALL] Generate files from %DOC%.ins ===
    if not exist "%DOC%.ins" (
        echo [ERROR] %DOC%.ins not found.
        popd >nul 2>&1
        exit /b 1
    )
    call :runstep "%PDFLATEX%" %PDFLATEX_FLAGS% "%DOC%.ins"
    echo.
    echo [OK] Installation files generated.
    popd >nul 2>&1
    exit /b 0

:doc
    echo.
    echo === [DOC] Build manual from %DOC%.dtx ===
    if not exist "%DOC%.dtx" (
        echo [ERROR] %DOC%.dtx not found.
        popd >nul 2>&1
        exit /b 1
    )
    rem 1st LaTeX (creates .bcf)
    call :runstep "%PDFLATEX%" %PDFLATEX_FLAGS% "%DOC%.dtx" 1^> "%LOGDIR%\%DOC%-1.log" 2^>^&1

    rem Index/glossary (optional; use only if your driver produces .glo/.idx)
    if exist "%DOC%.glo" call :runstep "%MAKEINDEX%" -s gglo.ist -o "%DOC%.gls" "%DOC%.glo"
    if exist "%DOC%.idx" call :runstep "%MAKEINDEX%" -s gind.ist -o "%DOC%.ind" "%DOC%.idx"

    rem Biber
    if exist "%DOC%.bcf" (
        call :runstep "%BIBER%" "%DOC%"
    ) else (
        echo [WARN] %DOC%.bcf not found; skipping biber (biblatex likely not loaded in driver).
    )

    rem 2nd and 3rd LaTeX passes
    call :runstep "%PDFLATEX%" %PDFLATEX_FLAGS% "%DOC%.dtx" 1^> "%LOGDIR%\%DOC%-2.log" 2^>^&1
    call :runstep "%PDFLATEX%" %PDFLATEX_FLAGS% "%DOC%.dtx" 1^> "%LOGDIR%\%DOC%-3.log" 2^>^&1

    echo.
    if exist "%DOC%.pdf" (
        echo [OK] Manual built: %DOC%.pdf
    ) else (
        echo [ERROR] Manual PDF was not produced.
        popd >nul 2>&1
        exit /b 1
    )
    popd >nul 2>&1
    exit /b 0

:example
    echo.
    echo === [EXAMPLE] Build %EXAMPLE%.tex ===
    if not exist "%EXAMPLE%.tex" (
        echo [ERROR] %EXAMPLE%.tex not found.
        popd >nul 2>&1
        exit /b 1
    )

    rem 1st LaTeX (creates .bcf, .aux etc.)
    call :runstep "%PDFLATEX%" %PDFLATEX_FLAGS% "%EXAMPLE%.tex" 1^> "%LOGDIR%\%EXAMPLE%-1.log" 2^>^&1

    rem Optional: custom makeindex runs if your example produces special indices
    if exist "%EXAMPLE%.abx" call :runstep "%MAKEINDEX%" -s coppe.ist -o "%EXAMPLE%.lab" "%EXAMPLE%.abx"
    if exist "%EXAMPLE%.syx" call :runstep "%MAKEINDEX%" -s coppe.ist -o "%EXAMPLE%.los" "%EXAMPLE%.syx"

    rem Biber
    if exist "%EXAMPLE%.bcf" (
        call :runstep "%BIBER%" "%EXAMPLE%"
    ) else (
        echo [WARN] %EXAMPLE%.bcf not found; skipping biber (no biblatex?).
    )

    rem 2nd and 3rd LaTeX passes
    call :runstep "%PDFLATEX%" %PDFLATEX_FLAGS% "%EXAMPLE%.tex" 1^> "%LOGDIR%\%EXAMPLE%-2.log" 2^>^&1
    call :runstep "%PDFLATEX%" %PDFLATEX_FLAGS% "%EXAMPLE%.tex" 1^> "%LOGDIR%\%EXAMPLE%-3.log" 2^>^&1

    echo.
    if exist "%EXAMPLE%.pdf" (
        echo [OK] Example built: %EXAMPLE%.pdf
    ) else (
        echo [ERROR] Example PDF was not produced.
        popd >nul 2>&1
        exit /b 1
    )
    popd >nul 2>&1
    exit /b 0

:all
    echo.
    echo === [ALL] install -> doc -> example ===
    call :install
    if errorlevel 1 exit /b 1
    call :doc
    if errorlevel 1 exit /b 1
    call :example
    if errorlevel 1 exit /b 1
    echo.
    echo [OK] All targets completed.
    popd >nul 2>&1
    exit /b 0

:clean
    echo.
    echo === [CLEAN] Removing aux files ===
    for %%F in (aux bcf bbl blg idx ind ilg glo gls ist lof log lot out run.xml toc synctex.gz
                lab los abx syx fls fdb_latexmk) do (
        del /q "%DOC%.%%F" 2>nul
        del /q "%EXAMPLE%.%%F" 2>nul
    )
    echo [OK] Clean done.
    popd >nul 2>&1
    exit /b 0
