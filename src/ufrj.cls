%%
%% This is file `ufrj.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% ufrj.dtx  (with options: `class')
%% 
%% This is the `ufrj' document class used for composition of LaTeX
%% monographs (master's dissertations, PhD theses and qualifying exams)
%% satisfying the requirements of the Federal University of Rio de
%% Janeiro (UFRJ), specialized for each academic unit by a unit style.
%% 
%% Copyright (C) 2008-2026 Vicente Helano F. Batista, George O. Ainsworth Jr.,
%% Geraldo Xexéo and Eduardo Mangeli.
%% 
%% This program is free software; you can redistribute it and/or modify
%% it under the terms of the GNU General Public License version 3 as
%% published by the Free Software Foundation.
%% 
%% This program is distributed in the hope that it will be useful,
%% but WITHOUT ANY WARRANTY; without even the implied warranty of
%% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
%% GNU General Public License version 3 for more details.
%% 
%% You should have received a copy of the GNU General Public License
%% version 3 along with this package (see the COPYING.txt file).
%% If not, see <http://www.gnu.org/licenses/>.
%% 
%% Author(s): Vicente Helano F. Batista
%%            George O. Ainsworth Jr.
%%            Geraldo Xexéo
%%            Eduardo Mangeli
%% 
\def\filename{ufrj.dtx}
\def\fileversion{v5.0}
\def\filedate{2026/09/15}
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{ufrj}[\filedate\ \fileversion\ UFRJ Dissertations and Theses]
\let\ufrj@version\fileversion
\let\ufrj@date\filedate
\edef\ufrj@docmonth{\the\month}
\edef\ufrj@docyear{\the\year}
\LoadClass[12pt,a4paper,oneside]{book}
\RequirePackage{hyphenat}
\RequirePackage{lastpage}
\RequirePackage{ifthen}
\RequirePackage{graphicx}
\graphicspath{{./}{logos/}}
\newcommand\ufrj@logo[2][2cm]{%
  \IfFileExists{logos/#2.pdf}
    {\includegraphics[height=#1]{logos/#2}}
    {\IfFileExists{#2.pdf}
      {\includegraphics[height=#1]{#2}}
      {\ClassError{ufrj}{Logotipo `#2.pdf' nao encontrado}%
        {Ele vem junto com a classe ou com o estilo da unidade. Procurei\MessageBreak
         em logos/#2.pdf e em #2.pdf, e nao achei em nenhum dos dois.\MessageBreak
         Copie a pasta logos/ para junto do seu trabalho, ou ponha\MessageBreak
         #2.pdf ao lado do ufrj.cls na arvore do TeX. Os logotipos\MessageBreak
         estao em dist/logos/ no repositorio.}%
       \framebox[3cm][c]{\rule{0pt}{#1}\ttfamily #2?}}}}
\RequirePackage{tabularx}
\RequirePackage{booktabs}      % regras de tabela profissionais (toprule/midrule/bottomrule)
\RequirePackage{longtable}     % tabelas que quebram entre páginas
\RequirePackage{etoolbox}
\RequirePackage{ltxcmds}
\RequirePackage{hologo}        % TeX-family logos: \hologo{TeX}, \hologo{LaTeX}, ...
\def\TeX{\hologo{TeX}}
\def\LaTeX{\hologo{LaTeX}}
\def\LaTeXe{\hologo{LaTeXe}}
\def\BibTeX{\hologo{BibTeX}}
\def\pdfLaTeX{\hologo{pdfLaTeX}}
\def\pdfTeX{\hologo{pdfTeX}}
\def\LuaLaTeX{\hologo{LuaLaTeX}}
\def\XeLaTeX{\hologo{XeLaTeX}}
\def\MiKTeX{\hologo{MiKTeX}}
\RequirePackage{iftex}
\ifPDFTeX
  \RequirePackage[utf8]{inputenc}
\fi
\RequirePackage{lmodern}
\ifPDFTeX
  \RequirePackage[T1]{fontenc}
\fi
\begingroup
  \fontencoding{\encodingdefault}\fontfamily{lmss}\selectfont
  \fontfamily{lmtt}\selectfont
\endgroup
\ifPDFTeX
  \DeclareFontShape{T1}{lmss}{m}{it}
    {<-8.5> ec-lmsso8 <8.5-9.5> ec-lmsso9 <9.5-11> ec-lmsso10
     <11-15.5> ec-lmsso12 <15.5-> ec-lmsso17}{}
  \DeclareFontShape{T1}{lmss}{bx}{it}{<-> ec-lmssbo10}{}
  \DeclareFontShape{T1}{lmss}{b}{n}{<-> ec-lmssbx10}{}
  \DeclareFontShape{T1}{lmss}{b}{sl}{<-> ec-lmssbo10}{}
  \DeclareFontShape{T1}{lmss}{b}{it}{<-> ec-lmssbo10}{}
  \DeclareFontShape{T1}{lmss}{sbc}{it}{<-> ec-lmssdo10}{}
  \DeclareFontShape{T1}{lmtt}{bx}{n}{<-> ec-lmtk10}{}
  \DeclareFontShape{T1}{lmtt}{bx}{sl}{<-> ec-lmtko10}{}
  \DeclareFontShape{T1}{lmtt}{bx}{it}{<-> ec-lmtko10}{}
  \DeclareFontShape{T1}{lmtt}{b}{it}{<-> ec-lmtko10}{}
\else
  \DeclareFontShape{TU}{lmss}{m}{it}
    {<-8.5> \UnicodeFontFile{lmsans8-oblique}{\UnicodeFontTeXLigatures}
     <8.5-9.5> \UnicodeFontFile{lmsans9-oblique}{\UnicodeFontTeXLigatures}
     <9.5-11> \UnicodeFontFile{lmsans10-oblique}{\UnicodeFontTeXLigatures}
     <11-15.5> \UnicodeFontFile{lmsans12-oblique}{\UnicodeFontTeXLigatures}
     <15.5-> \UnicodeFontFile{lmsans17-oblique}{\UnicodeFontTeXLigatures}}{}
  \DeclareFontShape{TU}{lmss}{bx}{it}
    {<-> \UnicodeFontFile{lmsans10-boldoblique}{\UnicodeFontTeXLigatures}}{}
  \DeclareFontShape{TU}{lmss}{b}{n}
    {<-> \UnicodeFontFile{lmsans10-bold}{\UnicodeFontTeXLigatures}}{}
  \DeclareFontShape{TU}{lmss}{b}{sl}
    {<-> \UnicodeFontFile{lmsans10-boldoblique}{\UnicodeFontTeXLigatures}}{}
  \DeclareFontShape{TU}{lmss}{b}{it}
    {<-> \UnicodeFontFile{lmsans10-boldoblique}{\UnicodeFontTeXLigatures}}{}
  \DeclareFontShape{TU}{lmss}{sbc}{it}
    {<-> \UnicodeFontFile{lmsansdemicond10-oblique}{\UnicodeFontTeXLigatures}}{}
  \DeclareFontShape{TU}{lmtt}{bx}{n}{<-> \UnicodeFontFile{lmmonolt10-bold}{}}{}
  \DeclareFontShape{TU}{lmtt}{bx}{sl}{<-> \UnicodeFontFile{lmmonolt10-boldoblique}{}}{}
  \DeclareFontShape{TU}{lmtt}{bx}{it}{<-> \UnicodeFontFile{lmmonolt10-boldoblique}{}}{}
  \DeclareFontShape{TU}{lmtt}{b}{it}{<-> \UnicodeFontFile{lmmonolt10-boldoblique}{}}{}
\fi
\RequirePackage{amsmath}
\RequirePackage[a4paper,headheight=15pt,headsep=16.87pt,%
top=3cm,bottom=2cm,left=3cm,right=2cm]{geometry}
\setlength\emergencystretch{3em}
\RequirePackage{indentfirst}
\RequirePackage{titlesec}
\newif\if@ufrjappendix \@ufrjappendixfalse
\titleformat{\chapter}[hang]
  {\normalfont\normalsize\bfseries}
  {\if@ufrjappendix\MakeUppercase{\appendixname}\ \thechapter\ \textemdash\else\thechapter\fi}
  {1ex}{\MakeUppercase}
\titlespacing*{\chapter}{0pt}{10pt}{1.5\baselineskip}
\newcommand\ufrj@appendixheadings{%
  \titleformat{\chapter}[block]
    {\normalfont\normalsize\bfseries\filcenter}
    {\MakeUppercase{\appendixname}\ \thechapter\ \textemdash}
    {1ex}{\MakeUppercase}%
  \titlespacing*{\chapter}{0pt}{10pt}{1.5\baselineskip}}
\let\ufrj@orig@appendix\appendix
\renewcommand\appendix{%
  \ufrj@orig@appendix\@ufrjappendixtrue\ufrj@appendixheadings}
\newif\if@ufrjannex \@ufrjannexfalse
\newcommand\ufrj@tocapp[1]{%
  \MakeUppercase{\ufrjstring{appendix}}%
  \nobreakspace#1\nobreakspace\textemdash\nobreakspace}
\newcommand\ufrj@tocanx[1]{%
  \MakeUppercase{\ufrjstring{annex}}%
  \nobreakspace#1\nobreakspace\textemdash\nobreakspace}
\def\@chapter[#1]#2{%
  \ifnum \c@secnumdepth >\m@ne
    \if@mainmatter
      \refstepcounter{chapter}%
      \typeout{\@chapapp\space\thechapter.}%
      \if@ufrjappendix
        \if@ufrjannex
          \addcontentsline{toc}{chapter}{\protect\numberline{}\protect\ufrj@tocanx{\thechapter}#1}%
        \else
          \addcontentsline{toc}{chapter}{\protect\numberline{}\protect\ufrj@tocapp{\thechapter}#1}%
        \fi
      \else
        \addcontentsline{toc}{chapter}{\protect\numberline{\thechapter}#1}%
      \fi
    \else
      \addcontentsline{toc}{chapter}{\protect\numberline{}#1}%
    \fi
  \else
    \addcontentsline{toc}{chapter}{\protect\numberline{}#1}%
  \fi
  \chaptermark{#1}%
  \addtocontents{lof}{\protect\addvspace{10\p@}}%
  \addtocontents{lot}{\protect\addvspace{10\p@}}%
  \if@twocolumn
    \@topnewpage[\@makechapterhead{#2}]%
  \else
    \@makechapterhead{#2}%
    \@afterheading
  \fi}
\titleformat{name=\chapter,numberless}[hang]
  {\normalfont\normalsize\bfseries\filcenter}{}{0pt}{\MakeUppercase}
\titlespacing*{name=\chapter,numberless}{0pt}{10pt}{1.5\baselineskip}
\titleformat{\section}
  {\normalfont\normalsize}{\thesection}{1ex}{\MakeUppercase}
\titleformat{\subsection}
  {\normalfont\bfseries}{\thesubsection}{1ex}{}
\titleformat{\subsubsection}
  {\normalfont\bfseries\itshape}{\thesubsubsection}{1ex}{}
\titlespacing*{\section}{0pt}{\baselineskip}{\baselineskip}
\titlespacing*{\subsection}{0pt}{\baselineskip}{\baselineskip}
\titlespacing*{\subsubsection}{0pt}{\baselineskip}{\baselineskip}
\titleformat{\paragraph}[hang]
  {\normalfont\itshape}{\theparagraph}{1ex}{}
\titlespacing*{\paragraph}{0pt}{\baselineskip}{\baselineskip}
\setcounter{secnumdepth}{4}
\setcounter{tocdepth}{4}
\newlength\ufrj@tocnumwidth
\newlength\ufrj@tocnummax
\newlength\ufrj@tocnumsep
\setlength\ufrj@tocnumsep{0.5em}
\setlength\ufrj@tocnumwidth{1.75cm}
\setlength\ufrj@tocnummax{\z@}
\protected\def\ufrj@tocnumberline#1{%
  \settowidth\@tempdima{#1}%
  \ifdim\@tempdima>\ufrj@tocnummax \global\ufrj@tocnummax\@tempdima \fi
  \hb@xt@\ufrj@tocnumwidth{#1\hfil}}
\AtBeginDocument{%
  \@ifundefined{ufrj@tocnumsaved}{}{%
    \setlength\@tempdima{\ufrj@tocnumsaved}%
    \addtolength\@tempdima\ufrj@tocnumsep
    \ifdim\@tempdima>\ufrj@tocnumwidth
      \setlength\ufrj@tocnumwidth\@tempdima
    \fi}}
\AtEndDocument{%
  \ifdim\ufrj@tocnummax>\z@
    \if@filesw
      \immediate\write\@auxout{\string\gdef\string\ufrj@tocnumsaved
        {\the\ufrj@tocnummax}}%
    \fi
    \setlength\@tempdima\ufrj@tocnummax
    \addtolength\@tempdima\ufrj@tocnumsep
    \ifdim\@tempdima>\ufrj@tocnumwidth
      \ClassWarning{ufrj}{A coluna do sumario cresceu; rode LaTeX de novo}%
    \fi
  \fi}
\newcommand\ufrj@tocline[4]{%
  \ifnum #1>\c@tocdepth\else
    \vskip\z@\@plus.2\p@
    {\leftskip\z@ \rightskip\@tocrmarg \parfillskip-\rightskip
     \parindent\z@ \interlinepenalty\@M
     \leavevmode
     #2%
     \advance\leftskip\ufrj@tocnumwidth
     \null\nobreak\hskip-\leftskip
     #3\nobreak
     \leaders\hbox{$\m@th\mkern\@dotsep mu\hbox{.}\mkern\@dotsep mu$}%
       \hfill\nobreak
     \hb@xt@\@pnumwidth{\hss #4}\par}%
  \fi}
\renewcommand\@dotsep{2}
\renewcommand*\l@chapter[2]{%
  \addpenalty{-\@highpenalty}%
  \ufrj@tocline{0}{\bfseries}{\MakeUppercase{#1}}{#2}%
  \penalty\@highpenalty}
\renewcommand*\l@section[2]{%
  \ufrj@tocline{1}{\normalfont}{\MakeUppercase{#1}}{#2}}
\renewcommand*\l@subsection[2]{%
  \ufrj@tocline{2}{\normalfont\bfseries}{#1}{#2}}
\renewcommand*\l@subsubsection[2]{%
  \ufrj@tocline{3}{\normalfont\bfseries\itshape}{#1}{#2}}
\renewcommand*\l@paragraph[2]{%
  \ufrj@tocline{4}{\normalfont\itshape}{#1}{#2}}
\RequirePackage{caption}
\DeclareCaptionLabelSeparator{emdash}{\space\textemdash\space}
\captionsetup{font=footnotesize,labelsep=emdash,justification=centering}
\RequirePackage{subcaption}
\RequirePackage{float}
\floatstyle{plaintop}
\restylefloat{figure}
\restylefloat{table}
\providecommand{\quadroname}{\ufrjstring{frame}}
\providecommand{\listquadroname}{\ufrjstring{listframe}}
\newfloat{quadro}{htbp}{loq}[chapter]
\floatname{quadro}{\quadroname}
\providecommand{\quadroautorefname}{\quadroname}
\let\l@quadro\l@figure
\newcommand\listofquadros{%
  \chapter*{\listquadroname}%
  \ufrj@listtoc{\listquadroname}%
  \@mkboth{\MakeUppercase\listquadroname}{\MakeUppercase\listquadroname}%
  \@starttoc{loq}}
\newcommand{\cpsourcename}{\ufrjstring{source}}
\newcommand{\cpsource}[1]{%
  \par\addvspace{\smallskipamount}%
  {\footnotesize\singlespacing\centering\cpsourcename: #1\par}}
\let\cpfonte\cpsource
\@ifundefined{source}{\let\source\cpsource}{}%
\@ifundefined{fonte}{\let\fonte\cpsource}{}%
\newcommand{\newufrjfloat}[3]{%
  \floatstyle{plaintop}\newfloat{#1}{htbp}{lo#1}[chapter]%
  \floatname{#1}{#2}%
  \expandafter\let\csname l@#1\endcsname\l@figure
  \expandafter\def\csname ufrj@listname@lo#1\endcsname{#2}%
  \AtBeginDocument{\expandafter\let\csname l@#1\endcsname\l@figure}%
  \expandafter\providecommand\csname #1autorefname\endcsname{#2}%
  \expandafter\newcommand\csname listof#1s\endcsname{%
    \chapter*{#3}\ufrj@listtoc{#3}%
    \@mkboth{\MakeUppercase{#3}}{\MakeUppercase{#3}}%
    \@starttoc{lo#1}}}
\let\ufrj@orig@footnotetext\@footnotetext
\long\def\@footnotetext#1{\ufrj@orig@footnotetext{\singlespacing#1}}
\renewcommand\footnoterule{\kern-3\p@\hrule\@width 5cm\kern 2.6\p@}
\renewcommand\@makefntext[1]{%
  \setbox\@tempboxa\hbox{\@makefnmark}%
  \noindent\hangindent\wd\@tempboxa\hangafter\@ne
  \box\@tempboxa #1}
\interfootnotelinepenalty=\@M
\RequirePackage{enumitem}
\newlist{alineas}{enumerate}{2}
\setlist[alineas,1]{label=\alph*),leftmargin=1.8em,itemsep=0pt}
\setlist[alineas,2]{label=--,leftmargin=1.8em,itemsep=0pt}
\newcommand\ufrj@checkwrites[1]{%
  \ifdefined\directlua\else
    \if@ufrjmorewrites\else
      \@ifundefined{tf@#1}{%
        \ifnum\count17>14
          \ClassError{ufrj}{Acabaram os 16 fluxos de escrita do TeX}{%
            Este trabalho pede mais listas do que o pdfTeX consegue manter
            abertas ao mesmo tempo.\MessageBreak
            Tres saidas, nesta ordem de preferencia:\MessageBreak
            (1) compile com lualatex, que tem 128 fluxos;\MessageBreak
            (2) tire a opcao `semmorewrites', se a passou (ou passe
            `morewrites');\MessageBreak
            (3) remova uma lista que o trabalho nao usa.\MessageBreak
            A lista que faltou agora foi a de extensao `#1', mas o problema
            nao e dela: e a soma de todas.}%
        \fi}{}%
    \fi
  \fi}
\newcommand\ufrj@listnumberline[1]{%
  \ufrj@listname\nobreakspace#1\nobreakspace\textemdash\space}
\def\ufrj@listname@lof{\figurename}
\def\ufrj@listname@lot{\tablename}
\def\ufrj@listname@loq{\quadroname}
\def\ufrj@listname@lol{\lstlistingname}
\def\ufrj@listname@loa{\algorithmcfname}
\newcommand\ufrj@wrapstarttoc{%
  \let\ufrj@orig@starttoc\@starttoc
  \def\@starttoc##1{%
    \ufrj@checkwrites{##1}%
    \begingroup
      \def\ufrj@@ext{##1}\def\ufrj@@toc{toc}%
      \ifx\ufrj@@ext\ufrj@@toc
        \let\numberline\ufrj@tocnumberline
      \else
        \@ifundefined{ufrj@listname@##1}{}{%
          \edef\ufrj@listname{\expandafter\noexpand
            \csname ufrj@listname@##1\endcsname}%
          \let\numberline\ufrj@listnumberline}%
      \fi
      \ufrj@orig@starttoc{##1}%
    \endgroup}}
\AtBeginDocument{\ufrj@wrapstarttoc}
\AtBeginDocument{%
  \renewcommand*\l@figure{\@dottedtocline{1}{0pt}{0pt}}%
  \let\l@table\l@figure
  \let\l@quadro\l@figure
  \let\l@lstlisting\l@figure
  \let\l@algocf\l@figure}
\RequirePackage{fancyhdr}
\newcommand\ufrj@listtoc[1]{%
  \if@ufrjlistastoc\addcontentsline{toc}{chapter}{\protect\numberline{}#1}\fi}
\newif\if@ufrjglosspre \@ufrjglossprefalse
\newcommand\ufrj@folio{{\footnotesize\thepage}}
\newcommand\ufrj@foliohead{%
  \if@ufrjtwoside
    \fancyhead[RO,LE]{\ufrj@folio}%
  \else
    \fancyhead[R]{\ufrj@folio}%
  \fi}
\fancypagestyle{ufrj}{\fancyhf{}\ufrj@foliohead
  \renewcommand{\headrulewidth}{0pt}}
\renewcommand{\cleardoublepage}{%
  \clearpage
  \if@twoside
    \ifodd\c@page\else
      \hbox{}\thispagestyle{empty}\newpage
      \if@twocolumn\hbox{}\newpage\fi
    \fi
  \fi}
\def\CoppeTeX{{\rmfamily C\kern-.05em{\scshape o\kern-.025em p\kern-.025em
p\kern-.025em e}}\kern-.08em
T\kern-.1667em\lower.5ex\hbox{E}\kern-.125emX\spacefactor1000}
\newboolean{maledoc}
\setboolean{maledoc}{false}
\newif\if@ufrjexame \@ufrjexamefalse
\def\ufrj@mainlang{brazilian}
\def\ufrj@foreignlang{english}
\DeclareOption{brazilian}{%
  \def\ufrj@mainlang{brazilian}\def\ufrj@foreignlang{english}}
\DeclareOption{english}{%
  \def\ufrj@mainlang{english}\def\ufrj@foreignlang{brazilian}}
\DeclareOption{spanish}{%
  \def\ufrj@mainlang{spanish}\def\ufrj@foreignlang{english}}
\DeclareOption{french}{%
  \def\ufrj@mainlang{french}\def\ufrj@foreignlang{english}}
\DeclareOption{italian}{%
  \def\ufrj@mainlang{italian}\def\ufrj@foreignlang{english}}
\DeclareOption{msc}{%
  \def\ufrj@doctypekey{msc}\def\ufrj@degkey{msc}
  \newcommand{\@degree}{M.Sc.}
  \newcommand{\@degreename}{Mestrado}
  \newcommand{\local@degname}{Mestre}
  \newcommand{\foreign@degname}{Master}
  \newcommand\local@doctype{Dissertação}
  \newcommand\foreign@doctype{Dissertation}
}
\DeclareOption{dscexam}{%
  \def\ufrj@doctypekey{exam}\def\ufrj@degkey{dsc}
  \newcommand{\@degree}{D.Sc.}
  \newcommand{\@degreename}{Doutorado}
  \newcommand{\local@degname}{Doutor}
  \newcommand{\foreign@degname}{Doctor}
  \setboolean{maledoc}{true}\@ufrjexametrue
  \newcommand\local@doctype{Exame de Qualificação}
  \newcommand\foreign@doctype{Qualifying Exam}
}
\DeclareOption{mscexam}{%
  \def\ufrj@doctypekey{exam}\def\ufrj@degkey{msc}
 \newcommand{\@degree}{M.Sc.}
  \newcommand{\@degreename}{Mestrado}
  \newcommand{\local@degname}{Mestre}
  \newcommand{\foreign@degname}{Master}
  \setboolean{maledoc}{true}\@ufrjexametrue
  \newcommand\local@doctype{Exame de Qualificação}
  \newcommand\foreign@doctype{Qualifying Exam}
}
\DeclareOption{mscsem}{%
  \def\ufrj@doctypekey{sem}\def\ufrj@degkey{msc}
  \newcommand{\@degree}{M.Sc.}
  \newcommand{\@degreename}{Mestrado}
  \newcommand{\local@degname}{Mestre}
  \newcommand{\foreign@degname}{Master}
  \setboolean{maledoc}{true}\@ufrjexametrue
  \newcommand\local@doctype{Seminário}
  \newcommand\foreign@doctype{Seminar}
}
\DeclareOption{dsc}{%
  \def\ufrj@doctypekey{dsc}\def\ufrj@degkey{dsc}
  \newcommand{\@degree}{D.Sc.}
  \newcommand{\@degreename}{Doutorado}
  \newcommand{\local@degname}{Doutor}
  \newcommand{\foreign@degname}{Doctor}
  \newcommand\local@doctype{Tese}
  \newcommand\foreign@doctype{Thesis}
}
\newif\if@ufrjnumeric\@ufrjnumericfalse
\DeclareOption{numbers}{\@ufrjnumerictrue}
\newif\if@ufrjroman\@ufrjromanfalse
\DeclareOption{numeraisromanos}{\@ufrjromantrue}
\newif\if@ufrjdoublespace\@ufrjdoublespacefalse
\DeclareOption{doublespacing}{\@ufrjdoublespacetrue}
\newif\if@ufrjpdfa \@ufrjpdfatrue
\DeclareOption{pdfa}{\@ufrjpdfatrue}
\DeclareOption{sempdfa}{\@ufrjpdfafalse}
\newif\if@ufrjorientexam \@ufrjorientexamtrue
\DeclareOption{orientadorexamina}{\@ufrjorientexamtrue}
\DeclareOption{semorientadornabanca}{\@ufrjorientexamfalse}
\newif\if@ufrjsemlinks \@ufrjsemlinksfalse
\DeclareOption{semlinks}{\@ufrjsemlinkstrue}
\newif\if@ufrjlinksmoldura \@ufrjlinksmoldurafalse
\DeclareOption{linkscommoldura}{\@ufrjlinksmolduratrue}
\newif\if@ufrjlinkscor \@ufrjlinkscorfalse
\DeclareOption{linkscoloridos}{\@ufrjlinkscortrue}
\newif\if@ufrjsetavermelha \@ufrjsetavermelhafalse
\DeclareOption{setavermelha}{\@ufrjsetavermelhatrue}
\DeclareOption{assinaturas}{\ClassWarningNoLine{ufrj}{A opcao `assinaturas'
  nao faz mais nada: a folha de aprovacao nao tem mais linhas de assinatura,
  porque a entrega e digital desde a Resolucao CEPG n. 246/2023}}
\newif\if@ufrjcoadvresumo \@ufrjcoadvresumofalse
\DeclareOption{coorientador}{\@ufrjcoadvresumotrue}
\newif\if@ufrjrefresumo \@ufrjrefresumotrue
\DeclareOption{resumosemreferencia}{\@ufrjrefresumofalse}
\newif\if@ufrjresidpag \@ufrjresidpagtrue
\newif\if@ufrjrestitulo \@ufrjrestitulotrue
\newif\if@ufrjresorient \@ufrjresorienttrue
\newif\if@ufrjlistastoc \@ufrjlistastocfalse
\DeclareOption{listasnosumario}{\@ufrjlistastoctrue}
\newif\if@ufrjarearosto \@ufrjarearostofalse
\DeclareOption{areanafolhaderosto}{\@ufrjarearostotrue}
\newif\if@ufrjsimbalfa \@ufrjsimbalfafalse
\DeclareOption{simbolosalfabeticos}{\@ufrjsimbalfatrue}
\newif\if@ufrjrascunho \@ufrjrascunhofalse
\DeclareOption{rascunhoficha}{\@ufrjrascunhotrue}
\newif\if@ufrjtwoside \@ufrjtwosidefalse
\DeclareOption{twoside}{\@ufrjtwosidetrue}
\DeclareOption{oneside}{\@ufrjtwosidefalse}
\newif\if@ufrjmorewrites \@ufrjmorewritestrue
\newif\if@ufrjmwforced   \@ufrjmwforcedfalse
\DeclareOption{morewrites}{\@ufrjmorewritestrue\@ufrjmwforcedtrue}
\DeclareOption{semmorewrites}{\@ufrjmorewritesfalse}
\newif\if@ufrjmakeindex \@ufrjmakeindextrue
\DeclareOption{semmakeindex}{\@ufrjmakeindexfalse}
\newif\if@ufrjsansserif \@ufrjsansseriftrue
\DeclareOption{semserifa}{\@ufrjsansseriftrue}
\DeclareOption{comserifa}{\@ufrjsansseriffalse}
\ProcessOptions\relax
\@ifundefined{ufrj@doctypekey}{%
  \ClassError{ufrj}{Falta dizer o tipo do trabalho}{%
    A classe ufrj precisa de exatamente uma opcao de tipo: msc, dsc,
    mscexam,\MessageBreak
    dscexam ou mscsem. Escreva, por exemplo,
    \string\documentclass[dsc]\string{ufrj\string}.}%
  \def\ufrj@doctypekey{dsc}\def\ufrj@degkey{dsc}
  \newcommand{\@degree}{??}
  \newcommand{\@degreename}{??}
  \newcommand{\local@degname}{??}
  \newcommand{\foreign@degname}{??}
  \newcommand\local@doctype{??}
  \newcommand\foreign@doctype{??}
}{}
\if@ufrjsansserif
  \renewcommand{\familydefault}{\sfdefault}%
\fi
\if@ufrjmorewrites
  \ifdefined\directlua
    \ClassInfo{ufrj}{morewrites dispensado: o LuaTeX ja tem 128 fluxos}%
    \@ufrjmorewritesfalse
  \else
    \IfFileExists{morewrites.sty}
      {\RequirePackage{morewrites}%
       \morewritessetup{allocate=\the\numexpr 15-\count17\relax}}
      {\if@ufrjmwforced
         \ClassError{ufrj}{Opcao `morewrites' pedida, mas morewrites.sty nao
           esta instalado}{Instale o pacote morewrites, ou compile com lualatex,
           que nao precisa dele.}%
       \else
         \ClassWarningNoLine{ufrj}{O pacote morewrites nao esta instalado.\MessageBreak
           Sem ele o pdfTeX so aguenta 16 fluxos de escrita, e um trabalho\MessageBreak
           com todas as listas passa disso. Se a compilacao parar por falta\MessageBreak
           de fluxo, instale morewrites ou compile com lualatex}%
         \@ufrjmorewritesfalse
       \fi}%
  \fi
\fi
\if@ufrjtwoside
  \@twosidetrue
  \geometry{twoside}%
\fi
\def\ufrj@@brazilianstr{brazilian}
\def\ufrj@@englishstr{english}
\edef\ufrj@babelopts{\ufrj@foreignlang,\ufrj@mainlang}
\@namedef{ufrj@babelextra@spanish}{,es-nosectiondot}
\let\ufrj@babelload\ufrj@babelopts
\@ifundefined{ufrj@babelextra@\ufrj@mainlang}{}{%
  \edef\ufrj@babelload{\ufrj@babelload\@nameuse{ufrj@babelextra@\ufrj@mainlang}}}
\expandafter\RequirePackage\expandafter[\ufrj@babelload]{babel}
\@ifundefined{captionsbrazilian}{}{%
  \addto\captionsbrazilian{\def\seename{ver}\def\alsoname{ver também}}}
\providecommand{\ufrjdefstring}[3]{%
  \expandafter\gdef\csname ufrj@str@#1@#2\endcsname{#3}}
\providecommand{\ufrjstring}[1]{\@nameuse{ufrj@str@\languagename @#1}}
\providecommand{\ufrjmainstring}[1]{\@nameuse{ufrj@str@\ufrj@mainlang @#1}}
\providecommand{\ufrjforeignstring}[1]{\@nameuse{ufrj@str@\ufrj@foreignlang @#1}}
\providecommand{\useufrjlanguage}[1]{%
  \def\ufrj@@cur{#1}%
  \ifx\ufrj@@cur\ufrj@@brazilianstr\else
  \ifx\ufrj@@cur\ufrj@@englishstr\else
    \InputIfFileExists{ufrj-lang-#1.def}{}
      {\ClassWarning{ufrj}{Language pack ufrj-lang-#1.def not found}}%
  \fi\fi}
\providecommand{\titlein}[2]{%
  \expandafter\gdef\csname ufrj@title@#1\endcsname{#2}}
\ufrjdefstring{brazilian}{appendix}{Apêndice}
\ufrjdefstring{english}  {appendix}{Appendix}
\ufrjdefstring{brazilian}{annex}   {Anexo}
\ufrjdefstring{english}  {annex}   {Annex}
\ufrjdefstring{brazilian}{frame}        {Quadro}
\ufrjdefstring{english}  {frame}        {Frame}
\ufrjdefstring{brazilian}{listframe}    {Lista de Quadros}
\ufrjdefstring{english}  {listframe}    {List of Frames}
\ufrjdefstring{brazilian}{source}       {Fonte}
\ufrjdefstring{english}  {source}       {Source}
\ufrjdefstring{brazilian}{program}      {Programa}
\ufrjdefstring{english}  {program}      {Program}
\ufrjdefstring{brazilian}{listprogram}  {Lista de Programas}
\ufrjdefstring{english}  {listprogram}  {List of Programs}
\ufrjdefstring{brazilian}{references}   {Referências}
\ufrjdefstring{english}  {references}   {References}
\ufrjdefstring{brazilian}{in:}          {em}
\ufrjdefstring{english}  {in:}          {in}
\ufrjdefstring{brazilian}{art}          {Ilustração}
\ufrjdefstring{english}  {art}          {Art}
\ufrjdefstring{brazilian}{platform}     {Plataforma}
\ufrjdefstring{english}  {platform}     {Platform}
\ufrjdefstring{brazilian}{directedby}   {Direção de}
\ufrjdefstring{english}  {directedby}   {Directed by}
\ufrjdefstring{brazilian}{producedby}   {Produção de}
\ufrjdefstring{english}  {producedby}   {Produced by}
\ufrjdefstring{brazilian}{listabbreviation}{Lista de Abreviaturas e Siglas}
\ufrjdefstring{english}  {listabbreviation}{List of Abbreviations and Acronyms}
\ufrjdefstring{brazilian}{listabbreviationonly}{Lista de Abreviaturas}
\ufrjdefstring{english}  {listabbreviationonly}{List of Abbreviations}
\ufrjdefstring{brazilian}{listsigla}       {Lista de Siglas}
\ufrjdefstring{english}  {listsigla}       {List of Acronyms}
\ufrjdefstring{brazilian}{listsymbol}      {Lista de Símbolos}
\ufrjdefstring{english}  {listsymbol}      {List of Symbols}
\ufrjdefstring{brazilian}{glossary}        {Glossário}
\ufrjdefstring{english}  {glossary}        {Glossary}
\ufrjdefstring{brazilian}{abstractname}     {Resumo}
\ufrjdefstring{english}  {abstractname}     {Abstract}
\ufrjdefstring{brazilian}{abstractofmale}   {do}
\ufrjdefstring{brazilian}{abstractoffemale} {da}
\ufrjdefstring{english}  {abstractofmale}   {of}
\ufrjdefstring{english}  {abstractoffemale} {of}
\ufrjdefstring{brazilian}{presentedmale}    {apresentado}
\ufrjdefstring{brazilian}{presentedfemale}  {apresentada}
\ufrjdefstring{english}  {presentedmale}    {presented}
\ufrjdefstring{english}  {presentedfemale}  {presented}
\ufrjdefstring{brazilian}{tounit}           {à UFRJ}
\ufrjdefstring{english}  {tounit}           {to UFRJ}
\ufrjdefstring{brazilian}{abstracttail}{como parte dos
  requisitos necessários para a obtenção do grau de}
\ufrjdefstring{english}{abstracttail}{as a partial fulfillment
  of the requirements for the degree of}
\ufrjdefstring{brazilian}{doctypemsc}  {Dissertação}
\ufrjdefstring{english}  {doctypemsc}  {Dissertation}
\ufrjdefstring{brazilian}{doctypedsc}  {Tese}
\ufrjdefstring{english}  {doctypedsc}  {Thesis}
\ufrjdefstring{brazilian}{doctypeexam} {Exame de Qualificação}
\ufrjdefstring{english}  {doctypeexam} {Qualifying Exam}
\ufrjdefstring{brazilian}{doctypesem}  {Seminário}
\ufrjdefstring{english}  {doctypesem}  {Seminar}
\ufrjdefstring{brazilian}{degnamemsc}  {Mestre}
\ufrjdefstring{english}  {degnamemsc}  {Master}
\ufrjdefstring{brazilian}{degnamedsc}  {Doutor}
\ufrjdefstring{english}  {degnamedsc}  {Doctor}
\ufrjdefstring{brazilian}{advisor}      {Orientador}
\ufrjdefstring{english}  {advisor}      {Advisor}
\ufrjdefstring{brazilian}{advisors}     {Orientadores}
\ufrjdefstring{english}  {advisors}     {Advisors}
\ufrjdefstring{brazilian}{dept}         {Programa}
\ufrjdefstring{english}  {dept}         {Department}
\ufrjdefstring{brazilian}{approvedmale}  {Aprovado por}
\ufrjdefstring{brazilian}{approvedfemale}{Aprovada por}
\ufrjdefstring{brazilian}{approvedonmale}  {Aprovado em}
\ufrjdefstring{brazilian}{approvedonfemale}{Aprovada em}
\ufrjdefstring{brazilian}{keywordsname} {Palavras-chave}
\ufrjdefstring{brazilian}{volumename} {Volume}
\ufrjdefstring{brazilian}{coadvisor}  {Coorientador}
\ufrjdefstring{brazilian}{coadvisors} {Coorientadores}
\ufrjdefstring{brazilian}{ofname}     {de}
\ufrjdefstring{brazilian}{researchline}{Linha de pesquisa}
\ufrjdefstring{brazilian}{tbddate}   {a ser determinada}
\ufrjdefstring{english}  {approvedmale}  {Approved by}
\ufrjdefstring{english}  {approvedfemale}{Approved by}
\ufrjdefstring{english}  {approvedonmale}  {Approved on}
\ufrjdefstring{english}  {approvedonfemale}{Approved on}
\ufrjdefstring{english}  {keywordsname} {Keywords}
\ufrjdefstring{english}  {volumename} {Volume}
\ufrjdefstring{english}  {coadvisor}  {Co-advisor}
\ufrjdefstring{english}  {coadvisors} {Co-advisors}
\ufrjdefstring{english}  {ofname}     {of}
\ufrjdefstring{english}  {researchline}{Research line}
\ufrjdefstring{english}  {tbddate}    {to be determined}
\ufrjdefstring{brazilian}{monthname1} {Janeiro}
\ufrjdefstring{brazilian}{monthname2} {Fevereiro}
\ufrjdefstring{brazilian}{monthname3} {Março}
\ufrjdefstring{brazilian}{monthname4} {Abril}
\ufrjdefstring{brazilian}{monthname5} {Maio}
\ufrjdefstring{brazilian}{monthname6} {Junho}
\ufrjdefstring{brazilian}{monthname7} {Julho}
\ufrjdefstring{brazilian}{monthname8} {Agosto}
\ufrjdefstring{brazilian}{monthname9} {Setembro}
\ufrjdefstring{brazilian}{monthname10}{Outubro}
\ufrjdefstring{brazilian}{monthname11}{Novembro}
\ufrjdefstring{brazilian}{monthname12}{Dezembro}
\ufrjdefstring{english}{monthname1} {January}
\ufrjdefstring{english}{monthname2} {February}
\ufrjdefstring{english}{monthname3} {March}
\ufrjdefstring{english}{monthname4} {April}
\ufrjdefstring{english}{monthname5} {May}
\ufrjdefstring{english}{monthname6} {June}
\ufrjdefstring{english}{monthname7} {July}
\ufrjdefstring{english}{monthname8} {August}
\ufrjdefstring{english}{monthname9} {September}
\ufrjdefstring{english}{monthname10}{October}
\ufrjdefstring{english}{monthname11}{November}
\ufrjdefstring{english}{monthname12}{December}
\ufrjdefstring{brazilian}{algorithm2eopt}{portuguese}
\ufrjdefstring{english}  {algorithm2eopt}{}
\ufrjdefstring{brazilian}{babelname}{brazilian}
\ufrjdefstring{english}  {babelname}{english}
\@for\ufrj@@lang:=\ufrj@babelopts\do{%
  \edef\ufrj@@cur{\ufrj@@lang}%
  \ifx\ufrj@@cur\ufrj@@brazilianstr\else
  \ifx\ufrj@@cur\ufrj@@englishstr\else
    \InputIfFileExists{ufrj-lang-\ufrj@@cur.def}
      {\ClassInfo{ufrj}{Loaded language pack ufrj-lang-\ufrj@@cur.def}}
      {\ClassError{ufrj}
        {Missing language pack 'ufrj-lang-\ufrj@@cur.def'.}
        {Install it next to ufrj.cls, or pick a built-in language.}}%
  \fi\fi}
\RequirePackage{csquotes}
\newcommand{\citacao}[1]{\enquote{#1}}
\RequirePackage{xcolor}
\RequirePackage{listings}
\RequirePackage{fancyvrb}
\ifPDFTeX
  \DeclareFixedFont{\ttb}{T1}{txtt}{bx}{n}{10}
  \DeclareFixedFont{\ttm}{T1}{txtt}{m}{n}{10}
\else
  \DeclareFixedFont{\ttb}{TU}{lmtt}{b}{n}{10}
  \DeclareFixedFont{\ttm}{TU}{lmtt}{m}{n}{10}
\fi
\lstset{captionpos=t,extendedchars=true,basicstyle=\ttfamily,inputencoding=utf8,%
  breaklines=true,postbreak=\usebox\ufrj@lstarrow,%
  literate=%
  {ã}{{\~{a}}}1 {á}{{\'{a}}}1 {â}{{\^{a}}}1 {à}{{\`{a}}}1 {é}{{\'{e}}}1%
  {è}{{\`{e}}}1 {ê}{{\^{e}}}1 {î}{{\^{i}}}1 {í}{{\'{i}}}1 {ô}{{\^{o}}}1%
  {ó}{{\'{o}}}1 {õ}{{\~{o}}}1 {û}{{\^{u}}}1 {ú}{{\'{u}}}1 {ç}{{\c{c}}}1%
  {Ç}{{\c{C}}}1 {À}{{\`{A}}}1 {Â}{{\^{A}}}1 {Á}{{\'{A}}}1 {É}{{\'{E}}}1%
  {Ê}{{\^{E}}}1 {Í}{{\'{I}}}1 {Ó}{{\'{O}}}1 {Ô}{{\^{O}}}1 {Õ}{{\~{O}}}1%
  {Ú}{{\'{U}}}1%
}
\AtBeginDocument{%
  \renewcommand\lstlistingname{\ufrjstring{program}}%
  \renewcommand\lstlistlistingname{\ufrjstring{listprogram}}}
\newcommand\listofprogramas{%
  \chapter*{\lstlistlistingname}%
  \ufrj@listtoc{\lstlistlistingname}%
  \@mkboth{\MakeUppercase\lstlistlistingname}{\MakeUppercase\lstlistlistingname}%
  \@starttoc{lol}}
\newsavebox\ufrj@lstarrow
\AtBeginDocument{\sbox\ufrj@lstarrow{%
  \if@ufrjsetavermelha\textcolor{red}{$\hookrightarrow$}\else$\hookrightarrow$\fi
  \space}}
\newcommand\pythonstyle{\lstset{language=Python,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,xleftmargin=2em,commentstyle=\color{purple},%
  morekeywords={self,as},keywordstyle=\ttb\color[rgb]{0,0,0.5},%
  emph={MyClass,__init__},emphstyle=\ttb\color[rgb]{0.6,0,0},%
  stringstyle=\color[rgb]{0,0.5,0},frame=tb,showstringspaces=false,%
  extendedchars=true,firstnumber=auto,inputencoding=utf8,breaklines=true,%
  escapechar=`,postbreak=\usebox\ufrj@lstarrow}}
\lstnewenvironment{python}[1][]{\pythonstyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\pythoninline[1]{{\pythonstyle\lstinline!#1!}}
\newcommand\pythonexternal[2][]{{\pythonstyle\lstinputlisting[#1]{#2}}}
\newcommand\xmlstyle{\lstset{language=XML,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,xleftmargin=2em,%
  morekeywords={xs:schema,xs:element,xs:sequence,xs:complexType},%
  keywordstyle=\ttb\color[rgb]{0,0,0.5},%
  emph={name,type,attributeFormDefault,elementFormDefault,xmlns:xs},%
  emphstyle=\ttb\color[rgb]{0.6,0,0},stringstyle=\color[rgb]{0,0.5,0},frame=tb,%
  showstringspaces=false,extendedchars=true,inputencoding=utf8,breaklines=true,%
  postbreak=\usebox\ufrj@lstarrow}}
\lstnewenvironment{xml}[1][]{\xmlstyle\lstset{#1}}{}
\newcommand\htmlstyle{\lstset{language=HTML,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,xleftmargin=2em,%
  keywordstyle=\ttb\color[rgb]{0,0,0.5},emphstyle=\ttb\color[rgb]{0.6,0,0},%
  stringstyle=\color[rgb]{0,0.5,0},frame=tb,showstringspaces=false,%
  extendedchars=true,inputencoding=utf8,breaklines=true,%
  postbreak=\usebox\ufrj@lstarrow}}
\lstnewenvironment{html}[1][]{\htmlstyle\lstset{#1}}{}
\newcommand\prologstyle{\lstset{language=Prolog,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,xleftmargin=2em,commentstyle=\color{purple},%
  keywordstyle=\ttb\color[rgb]{0,0,0.5},emph={MyClass,__init__},%
  emphstyle=\ttb\color[rgb]{0.6,0,0},stringstyle=\color[rgb]{0,0.5,0},frame=tb,%
  showstringspaces=false,extendedchars=true,firstnumber=auto,inputencoding=utf8,%
  breaklines=true,escapechar=`,%
  postbreak=\usebox\ufrj@lstarrow}}
\lstnewenvironment{prolog}[1][]{\prologstyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\javastyle{\lstset{language=Java,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,xleftmargin=2em,commentstyle=\color{purple},%
  morekeywords={self,as},keywordstyle=\ttb\color[rgb]{0,0,0.5},%
  emphstyle=\ttb\color[rgb]{0.6,0,0},stringstyle=\color[rgb]{0,0.5,0},frame=tb,%
  showstringspaces=false,extendedchars=true,firstnumber=auto,inputencoding=utf8,%
  breaklines=true,escapechar=`,%
  postbreak=\usebox\ufrj@lstarrow}}
\lstnewenvironment{java}[1][]{\javastyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\javainline[1]{{\javastyle\lstinline!#1!}}
\newcommand\javaexternal[2][]{{\javastyle\lstinputlisting[#1]{#2}}}
\renewcommand{\theFancyVerbLine}{{\small\ttfamily\arabic{FancyVerbLine}}}
\edef\ufrj@@algolang{\ufrjmainstring{algorithm2eopt}}
\ifx\ufrj@@algolang\@empty
  \RequirePackage[linesnumbered,lined,algochapter,ruled]{algorithm2e}
\else
  % onelanguage: os comandos em ingles (\For, \While, \KwData...) passam a
  % imprimir as palavras do idioma do trabalho, e o .tex pode usa-los sem que o
  % PDF saia com "for" e "while" no meio do portugues.
  \expandafter\RequirePackage\expandafter[\ufrj@@algolang,onelanguage,linesnumbered,lined,algochapter,ruled]{algorithm2e}
\fi
\SetAlgoCaptionSeparator{\ \textemdash}
\SetAlCapFnt{\footnotesize}
\SetAlCapNameFnt{\footnotesize}
\SetAlCapSty{textnormal}
\SetAlCapNameSty{textnormal}
\SetKwFor{Para}{para}{faça}{fim do para}
\SetKwFor{Enquanto}{enquanto}{faça}{fim do enquanto}
\ifx\ufrj@mainlang\ufrj@@brazilianstr
  \SetKwFor{For}{para}{faça}{fim do para}
  \SetKwFor{While}{enquanto}{faça}{fim do enquanto}
\fi
\newcommand*\local@instname{}
\newcommand*\ufrj@unitcover{}
\newcommand*\ufrj@unitacronym{}
\newcommand\ufrjdeclareunit[3]{%
  \gdef\local@instname{#1}%
  \gdef\ufrj@unitcover{#2}%
  \gdef\ufrj@unitacronym{#3}}
\newcommand*\ufrj@unitsep{ \ifx\ufrj@unitacronym\@empty\else\ufrj@unitacronym, \fi}
\newcommand*\ufrj@unitshort{%
  \ifx\ufrj@unitacronym\@empty\else\ufrj@unitacronym/\fi UFRJ}
\newcommand*\ufrj@unitshortrev{%
  UFRJ\ifx\ufrj@unitacronym\@empty\else/\ufrj@unitacronym\fi}
\newcommand*\ufrj@logoheight{2cm}
\newcommand*\ufrj@logoleft{ufrj-logo}
\newcommand*\ufrj@logoright{}
\newcommand\ufrjdeclarelogos[3][2cm]{%
  \gdef\ufrj@logoheight{#1}%
  \gdef\ufrj@logoleft{#2}%
  \gdef\ufrj@logoright{#3}}
\newcommand\ufrj@logoline{%
  \makebox[\linewidth]{%
    \ifx\ufrj@logoleft\@empty\else
      \ufrj@logo[\ufrj@logoheight]{\ufrj@logoleft}\fi
    \hfill
    \ifx\ufrj@logoright\@empty\else
      \ufrj@logo[\ufrj@logoheight]{\ufrj@logoright}\fi}}
\newcommand\ufrjdeclareprogram[3]{%
  \expandafter\gdef\csname ufrj@prog@#1@brazilian\endcsname{#2}%
  \expandafter\gdef\csname ufrj@prog@#1@english\endcsname{#3}}
\newcommand\ufrjdefunitstring[3]{%
  \expandafter\gdef\csname ufrj@unit@#1@#2\endcsname{#3}}
\newcommand\ufrj@unitstr[2]{%
  \@ifundefined{ufrj@unit@#1@#2}%
    {\@nameuse{ufrj@str@#1@#2}}%
    {\@nameuse{ufrj@unit@#1@#2}}}
\newcommand\ufrj@unitstrsp[2]{%
  \@ifundefined{ufrj@unit@#1@#2}%
    {\@ifundefined{ufrj@str@#1@#2}{}{\ \@nameuse{ufrj@str@#1@#2}}}%
    {\ \@nameuse{ufrj@unit@#1@#2}}}
\newcommand\ufrj@unitstrmain[1]{%
  \@ifundefined{ufrj@unit@\ufrj@mainlang @#1}%
    {\@ifundefined{ufrj@str@\ufrj@mainlang @#1}%
      {\ufrj@unitstr{brazilian}{#1}}%
      {\@nameuse{ufrj@str@\ufrj@mainlang @#1}}}%
    {\@nameuse{ufrj@unit@\ufrj@mainlang @#1}}}
\newcommand\ufrj@letunitstr[3]{%
  \@ifundefined{ufrj@unit@#2@#3}%
    {\expandafter\let\expandafter#1\csname ufrj@str@#2@#3\endcsname}%
    {\expandafter\let\expandafter#1\csname ufrj@unit@#2@#3\endcsname}}
\newcommand*\ufrj@finalmanualart{o }
\newcommand\ufrjdeclarenorm[2]{%
  \gdef\ufrj@finalmanualart{#1 }%
  \gdef\ufrjfinalmanual{#2}}
\ufrjdefstring{brazilian}{coverprogram}{Programa de Pós-Graduação em \local@deptname}
\ufrjdefstring{brazilian}{natureza}{\local@doctype\ de \@degreename\
  \ifthenelse{\boolean{maledoc}}{apresentado}{apresentada}
  ao Programa de Pós-graduação em \local@deptname,\ufrj@unitsep
  da \local@universityname, como parte dos requisitos
  necessários à obtenção do título de
  \local@degname\ em \local@deptname.}
\newcommand\ufrj@deptcode{}
\newcommand\meta@deptname{}
\newcommand\department[1]{%
  \gdef\ufrj@deptcode{#1}%
  \@ifundefined{ufrj@prog@#1@brazilian}{%
    \ClassError{ufrj}{Programa `#1' nao declarado}{%
      A sigla dada a \string\department\space tem de ser a de um\MessageBreak
      Programa declarado pelo estilo da unidade, com\MessageBreak
      \string\ufrjdeclareprogram.}%
  }{%
    \ufrj@gletcs\local@deptname{ufrj@prog@#1@brazilian}%
    \ufrj@gletcs\meta@deptname{ufrj@prog@#1@brazilian}%
    \ufrj@gletcs\foreign@deptname{ufrj@prog@#1@english}}}
\newcommand\ufrj@gletcs[2]{%
  \expandafter\global\expandafter\let\expandafter#1\csname #2\endcsname}
\renewcommand\title[1]{%
  \global\def\local@title{#1}%
  \expandafter\gdef\csname ufrj@title@brazilian\endcsname{#1}%
}
\newcommand\foreigntitle[1]{%
  \global\def\foreign@title{#1}%
  \expandafter\gdef\csname ufrj@title@english\endcsname{#1}%
}
\newcommand\ufrj@selecttitle{\@nameuse{ufrj@title@\ufrj@mainlang}}
\newcommand\subtitle[1]{%
  \expandafter\gdef\csname ufrj@subtitle@brazilian\endcsname{#1}}
\newcommand\foreignsubtitle[1]{%
  \expandafter\gdef\csname ufrj@subtitle@english\endcsname{#1}}
\newcommand\subtitlein[2]{%
  \expandafter\gdef\csname ufrj@subtitle@#1\endcsname{#2}}
\newcommand\ufrj@selectsubtitle{\@nameuse{ufrj@subtitle@\ufrj@mainlang}}
\newcommand\ufrj@titleblock{%
  \MakeUppercase{\ufrj@selecttitle}%
  \@ifundefined{ufrj@subtitle@\ufrj@mainlang}{}{: \ufrj@selectsubtitle}}
\newcount\@coadvisor\@coadvisor0
\newcommand\coadvisor[5][]{%
  \global\@namedef{UfrjCoadvisorTitle:\expandafter\the\@coadvisor}{#1}
  \global\@namedef{UfrjCoadvisorName:\expandafter\the\@coadvisor}{#2}
  \global\@namedef{UfrjCoadvisorSurname:\expandafter\the\@coadvisor}{#3}
  \global\@namedef{UfrjCoadvisorDegree:\expandafter\the\@coadvisor}{#4}
  \global\@namedef{UfrjCoadvisorInst:\expandafter\the\@coadvisor}{#5}
  \global\advance\@coadvisor by 1
}
\newcommand\local@coadvisorstring{%
  \ifnum\@coadvisor>1
    \ufrjmainstring{coadvisors}%
  \else
    \ufrjmainstring{coadvisor}%
  \fi}
\newcommand\foreign@coadvisorstring{%
  \ifnum\@coadvisor>1
    \ufrjforeignstring{coadvisors}%
  \else
    \ufrjforeignstring{coadvisor}%
  \fi}
\newcommand\ufrj@idcoadvisorstring{%
  \ifnum\@coadvisor>1
    \ufrj@unitstr{brazilian}{coadvisors}%
  \else
    \ufrj@unitstr{brazilian}{coadvisor}%
  \fi}
\newcommand\ufrj@nvolumes{1}
\newcommand\ufrj@thisvolume{1}
\newcommand\volumes[1]{\gdef\ufrj@nvolumes{#1}}
\newcommand\volume[1]{\gdef\ufrj@thisvolume{#1}}
\newcommand\ufrj@volumeline{%
  \ifnum\ufrj@nvolumes>1
    \par\vspace*{4mm}%
    \ufrjmainstring{volumename}\space\ufrj@thisvolume\space
    \ufrjmainstring{ofname}\space\ufrj@nvolumes
    \par
  \fi}
\newcount\@advisor\@advisor0
\newcommand\advisor[5][]{%
  \global\@namedef{UfrjAdvisorTitle:\expandafter\the\@advisor}{#1}
  \global\@namedef{UfrjAdvisorName:\expandafter\the\@advisor}{#2}
  \global\@namedef{UfrjAdvisorSurname:\expandafter\the\@advisor}{#3}
  \global\@namedef{UfrjAdvisorDegree:\expandafter\the\@advisor}{#4}
  \global\@namedef{UfrjAdvisorInst:\expandafter\the\@advisor}{#5}
  \global\advance\@advisor by 1
  \ifnum\@advisor>1
    \renewcommand\local@advisorstring{Orientadores}
    \renewcommand\foreign@advisorstring{Advisors}
  \fi
}
\newcount\@examiner\@examiner0
\newcommand\examiner[4][]{%
  \global\@namedef{UfrjExaminerTitle:\expandafter\the\@examiner}{#1}
  \global\@namedef{UfrjExaminerName:\expandafter\the\@examiner}{#2}
  \global\@namedef{UfrjExaminerDegree:\expandafter\the\@examiner}{#3}
  \global\@namedef{UfrjExaminerInst:\expandafter\the\@examiner}{#4}
  \global\@namedef{UfrjExaminer:\expandafter\the\@examiner}{#1\ #2}
  \global\advance\@examiner by 1
}
\renewcommand\author[2]{%
  \global\def\@authname{#1}
  \global\def\@authsurn{#2}
}
\renewcommand\date[2]{%
  \def\ufrj@docmonth{#1}%
  \def\ufrj@docyear{#2}}
\newcommand\local@monthname{\ifcase\ufrj@docmonth\or
  Janeiro\or Fevereiro\or Março\or Abril\or Maio\or Junho\or
  Julho\or Agosto\or Setembro\or Outubro\or Novembro\or Dezembro\fi}
\newcommand\foreign@monthname{\ifcase\ufrj@docmonth\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi}
\newcounter{keywords}
\newcommand\keyword[1]{%
  \global\@namedef{UfrjKeyword:\expandafter\the\c@keywords}{#1}
  \global\addtocounter{keywords}{1}
}
\newcounter{foreignkeywords}
\newcommand\foreignkeyword[1]{%
  \global\@namedef{UfrjForeignKeyword:\expandafter\the\c@foreignkeywords}{#1}
  \global\addtocounter{foreignkeywords}{1}
}
\newcounter{braziliankeywords}
\newcommand\braziliankeyword[1]{%
  \global\@namedef{UfrjBrazilianKeyword:\expandafter\the\c@braziliankeywords}{#1}
  \global\addtocounter{braziliankeywords}{1}
}
\newcommand\ufrj@printkeywords[3]{%
  \ifnum#3>0
    \par\vspace*{7mm}%
    \noindent{\singlespacing\textbf{#1:}\enspace
    \count1=0
    \@whilenum\count1<#3\do{%
      \ifnum\count1>0 ;\space\fi
      \csname #2\the\count1\endcsname
      \advance\count1 by 1}%
    .\par}%
  \fi}
\newcommand\ufrj@areaconc{}
\newcommand\areaconcentracao[1]{\gdef\ufrj@areaconc{#1}}
\newcommand\ufrj@dataaprov{}
\newcommand\dataaprovacao[1]{\gdef\ufrj@dataaprov{#1}}
\newcommand\ufrj@linhapesq{}
\newcommand\linhapesquisa[1]{\gdef\ufrj@linhapesq{#1}}
\newcommand\ufrj@tipoproducao{}
\newcommand\tipoproducao[1]{\gdef\ufrj@tipoproducao{#1}}
\newcommand\ufrj@projetovinc{}
\newcommand\projetovinculado[1]{\gdef\ufrj@projetovinc{#1}}
\newcommand\ufrj@nomeprojeto{}
\newcommand\nomeprojeto[1]{\gdef\ufrj@nomeprojeto{#1}}
\newcounter{ufrjagencias}
\newcommand\agenciafomento[2]{%
  \global\@namedef{UfrjAgencia:\expandafter\the\c@ufrjagencias}{#1}%
  \global\@namedef{UfrjAgenciaSigla:\expandafter\the\c@ufrjagencias}{#2}%
  \global\addtocounter{ufrjagencias}{1}}
\newcommand\freeconfig[6]{%
\providecommand\@degree{}
\renewcommand\@degree{#1}
\providecommand\@degreename{}
\renewcommand\@degreename{#2}
\providecommand\local@degname{}
\renewcommand\local@degname{#3}
\providecommand\foreign@degname{}
\renewcommand\foreign@degname{#4}
\providecommand\local@doctype{}
\renewcommand\local@doctype{#5}
\providecommand\foreign@doctype{}
\renewcommand\foreign@doctype{#6}%
}
\renewcommand\frontmatter{%
  \cleardoublepage
  \@mainmatterfalse
  \if@ufrjroman
    \ClassWarningNoLine{ufrj}{Option `numeraisromanos' prints roman numerals
      on the pre-textual folhas and restarts the arabic count at 1 in the
      textual part. Section 2.7 of the SiBI manual (9th rev. ed., 2026) has
      those folhas counted but not numbered, and the arabic numbering
      continuing the count. Drop the option to comply}%
    \pagenumbering{roman}%
  \fi
  \begingroup
    \pagestyle{empty}\thispagestyle{empty}
    \singlespacing
    \makefrontpage
    \clearpage
  \endgroup
  \if@ufrjroman
    \fancypagestyle{plain}{\fancyhf{}\ufrj@foliohead
      \renewcommand{\headrulewidth}{0pt}}%
    \pagestyle{ufrj}%
  \else
    \fancypagestyle{plain}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}}%
    \pagestyle{empty}%
  \fi
}
\renewcommand\mainmatter{%
  \ufrj@mainBegin
  \cleardoublepage
  \@mainmattertrue
  \fancypagestyle{plain}{\fancyhf{}\ufrj@foliohead
    \renewcommand{\headrulewidth}{0pt}}%
  \pagestyle{ufrj}%
  \if@ufrjroman\pagenumbering{arabic}\fi}
\renewcommand\backmatter{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi}
\providecommand{\ufrjfinalengine}{%
  \ifPDFTeX\hologo{pdfTeX}~\expandafter\ufrj@dotversion\the\pdftexversion
    \@nil.\pdftexrevision\fi
  \ifLuaTeX\hologo{LuaTeX}~\expandafter\ufrj@dotversion\the\luatexversion
    \@nil.\luatexrevision\fi
  \ifXeTeX\hologo{XeTeX}~\the\XeTeXversion\XeTeXrevision\fi}
\def\ufrj@dotversion#1#2#3\@nil{#1.#2#3}
\providecommand{\ufrjfinaltexsystem}{%
  \ifPDFTeX\texttt{\detokenize\expandafter{\pdftexbanner}}\fi
  \ifLuaTeX\texttt{\detokenize\expandafter{\luatexbanner}}\fi
  \ifXeTeX\texttt{\hologo{XeTeX}\space\XeTeXrevision}\fi}
\def\ufrj@lmrname{lmr}
\def\ufrj@lmssname{lmss}
\providecommand{\ufrjfinalfont}{%
  \edef\ufrj@temp{\familydefault}%
  \ifx\ufrj@temp\ufrj@lmrname
    Latin Modern (\texttt{\ufrj@temp}/\texttt{\encodingdefault})%
  \else
    \ifx\ufrj@temp\ufrj@lmssname
      Latin Modern Sans (\texttt{\ufrj@temp}/\texttt{\encodingdefault})%
    \else
      da família \texttt{\ufrj@temp}, codificação
      \texttt{\encodingdefault}%
    \fi
  \fi}
\let\ufrj@sysname\@empty
\let\ufrj@sysnode\@empty
\let\ufrj@sysmach\@empty
\ifLuaTeX
  \edef\ufrj@sysname{\directlua{%
    local u = os.uname and os.uname() or {}
    tex.sprint(-2, u.sysname or tostring(os.name) or "")}}
  \edef\ufrj@sysnode{\directlua{%
    local u = os.uname and os.uname() or {}
    tex.sprint(-2, u.nodename or "")}}
  \edef\ufrj@sysmach{\directlua{%
    local u = os.uname and os.uname() or {}
    tex.sprint(-2, u.machine or "")}}
\else
  \immediate\openin\@inputcheck=nul:\relax
  \ifeof\@inputcheck\else\def\ufrj@sysname{Windows}\fi
  \immediate\closein\@inputcheck
\fi
\providecommand{\ufrjfinalsystem}{%
  \ifx\ufrj@sysname\@empty\else
    , em \ufrj@sysname
    \ifx\ufrj@sysnode\@empty\else, na máquina \texttt{\ufrj@sysnode}\fi
    \ifx\ufrj@sysmach\@empty\else\space(\texttt{\ufrj@sysmach})\fi
  \fi}
\newcount\ufrj@finalhh
\newcount\ufrj@finalmm
\providecommand{\ufrjfinaltime}{%
  \ufrj@finalhh=\time \divide\ufrj@finalhh by 60
  \ufrj@finalmm=\ufrj@finalhh \multiply\ufrj@finalmm by -60
  \advance\ufrj@finalmm by \time
  \ifnum\ufrj@finalhh<10 0\fi\the\ufrj@finalhh:%
  \ifnum\ufrj@finalmm<10 0\fi\the\ufrj@finalmm}
\def\ufrj@grabversion#1 #2 #3\@nil{#2}
\newcommand\ufrj@pkgversion[1]{%
  \@ifundefined{ver@#1}{}{%
    \expandafter\expandafter\expandafter\ufrj@grabversion
      \csname ver@#1\endcsname\space\space\@nil}}
\providecommand{\ufrjfinalmanual}{%
  \emph{Manual para elaboração e normalização de trabalhos acadêmicos} da
  UFRJ/SiBI}
\newcommand{\ufrjfinalpage}{%
  \clearpage
  % Force the colophon onto a verso (even) page so it faces the rear cover.
  % If the current page is odd (recto), fill it with an empty verso first.
  \if@twoside
    \ifodd\c@page
      \hbox{}\thispagestyle{empty}\newpage
    \fi
  \fi
  \thispagestyle{empty}%
  \null\vfill
  \begin{otherlanguage}{brazilian}%
    \begin{center}
      {\footnotesize\setstretch{1.0}%
      \textbf{Colofão}\par
      \vspace{0.7em}
      \begin{minipage}{0.75\textwidth}\centering
      Este documento foi composto em \LaTeX{} com \ufrjfinalengine{},
      na fonte \ufrjfinalfont. \@ifpackageloaded{biblatex}{A bibliografia
      foi processada por Bib\LaTeX~\ufrj@pkgversion{biblatex.sty} e
      Biber. }{}Foi utilizada a classe \texttt{ufrj}, do projeto \CoppeTeX,
      versão~\ufrj@version, disponível no repositório GitHub
      \mbox{\url{https://github.com/COPPE-UFRJ/CoppeTeX}}, em
      conformidade com \ufrj@finalmanualart\ufrjfinalmanual.
      \par\vspace{0.5em}
      Gerado em \today, às \ufrjfinaltime\ufrjfinalsystem, por
      \ufrjfinaltexsystem{} com o formato \LaTeX{} de \fmtversion.
      \end{minipage}\par}
    \end{center}
  \end{otherlanguage}%
  \vspace*{2cm}%
  \clearpage}
\newcommand\makecover{%
  \begin{titlepage}%
  \pagestyle{empty}%
  \singlespacing
  \centering
  \ufrj@logoline\par
  \vspace{1.5cm}
  {\singlespacing
 \MakeUppercase{\local@universityname}\par
   \ifx\ufrj@unitcover\@empty\else
     \nohyphens{\MakeUppercase{\ufrj@unitcover}}\par
   \fi
   \ufrj@letunitstr\ufrj@tmpcover{brazilian}{coverprogram}%
   \MakeUppercase{\ufrj@tmpcover}\par}
  \vspace{\stretch{2}}
  \textbf{\MakeUppercase{\textbf{\@authname\ \@authsurn}}}\par
  \vspace{\stretch{2}}
  \nohyphens{\ufrj@titleblock}\par
  \ufrj@volumeline
  \vspace{\stretch{3}}
  \MakeUppercase{\local@cityname}\par
  \ufrj@docyear
  \end{titlepage}%
}
\renewcommand\maketitle{%
  \pagenumbering{alph}
  \ltx@ifpackageloaded{hyperref}{\ufrj@hypersetup}{}%
  \makecover
  \pagenumbering{arabic}
  \begin{titlepage}
  \pagestyle{empty}%
  \singlespacing
  \vspace*{1.5cm}
  \begin{center}
  \nohyphens{\@authname\ \@authsurn}\par
  \vspace*{3cm}
  \nohyphens{\ufrj@titleblock}\par
  \ufrj@volumeline
  \end{center}
  \vspace*{2.1cm}
  \begin{flushright}
  \begin{minipage}{0.5\textwidth}
  \singlespacing\frontcover@maintext
  \end{minipage}\par
  \end{flushright}
  \vspace*{12mm}
  {\singlespacing
  \ifthenelse{\equal{\ufrj@linhapesq}{}}{}{%
    \noindent\ufrj@unitstr{brazilian}{researchline}: \ufrj@linhapesq\par
    \vspace*{5mm}}%
  \nohyphens{%
  \noindent\begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
    \local@advisorstring: &
    \count1=0
    \toks@={}
    \@whilenum \count1<\@advisor \do{%
    \ifcase\count1 % same as \ifnum0=\count1
      \toks@=\expandafter{\csname UfrjAdvisorName:\the\count1%
        \expandafter\endcsname\expandafter\space%
        \csname UfrjAdvisorSurname:\the\count1\endcsname\\}
    \else
      \toks@=\expandafter\expandafter\expandafter{%
        \expandafter\the\expandafter\toks@%
        \expandafter&\expandafter\space%
        \csname UfrjAdvisorName:\the\count1\expandafter\endcsname%
        \expandafter\space\csname UfrjAdvisorSurname:\the\count1\endcsname\\
      }%
    \fi
    \advance\count1 by 1}
    \the\toks@
  \end{tabularx}}%
  \ifnum\@coadvisor>0
    \par\vspace*{2mm}%
    \nohyphens{%
    \noindent\begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
      \ufrj@idcoadvisorstring: &
      \count1=0
      \toks@={}
      \@whilenum \count1<\@coadvisor \do{%
      \ifcase\count1
        \toks@=\expandafter{\csname UfrjCoadvisorName:\the\count1%
          \expandafter\endcsname\expandafter\space%
          \csname UfrjCoadvisorSurname:\the\count1\endcsname\\}
      \else
        \toks@=\expandafter\expandafter\expandafter{%
          \expandafter\the\expandafter\toks@%
          \expandafter&\expandafter\space%
          \csname UfrjCoadvisorName:\the\count1\expandafter\endcsname%
          \expandafter\space\csname UfrjCoadvisorSurname:\the\count1\endcsname\\
        }%
      \fi
      \advance\count1 by 1}
      \the\toks@
    \end{tabularx}}%
  \fi
  \par}
  \vspace*{\fill}
  \begin{center}
  \local@cityname\par
  \ufrj@docyear
  \end{center}
  \end{titlepage}
  % Folha adicional (3.1.2.1.2): a sheet of its own right after the folha de
  % rosto, ahead of the approval sheet produced by \frontmatter. Until the 2026
  % edition this content lived on the VERSO of the folha de rosto (NBR 14724,
  % R57); the verso is gone with the printed copy.
  \setcounter{page}{2}%
  \if@ufrjexame\else
    \begingroup
      \def\thepage{\arabic{page}-folhaadicional}%
      \makefolhaadicional\clearpage
    \endgroup
    \addtocounter{page}{-1}%
  \fi
  \global\let\maketitle\relax%
  \global\let\and\relax}
\newcommand\ufrj@membroid[4]{%
  \ifthenelse{\equal{#1}{}}{}{#1\ }#2%
  \ifthenelse{\equal{#3}{}}{}{, #3}%
  \ifthenelse{\equal{#4}{}}{}{, #4}}
\newlength\ufrj@membrogap
\setlength\ufrj@membrogap{9mm minus 2mm}
\newcount\ufrj@bancasize
\newcommand\ufrj@membro[4]{%
  \noindent\hspace*{8mm}%
  \begin{minipage}{\dimexpr\textwidth-8mm\relax}
    \ufrj@membroid{#1}{#2}{#3}{#4}
  \end{minipage}\par\vspace{2mm}}
\newcommand\makefrontpage{%
  \begin{center}
    \nohyphens{\@authname\ \@authsurn}\par
    \vspace*{7mm}
    \sloppy\nohyphens{\ufrj@selecttitle
      \@ifundefined{ufrj@subtitle@\ufrj@mainlang}{}{:
        \ufrj@selectsubtitle}}\par
  \end{center}\par
  \vspace*{8mm}
  \begin{flushright}
  \begin{minipage}{0.5\textwidth}
  \singlespacing\frontcover@maintext
  \end{minipage}
  \end{flushright}
  \vspace*{12mm}
  \noindent\local@approvedonname:\enspace
  \ifthenelse{\equal{\ufrj@dataaprov}{}}
    {\ufrjmainstring{tbddate}}{\ufrj@dataaprov}\par
  \vspace*{12mm}
  \ufrj@bancasize=\@examiner
  \if@ufrjorientexam
    \advance\ufrj@bancasize by \@advisor
    \advance\ufrj@bancasize by \@coadvisor
  \fi
  \ifnum\ufrj@bancasize>7
    \setlength\ufrj@membrogap{3.5mm minus 1.5mm}%
  \else\ifnum\ufrj@bancasize>6
    \setlength\ufrj@membrogap{5mm minus 2mm}%
  \else\ifnum\ufrj@bancasize>5
    \setlength\ufrj@membrogap{7mm minus 2mm}%
  \fi\fi\fi
  \gdef\ufrj@bancalist{}%
  \if@ufrjorientexam
    \count1=0
    \@whilenum\count1<\@advisor\do{%
      \protected@edef\ufrj@tmp{\noexpand\ufrj@membro
        {\csname UfrjAdvisorTitle:\the\count1\endcsname}%
        {\csname UfrjAdvisorName:\the\count1\endcsname\space
         \csname UfrjAdvisorSurname:\the\count1\endcsname}%
        {\csname UfrjAdvisorDegree:\the\count1\endcsname}%
        {\csname UfrjAdvisorInst:\the\count1\endcsname}}%
      \expandafter\g@addto@macro\expandafter\ufrj@bancalist
        \expandafter{\ufrj@tmp}%
      \advance\count1 by 1}%
    \count1=0
    \@whilenum\count1<\@coadvisor\do{%
      \protected@edef\ufrj@tmp{\noexpand\ufrj@membro
        {\csname UfrjCoadvisorTitle:\the\count1\endcsname}%
        {\csname UfrjCoadvisorName:\the\count1\endcsname\space
         \csname UfrjCoadvisorSurname:\the\count1\endcsname}%
        {\csname UfrjCoadvisorDegree:\the\count1\endcsname}%
        {\csname UfrjCoadvisorInst:\the\count1\endcsname}}%
      \expandafter\g@addto@macro\expandafter\ufrj@bancalist
        \expandafter{\ufrj@tmp}%
      \advance\count1 by 1}%
  \fi
  \count1=0
  \@whilenum\count1<\@examiner\do{%
    \protected@edef\ufrj@tmp{\noexpand\ufrj@membro
      {\csname UfrjExaminerTitle:\the\count1\endcsname}%
      {\csname UfrjExaminerName:\the\count1\endcsname}%
      {\csname UfrjExaminerDegree:\the\count1\endcsname}%
      {\csname UfrjExaminerInst:\the\count1\endcsname}}%
    \expandafter\g@addto@macro\expandafter\ufrj@bancalist
      \expandafter{\ufrj@tmp}%
    \advance\count1 by 1}%
  \noindent\local@approvedname:\par
  \nohyphens{\singlespacing\ufrj@bancalist}\par
  \vspace*{\fill}}
\newcommand\ufrj@hypersetup{%
\begingroup
  % changes to \toks@ and \count@ are kept local;
  % it's not necessary for them, but it is usually the case
  % for \count1, because the first ten counters are written
  % to the DVI file, thus you got lucky because of PDF output
  \toks@={}% in this special case not necessary
  \count@=0 %
  \@whilenum\count@<\value{keywords}\do{%
    % * a keyword separator is not necessary,
    %    if there is just one keyword
    % * \csname UfrjKeyword:\the\count@\endcsname must be expanded
    %    at least once, to get rid of the loop depended \count@
    \ifcase\count@ % same as \ifnum0=\count@
      \toks@=\expandafter{\csname UfrjKeyword:\the\count@\endcsname}%
    \else
      \toks@=\expandafter\expandafter\expandafter{%
        \expandafter\the\expandafter\toks@
        \expandafter;\expandafter\space
        \csname UfrjKeyword:\the\count@\endcsname
      }%
    \fi
    \advance\count@ by 1 %
  }%
  \edef\x{\endgroup
    \noexpand\hypersetup{%
      pdfkeywords={\the\toks@}%
    }%
  }%
\if@ufrjpdfa
  \endgroup
\else
  \x
  \hypersetup{%
    pdfauthor={\@authname\ \@authsurn},
    pdftitle={\local@title},
    pdfsubject={\local@doctype\ de \@degreename\ em \local@deptname\ da \ufrj@unitshort},
    pdfcreator={LaTeX with CoppeTeX toolkit}}%
\fi
\hypersetup{%
  breaklinks={true},
  raiselinks={true},
  pageanchor={true},
}%
}
\newcommand\makecatalog{%
  \vspace*{\fill}
  \begin{center}
    \setlength{\fboxsep}{5mm}
    \framebox[120mm][c]{\makebox[5mm][c]{}%
      \begin{minipage}[c]{105mm}
      \setlength{\parindent}{5mm}
      \noindent\sloppy\nohyphens\@authsurn,
      \nohyphens\@authname\par
      \nohyphens{%
        \ufrj@selecttitle/\@authname\ \@authsurn. -- \local@cityname:
      \ufrj@unitshortrev, \ufrj@docyear.}\par
      \pageref{front:pageno},
      \pageref{LastPage}
      p.\@ifundefined{r@cat:lofflag}{}{\pageref{cat:lofflag}} $29,7$cm.\par
      % There is an issue here. When the last entry must be split between lines,
      % the spacing between it and the next paragraph becomes smaller.
      % Should we manually introduce a fixed space? But how could we know that
      % a name was split? Is this happening yet?
      \nohyphens{%
      \begin{tabularx}{100mm}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
        \local@advisorstring: &
        \count1=0
        \toks@={}
        \@whilenum \count1<\@advisor \do{%
        \ifcase\count1 % same as \ifnum0=\count1
          \toks@=\expandafter{\csname UfrjAdvisorName:\the\count1%
          \expandafter\endcsname\expandafter\space%
          \csname UfrjAdvisorSurname:\the\count1\endcsname\\}
        \else
          \toks@=\expandafter\expandafter\expandafter{%
            \expandafter\the\expandafter\toks@
            \expandafter&\expandafter\space
            \csname UfrjAdvisorName:\the\count1\expandafter\endcsname%
            \expandafter\space\csname UfrjAdvisorSurname:\the\count1\endcsname\\
          }%
        \fi
        \advance\count1 by 1}
        \the\toks@
      \end{tabularx}}\par
      \nohyphens{\local@doctype\ ({\MakeLowercase\@degreename}) --
      \ufrj@unitshortrev/Programa de \local@deptname, \ufrj@docyear.}\par
      Referências Bibliográficas: p. \pageref{bib:begin} -- \pageref{bib:end}.\par
      \count1=0
      \count2=1
      \nohyphens{\@whilenum \count1<\value{keywords} \do {%
        \number\count2. \csname UfrjKeyword:\the\count1 \endcsname.
        \advance\count1 by 1
        \advance\count2 by 1}
      I. \csname UfrjAdvisorSurname:0\endcsname,%
      \ \csname UfrjAdvisorName:0\endcsname%
      \ifthenelse{\@advisor>1}{\ \emph{et~al.}{}}.
      II. \local@universityname,\ufrj@unitsep Programa de \local@deptname.
      III. Título.}
    \end{minipage}}
  \end{center}
  \vspace*{\fill}}
\newcommand\ufrj@fichafile{}
\newcommand\ufrj@fichapage{1}
\newcommand\fichacatalografica[2][1]{%
  \gdef\ufrj@fichapage{#1}\gdef\ufrj@fichafile{#2}}
\newcommand\ufrj@marcatipo[1]{%
  \ifthenelse{\equal{\ufrj@tipoproducao}{#1}}{$\times$}{\phantom{$\times$}}}
\newcommand\ufrj@marcavinc[1]{%
  \ifthenelse{\equal{\ufrj@projetovinc}{#1}}{$\times$}{\phantom{$\times$}}}
\newlength\ufrj@capesgap
\setlength\ufrj@capesgap{11mm}
\newcommand\ufrj@campo[1]{%
  \ifthenelse{\equal{#1}{}}{\vspace*{\ufrj@capesgap}}{\par#1}}
\newcommand\ufrj@capescelula[2]{%
  \begin{minipage}[t]{\dimexpr\linewidth-2\tabcolsep\relax}
    \vspace{1mm}#1\par#2\vspace{1.5mm}
  \end{minipage}\\\hline}
\newcommand\ufrj@checatipo{%
  \ifthenelse{\equal{\ufrj@tipoproducao}{}}{}{%
    \ifthenelse{\equal{\ufrj@tipoproducao}{bibliografica}\OR
                \equal{\ufrj@tipoproducao}{artistica}\OR
                \equal{\ufrj@tipoproducao}{tecnologica}\OR
                \equal{\ufrj@tipoproducao}{tecnica}}{}{%
      \ClassWarning{ufrj}{Unknown \string\tipoproducao{} value
        `\ufrj@tipoproducao'. Annex H of the SiBI manual allows only
        bibliografica, artistica, tecnologica or tecnica; no box will be
        ticked}}}}
\newcommand\makefolhaadicional{%
  \clearpage
  \thispagestyle{empty}%
  \ufrj@checatipo
  {\singlespacing
  \begin{center}
    {\bfseries Informações Coleta CAPES}
  \end{center}
  \vspace{7mm}
  \noindent\begin{tabular}{|@{\hspace{\tabcolsep}}p{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth\relax}@{\hspace{\tabcolsep}}|}
    \hline
    \ufrj@capescelula{Tipo de produção intelectual:}{%
      \vspace{1mm}
      \hspace*{10mm}(\ufrj@marcatipo{bibliografica})\enspace
        Bibliográfica\par
      \hspace*{10mm}(\ufrj@marcatipo{artistica})\enspace Artística\par
      \hspace*{10mm}(\ufrj@marcatipo{tecnologica})\enspace Tecnológica\par
      \hspace*{10mm}(\ufrj@marcatipo{tecnica})\enspace Técnica}
    \ufrj@capescelula{Projeto de pesquisa vinculado à produção
      intelectual?}{%
      \vspace{1mm}
      \hspace*{10mm}(\ufrj@marcavinc{sim})\enspace Sim\par
      \hspace*{10mm}(\ufrj@marcavinc{nao})\enspace Não}
    \ufrj@capescelula{Nome do projeto de pesquisa:}{%
      \ufrj@campo{\ufrj@nomeprojeto}}
    \ufrj@capescelula{Área de concentração da produção
      intelectual:}{\ufrj@campo{\ufrj@areaconc}}
    \ufrj@capescelula{Agência(s) de fomento financiadora(s) da produção
      intelectual:}{%
      \ifthenelse{\value{ufrjagencias}=0}{\vspace*{\ufrj@capesgap}}{%
        \count1=0
        \@whilenum\count1<\value{ufrjagencias}\do{%
          \hspace*{10mm}\csname UfrjAgencia:\the\count1\endcsname
          \ (\csname UfrjAgenciaSigla:\the\count1\endcsname)\par
          \advance\count1 by 1}}}
  \end{tabular}\par
  \vspace{9mm}
  \begin{center}
    {\bfseries Ficha catalográfica}\par
    \vspace{4mm}
    \ifthenelse{\equal{\ufrj@fichafile}{}}{%
      \if@ufrjrascunho
        \makecatalog
      \else
        \framebox[125mm][c]{\parbox[c][62mm][c]{115mm}{\centering\footnotesize
          Espaço reservado à ficha catalográfica.\\[1ex]
          Gere-a em \texttt{fichacatalografica.sibi.ufrj.br} e inclua o
          arquivo com \texttt{\string\fichacatalografica\{arquivo.pdf\}},
          ou solicite-a à biblioteca do seu Programa.}}%
      \fi}{%
      \includegraphics[page=\ufrj@fichapage,width=125mm]{\ufrj@fichafile}}%
  \end{center}
  \par}}
\newcommand\dedication[1]{%
  \gdef\@dedic{#1}%
  \cleardoublepage
  \vspace*{\fill}%
  \begin{flushright}
    \begin{minipage}{0.5\textwidth}
      \raggedright\itshape\normalsize \@dedic
    \end{minipage}
  \end{flushright}}
\newcommand\epigrafe[2]{%
  \cleardoublepage
  \vspace*{\fill}%
  \begin{flushright}
    \begin{minipage}{0.5\textwidth}
      \raggedright\itshape\normalsize #1\par
      \vspace{1ex}{\raggedleft\normalfont\small #2\par}
    \end{minipage}
  \end{flushright}}

\newcommand\ufrj@coadvisorrows[1]{%
  \if@ufrjcoadvresumo
    \ifnum\@coadvisor>0
      \par\vspace*{2mm}%
      \noindent\begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
        #1: &
        \count1=0
        \toks@={}
        \@whilenum \count1<\@coadvisor \do{%
        \ifcase\count1
          \toks@=\expandafter{\csname UfrjCoadvisorName:\the\count1%
            \expandafter\endcsname\expandafter\space%
            \csname UfrjCoadvisorSurname:\the\count1\endcsname\\}
        \else
          \toks@=\expandafter\expandafter\expandafter{%
            \expandafter\the\expandafter\toks@%
            \expandafter&\expandafter\space%
            \csname UfrjCoadvisorName:\the\count1\expandafter\endcsname%
            \expandafter\space\csname UfrjCoadvisorSurname:\the\count1\endcsname\\
          }%
        \fi
        \advance\count1 by 1}
        \the\toks@
      \end{tabularx}%
    \fi
  \fi}
\newcommand\ufrj@refresumo{%
  \if@ufrjrefresumo
    \if@ufrjexame\else
      {\singlespacing\noindent\raggedright\sloppy
        \nohyphens{%
          \MakeUppercase{\@authsurn}, \@authname.
          \textbf{\ufrj@selecttitle}%
          \@ifundefined{ufrj@subtitle@\ufrj@mainlang}{}{%
            : \ufrj@selectsubtitle}.
          \local@cityname, \ufrj@docyear.
          \local@doctype\ (\@degreename\ em \local@deptname)
          \textemdash{}
          \ifx\local@instname\@empty\else\local@instname, \fi
          \local@universityname,
          \local@cityname, \ufrj@docyear.}\par}%
      \vspace*{4mm}
    \fi
  \fi}
\def\ufrj@yes{true}
\def\ufrj@no{false}
\newcommand\ufrj@setresflag[2]{%
  \def\ufrj@temp{#2}%
  \ifx\ufrj@temp\ufrj@yes
    \csname @ufrj#1true\endcsname
  \else
    \ifx\ufrj@temp\ufrj@no
      \csname @ufrj#1false\endcsname
    \else
      \ClassError{ufrj}{%
        \string\configuraresumos: argumento `#2' invalido}{%
        Cada um dos quatro argumentos de \string\configuraresumos\space tem
        de ser `true' ou `false'.}%
    \fi
  \fi}
\newcommand\configuraresumos[4]{%
  \ufrj@setresflag{residpag}{#1}%
  \ufrj@setresflag{restitulo}{#2}%
  \ufrj@setresflag{resorient}{#3}%
  \ufrj@setresflag{refresumo}{#4}}
\newcommand\ufrj@res@heading[1]{%
  \begin{center}
    \bfseries\MakeUppercase{\@nameuse{ufrj@str@#1@abstractname}}%
  \end{center}\par
  \vspace*{4mm}}
\newcommand\ufrj@resumocabeca{%
  \ufrj@res@heading{\ufrj@reslang}%
  \if@ufrjresidpag
    \ufrj@toptext{\ufrj@reslang}\par
    \vspace*{6mm}
  \fi
  \if@ufrjrestitulo
    \begin{center}
      \sloppy\nohyphens{\MakeUppercase{\ufrj@res@title{\ufrj@reslang}}%
        \ufrj@res@subtitle{\ufrj@reslang}}\par
      \vspace*{8mm}
      \@authname\ \@authsurn \par
      \vspace*{5mm}
      \ufrj@res@month{\ufrj@reslang}/\ufrj@docyear
    \end{center}\par
    \vspace*{9mm}
  \fi
  \if@ufrjresorient
    \noindent%
    \begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
      \ufrj@res@advisor{\ufrj@reslang}: &
      \count1=0
      \toks@={}
      \@whilenum \count1<\@advisor \do{%
      \ifcase\count1 % same as \ifnum0=\count1
        \toks@=\expandafter{\csname UfrjAdvisorName:\the\count1%
        \expandafter\endcsname\expandafter\space%
        \csname UfrjAdvisorSurname:\the\count1\endcsname\\}
      \else
        \toks@=\expandafter\expandafter\expandafter{%
          \expandafter\the\expandafter\toks@
          \expandafter&\expandafter\space
          \csname UfrjAdvisorName:\the\count1\expandafter\endcsname%
          \expandafter\space\csname UfrjAdvisorSurname:\the\count1\endcsname\\
        }%
      \fi
      \advance\count1 by 1}
      \the\toks@
    \end{tabularx}%
    \ufrj@coadvisorrows{\ufrj@res@coadvisor{\ufrj@reslang}}\par
    \vspace*{2mm}
    \noindent\ufrj@res@deptlabel{\ufrj@reslang}:
      \ufrj@res@deptname{\ufrj@reslang}\par
    \vspace*{5mm}%
  \fi
  \ufrj@refresumo}
\newenvironment{abstract}{%
  \cleardoublepage
  \thispagestyle{plain}
  \edef\ufrj@reslang{\ufrj@mainlang}%
  \ufrj@resumocabeca}{%
  \ufrj@printkeywords{\ufrjmainstring{keywordsname}}%
    {UfrjKeyword:}{\value{keywords}}%
  \vspace*{\fill}}
\newenvironment{foreignabstract}{%
  \cleardoublepage
  \thispagestyle{plain}
  \edef\ufrj@reslang{\ufrj@foreignlang}%
  \begin{otherlanguage}{\ufrj@foreignlang}
  \ufrj@resumocabeca}{%
  \ifnum\value{foreignkeywords}>0
    \ufrj@printkeywords{\ufrjforeignstring{keywordsname}}%
      {UfrjForeignKeyword:}{\value{foreignkeywords}}%
  \else
    \ufrj@printkeywords{\ufrjforeignstring{keywordsname}}%
      {UfrjKeyword:}{\value{keywords}}%
  \fi
  \end{otherlanguage}
  \vspace*{\fill}}
\newenvironment{brazilianabstract}{%
  \cleardoublepage
  \thispagestyle{plain}
  \def\ufrj@reslang{brazilian}%
  \begin{otherlanguage}{brazilian}
  \ufrj@resumocabeca}{%
  \ifnum\value{braziliankeywords}>0
    \ufrj@printkeywords{\ufrjstring{keywordsname}}%
      {UfrjBrazilianKeyword:}{\value{braziliankeywords}}%
  \else
    \ufrj@printkeywords{\ufrjstring{keywordsname}}%
      {UfrjKeyword:}{\value{keywords}}%
  \fi
  \end{otherlanguage}
  \vspace*{\fill}}
\renewcommand\listoffigures{%
    \ufrj@hasLof
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\listfigurename}%
      \ufrj@listtoc{\listfigurename}%
      \@mkboth{\MakeUppercase\listfigurename}%
              {\MakeUppercase\listfigurename}%
    \@starttoc{lof}%
    \if@restonecol\twocolumn\fi
    }
\renewcommand\listoftables{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\listtablename}%
      \ufrj@listtoc{\listtablename}%
      \@mkboth{%
          \MakeUppercase\listtablename}%
         {\MakeUppercase\listtablename}%
    \@starttoc{lot}%
    \if@restonecol\twocolumn\fi
    }
\newcommand\printlosymbols{%
\begingroup\@ufrjglosspretrue
\renewcommand\glossaryname{\listsymbolname}%
\@input@{\jobname.los}\endgroup}
\newcount\ufrj@symcount
\newcommand\ufrj@symzeros[1]{%
  \ifnum#1<10000 0\fi\ifnum#1<1000 0\fi\ifnum#1<100 0\fi\ifnum#1<10 0\fi
  \number#1}
\newcommand\ufrj@symchave[1]{%
  \expandafter\ifx\csname ufrj@sym@\detokenize{#1}\endcsname\relax
    \global\advance\ufrj@symcount\@ne
    \expandafter\xdef\csname ufrj@sym@\detokenize{#1}\endcsname{%
      \ufrj@symzeros\ufrj@symcount}%
  \fi
  \edef\@tempsymbl{\csname ufrj@sym@\detokenize{#1}\endcsname=}}
\def\makelosymbols{%
  \newwrite\@losfile
  \immediate\openout\@losfile=\jobname.syx
  \newcommand\symbl[3][]{\@bsphack\begingroup
  \if@ufrjsimbalfa
    \ifstrempty{##1}{\def\@tempsymbl{##2=}}{\def\@tempsymbl{##1=}}%
  \else
    \ufrj@symchave{##2}%
  \fi
             \@sanitize%
             \@wrlos{\@tempsymbl}{##2}{##3}}\typeout%
  {Writing index of symbols file \jobname.syx}%
  \let\makelosymbols\@empty%
}%
\@onlypreamble\makelosymbols
\newcommand\ufrj@semfolio[1]{}
\newcommand\@wrlos[3]{%
  \protected@write\@losfile{}%
    {\string\indexentry{#1[#2] #3|ufrj@semfolio}{\thepage}}%
  \endgroup%
  \@esphack}
\newcommand\printloabbreviations{%
\begingroup\@ufrjglosspretrue
\renewcommand\glossaryname{\listabbreviationname}%
\@input@{\jobname.lab}\endgroup}
\def\makeloabbreviations{%
  \newwrite\@labfile
  \immediate\openout\@labfile=\jobname.abx
   \newcommand\abbrev[3][]{\@bsphack\begingroup
              \ifstrempty{##1}{\def\@tempsymbl{##2=}}{\def\@tempsymbl{##1=}}
              \@sanitize
              \@wrlab{\@tempsymbl}{##2}{##3}}\typeout
  {Writing index of abbreviations file \jobname.abx}%
  \let\makeloabbreviations\@empty
}
\@onlypreamble\makeloabbreviations
\newcommand\@wrlab[3]{%
  \protected@write\@labfile{}%
    {\string\indexentry{#1[#2] #3|ufrj@semfolio}{\thepage}}%
  \endgroup%
  \@esphack}
\newif\if@ufrjsiglas \@ufrjsiglasfalse
\def\makelosiglas{%
  \newwrite\@lsgfile
  \immediate\openout\@lsgfile=\jobname.sgx
  \global\@ufrjsiglastrue
  \typeout{Writing index of acronyms file \jobname.sgx}%
  \let\makelosiglas\@empty}
\@onlypreamble\makelosiglas
\newcommand\@wrsgx[3]{%
  \protected@write\@lsgfile{}%
    {\string\indexentry{#1[#2] #3|ufrj@semfolio}{\thepage}}%
  \endgroup
  \@esphack}
\newcommand\acron[3][]{%
  \if@ufrjsiglas
    \@bsphack\begingroup
    \ifstrempty{#1}{\def\@tempsymbl{#2=}}{\def\@tempsymbl{#1=}}%
    \@sanitize
    \@wrsgx{\@tempsymbl}{#2}{#3}%
  \else
    \@ifundefined{abbrev}{}{\abbrev[#1]{#2}{#3}}%
  \fi}
\newcommand\printlosiglas{%
\begingroup\@ufrjglosspretrue
\renewcommand\glossaryname{\listsiglaname}%
\@input@{\jobname.lsg}\endgroup}
\def\makeglossarylist{%
  \newwrite\@gsxfile
  \immediate\openout\@gsxfile=\jobname.gsx
  \typeout{Writing glossary file \jobname.gsx}%
  \let\makeglossarylist\@empty}
\@onlypreamble\makeglossarylist
\newcommand\@wrgsx[3]{%
  \protected@write\@gsxfile{}%
    {\string\indexentry{#1[#2] #3|ufrj@semfolio}{\thepage}}%
  \endgroup
  \@esphack}
\newcommand\glossaryterm[3][]{%
  \ifdefined\@gsxfile
    \@bsphack\begingroup
    \ifstrempty{#1}{\ufrj@glosskey{#2}}{\def\@tempsymbl{#1=}}%
    \@sanitize
    \@wrgsx{\@tempsymbl}{#2}{#3}%
  \else
    \ClassWarning{ufrj}{\string\glossaryterm\space sem
      \string\makeglossarylist\space no preambulo: o termo `#2' nao entra
      no glossario}%
  \fi}
\newcommand\printglossarylist{%
  \begingroup
  \renewcommand\glossaryname{\ufrjstring{glossary}}%
  \@input@{\jobname.lgs}%
  \endgroup}
\RequirePackage{shellesc}
\newcommand\ufrj@makeindex[3]{% #1 arquivo de escrita, #2 entrada, #3 estilo
  \ifdefined#1%
    \immediate\closeout#1%
    \ShellEscape{makeindex -q #3 -o \jobname.#2 \jobname.\csname ufrj@ext@#2\endcsname}%
  \fi}
\def\ufrj@ext@lab{abx}
\def\ufrj@ext@los{syx}
\def\ufrj@ext@lsg{sgx}
\def\ufrj@ext@lgs{gsx}
\def\ufrj@ext@ind{idx}
\newcommand\ufrj@makeindexauto{%
  \if@ufrjmakeindex
    \ifdefined\pdf@shellescape
      \ifnum\pdf@shellescape>\z@
        \ufrj@makeindex\@labfile{lab}{-s ufrj.ist}%
        \ufrj@makeindex\@losfile{los}{-s ufrj.ist}%
        \ufrj@makeindex\@lsgfile{lsg}{-s ufrj.ist}%
        \ufrj@makeindex\@gsxfile{lgs}{-s ufrj.ist}%
        \@ifpackageloaded{imakeidx}{}{%
          \ufrj@makeindex\@indexfile{ind}{}}%
      \fi
    \fi
  \fi}
\AddToHook{enddocument/afterlastpage}{\ufrj@makeindexauto}
\ExplSyntaxOn
\str_new:N \l__ufrj_idx_str
\str_new:N \l__ufrj_idx_enc_str
\str_new:N \l__ufrj_idx_lvl_str
\str_new:N \l__ufrj_idx_key_str
\str_new:N \l__ufrj_idx_out_str
\seq_new:N \l__ufrj_idx_seq
\seq_new:N \l__ufrj_idx_out_seq
\cs_new:Npn \__ufrj_idx_enc:w #1 | #2 \q_stop
  {
    \str_set:Nn \l__ufrj_idx_str {#1}
    \str_set:Nn \l__ufrj_idx_enc_str { | #2 }
  }
\cs_new_protected:Npn \__ufrj_idx_strip:N #1
  {
    \clist_map_inline:nn
      {
        {á}{a}, {à}{a}, {â}{a}, {ã}{a}, {ä}{a},
        {é}{e}, {è}{e}, {ê}{e}, {ë}{e},
        {í}{i}, {ì}{i}, {î}{i}, {ï}{i},
        {ó}{o}, {ò}{o}, {ô}{o}, {õ}{o}, {ö}{o},
        {ú}{u}, {ù}{u}, {û}{u}, {ü}{u},
        {ç}{c}, {ñ}{n},
        {Á}{A}, {À}{A}, {Â}{A}, {Ã}{A}, {Ä}{A},
        {É}{E}, {È}{E}, {Ê}{E}, {Ë}{E},
        {Í}{I}, {Ì}{I}, {Î}{I}, {Ï}{I},
        {Ó}{O}, {Ò}{O}, {Ô}{O}, {Õ}{O}, {Ö}{O},
        {Ú}{U}, {Ù}{U}, {Û}{U}, {Ü}{U},
        {Ç}{C}, {Ñ}{N}
      }
      { \str_replace_all:Nnn #1 ##1 }
  }
\cs_new_protected:Npn \ufrj@idxkey #1
  {
    \str_set:Nn \l__ufrj_idx_str {#1}
    \str_if_in:NnTF \l__ufrj_idx_str { " }
      { \str_set_eq:NN \l__ufrj_idx_out_str \l__ufrj_idx_str }
      {
        \str_clear:N \l__ufrj_idx_enc_str
        \str_if_in:NnT \l__ufrj_idx_str { | }
          { \exp_after:wN \__ufrj_idx_enc:w \l__ufrj_idx_str \q_stop }
        \seq_set_split_keep_spaces:NnV \l__ufrj_idx_seq { ! } \l__ufrj_idx_str
        \seq_clear:N \l__ufrj_idx_out_seq
        \seq_map_inline:Nn \l__ufrj_idx_seq
          {
            \str_set:Nn \l__ufrj_idx_lvl_str {##1}
            \str_set_eq:NN \l__ufrj_idx_key_str \l__ufrj_idx_lvl_str
            \str_if_in:NnF \l__ufrj_idx_lvl_str { @ }
              { \__ufrj_idx_strip:N \l__ufrj_idx_key_str }
            \str_if_eq:NNTF \l__ufrj_idx_key_str \l__ufrj_idx_lvl_str
              { \seq_put_right:NV \l__ufrj_idx_out_seq \l__ufrj_idx_lvl_str }
              {
                \seq_put_right:Nx \l__ufrj_idx_out_seq
                  { \l__ufrj_idx_key_str @ \l__ufrj_idx_lvl_str }
              }
          }
        \str_set:Nx \l__ufrj_idx_out_str
          { \seq_use:Nn \l__ufrj_idx_out_seq { ! } \l__ufrj_idx_enc_str }
      }
  }
\cs_new_protected:Npn \ufrj@glosskey #1
  {
    \str_set:Nn \l__ufrj_idx_key_str {#1}
    \__ufrj_idx_strip:N \l__ufrj_idx_key_str
    \tl_set:Nx \@tempsymbl { \l__ufrj_idx_key_str = }
  }
\cs_new_protected:Npn \__ufrj_idx_one:n #1
  {
    \ufrj@idxkey {#1}
    \exp_args:NV \ufrj@orig@wrindex \l__ufrj_idx_out_str
  }
\cs_new_protected:Npn \__ufrj_idx_two:nn #1#2
  {
    \ufrj@idxkey {#2}
    \exp_args:NnV \ufrj@orig@wrindex {#1} \l__ufrj_idx_out_str
  }
\AddToHook{begindocument/end}
  {
    \cs_if_exist:NT \@wrindex
      {
        \cs_set_eq:NN \ufrj@orig@wrindex \@wrindex
        \ltx@ifpackageloaded{imakeidx}
          { \cs_set_eq:NN \@wrindex \__ufrj_idx_two:nn }
          { \cs_set_eq:NN \@wrindex \__ufrj_idx_one:n }
      }
  }
\ExplSyntaxOff
\newcommand\newsigla[3]{%
  \@namedef{ufrj@sigla@s@#1}{#2}%
  \@namedef{ufrj@sigla@l@#1}{#3}}
\newcommand\ufrj@sigla@reg[1]{%
  \acron{\@nameuse{ufrj@sigla@s@#1}}{\@nameuse{ufrj@sigla@l@#1}}}
\newcommand\ufrj@sigla@full[1]{%
  \@nameuse{ufrj@sigla@l@#1}\space(\@nameuse{ufrj@sigla@s@#1})}
\newcommand\ufrj@sigla@undef[1]{%
  \PackageWarning{ufrj}{Sigla '#1' nao declarada com \string\newsigla}%
  \textbf{??#1??}}
\newcommand\ufrj@sigla@first[1]{%
  \global\@namedef{ufrj@sigla@done@#1}{}\ufrj@sigla@reg{#1}\ufrj@sigla@full{#1}}
\newcommand\ufrj@sigla@norm[1]{%
  \@ifundefined{ufrj@sigla@s@#1}{\ufrj@sigla@undef{#1}}%
    {\@ifundefined{ufrj@sigla@done@#1}{\ufrj@sigla@first{#1}}%
      {\@nameuse{ufrj@sigla@s@#1}}}}
\newcommand\ufrj@sigla@star[1]{%
  \@ifundefined{ufrj@sigla@s@#1}{\ufrj@sigla@undef{#1}}%
    {\global\@namedef{ufrj@sigla@done@#1}{}\ufrj@sigla@full{#1}}}
\newcommand\sigla{\@ifstar\ufrj@sigla@star\ufrj@sigla@norm}
\AtBeginDocument{%
  \ltx@ifpackageloaded{hyperref}{%
    \def\ufrj@bibEnd{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{bib:end}}%
          {{}{\number\c@page}{}{\detokenize{page.}\number\c@page}{}}}}%
    \def\ufrj@bibBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{bib:begin}}%
          {{}{\number\c@page}{}{\detokenize{page.}\number\c@page}{}}}}%
    \def\ufrj@mainBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{front:pageno}}%
          {{}{\Roman{page}}{}{\detokenize{page.}\romannumeral\c@page}{}}}}%
    \def\ufrj@hasLof{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{cat:lofflag}}%
          {{}{\detokenize{:~il.;}}{}{\detokenize{page.}\romannumeral\c@page}{}}}}%
  }{%
    \def\ufrj@bibEnd{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{bib:end}}{{}{\number\c@page}{}}}}%
    \def\ufrj@bibBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{bib:begin}}{{}{\number\c@page}{}}}}%
    \def\ufrj@mainBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{front:pageno}}{{}{\Roman{page}}{}}}}%
    \def\ufrj@hasLof{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{cat:lofflag}}{{}{\detokenize{:~il.;}}{}}}}%
  }%
}
\newlength{\recuolongquote}
\setlength{\recuolongquote}{4cm}

\newenvironment*{longquote}[1][default]{%
\begin{list}{}{%
\setlength{\leftmargin}{\recuolongquote}%
\setlength{\rightmargin}{0pt}%
\setlength{\itemindent}{0pt}%
\setlength{\listparindent}{0pt}%
\setlength{\parsep}{0pt}%
\setlength{\topsep}{\baselineskip}%
}%
\item\relax
\footnotesize
\singlespacing
\ifthenelse{\not\equal{#1}{default}}%
{\itshape\selectlanguage{#1}}%
{}%
\ignorespaces
}{%
\end{list}%
\ignorespacesafterend
}
\newenvironment{theglossary}{%
  \if@twocolumn%
    \@restonecoltrue\onecolumn%
  \else%
    \@restonecolfalse%
  \fi%
  \@mkboth{\MakeUppercase\glossaryname}%
  {\MakeUppercase\glossaryname}%
  \chapter*{\glossaryname}%
  \if@ufrjglosspre
    \ufrj@listtoc{\glossaryname}%
  \else
    \addcontentsline{toc}{chapter}{\protect\numberline{}\glossaryname}%
  \fi
  \list{}
  {\setlength{\listparindent}{0in}%
   \setlength{\labelwidth}{1.0in}%
   \setlength{\leftmargin}{1.5in}%
   \setlength{\labelsep}{0.5in}%
   \setlength{\itemindent}{0in}}%
   \sloppy}%
  {\if@restonecol\twocolumn\fi%
\endlist}
\renewenvironment{theindex}{%
  \if@twocolumn
    \@restonecolfalse
  \else
    \@restonecoltrue
  \fi
  \twocolumn[\@makeschapterhead{\indexname}]%
  \@mkboth{\MakeUppercase\indexname}%
  {\MakeUppercase\indexname}%
  \thispagestyle{plain}\parindent\z@
  \ifdefined\phantomsection\phantomsection\fi
  \addcontentsline{toc}{chapter}{\protect\numberline{}\indexname}
  \parskip\z@ \@plus .3\p@\relax
  \columnseprule \z@
  \columnsep 35\p@
  \let\item\@idxitem}
  {\if@restonecol\onecolumn\else\clearpage\fi}
\newcommand\listabbreviationname{%
  \if@ufrjsiglas\ufrjmainstring{listabbreviationonly}%
  \else\ufrjmainstring{listabbreviation}\fi}
\newcommand\listsiglaname{\ufrjmainstring{listsigla}}
\newcommand\listsymbolname{\ufrjmainstring{listsymbol}}
\newcommand\glossaryname{\ufrjmainstring{glossary}}
\newcommand\local@advisorstring{Orientador}
\newcommand\foreign@advisorstring{Advisor}
\ifthenelse{\boolean{maledoc}}{%
  \newcommand\local@approvedname{\ufrj@unitstr{brazilian}{approvedmale}}%
}{%
  \newcommand\local@approvedname{\ufrj@unitstr{brazilian}{approvedfemale}}%
}
\ifthenelse{\boolean{maledoc}}{%
  \newcommand\local@approvedonname{\ufrj@unitstr{brazilian}{approvedonmale}}%
}{%
  \newcommand\local@approvedonname{\ufrj@unitstr{brazilian}{approvedonfemale}}%
}
\newcommand\local@universityname{Universidade Federal do Rio de Janeiro}
\newcommand\local@deptstring{Programa}
\newcommand\foreign@deptstring{Department}
\newcommand\local@cityname{Rio de Janeiro}
\newcommand\local@statename{RJ}
\newcommand\local@countryname{Brasil}
\newcommand\frontcover@maintext{
  \sloppy\nohyphens{\ufrj@unitstr{brazilian}{natureza}}%
  \if@ufrjarearosto
    \ifthenelse{\equal{\ufrj@areaconc}{}}{}{%
      \par\vspace{1ex}%
      \sloppy\nohyphens{Área de concentração: \ufrj@areaconc.}}%
  \fi
}
\newcommand\ufrj@toptext[1]{%
  \noindent \@nameuse{ufrj@str@#1@abstractname}\
  \ifthenelse{\boolean{maledoc}}%
    {\@nameuse{ufrj@str@#1@abstractofmale}}%
    {\@nameuse{ufrj@str@#1@abstractoffemale}}\
  \@nameuse{ufrj@str@#1@doctype\ufrj@doctypekey}\
  \ifthenelse{\boolean{maledoc}}%
    {\@nameuse{ufrj@str@#1@presentedmale}}%
    {\@nameuse{ufrj@str@#1@presentedfemale}}
  \sloppy\nohyphens{\ufrj@unitstr{#1}{tounit} \@nameuse{ufrj@str@#1@abstracttail}\
  \@nameuse{ufrj@str@#1@degname\ufrj@degkey}\ufrj@unitstrsp{#1}{sciencename} (\@degree)}%
}
\newcommand\ufrj@res@title[1]{%
  \@ifundefined{ufrj@title@#1}%
    {\@nameuse{ufrj@title@brazilian}}%
    {\@nameuse{ufrj@title@#1}}}
\newcommand\ufrj@res@subtitle[1]{%
  \@ifundefined{ufrj@title@#1}%
    {\@ifundefined{ufrj@subtitle@brazilian}{}%
       {: \@nameuse{ufrj@subtitle@brazilian}}}%
    {\@ifundefined{ufrj@subtitle@#1}{}%
       {: \@nameuse{ufrj@subtitle@#1}}}}
\newcommand\ufrj@res@month[1]{%
  \@nameuse{ufrj@str@#1@monthname\number\ufrj@docmonth}}
\newcommand\ufrj@res@advisor[1]{%
  \ifnum\@advisor>1
    \@nameuse{ufrj@str@#1@advisors}%
  \else
    \@nameuse{ufrj@str@#1@advisor}%
  \fi}
\newcommand\ufrj@res@coadvisor[1]{%
  \ifnum\@coadvisor>1
    \@nameuse{ufrj@str@#1@coadvisors}%
  \else
    \@nameuse{ufrj@str@#1@coadvisor}%
  \fi}
\newcommand\ufrj@res@deptlabel[1]{\@nameuse{ufrj@str@#1@dept}}
\newcommand\ufrj@res@deptname[1]{%
  \edef\ufrj@@lg{#1}\def\ufrj@@en{english}%
  \ifx\ufrj@@lg\ufrj@@en \foreign@deptname \else \local@deptname \fi}
\RequirePackage{setspace}
\if@ufrjdoublespace\doublespacing\else\onehalfspacing\fi
\if@ufrjpdfa
  \let\ufrj@PackageWarning\PackageWarning
  \def\PackageWarning#1#2{%
    \in@{Setting all color commands}{#2}%
    \ifin@\PackageInfo{#1}{#2}\else\ufrj@PackageWarning{#1}{#2}\fi}
  \RequirePackage[a-2b]{pdfx}
  \let\PackageWarning\ufrj@PackageWarning
  \ifdefined\pdfsuppressptexinfo
    \pdfsuppressptexinfo=-1
  \else
    \ifdefined\pdfvariable
      \pdfvariable suppressoptionalinfo=15
    \fi
  \fi
  \ifdefined\AddToHook
    \let\ufrj@xmpout\@mainaux
    \def\ufrj@xmphook{\AddToHook{enddocument/afteraux}}%
  \else
    \newwrite\ufrj@xmpout
    \let\ufrj@xmphook\AtEndDocument
  \fi
  \ufrj@xmphook{%
    \gdef\ufrj@xmpkeys{}%
    \count@=0
    \@whilenum\count@<\value{keywords}\do{%
      \ifnum\count@>0
        \g@addto@macro\ufrj@xmpkeys{\string\sep\space}%
      \fi
      \protected@edef\ufrj@tmp{\csname UfrjKeyword:\the\count@\endcsname}%
      \expandafter\g@addto@macro\expandafter\ufrj@xmpkeys
        \expandafter{\ufrj@tmp}%
      \advance\count@ by 1}%
    \immediate\openout\ufrj@xmpout=\jobname.xmpdata
    \begingroup
      \let\protect\string
      \@ifundefined{ufrj@title@\ufrj@mainlang}{}{%
        \immediate\write\ufrj@xmpout{\string\Title{\ufrj@selecttitle}}}%
      \@ifundefined{@authname}{}{%
        \immediate\write\ufrj@xmpout{%
          \string\Author{\@authname\space\@authsurn}}}%
      \immediate\write\ufrj@xmpout{\string\Keywords{\ufrj@xmpkeys}}%
      \ifthenelse{\equal{\ufrj@deptcode}{}}{}{%
        \immediate\write\ufrj@xmpout{\string\Subject{\local@doctype\space de
          \@degreename. Programa de \meta@deptname\space(\ufrj@deptcode),
          \ufrj@unitshort}}}%
      \immediate\write\ufrj@xmpout{\string\Publisher{\local@universityname}}%
      \@ifundefined{ufrj@docyear}{}{%
        \immediate\write\ufrj@xmpout{\string\Date{\ufrj@docyear}}}%
    \endgroup
    \immediate\closeout\ufrj@xmpout}%
\fi
\RequirePackage{hyperref}
\if@ufrjsemlinks
  \hypersetup{hidelinks}
\else
  \if@ufrjlinkscor
    \hypersetup{colorlinks=true,
      linkcolor={blue!65!black}, citecolor={green!40!black},
      urlcolor={blue!65!black}, filecolor={blue!65!black},
      menucolor={blue!65!black}, runcolor={blue!65!black}}
  \else
    \if@ufrjlinksmoldura
      \hypersetup{colorlinks=false, pdfborder={0 0 1}}
    \else
      \hypersetup{hidelinks}
    \fi
  \fi
\fi
\if@ufrjnumeric
  \RequirePackage[backend=biber,datamodel=ufrj,%
    bibstyle=ufrj-numeric,citestyle=ufrj-numeric,natbib=true]{biblatex}
\else
  \RequirePackage[backend=biber,datamodel=ufrj,%
    bibstyle=ufrj,citestyle=ufrj,natbib=true]{biblatex}
\fi
\defbibheading{bibliography}{%
  \chapter*{\ufrjstring{references}}%
  \addcontentsline{toc}{chapter}{\protect\numberline{}\ufrjstring{references}}}
\AtBeginBibliography{\ufrj@bibBegin}
\let\ufrj@orig@printbibliography\printbibliography
\renewcommand\printbibliography[1][]{%
  \ufrj@orig@printbibliography[#1]%
  \ufrj@bibEnd}
\let\defineacronym\newsigla
\let\useacronym\sigla
\let\makeloacronyms\makelosiglas
\@onlypreamble\makeloacronyms
\let\printloacronyms\printlosiglas
\let\approvaldate\dataaprovacao
\let\concentrationarea\areaconcentracao
\let\researchline\linhapesquisa
\let\projectname\nomeprojeto
\let\fundingagency\agenciafomento
\let\catalogcard\fichacatalografica
\let\setupabstracts\configuraresumos
\let\listofframes\listofquadros
\let\listofprograms\listofprogramas
\newenvironment{framefloat}[1][htbp]{\begin{quadro}[#1]}{\end{quadro}}
\newcommand\ufrj@valorpt[3]{%
  \def\ufrj@ptval{#3}%
  \@for\ufrj@par:=#2\do{%
    \expandafter\ufrj@valorpar\ufrj@par\@nil}%
  \expandafter#1\expandafter{\ufrj@ptval}}
\def\ufrj@valorpar#1/#2\@nil{%
  \def\ufrj@tmpv{#1}\ifx\ufrj@tmpv\ufrj@ptval\def\ufrj@ptval{#2}\fi}
\newcommand\productiontype[1]{\ufrj@valorpt\tipoproducao
  {bibliographic/bibliografica,artistic/artistica,technological/tecnologica,technical/tecnica}{#1}}
\newcommand\linkedproject[1]{\ufrj@valorpt\projetovinculado{yes/sim,no/nao}{#1}}
\AtBeginDocument{\providecommand\epigraph{\epigrafe}}
\newcommand{\annex}{
    \renewcommand{\appendixname}{\ufrjstring{annex}}%
    \appendix
    \@ufrjannextrue
    \def\theHchapter{annex.\Alph{chapter}}%
    \ufrj@appendixheadings
}

%% 
%%
%% End of file `ufrj.cls'.
