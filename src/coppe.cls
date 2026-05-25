%%
%% This is file `coppe.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% coppe.dtx  (with options: `class')
%% 
%% This is the `coppe' document class used for composition of LaTeX
%% monographs (master and PhD thesis, and PhD qualifying exams)
%% satisfying the requirements of the Coordination of Research and
%% Graduate Courses in Engineering at the Federal University of
%% Rio de Janeiro.
%% 
%% Copyright (C) 2008 Vicente Helano and George Ainsworth Jr.
%% Copyright (C) 2024 Vicente Helano and George Ainsworth Jr. and Geraldo Xexéo and Eduardo Mangeli
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
%% version 3 along with this package (see COPYING file).
%% If not, see <http://www.gnu.org/licenses/>.
%% 
%% Author(s): Vicente Helano,
%%            George Ainsworth
%%            Geraldo Xexéo
%%            Eduardo Mangeli
%% 
%% \CheckSum{1642}
%% \CharacterTable
%%  {Upper-case    \A\B\C\D\E\F\G\H\I\J\K\L\M\N\O\P\Q\R\S\T\U\V\W\X\Y\Z
%%   Lower-case    \a\b\c\d\e\f\g\h\i\j\k\l\m\n\o\p\q\r\s\t\u\v\w\x\y\z
%%   Digits        \0\1\2\3\4\5\6\7\8\9
%%   Exclamation   \!     Double quote  \"     Hash (number) \#
%%   Dollar        \$     Percent       \%     Ampersand     \&
%%   Acute accent  \'     Left paren    \(     Right paren   \)
%%   Asterisk      \*     Plus          \+     Comma         \,
%%   Minus         \-     Point         \.     Solidus       \/
%%   Colon         \:     Semicolon     \;     Less than     \<
%%   Equals        \=     Greater than  \>     Question mark \?
%%   Commercial at \@     Left bracket  \[     Backslash     \\
%%   Right bracket \]     Circumflex    \^     Underscore    \_
%%   Grave accent  \`     Left brace    \{     Vertical bar  \|
%%   Right brace   \}     Tilde         \~}
%%
\def\filename{coppe.dtx}
\def\fileversion{v3.8}
\def\filedate{2026/05/25}
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{coppe}[\filedate\ \fileversion\ COPPE Dissertations and Thesis]
\LoadClass[12pt,a4paper,twoside]{book}
\RequirePackage{hyphenat}
\RequirePackage{lastpage}
\RequirePackage{ifthen}
\RequirePackage{graphicx}
\RequirePackage{setspace}
\RequirePackage{tabularx}
\RequirePackage{etoolbox}
\RequirePackage{eqparbox}
\RequirePackage{ltxcmds}
\RequirePackage[T1]{fontenc}
\RequirePackage[a4paper,twoside,bindingoffset=1cm,%
top=3cm,bottom=2cm,inner=2cm,outer=2cm]{geometry}
\RequirePackage{titlesec}
\newif\if@coppeappendix \@coppeappendixfalse
\titleformat{\chapter}[hang]
  {\normalfont\Large\bfseries}
  {\if@coppeappendix\MakeUppercase{\appendixname}\ \thechapter\ \textendash\else\thechapter\fi}
  {1ex}{\MakeUppercase}
\titlespacing*{\chapter}{0pt}{10pt}{1.5\baselineskip}
\let\coppe@orig@appendix\appendix
\renewcommand\appendix{\coppe@orig@appendix\@coppeappendixtrue}
\titleformat{name=\chapter,numberless}[hang]
  {\normalfont\Large\bfseries\filcenter}{}{0pt}{\MakeUppercase}
\titlespacing*{name=\chapter,numberless}{0pt}{10pt}{1.5\baselineskip}
\titleformat{\section}
  {\normalfont\large\bfseries}{\thesection}{1ex}{\MakeUppercase}
\titleformat{\subsection}
  {\normalfont\bfseries}{\thesubsection}{1ex}{}
\titleformat{\subsubsection}
  {\normalfont\bfseries\itshape}{\thesubsubsection}{1ex}{}
\RequirePackage{caption}
\captionsetup{font=footnotesize,labelsep=endash}
\RequirePackage{float}
\floatstyle{plaintop}
\restylefloat{figure}
\restylefloat{table}
\providecommand{\quadroname}{\iflanguage{brazilian}{Quadro}{Frame}}
\providecommand{\listquadroname}{%
  \iflanguage{brazilian}{Lista de Quadros}{List of Frames}}
\newfloat{quadro}{htbp}{loq}[chapter]
\floatname{quadro}{\quadroname}
\providecommand{\quadroautorefname}{\quadroname}
\let\l@quadro\l@figure
\newcommand\listofquadros{%
  \chapter*{\listquadroname}%
  \addcontentsline{toc}{chapter}{\listquadroname}%
  \@mkboth{\MakeUppercase\listquadroname}{\MakeUppercase\listquadroname}%
  \@starttoc{loq}}
\newcommand{\cpsourcename}{\iflanguage{brazilian}{Fonte}{Source}}
\newcommand{\cpsource}[1]{%
  \par\addvspace{\smallskipamount}%
  {\footnotesize\singlespacing\centering\cpsourcename: #1\par}}
\let\cpfonte\cpsource
\@ifundefined{source}{\let\source\cpsource}{}%
\@ifundefined{fonte}{\let\fonte\cpsource}{}%
\newcommand{\newcoppefloat}[3]{%
  {\floatstyle{plaintop}\newfloat{#1}{htbp}{lo#1}}%
  \floatname{#1}{#2}%
  \expandafter\newcommand\csname listof#1s\endcsname{%
    \chapter*{#3}\addcontentsline{toc}{chapter}{#3}%
    \@mkboth{\MakeUppercase{#3}}{\MakeUppercase{#3}}%
    \@starttoc{lo#1}}}
\let\coppe@orig@footnotetext\@footnotetext
\long\def\@footnotetext#1{\coppe@orig@footnotetext{\singlespacing#1}}
\renewcommand\footnoterule{\kern-3\p@\hrule\@width 5cm\kern 2.6\p@}
\RequirePackage{enumitem}
\newlist{alineas}{enumerate}{2}
\setlist[alineas,1]{label=\alph*),leftmargin=1.8em,itemsep=0pt}
\setlist[alineas,2]{label=--,leftmargin=1.8em,itemsep=0pt}
\RequirePackage{fancyhdr}
\fancypagestyle{coppe}{\fancyhf{}\fancyhead[RO,LE]{\thepage}%
  \renewcommand{\headrulewidth}{0pt}}
\renewcommand{\cleardoublepage}{%
  \clearpage
  \if@twoside
    \ifodd\c@page\else
      \hbox{}\thispagestyle{empty}\newpage
      \if@twocolumn\hbox{}\newpage\fi
    \fi
  \fi}
\def\CoppeTeX{{\rm C\kern-.05em{\sc o\kern-.025em p\kern-.025em
p\kern-.025em e}}\kern-.08em
T\kern-.1667em\lower.5ex\hbox{E}\kern-.125emX\spacefactor1000}
\newboolean{maledoc}
\setboolean{maledoc}{false}
\newif\if@english\@englishfalse
\DeclareOption{english}{\@englishtrue}
\DeclareOption{msc}{%
  \newcommand{\@degree}{M.Sc.}
  \newcommand{\@degreename}{Mestrado}
  \newcommand{\local@degname}{Mestre}
  \newcommand{\foreign@degname}{Master}
  \newcommand\local@doctype{Disserta{\c c}{\~ a}o}
  \newcommand\foreign@doctype{Dissertation}
}
\DeclareOption{dscexam}{%
  \newcommand{\@degree}{D.Sc.}
  \newcommand{\@degreename}{Doutorado}
  \newcommand{\local@degname}{Doutor}
  \newcommand{\foreign@degname}{Doctor}
  \setboolean{maledoc}{true}
  \newcommand\local@doctype{Exame de Qualifica{\c c}{\~ a}o}
  \newcommand\foreign@doctype{Qualifying Exam}
}
\DeclareOption{mscexam}{%
 \newcommand{\@degree}{M.Sc.}
  \newcommand{\@degreename}{Mestrado}
  \newcommand{\local@degname}{Mestre}
  \newcommand{\foreign@degname}{Master}
  \setboolean{maledoc}{true}
  \newcommand\local@doctype{Exame de Qualifica{\c c}{\~ a}o}
  \newcommand\foreign@doctype{Qualifying Exam}
}
\DeclareOption{dsc}{%
  \newcommand{\@degree}{D.Sc.}
  \newcommand{\@degreename}{Doutorado}
  \newcommand{\local@degname}{Doutor}
  \newcommand{\foreign@degname}{Doctor}
  \newcommand\local@doctype{Tese}
  \newcommand\foreign@doctype{Thesis}
}
\newif\if@coppenumeric\@coppenumericfalse
\DeclareOption{numbers}{\@coppenumerictrue}
\newif\if@copperoman\@copperomanfalse
\DeclareOption{numeraisromanos}{\@copperomantrue}
\onehalfspacing
\DeclareOption{doublespacing}{%
  \doublespacing
}
\ProcessOptions\relax
\if@english
  \RequirePackage[brazilian,english]{babel}
\else
  \RequirePackage[english,brazilian]{babel}
\fi
\RequirePackage{csquotes}
\newcommand{\citacao}[1]{\enquote{#1}}
\RequirePackage{xcolor}
\RequirePackage{listings}
\RequirePackage{fancyvrb}
\definecolor{deepblue}{rgb}{0,0,0.5}
\definecolor{deepred}{rgb}{0.6,0,0}
\definecolor{deepgreen}{rgb}{0,0.5,0}
\DeclareFixedFont{\ttb}{T1}{txtt}{bx}{n}{10}
\DeclareFixedFont{\ttm}{T1}{txtt}{m}{n}{10}
\newcommand{\gxnumbersep}{0.5em}
\lstset{captionpos=t,extendedchars=true,basicstyle=\ttfamily,inputencoding=utf8,%
  literate=%
  {ã}{{\~{a}}}1 {á}{{\'{a}}}1 {â}{{\^{a}}}1 {à}{{\`{a}}}1 {é}{{\'{e}}}1%
  {è}{{\`{e}}}1 {ê}{{\^{e}}}1 {î}{{\^{i}}}1 {í}{{\'{i}}}1 {ô}{{\^{o}}}1%
  {ó}{{\'{o}}}1 {õ}{{\~{o}}}1 {û}{{\^{u}}}1 {ú}{{\'{u}}}1 {ç}{{\c{c}}}1%
  {Ç}{{\c{C}}}1 {À}{{\`{A}}}1 {Â}{{\^{A}}}1 {Á}{{\'{A}}}1 {É}{{\'{E}}}1%
  {Ê}{{\^{E}}}1 {Í}{{\'{I}}}1 {Ó}{{\'{O}}}1 {Ô}{{\^{O}}}1 {Õ}{{\~{O}}}1%
  {Ú}{{\'{U}}}1%
}
\AtBeginDocument{%
  \renewcommand\lstlistingname{\iflanguage{brazilian}{Programa}{Program}}%
  \renewcommand\lstlistlistingname{%
    \iflanguage{brazilian}{Lista de Programas}{List of Programs}}}
\newcommand\listofprogramas{%
  \chapter*{\lstlistlistingname}%
  \addcontentsline{toc}{chapter}{\lstlistlistingname}%
  \@mkboth{\MakeUppercase\lstlistlistingname}{\MakeUppercase\lstlistlistingname}%
  \@starttoc{lol}}
\newcommand\pythonstyle{\lstset{language=Python,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=\gxnumbersep,commentstyle=\color{purple},%
  morekeywords={self,as},keywordstyle=\ttb\color{deepblue},%
  emph={MyClass,__init__},emphstyle=\ttb\color{deepred},%
  stringstyle=\color{deepgreen},frame=tb,showstringspaces=false,%
  extendedchars=true,firstnumber=auto,inputencoding=utf8,breaklines=true,%
  escapechar=`,postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{python}[1][]{\pythonstyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\pythoninline[1]{{\pythonstyle\lstinline!#1!}}
\newcommand\pythonexternal[2][]{{\pythonstyle\lstinputlisting[#1]{#2}}}
\newcommand\xmlstyle{\lstset{language=XML,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=\gxnumbersep,%
  morekeywords={xs:schema,xs:element,xs:sequence,xs:complexType},%
  keywordstyle=\ttb\color{deepblue},%
  emph={name,type,attributeFormDefault,elementFormDefault,xmlns:xs},%
  emphstyle=\ttb\color{deepred},stringstyle=\color{deepgreen},frame=tb,%
  showstringspaces=false,extendedchars=true,inputencoding=utf8,breaklines=true,%
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{xml}[1][]{\xmlstyle\lstset{#1}}{}
\newcommand\htmlstyle{\lstset{language=HTML,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=\gxnumbersep,%
  keywordstyle=\ttb\color{deepblue},emphstyle=\ttb\color{deepred},%
  stringstyle=\color{deepgreen},frame=tb,showstringspaces=false,%
  extendedchars=true,inputencoding=utf8,breaklines=true,%
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{html}[1][]{\htmlstyle\lstset{#1}}{}
\newcommand\prologstyle{\lstset{language=Prolog,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=\gxnumbersep,commentstyle=\color{purple},%
  keywordstyle=\ttb\color{deepblue},emph={MyClass,__init__},%
  emphstyle=\ttb\color{deepred},stringstyle=\color{deepgreen},frame=tb,%
  showstringspaces=false,extendedchars=true,firstnumber=auto,inputencoding=utf8,%
  breaklines=true,escapechar=`,%
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{prolog}[1][]{\prologstyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\javastyle{\lstset{language=Java,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=\gxnumbersep,commentstyle=\color{purple},%
  morekeywords={self,as},keywordstyle=\ttb\color{deepblue},%
  emphstyle=\ttb\color{deepred},stringstyle=\color{deepgreen},frame=tb,%
  showstringspaces=false,extendedchars=true,firstnumber=auto,inputencoding=utf8,%
  breaklines=true,escapechar=`,%
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{java}[1][]{\javastyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\javainline[1]{{\javastyle\lstinline!#1!}}
\newcommand\javaexternal[2][]{{\javastyle\lstinputlisting[#1]{#2}}}
\DefineVerbatimEnvironment{gxoutput}{Verbatim}%
  {frame=lines,numbers=left,numbersep=\gxnumbersep}
\DefineVerbatimEnvironment{gxoutputs}{Verbatim}%
  {frame=lines,numbers=left,numbersep=\gxnumbersep,fontsize=\small}
\renewcommand{\theFancyVerbLine}{{\small\ttfamily\arabic{FancyVerbLine}}}
\if@english
  \RequirePackage[linesnumbered,lined,algochapter,ruled]{algorithm2e}
\else
  \RequirePackage[portuguese,linesnumbered,lined,algochapter,ruled]{algorithm2e}
\fi
\SetKwFor{Para}{para}{faça}{fim do para}
\SetKwFor{Enquanto}{enquanto}{faça}{fim do enquanto}
\if@coppenumeric
  \RequirePackage[backend=biber,datamodel=coppe,%
    bibstyle=coppe-numeric,citestyle=coppe-numeric,natbib=true]{biblatex}
\else
  \RequirePackage[backend=biber,datamodel=coppe,%
    bibstyle=coppe,citestyle=coppe,natbib=true]{biblatex}
\fi
\defbibheading{bibliography}{%
  \chapter*{\iflanguage{brazilian}{Refer\^encias}{References}}%
  \addcontentsline{toc}{chapter}{\iflanguage{brazilian}{Refer\^encias}{References}}}
\AtBeginBibliography{\coppe@bibBegin}
\let\coppe@orig@printbibliography\printbibliography
\renewcommand\printbibliography[1][]{%
  \coppe@orig@printbibliography[#1]%
  \coppe@bibEnd}
\newcommand\department[1]{%
  \ifthenelse{\equal{#1}{PEB}}
    {\global\def\local@deptname{Engenharia Biom{\' e}dica}
     \global\def\foreign@deptname{Biomedical Engineering}}{}
  \ifthenelse{\equal{#1}{PEC}}
    {\global\def\local@deptname{Engenharia Civil}
     \global\def\foreign@deptname{Civil Engineering}}{}
  \ifthenelse{\equal{#1}{PEE}}
    {\global\def\local@deptname{Engenharia El{\' e}trica}
     \global\def\foreign@deptname{Electrical Engineering}}{}
  \ifthenelse{\equal{#1}{PEM}}
    {\global\def\local@deptname{Engenharia Mec{\^ a}nica}
     \global\def\foreign@deptname{Mechanical Engineering}}{}
  \ifthenelse{\equal{#1}{PEMM}}
    {\global\def\local@deptname{Engenharia Metal{\' u}rgica e de Materiais}
\global\def\foreign@deptname{Metallurgical and Materials Engineering}}{}
  \ifthenelse{\equal{#1}{PEN}}
    {\global\def\local@deptname{Engenharia Nuclear}
     \global\def\foreign@deptname{Nuclear Engineering}}{}
  \ifthenelse{\equal{#1}{PENO}}
    {\global\def\local@deptname{Engenharia Oce{\^ a}nica}
     \global\def\foreign@deptname{Ocean Engineering}}{}
  \ifthenelse{\equal{#1}{PPE}}
    {\global\def\local@deptname{Planejamento Energ{\' e}tico}
     \global\def\foreign@deptname{Energy Planning}}{}
  \ifthenelse{\equal{#1}{PEP}}
    {\global\def\local@deptname{Engenharia de Produ{\c c}{\~ a}o}
     \global\def\foreign@deptname{Production Engineering}}{}
  \ifthenelse{\equal{#1}{PEQ}}
    {\global\def\local@deptname{Engenharia Qu{\' i}mica}
     \global\def\foreign@deptname{Chemical Engineering}}{}
  \ifthenelse{\equal{#1}{PESC}}
    {\global\def\local@deptname{Engenharia de Sistemas e Computa{\c c}{\~ a}o}
     \global\def\foreign@deptname{Systems Engineering and Computer Science}}{}
  \ifthenelse{\equal{#1}{PET}}
    {\global\def\local@deptname{Engenharia de Transportes}
     \global\def\foreign@deptname{Transportation Engineering}}{}
  \ifthenelse{\equal{#1}{PENT}}
    {\global\def\local@deptname{Engenharia de Nanotecnologia}
      \global\def\foreign@deptname{Nanotechnology Engineering}}{}
}
\renewcommand\title[1]{%
  \global\def\local@title{#1}%
}
\newcommand\foreigntitle[1]{%
  \global\def\foreign@title{#1}%
}
\newcount\@advisor\@advisor0
\newcommand\advisor[4]{%
  \global\@namedef{CoppeAdvisorTitle:\expandafter\the\@advisor}{#1}
  \global\@namedef{CoppeAdvisorName:\expandafter\the\@advisor}{#2}
  \global\@namedef{CoppeAdvisorSurname:\expandafter\the\@advisor}{#3}
  \global\@namedef{CoppeAdvisorDegree:\expandafter\the\@advisor}{#4}
  \global\advance\@advisor by 1
  \ifnum\@advisor>1
    \renewcommand\local@advisorstring{Orientadores}
    \renewcommand\foreign@advisorstring{Advisors}
  \fi
}
\newcount\@examiner\@examiner0
\newcommand\examiner[3]{%
  \global\@namedef{CoppeExaminer:\expandafter\the\@examiner}{#1\ #2}
  \global\advance\@examiner by 1
}
\renewcommand\author[2]{%
  \global\def\@authname{#1}
  \global\def\@authsurn{#2}
}
\renewcommand\date[2]{%
  \month=#1
  \year=#2
}
\newcommand\local@monthname{\ifcase\month\or
  Janeiro\or Fevereiro\or Mar{\c c}o\or Abril\or Maio\or Junho\or
  Julho\or Agosto\or Setembro\or Outubro\or Novembro\or Dezembro\fi}
\newcommand\foreign@monthname{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi}
\newcounter{keywords}
\newcommand\keyword[1]{%
  \global\@namedef{CoppeKeyword:\expandafter\the\c@keywords}{#1}
  \global\addtocounter{keywords}{1}
}
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
  \pagenumbering{roman}
  \thispagestyle{empty}
  % folha de rosto = counted page 1 (ABNT: the capa is not counted). An odd
  % start keeps the page-counter parity aligned with the physical (recto) side,
  % so \cleardoublepage lands every pre-textual element on an odd (front) page.
  \setcounter{page}{1}
  \makefrontpage
  \clearpage
  \if@copperoman
    \fancypagestyle{plain}{\fancyhf{}\fancyhead[RO,LE]{\thepage}%
      \renewcommand{\headrulewidth}{0pt}}%
    \pagestyle{coppe}%
  \else
    \fancypagestyle{plain}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}}%
    \pagestyle{empty}%
  \fi
  \ifthenelse{\boolean{maledoc}}{}{\makecatalog}%
}
\renewcommand\mainmatter{%
  \coppe@mainBegin
  \cleardoublepage
  \@mainmattertrue
  \fancypagestyle{plain}{\fancyhf{}\fancyhead[RO,LE]{\thepage}%
    \renewcommand{\headrulewidth}{0pt}}%
  \pagestyle{coppe}%
  \pagenumbering{arabic}}
\renewcommand\backmatter{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi}
\renewcommand\maketitle{%
  \pagenumbering{alph}
  \ltx@ifpackageloaded{hyperref}{\coppe@hypersetup}{}%
  \begin{titlepage}
  \begin{flushleft}
  \vspace*{1.5mm}
  \setlength\baselineskip{0pt}
  \setlength\parskip{1mm}
  \makebox[\linewidth]{%
    \includegraphics[height=2cm]{ufrj-logo}\hfill
    \includegraphics[height=2cm]{coppe-logo}}
  \end{flushleft}
  \vspace{1.05cm}
  \begin{center}
  \nohyphens{%
    \if@english
      \MakeUppercase\foreign@title
    \else
      \MakeUppercase\local@title
    \fi}\par
  \vspace*{3cm}
  \nohyphens{\@authname\ \@authsurn}\par
  \end{center}
  \vspace*{2.1cm}
  \begin{flushright}
  \begin{minipage}{8.45cm}
  \frontcover@maintext
  \end{minipage}\par
  \vspace*{7.5mm}
  \nohyphens{%
  \begin{tabularx}{8.45cm}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
    \local@advisorstring: &
    \count1=0
    \toks@={}
    \@whilenum \count1<\@advisor \do{%
    \ifcase\count1 % same as \ifnum0=\count1
      \toks@=\expandafter{\csname CoppeAdvisorName:\the\count1%
        \expandafter\endcsname\expandafter\space%
        \csname CoppeAdvisorSurname:\the\count1\endcsname\\}
    \else
      \toks@=\expandafter\expandafter\expandafter{%
        \expandafter\the\expandafter\toks@%
        \expandafter&\expandafter\space%
        \csname CoppeAdvisorName:\the\count1\expandafter\endcsname%
        \expandafter\space\csname CoppeAdvisorSurname:\the\count1\endcsname\\
      }%
    \fi
    \advance\count1 by 1}
    \the\toks@
  \end{tabularx}}\par
  \end{flushright}
  \vspace*{\fill}
  \begin{center}
  \local@cityname\par
  \local@monthname\ de \number\year
  \end{center}
  \end{titlepage}
  \global\let\maketitle\relax%
  \global\let\and\relax}
\newcommand\makefrontpage{%
  \begin{center}
    \sloppy\nohyphens{
      \if@english
        \MakeUppercase\foreign@title
      \else
        \MakeUppercase\local@title
      \fi}\par
    \vspace*{7mm}
    {\@authname\ \@authsurn}\par
  \end{center}\par
  \vspace*{4mm}
  \frontpage@maintext
  \vspace*{16mm}
  \nohyphens{%
  \noindent\begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
    \local@advisorstring: &
    \count1=0
    \toks@={}
    \@whilenum \count1<\@advisor \do{%
    \ifcase\count1 % same as \ifnum0=\count1
      \toks@=\expandafter{\csname CoppeAdvisorName:\the\count1%
        \expandafter\endcsname\expandafter\space%
        \csname CoppeAdvisorSurname:\the\count1\endcsname\\}
    \else
      \toks@=\expandafter\expandafter\expandafter{%
        \expandafter\the\expandafter\toks@%
        \expandafter&\expandafter\space%
        \csname CoppeAdvisorName:\the\count1\expandafter\endcsname%
        \expandafter\space\csname CoppeAdvisorSurname:\the\count1\endcsname\\
      }%
    \fi
    \advance\count1 by 1}
    \the\toks@
  \end{tabularx}\par
  \vspace*{20mm}
  \noindent\begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
    Aprovada por: &
    \count1=0
    \toks@={}
    \@whilenum \count1<\@examiner \do{%
    \ifcase\count1 % same as \ifnum0=\count1
      \toks@=\expandafter{\csname CoppeExaminer:\the\count1%
        \expandafter\endcsname\expandafter\\}
    \else
      \toks@=\expandafter\expandafter\expandafter{%
        \expandafter\the\expandafter\toks@%
        \expandafter&\expandafter\space%
        \csname CoppeExaminer:\the\count1\expandafter\endcsname%
        \expandafter\space\\
      }%
    \fi
    \advance\count1 by 1}
    \the\toks@
    \end{tabularx}}\par
  \vspace*{\fill}
  \frontpage@bottomtext}
\newcommand\coppe@hypersetup{%
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
    % * \csname CoppeKeyword:\the\count@\endcsname must be expanded
    %    at least once, to get rid of the loop depended \count@
    \ifcase\count@ % same as \ifnum0=\count@
      \toks@=\expandafter{\csname CoppeKeyword:\the\count@\endcsname}%
    \else
      \toks@=\expandafter\expandafter\expandafter{%
        \expandafter\the\expandafter\toks@
        \expandafter;\expandafter\space
        \csname CoppeKeyword:\the\count@\endcsname
      }%
    \fi
    \advance\count@ by 1 %
  }%
  \edef\x{\endgroup
    \noexpand\hypersetup{%
      pdfkeywords={\the\toks@}%
    }%
  }%
\x
\hypersetup{%
  pdfauthor={\@authname\ \@authsurn},
  pdftitle={\local@title},
  pdfsubject={\local@doctype\ de \@degreename\ em \local@deptname\ da COPPE/UFRJ},
  pdfcreator={LaTeX with CoppeTeX toolkit},
  breaklinks={true},
  raiselinks={true},
  pageanchor={true},
}}
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
        \if@english
          \foreign@title%
        \else
          \local@title%
        \fi/\@authname\ \@authsurn. -- \local@cityname:
      UFRJ/COPPE, \number\year.}\par
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
          \toks@=\expandafter{\csname CoppeAdvisorName:\the\count1%
          \expandafter\endcsname\expandafter\space%
          \csname CoppeAdvisorSurname:\the\count1\endcsname\\}
        \else
          \toks@=\expandafter\expandafter\expandafter{%
            \expandafter\the\expandafter\toks@
            \expandafter&\expandafter\space
            \csname CoppeAdvisorName:\the\count1\expandafter\endcsname%
            \expandafter\space\csname CoppeAdvisorSurname:\the\count1\endcsname\\
          }%
        \fi
        \advance\count1 by 1}
        \the\toks@
      \end{tabularx}}\par
      \nohyphens{\local@doctype\ ({\MakeLowercase\@degreename}) --
      UFRJ/COPPE/Programa de \local@deptname, \number\year.}\par
      Refer{\^ e}ncias Bibliogr{\' a}ficas: p. \pageref{bib:begin} -- \pageref{bib:end}.\par
      \count1=0
      \count2=1
      \nohyphens{\@whilenum \count1<\value{keywords} \do {%
        \number\count2. \csname CoppeKeyword:\the\count1 \endcsname.
        \advance\count1 by 1
        \advance\count2 by 1}
      I. \csname CoppeAdvisorSurname:0\endcsname,%
      \ \csname CoppeAdvisorName:0\endcsname%
      \ifthenelse{\@advisor>1}{\ \emph{et~al.}{}}.
      II. \local@universityname, COPPE, Programa de \local@deptname.
      III. T{\' i}tulo.}
    \end{minipage}}
  \end{center}
  \vspace*{\fill}}
\newcommand\dedication[1]{
  \gdef\@dedic{#1}
    \cleardoublepage
    \vspace*{\fill}
    \begin{flushright}
      \begin{minipage}{60mm}
        \raggedleft \it \normalsize \@dedic
      \end{minipage}
    \end{flushright}}

\newenvironment{abstract}{%
  \cleardoublepage
  \thispagestyle{plain}
  \abstract@toptext\par
  \vspace*{8.6mm}
  \begin{center}
    \sloppy\nohyphens{\MakeUppercase\local@title}\par
    \vspace*{13.2mm}
    \@authname\ \@authsurn \par
    \vspace*{7mm}
    \local@monthname/\number\year
  \end{center}\par
  \vspace*{1.5cm}
  \noindent%
  \begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
    \local@advisorstring: &
    \count1=0
    \toks@={}
    \@whilenum \count1<\@advisor \do{%
    \ifcase\count1 % same as \ifnum0=\count1
      \toks@=\expandafter{\csname CoppeAdvisorName:\the\count1%
      \expandafter\endcsname\expandafter\space%
      \csname CoppeAdvisorSurname:\the\count1\endcsname\\}
    \else
      \toks@=\expandafter\expandafter\expandafter{%
        \expandafter\the\expandafter\toks@
        \expandafter&\expandafter\space
        \csname CoppeAdvisorName:\the\count1\expandafter\endcsname%
        \expandafter\space\csname CoppeAdvisorSurname:\the\count1\endcsname\\
      }%
    \fi
    \advance\count1 by 1}
    \the\toks@
  \end{tabularx}\par
  \vspace*{2mm}
  \noindent\local@deptstring: \local@deptname\par
  \vspace*{7mm}}{\vspace*{\fill}}
\newenvironment{foreignabstract}{%
  \cleardoublepage
  \thispagestyle{plain}
  \begin{otherlanguage}{english}
  \foreignabstract@toptext\par
  \vspace*{8.6mm}
  \begin{center}
    \sloppy\nohyphens{\MakeUppercase\foreign@title}\par
    \vspace*{13.2mm}
    \@authname\ \@authsurn \par
    \vspace*{7mm}
    \foreign@monthname/\number\year
  \end{center}\par
  \vspace*{1.5cm}
  \noindent%
  \begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
    \foreign@advisorstring: &
    \count1=0
    \toks@={}
    \@whilenum \count1<\@advisor \do{%
    \ifcase\count1 % same as \ifnum0=\count1
      \toks@=\expandafter{\csname CoppeAdvisorName:\the\count1%
      \expandafter\endcsname\expandafter\space%
      \csname CoppeAdvisorSurname:\the\count1\endcsname\\}
    \else
      \toks@=\expandafter\expandafter\expandafter{%
        \expandafter\the\expandafter\toks@
        \expandafter&\expandafter\space
        \csname CoppeAdvisorName:\the\count1\expandafter\endcsname%
        \expandafter\space\csname CoppeAdvisorSurname:\the\count1\endcsname\\
      }%
    \fi
    \advance\count1 by 1}
    \the\toks@
  \end{tabularx}\par
  \vspace*{2mm}
  \noindent\foreign@deptstring: \foreign@deptname\par
  \vspace*{7mm}}{%
  \end{otherlanguage}
  \vspace*{\fill}
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\foreign@title\@empty
  \global\let\foreign@title\relax
  \global\let\local@title\@empty
  \global\let\local@title\relax
  \global\let\author\relax
  \global\let\author\relax
  \global\let\date\relax}
\renewcommand\listoffigures{%
    \coppe@hasLof
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\listfigurename}%
      \addcontentsline{toc}{chapter}{\listfigurename}%
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
      \addcontentsline{toc}{chapter}{\listtablename}%
      \@mkboth{%
          \MakeUppercase\listtablename}%
         {\MakeUppercase\listtablename}%
    \@starttoc{lot}%
    \if@restonecol\twocolumn\fi
    }
\newcommand\printlosymbols{%
\renewcommand\glossaryname{\listsymbolname}%
\@input@{\jobname.los}}
\def\makelosymbols{%
  \newwrite\@losfile
  \immediate\openout\@losfile=\jobname.syx
  \newcommand\symbl[3][]{\@bsphack\begingroup
  \ifstrempty{##1}{\def\@tempsymbl{##2=}}{\def\@tempsymbl{##1=}}%
             \@sanitize%
             \@wrlos{\@tempsymbl}{##2}{##3}}\typeout%
  {Writing index of symbols file \jobname.syx}%
  \let\makelosymbols\@empty%
}%
\@onlypreamble\makelosymbols
\AtBeginDocument{%
\@ifpackageloaded{hyperref}{%
  \newcommand\@wrlos[3]{%
    \protected@write\@losfile{}%
      {\string\indexentry{#1[#2] #3|hyperpage}{\thepage}}%
    \endgroup%
    \@esphack}}{%
  \newcommand\@wrlos[3]{%
    \protected@write\@losfile{}%
      {\string\indexentry{#1[#2] #3}{\thepage}}%
    \endgroup%
    \@esphack}}}%
\newcommand\printloabbreviations{%
\renewcommand\glossaryname{\listabbreviationname}%
\@input@{\jobname.lab}}
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
\AtBeginDocument{%
\@ifpackageloaded{hyperref}{%
  \newcommand\@wrlab[3]{%
    \protected@write\@labfile{}%
      {\string\indexentry{#1[#2] #3|hyperpage}{\thepage}}%
    \endgroup%
    \@esphack}}{%
  \newcommand\@wrlab[3]{%
    \protected@write\@labfile{}%
      {\string\indexentry{#1[#2] #3}{\thepage}}%
    \endgroup%
    \@esphack}}}%
\newcommand\newsigla[3]{%
  \@namedef{coppe@sigla@s@#1}{#2}%
  \@namedef{coppe@sigla@l@#1}{#3}}
\newcommand\coppe@sigla@reg[1]{%
  \@ifundefined{abbrev}{}%
    {\abbrev{\@nameuse{coppe@sigla@s@#1}}{\@nameuse{coppe@sigla@l@#1}}}}
\newcommand\coppe@sigla@full[1]{%
  \@nameuse{coppe@sigla@l@#1}\space(\@nameuse{coppe@sigla@s@#1})}
\newcommand\coppe@sigla@undef[1]{%
  \PackageWarning{coppe}{Sigla '#1' nao declarada com \string\newsigla}%
  \textbf{??#1??}}
\newcommand\coppe@sigla@first[1]{%
  \global\@namedef{coppe@sigla@done@#1}{}\coppe@sigla@reg{#1}\coppe@sigla@full{#1}}
\newcommand\coppe@sigla@norm[1]{%
  \@ifundefined{coppe@sigla@s@#1}{\coppe@sigla@undef{#1}}%
    {\@ifundefined{coppe@sigla@done@#1}{\coppe@sigla@first{#1}}%
      {\@nameuse{coppe@sigla@s@#1}}}}
\newcommand\coppe@sigla@star[1]{%
  \@ifundefined{coppe@sigla@s@#1}{\coppe@sigla@undef{#1}}%
    {\global\@namedef{coppe@sigla@done@#1}{}\coppe@sigla@full{#1}}}
\newcommand\sigla{\@ifstar\coppe@sigla@star\coppe@sigla@norm}
%%%%    \begin{macrocode}
%%%% \AtBeginDocument{%
%%%% \@ifpackageloaded{hyperref}{%
%%%%   \def\@wrlab#1#2{%
%%%% \protected@write\@labfile{}%
%%%%       {\string\indexentry{[#1] #2|hyperpage}{\thepage}}%
%%%%     \endgroup
%%%%     \@esphack}}{%
%%%%   \def\@wrlab#1#2{%
%%%%     \protected@write\@labfile{}%
%%%%       {\string\indexentry{[#1] #2}{\arabic{page}}}%
%%%%     \endgroup
%%%%     \@esphack}}}
\AtBeginDocument{%
  \ltx@ifpackageloaded{hyperref}{
    \def\coppe@bibEnd{%
      \immediate\write\@auxout{%
        \string\newlabel{bib:end}{{}{\arabic{page}}{}{page.\arabic{page}}{}}}}%
    \def\coppe@bibBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{bib:begin}{{}{\arabic{page}}{}{page.\arabic{page}}{}}}}%
    \def\coppe@mainBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{front:pageno}{{}{\Roman{page}}{}{page.\roman{page}}{}}}}%
    \def\coppe@hasLof{%
      \immediate\write\@auxout{%
        \string\newlabel{cat:lofflag}{{}{:~il.;}{}{page.\roman{page}}{}}}}%
  }{%
    \def\coppe@bibEnd{%
      \immediate\write\@auxout{%
      \string\newlabel{bib:end}{{}{\arabic{page}}{}}}}%
    \def\coppe@bibBegin{%
      \immediate\write\@auxout{%
      \string\newlabel{bib:begin}{{}{\arabic{page}}{}}}}%
    \def\coppe@mainBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{front:pageno}{{}{\Roman{page}}{}}}}%
    \def\coppe@hasLof{%
      \immediate\write\@auxout{%
        \string\newlabel{cat:lofflag}{{}{:~il.;}{}}}}%
  }%
}
\newlength{\recuolongquote}%
\setlength{\recuolongquote}{4cm}%
\newenvironment*{longquote}[1][default]{%
\list{}%
\footnotesize%
\addtolength{\leftskip}{\recuolongquote}%
\item[]%
\singlespacing%
\ifthenelse{\not\equal{#1}{default}}{\itshape\selectlanguage{#1}}{}%
}{\endlist}%
\newenvironment{theglossary}{%
  \if@twocolumn%
    \@restonecoltrue\onecolumn%
  \else%
    \@restonecolfalse%
  \fi%
  \@mkboth{\MakeUppercase\glossaryname}%
  {\MakeUppercase\glossaryname}%
  \chapter*{\glossaryname}%
  \addcontentsline{toc}{chapter}{\glossaryname}
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
  \addcontentsline{toc}{chapter}{\indexname}
  \parskip\z@ \@plus .3\p@\relax
  \columnseprule \z@
  \columnsep 35\p@
  \let\item\@idxitem}
  {\if@restonecol\onecolumn\else\clearpage\fi}
\if@english
  \newcommand\listabbreviationname{List of Abbreviations and Acronyms}
  \newcommand\listsymbolname{List of Symbols}
  \newcommand\glossaryname{Glossary}
\else
  \newcommand\listabbreviationname{Lista de Abreviaturas e Siglas}
  \newcommand\listsymbolname{Lista de S{\' i}mbolos}
  \newcommand\glossaryname{Gloss{\' a}rio}
\fi
\newcommand\local@advisorstring{Orientador}
\newcommand\foreign@advisorstring{Advisor}
\ifthenelse{\boolean{maledoc}}{%
  \newcommand\local@approvedname{Examinado por}%
}{%
  \newcommand\local@approvedname{Examinada por}%
}
\newcommand\local@universityname{Universidade Federal do Rio de Janeiro}
\newcommand\local@deptstring{Programa}
\newcommand\foreign@deptstring{Department}
\newcommand\local@cityname{Rio de Janeiro}
\newcommand\local@statename{RJ}
\newcommand\local@countryname{Brasil}
\newcommand\frontcover@maintext{
  \sloppy\nohyphens{\local@doctype\ de \@degreename\
  \ifthenelse{\boolean{maledoc}}{apresentado}{apresentada}
  ao Programa de P{\' o}s-gradua{\c c}{\~ a}o em \local@deptname,
  COPPE, da \local@universityname, como parte dos requisitos
  necess{\' a}rios {\` a} obten{\c c}{\~ a}o do t{\' i}tulo de
  \local@degname\ em \local@deptname.}
}
\newcommand\frontpage@maintext{
  \noindent {\MakeUppercase\local@doctype}
  \ifthenelse{\boolean{maledoc}}{SUBMETIDO}{SUBMETIDA}
  \sloppy\nohyphens{AO CORPO DOCENTE DO INSTITUTO ALBERTO LUIZ COIMBRA
  DE P{\' O}S-GRADUA{\c C}{\~ A}O E PESQUISA DE ENGENHARIA DA
  UNIVERSIDADE FEDERAL DO RIO DE JANEIRO COMO PARTE DOS REQUISITOS
  NECESS{\' A}RIOS PARA A OBTEN{\c C}{\~ A}O DO GRAU DE
  {\MakeUppercase\local@degname} EM CI{\^E}NCIAS EM
  {\MakeUppercase\local@deptname.\par}}%
}
\newcommand\frontpage@bottomtext{%
  \begin{center}
  {\MakeUppercase{\local@cityname, \local@statename\ -- \local@countryname}}\par
  {\MakeUppercase\local@monthname\ DE \number\year}
  \end{center}%
}
\newcommand\abstract@toptext{%
  \noindent Resumo \ifthenelse{\boolean{maledoc}}{do}{da}
  \local@doctype\ \ifthenelse{\boolean{maledoc}}{apresentado}{apresentada}
  \sloppy\nohyphens{{\` a} COPPE/UFRJ como parte dos requisitos
  necess{\' a}rios para a obten{\c c}{\~ a}o do grau de
  \local@degname\ em Ci{\^ e}ncias (\@degree)}
}
\newcommand\foreignabstract@toptext{%
  \noindent \sloppy\nohyphens{Abstract of \foreign@doctype\ presented to
  COPPE/UFRJ as a partial fulfillment of the requirements for the
  degree of \foreign@degname\ of Science (\@degree)}
}
\newcommand{\annex}{
    \iflanguage{brazilian}
        {\renewcommand{\appendixname}{Anexo}}
        {\renewcommand{\appendixname}{Annex}}
    \appendix
}
%% 
%%
%% End of file `coppe.cls'.
