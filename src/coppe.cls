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
%% \CheckSum{0}
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
\def\fileversion{v4.0}
\def\filedate{2026/05/28}
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{coppe}[\filedate\ \fileversion\ COPPE Dissertations and Thesis]
\let\coppe@version\fileversion
\let\coppe@date\filedate
\edef\coppe@docmonth{\the\month}
\edef\coppe@docyear{\the\year}
\LoadClass[12pt,a4paper,oneside]{book}
\RequirePackage{hyphenat}
\RequirePackage{lastpage}
\RequirePackage{ifthen}
\RequirePackage{graphicx}
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
  \AtEndOfClass{\ClassWarningNoLine{coppe}{%
    Although slower, you should try compiling with LuaLaTeX}}
\fi
\RequirePackage[T1]{fontenc}
\RequirePackage{amsmath}
\ifPDFTeX
  \RequirePackage{amssymb}
\else
  % Unicode engine: defer the check to end of document. Only warn if the
  % user did NOT add either unicode-math (the modern OpenType-math route)
  % or amssymb (the legacy route, which they would have loaded manually).
  % This avoids nagging authors who already followed the documented
  % \usepackage{unicode-math} workflow.
  \AtEndDocument{%
    \@ifpackageloaded{unicode-math}{}{%
      \@ifpackageloaded{amssymb}{}{%
        \ClassWarningNoLine{coppe}{%
          You are compiling with a Unicode engine (LuaLaTeX or XeLaTeX) and\MessageBreak
          neither unicode-math nor amssymb is loaded. AMS-style symbols\MessageBreak
          (\string\mathbb, \string\hbar, \string\varnothing, ...) will be undefined.\MessageBreak
          Add to your preamble:\MessageBreak
          \space\space\string\usepackage{unicode-math}\MessageBreak
          \space\space\string\setmathfont{Latin Modern Math}\MessageBreak
          Do NOT load amssymb together with unicode-math -- it would clash\MessageBreak
          with the OpenType math font setup}}}}
\fi
\RequirePackage[a4paper,headheight=15pt,%
top=3cm,bottom=2cm,left=3cm,right=2cm]{geometry}
\RequirePackage{indentfirst}
\RequirePackage{titlesec}
\newif\if@coppeappendix \@coppeappendixfalse
\titleformat{\chapter}[hang]
  {\normalfont\Large\bfseries}
  {\if@coppeappendix\MakeUppercase{\appendixname}\ \thechapter\ \textendash\else\thechapter\fi}
  {1ex}{\MakeUppercase}
\titlespacing*{\chapter}{0pt}{10pt}{1.5\baselineskip}
\let\coppe@orig@appendix\appendix
\renewcommand\appendix{\coppe@orig@appendix\@coppeappendixtrue}
\newif\if@coppeannex \@coppeannexfalse
\newcommand\coppe@tocapp[1]{%
  \MakeUppercase{\coppestring{appendix}}%
  \nobreakspace#1\nobreakspace\textendash\nobreakspace}
\newcommand\coppe@tocanx[1]{%
  \MakeUppercase{\coppestring{annex}}%
  \nobreakspace#1\nobreakspace\textendash\nobreakspace}
\def\@chapter[#1]#2{%
  \ifnum \c@secnumdepth >\m@ne
    \if@mainmatter
      \refstepcounter{chapter}%
      \typeout{\@chapapp\space\thechapter.}%
      \if@coppeappendix
        \if@coppeannex
          \addcontentsline{toc}{chapter}{\protect\coppe@tocanx{\thechapter}#1}%
        \else
          \addcontentsline{toc}{chapter}{\protect\coppe@tocapp{\thechapter}#1}%
        \fi
      \else
        \addcontentsline{toc}{chapter}{\protect\numberline{\thechapter}#1}%
      \fi
    \else
      \addcontentsline{toc}{chapter}{#1}%
    \fi
  \else
    \addcontentsline{toc}{chapter}{#1}%
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
  {\normalfont\Large\bfseries\filcenter}{}{0pt}{\MakeUppercase}
\titlespacing*{name=\chapter,numberless}{0pt}{10pt}{1.5\baselineskip}
\titleformat{\section}
  {\normalfont\large}{\thesection}{1ex}{\MakeUppercase}
\titleformat{\subsection}
  {\normalfont\bfseries}{\thesubsection}{1ex}{}
\titleformat{\subsubsection}
  {\normalfont\bfseries\itshape}{\thesubsubsection}{1ex}{}
\RequirePackage{caption}
\captionsetup{font=footnotesize,labelsep=endash}
\RequirePackage{subcaption}
\RequirePackage{float}
\floatstyle{plaintop}
\restylefloat{figure}
\restylefloat{table}
\providecommand{\quadroname}{\coppestring{frame}}
\providecommand{\listquadroname}{\coppestring{listframe}}
\newfloat{quadro}{htbp}{loq}[chapter]
\floatname{quadro}{\quadroname}
\providecommand{\quadroautorefname}{\quadroname}
\let\l@quadro\l@figure
\newcommand\listofquadros{%
  \chapter*{\listquadroname}%
  \addcontentsline{toc}{chapter}{\listquadroname}%
  \@mkboth{\MakeUppercase\listquadroname}{\MakeUppercase\listquadroname}%
  \@starttoc{loq}}
\newcommand{\cpsourcename}{\coppestring{source}}
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
\def\coppe@mainlang{brazilian}
\def\coppe@foreignlang{english}
\DeclareOption{brazilian}{%
  \def\coppe@mainlang{brazilian}\def\coppe@foreignlang{english}}
\DeclareOption{english}{%
  \def\coppe@mainlang{english}\def\coppe@foreignlang{brazilian}}
\DeclareOption{spanish}{%
  \def\coppe@mainlang{spanish}\def\coppe@foreignlang{english}}
\DeclareOption{french}{%
  \def\coppe@mainlang{french}\def\coppe@foreignlang{english}}
\DeclareOption{italian}{%
  \def\coppe@mainlang{italian}\def\coppe@foreignlang{english}}
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
\newif\if@coppedoublespace\@coppedoublespacefalse
\DeclareOption{doublespacing}{\@coppedoublespacetrue}
\newif\if@coppeassin \@coppeassinfalse
\DeclareOption{assinaturas}{\@coppeassintrue}
\newif\if@copperascunho \@copperascunhofalse
\DeclareOption{rascunhoficha}{\@copperascunhotrue}
\newif\if@coppetwoside \@coppetwosidefalse
\DeclareOption{twoside}{\@coppetwosidetrue}
\DeclareOption{oneside}{\@coppetwosidefalse}
\ProcessOptions\relax
\if@coppetwoside
  \@twosidetrue
  \geometry{twoside}%
\fi
\def\coppe@@brazilianstr{brazilian}
\def\coppe@@englishstr{english}
\edef\coppe@babelopts{\coppe@foreignlang,\coppe@mainlang}
\expandafter\RequirePackage\expandafter[\coppe@babelopts]{babel}
\providecommand{\copperdefstring}[3]{%
  \expandafter\gdef\csname coppe@str@#1@#2\endcsname{#3}}
\providecommand{\coppestring}[1]{\@nameuse{coppe@str@\languagename @#1}}
\providecommand{\coppemainstring}[1]{\@nameuse{coppe@str@\coppe@mainlang @#1}}
\providecommand{\coppeforeignstring}[1]{\@nameuse{coppe@str@\coppe@foreignlang @#1}}
\providecommand{\usecoppelanguage}[1]{%
  \def\coppe@@cur{#1}%
  \ifx\coppe@@cur\coppe@@brazilianstr\else
  \ifx\coppe@@cur\coppe@@englishstr\else
    \InputIfFileExists{coppe-lang-#1.def}{}
      {\ClassWarning{coppe}{Language pack coppe-lang-#1.def not found}}%
  \fi\fi}
\providecommand{\titlein}[2]{%
  \expandafter\gdef\csname coppe@title@#1\endcsname{#2}}
\copperdefstring{brazilian}{appendix}{Ap\^endice}
\copperdefstring{english}  {appendix}{Appendix}
\copperdefstring{brazilian}{annex}   {Anexo}
\copperdefstring{english}  {annex}   {Annex}
\copperdefstring{brazilian}{frame}        {Quadro}
\copperdefstring{english}  {frame}        {Frame}
\copperdefstring{brazilian}{listframe}    {Lista de Quadros}
\copperdefstring{english}  {listframe}    {List of Frames}
\copperdefstring{brazilian}{source}       {Fonte}
\copperdefstring{english}  {source}       {Source}
\copperdefstring{brazilian}{program}      {Programa}
\copperdefstring{english}  {program}      {Program}
\copperdefstring{brazilian}{listprogram}  {Lista de Programas}
\copperdefstring{english}  {listprogram}  {List of Programs}
\copperdefstring{brazilian}{references}   {Refer\^encias}
\copperdefstring{english}  {references}   {References}
\copperdefstring{brazilian}{in:}          {em}
\copperdefstring{english}  {in:}          {in}
\copperdefstring{brazilian}{art}          {Ilustra\c{c}\~ao}
\copperdefstring{english}  {art}          {Art}
\copperdefstring{brazilian}{platform}     {Plataforma}
\copperdefstring{english}  {platform}     {Platform}
\copperdefstring{brazilian}{directedby}   {Dire\c{c}\~ao}
\copperdefstring{english}  {directedby}   {Directed by}
\copperdefstring{brazilian}{producedby}   {Produ\c{c}\~ao}
\copperdefstring{english}  {producedby}   {Produced by}
\copperdefstring{brazilian}{listabbreviation}{Lista de Abreviaturas e Siglas}
\copperdefstring{english}  {listabbreviation}{List of Abbreviations and Acronyms}
\copperdefstring{brazilian}{listsymbol}      {Lista de S{\' i}mbolos}
\copperdefstring{english}  {listsymbol}      {List of Symbols}
\copperdefstring{brazilian}{glossary}        {Gloss{\' a}rio}
\copperdefstring{english}  {glossary}        {Glossary}
\copperdefstring{brazilian}{advisor}      {Orientador}
\copperdefstring{english}  {advisor}      {Advisor}
\copperdefstring{brazilian}{advisors}     {Orientadores}
\copperdefstring{english}  {advisors}     {Advisors}
\copperdefstring{brazilian}{dept}         {Programa}
\copperdefstring{english}  {dept}         {Department}
\copperdefstring{brazilian}{approvedmale}  {Aprovado por}
\copperdefstring{brazilian}{approvedfemale}{Aprovada por}
\copperdefstring{brazilian}{approvedonmale}  {Aprovado em}
\copperdefstring{brazilian}{approvedonfemale}{Aprovada em}
\copperdefstring{brazilian}{keywordsname} {Palavras-chave}
\copperdefstring{english}  {approvedmale}  {Approved by}
\copperdefstring{english}  {approvedfemale}{Approved by}
\copperdefstring{english}  {approvedonmale}  {Approved on}
\copperdefstring{english}  {approvedonfemale}{Approved on}
\copperdefstring{english}  {keywordsname} {Keywords}
\copperdefstring{brazilian}{universityname}{Universidade Federal do Rio de Janeiro}
\copperdefstring{english}  {universityname}{Universidade Federal do Rio de Janeiro}
\copperdefstring{brazilian}{cityname}     {Rio de Janeiro}
\copperdefstring{english}  {cityname}     {Rio de Janeiro}
\copperdefstring{brazilian}{statename}    {RJ}
\copperdefstring{english}  {statename}    {RJ}
\copperdefstring{brazilian}{countryname}  {Brasil}
\copperdefstring{english}  {countryname}  {Brasil}
\copperdefstring{brazilian}{monthname1} {Janeiro}
\copperdefstring{brazilian}{monthname2} {Fevereiro}
\copperdefstring{brazilian}{monthname3} {Mar{\c c}o}
\copperdefstring{brazilian}{monthname4} {Abril}
\copperdefstring{brazilian}{monthname5} {Maio}
\copperdefstring{brazilian}{monthname6} {Junho}
\copperdefstring{brazilian}{monthname7} {Julho}
\copperdefstring{brazilian}{monthname8} {Agosto}
\copperdefstring{brazilian}{monthname9} {Setembro}
\copperdefstring{brazilian}{monthname10}{Outubro}
\copperdefstring{brazilian}{monthname11}{Novembro}
\copperdefstring{brazilian}{monthname12}{Dezembro}
\copperdefstring{english}{monthname1} {January}
\copperdefstring{english}{monthname2} {February}
\copperdefstring{english}{monthname3} {March}
\copperdefstring{english}{monthname4} {April}
\copperdefstring{english}{monthname5} {May}
\copperdefstring{english}{monthname6} {June}
\copperdefstring{english}{monthname7} {July}
\copperdefstring{english}{monthname8} {August}
\copperdefstring{english}{monthname9} {September}
\copperdefstring{english}{monthname10}{October}
\copperdefstring{english}{monthname11}{November}
\copperdefstring{english}{monthname12}{December}
\copperdefstring{brazilian}{algorithm2eopt}{portuguese}
\copperdefstring{english}  {algorithm2eopt}{}
\copperdefstring{brazilian}{babelname}{brazilian}
\copperdefstring{english}  {babelname}{english}
\@for\coppe@@lang:=\coppe@babelopts\do{%
  \edef\coppe@@cur{\coppe@@lang}%
  \ifx\coppe@@cur\coppe@@brazilianstr\else
  \ifx\coppe@@cur\coppe@@englishstr\else
    \InputIfFileExists{coppe-lang-\coppe@@cur.def}
      {\ClassInfo{coppe}{Loaded language pack coppe-lang-\coppe@@cur.def}}
      {\ClassError{coppe}
        {Missing language pack 'coppe-lang-\coppe@@cur.def'.}
        {Install it next to coppe.cls, or pick a built-in language.}}%
  \fi\fi}
\RequirePackage{csquotes}
\newcommand{\citacao}[1]{\enquote{#1}}
\RequirePackage{xcolor}
\RequirePackage{listings}
\RequirePackage{fancyvrb}
\DeclareFixedFont{\ttb}{T1}{txtt}{bx}{n}{10}
\DeclareFixedFont{\ttm}{T1}{txtt}{m}{n}{10}
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
  \renewcommand\lstlistingname{\coppestring{program}}%
  \renewcommand\lstlistlistingname{\coppestring{listprogram}}}
\newcommand\listofprogramas{%
  \chapter*{\lstlistlistingname}%
  \addcontentsline{toc}{chapter}{\lstlistlistingname}%
  \@mkboth{\MakeUppercase\lstlistlistingname}{\MakeUppercase\lstlistlistingname}%
  \@starttoc{lol}}
\newcommand\pythonstyle{\lstset{language=Python,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,commentstyle=\color{purple},%
  morekeywords={self,as},keywordstyle=\ttb\color[rgb]{0,0,0.5},%
  emph={MyClass,__init__},emphstyle=\ttb\color[rgb]{0.6,0,0},%
  stringstyle=\color[rgb]{0,0.5,0},frame=tb,showstringspaces=false,%
  extendedchars=true,firstnumber=auto,inputencoding=utf8,breaklines=true,%
  escapechar=`,postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{python}[1][]{\pythonstyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\pythoninline[1]{{\pythonstyle\lstinline!#1!}}
\newcommand\pythonexternal[2][]{{\pythonstyle\lstinputlisting[#1]{#2}}}
\newcommand\xmlstyle{\lstset{language=XML,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,%
  morekeywords={xs:schema,xs:element,xs:sequence,xs:complexType},%
  keywordstyle=\ttb\color[rgb]{0,0,0.5},%
  emph={name,type,attributeFormDefault,elementFormDefault,xmlns:xs},%
  emphstyle=\ttb\color[rgb]{0.6,0,0},stringstyle=\color[rgb]{0,0.5,0},frame=tb,%
  showstringspaces=false,extendedchars=true,inputencoding=utf8,breaklines=true,%
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{xml}[1][]{\xmlstyle\lstset{#1}}{}
\newcommand\htmlstyle{\lstset{language=HTML,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,%
  keywordstyle=\ttb\color[rgb]{0,0,0.5},emphstyle=\ttb\color[rgb]{0.6,0,0},%
  stringstyle=\color[rgb]{0,0.5,0},frame=tb,showstringspaces=false,%
  extendedchars=true,inputencoding=utf8,breaklines=true,%
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{html}[1][]{\htmlstyle\lstset{#1}}{}
\newcommand\prologstyle{\lstset{language=Prolog,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,commentstyle=\color{purple},%
  keywordstyle=\ttb\color[rgb]{0,0,0.5},emph={MyClass,__init__},%
  emphstyle=\ttb\color[rgb]{0.6,0,0},stringstyle=\color[rgb]{0,0.5,0},frame=tb,%
  showstringspaces=false,extendedchars=true,firstnumber=auto,inputencoding=utf8,%
  breaklines=true,escapechar=`,%
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{prolog}[1][]{\prologstyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\javastyle{\lstset{language=Java,basicstyle=\ttm,numbers=left,%
  numberstyle=\small\ttfamily,numbersep=0.5em,commentstyle=\color{purple},%
  morekeywords={self,as},keywordstyle=\ttb\color[rgb]{0,0,0.5},%
  emphstyle=\ttb\color[rgb]{0.6,0,0},stringstyle=\color[rgb]{0,0.5,0},frame=tb,%
  showstringspaces=false,extendedchars=true,firstnumber=auto,inputencoding=utf8,%
  breaklines=true,escapechar=`,%
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}}}
\lstnewenvironment{java}[1][]{\javastyle\lstset{#1}%
  \csname\@lst @SetFirstNumber\endcsname}{\csname\@lst @SaveFirstNumber\endcsname}
\newcommand\javainline[1]{{\javastyle\lstinline!#1!}}
\newcommand\javaexternal[2][]{{\javastyle\lstinputlisting[#1]{#2}}}
\renewcommand{\theFancyVerbLine}{{\small\ttfamily\arabic{FancyVerbLine}}}
\edef\coppe@@algolang{\coppemainstring{algorithm2eopt}}
\ifx\coppe@@algolang\@empty
  \RequirePackage[linesnumbered,lined,algochapter,ruled]{algorithm2e}
\else
  \expandafter\RequirePackage\expandafter[\coppe@@algolang,linesnumbered,lined,algochapter,ruled]{algorithm2e}
\fi
\SetKwFor{Para}{para}{faça}{fim do para}
\SetKwFor{Enquanto}{enquanto}{faça}{fim do enquanto}
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
  \expandafter\gdef\csname coppe@title@brazilian\endcsname{#1}%
}
\newcommand\foreigntitle[1]{%
  \global\def\foreign@title{#1}%
  \expandafter\gdef\csname coppe@title@english\endcsname{#1}%
}
\newcommand\coppe@selecttitle{\@nameuse{coppe@title@\coppe@mainlang}}
\newcount\@advisor\@advisor0
\newcommand\advisor[5][]{%
  \global\@namedef{CoppeAdvisorInst:\expandafter\the\@advisor}{#1}
  \global\@namedef{CoppeAdvisorTitle:\expandafter\the\@advisor}{#2}
  \global\@namedef{CoppeAdvisorName:\expandafter\the\@advisor}{#3}
  \global\@namedef{CoppeAdvisorSurname:\expandafter\the\@advisor}{#4}
  \global\@namedef{CoppeAdvisorDegree:\expandafter\the\@advisor}{#5}
  \global\advance\@advisor by 1
  \ifnum\@advisor>1
    \renewcommand\local@advisorstring{Orientadores}
    \renewcommand\foreign@advisorstring{Advisors}
  \fi
}
\newcount\@examiner\@examiner0
\newcommand\examiner[4][]{%
  \global\@namedef{CoppeExaminerInst:\expandafter\the\@examiner}{#1}
  \global\@namedef{CoppeExaminerTitle:\expandafter\the\@examiner}{#2}
  \global\@namedef{CoppeExaminerName:\expandafter\the\@examiner}{#3}
  \global\@namedef{CoppeExaminerDegree:\expandafter\the\@examiner}{#4}
  \global\@namedef{CoppeExaminer:\expandafter\the\@examiner}{#2\ #3}
  \global\advance\@examiner by 1
}
\renewcommand\author[2]{%
  \global\def\@authname{#1}
  \global\def\@authsurn{#2}
}
\renewcommand\date[2]{%
  \def\coppe@docmonth{#1}%
  \def\coppe@docyear{#2}}
\newcommand\local@monthname{\ifcase\coppe@docmonth\or
  Janeiro\or Fevereiro\or Mar{\c c}o\or Abril\or Maio\or Junho\or
  Julho\or Agosto\or Setembro\or Outubro\or Novembro\or Dezembro\fi}
\newcommand\foreign@monthname{\ifcase\coppe@docmonth\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi}
\newcounter{keywords}
\newcommand\keyword[1]{%
  \global\@namedef{CoppeKeyword:\expandafter\the\c@keywords}{#1}
  \global\addtocounter{keywords}{1}
}
\newcounter{foreignkeywords}
\newcommand\foreignkeyword[1]{%
  \global\@namedef{CoppeForeignKeyword:\expandafter\the\c@foreignkeywords}{#1}
  \global\addtocounter{foreignkeywords}{1}
}
\newcounter{braziliankeywords}
\newcommand\braziliankeyword[1]{%
  \global\@namedef{CoppeBrazilianKeyword:\expandafter\the\c@braziliankeywords}{#1}
  \global\addtocounter{braziliankeywords}{1}
}
\newcommand\coppe@printkeywords[3]{%
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
\newcommand\coppe@areaconc{}
\newcommand\areaconcentracao[1]{\gdef\coppe@areaconc{#1}}
\newcommand\coppe@dataaprov{}
\newcommand\dataaprovacao[1]{\gdef\coppe@dataaprov{#1}}
\newcommand\coppe@linhapesq{}
\newcommand\linhapesquisa[1]{\gdef\coppe@linhapesq{#1}}
\newcommand\coppe@tipoproducao{}
\newcommand\tipoproducao[1]{\gdef\coppe@tipoproducao{#1}}
\newcommand\coppe@projetovinc{}
\newcommand\projetovinculado[1]{\gdef\coppe@projetovinc{#1}}
\newcommand\coppe@nomeprojeto{}
\newcommand\nomeprojeto[1]{\gdef\coppe@nomeprojeto{#1}}
\newcounter{coppeagencias}
\newcommand\agenciafomento[2]{%
  \global\@namedef{CoppeAgencia:\expandafter\the\c@coppeagencias}{#1}%
  \global\@namedef{CoppeAgenciaSigla:\expandafter\the\c@coppeagencias}{#2}%
  \global\addtocounter{coppeagencias}{1}}
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
  \if@copperoman
    \ClassWarningNoLine{coppe}{Option `numeraisromanos' prints roman numerals
      on the pre-textual folhas and restarts the arabic count at 1 in the
      textual part. Section 2.7 of the SiBI manual (9th rev. ed., 2026) has
      those folhas counted but not numbered, and the arabic numbering
      continuing the count. Drop the option to comply}%
    \pagenumbering{roman}%
  \fi
  \thispagestyle{empty}
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
}
\renewcommand\mainmatter{%
  \coppe@mainBegin
  \cleardoublepage
  \@mainmattertrue
  \fancypagestyle{plain}{\fancyhf{}\fancyhead[RO,LE]{\thepage}%
    \renewcommand{\headrulewidth}{0pt}}%
  \pagestyle{coppe}%
  \if@copperoman\pagenumbering{arabic}\fi}
\renewcommand\backmatter{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi}
\providecommand{\coppefinalengine}{%
  \ifPDFTeX\hologo{pdfLaTeX}\fi
  \ifLuaTeX\hologo{LuaLaTeX}\fi
  \ifXeTeX\hologo{XeLaTeX}\fi}
\providecommand{\coppefinalfont}{Computer Modern (padr\~ao \LaTeX{})}
\providecommand{\coppefinalmanual}{%
  \emph{Norma para a Elabora\c c\~ao Gr\'afica de Teses e Disserta\c c\~oes
  da COPPE/UFRJ}}
\newcommand{\coppetexfinalpage}{%
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
      \textsc{Colof\~ao}\par
      \vspace{0.7em}
      \begin{minipage}{0.75\textwidth}\centering
      Este documento foi composto em \LaTeX{} com \coppefinalengine{}
      em \today, na fonte \coppefinalfont. A bibliografia foi processada
      por Bib\LaTeX{} e Biber. Foi utilizada a classe \CoppeTeX,
      vers\~ao~\coppe@version, dispon\'\i vel no reposit\'orio GitHub
      \mbox{\url{https://github.com/COPPE-UFRJ/CoppeTeX}}, em
      conformidade com a \coppefinalmanual.
      \end{minipage}\par}
    \end{center}
  \end{otherlanguage}%
  \vspace*{2cm}%
  \clearpage}
\newcommand\makecover{%
  \begin{titlepage}%
  \centering
  \makebox[\linewidth]{%
    \includegraphics[height=2cm]{ufrj-logo}\hfill
    \includegraphics[height=2cm]{coppe-logo}}\par
  \vspace{1.5cm}
  {\singlespacing
 \MakeUppercase{\local@universityname}\par
   \nohyphens{\MakeUppercase{Instituto Alberto Luiz Coimbra de \\
     P{\' o}s-Gradua{\c c}{\~ a}o e Pesquisa de Engenharia}}\par
   \MakeUppercase{Programa de \local@deptname}\par}
  \vspace{\stretch{2}}
  \textbf{\MakeUppercase{\textbf{\@authname\ \@authsurn}}}\par
  \vspace{\stretch{2}}
  \nohyphens{\MakeUppercase{\coppe@selecttitle}}\par
  \vspace{\stretch{3}}
  \MakeUppercase{\local@cityname}\par
  \coppe@docyear
  \end{titlepage}%
}
\renewcommand\maketitle{%
  \pagenumbering{alph}
  \ltx@ifpackageloaded{hyperref}{\coppe@hypersetup}{}%
  \makecover
  \pagenumbering{arabic}
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
  \nohyphens{\@authname\ \@authsurn}\par
  \vspace*{3cm}
  \nohyphens{\MakeUppercase{\coppe@selecttitle}}\par
  \end{center}
  \vspace*{2.1cm}
  \begin{flushright}
  \begin{minipage}{0.5\textwidth}
  \singlespacing\frontcover@maintext
  \end{minipage}\par
  \end{flushright}
  \vspace*{12mm}
  {\singlespacing
  \ifthenelse{\equal{\coppe@linhapesq}{}}{}{%
    \noindent Linha de pesquisa: \coppe@linhapesq\par
    \vspace*{5mm}}%
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
  \end{tabularx}}\par}
  \vspace*{\fill}
  \begin{center}
  \local@cityname\par
  \coppe@docyear
  \end{center}
  \end{titlepage}
  % Ficha catalográfica on the verso of the folha de rosto (NBR 14724, R57):
  % the title page is a recto, so this lands on the immediately following verso,
  % ahead of the approval sheet produced by \frontmatter.
  \setcounter{page}{2}%
  \ifthenelse{\boolean{maledoc}}{}{%
    \makefolhaadicional\clearpage\addtocounter{page}{-1}}%
  \global\let\maketitle\relax%
  \global\let\and\relax}
\newcommand\coppe@membroid[4]{%
  #1\ #2%
  \ifthenelse{\equal{#3}{}}{}{, #3}%
  \ifthenelse{\equal{#4}{}}{}{, #4}}
\newcommand\coppe@membro[4]{%
  \if@coppeassin
    \vspace{9mm}%
    \begin{center}
      \rule{95mm}{0.4pt}\par
      \nopagebreak{\footnotesize\coppe@membroid{#1}{#2}{#3}{#4}}\par
    \end{center}%
  \else
    \noindent\hspace*{8mm}%
    \begin{minipage}{\dimexpr\textwidth-8mm\relax}
      \coppe@membroid{#1}{#2}{#3}{#4}
    \end{minipage}\par\vspace{2mm}%
  \fi}
\newcommand\makefrontpage{%
  \begin{center}
    \nohyphens{\@authname\ \@authsurn}\par
    \vspace*{7mm}
    \sloppy\nohyphens{\coppe@selecttitle}\par
  \end{center}\par
  \vspace*{8mm}
  \begin{flushright}
  \begin{minipage}{0.5\textwidth}
  \singlespacing\frontcover@maintext
  \end{minipage}
  \end{flushright}
  \vspace*{12mm}
  \noindent\local@approvedonname:\enspace
  \ifthenelse{\equal{\coppe@dataaprov}{}}{\hrulefill}{\coppe@dataaprov}\par
  \vspace*{12mm}
  \gdef\coppe@bancalist{}%
  \count1=0
  \@whilenum\count1<\@advisor\do{%
    \protected@edef\coppe@tmp{\noexpand\coppe@membro
      {\csname CoppeAdvisorTitle:\the\count1\endcsname}%
      {\csname CoppeAdvisorName:\the\count1\endcsname\space
       \csname CoppeAdvisorSurname:\the\count1\endcsname}%
      {\csname CoppeAdvisorDegree:\the\count1\endcsname}%
      {\csname CoppeAdvisorInst:\the\count1\endcsname}}%
    \expandafter\g@addto@macro\expandafter\coppe@bancalist
      \expandafter{\coppe@tmp}%
    \advance\count1 by 1}%
  \count1=0
  \@whilenum\count1<\@examiner\do{%
    \protected@edef\coppe@tmp{\noexpand\coppe@membro
      {\csname CoppeExaminerTitle:\the\count1\endcsname}%
      {\csname CoppeExaminerName:\the\count1\endcsname}%
      {\csname CoppeExaminerDegree:\the\count1\endcsname}%
      {\csname CoppeExaminerInst:\the\count1\endcsname}}%
    \expandafter\g@addto@macro\expandafter\coppe@bancalist
      \expandafter{\coppe@tmp}%
    \advance\count1 by 1}%
  \noindent\local@approvedname:\par
  \nohyphens{\singlespacing\coppe@bancalist}\par
  \vspace*{\fill}}
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
        \coppe@selecttitle/\@authname\ \@authsurn. -- \local@cityname:
      UFRJ/COPPE, \coppe@docyear.}\par
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
      UFRJ/COPPE/Programa de \local@deptname, \coppe@docyear.}\par
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
\newcommand\coppe@fichafile{}
\newcommand\coppe@fichapage{1}
\newcommand\fichacatalografica[2][1]{%
  \gdef\coppe@fichapage{#1}\gdef\coppe@fichafile{#2}}
\newcommand\coppe@marcatipo[1]{%
  \ifthenelse{\equal{\coppe@tipoproducao}{#1}}{$\times$}{\phantom{$\times$}}}
\newcommand\coppe@marcavinc[1]{%
  \ifthenelse{\equal{\coppe@projetovinc}{#1}}{$\times$}{\phantom{$\times$}}}
\newcommand\coppe@campo[1]{%
  \ifthenelse{\equal{#1}{}}{\hrulefill}{#1\enspace\hrulefill}}
\newcommand\coppe@checatipo{%
  \ifthenelse{\equal{\coppe@tipoproducao}{}}{}{%
    \ifthenelse{\equal{\coppe@tipoproducao}{bibliografica}\OR
                \equal{\coppe@tipoproducao}{artistica}\OR
                \equal{\coppe@tipoproducao}{tecnologica}\OR
                \equal{\coppe@tipoproducao}{tecnica}}{}{%
      \ClassWarning{coppe}{Unknown \string\tipoproducao{} value
        `\coppe@tipoproducao'. Annex H of the SiBI manual allows only
        bibliografica, artistica, tecnologica or tecnica; no box will be
        ticked}}}}
\newcommand\makefolhaadicional{%
  \clearpage
  \thispagestyle{empty}%
  \coppe@checatipo
  {\singlespacing
  \begin{center}
    {\large\bfseries Informa\c c\~oes Coleta CAPES}
  \end{center}
  \vspace{7mm}
  \noindent Tipo de produ\c c\~ao intelectual:\par
  \vspace{1mm}
  \hspace*{10mm}(\coppe@marcatipo{bibliografica})\enspace Bibliogr\'afica\par
  \hspace*{10mm}(\coppe@marcatipo{artistica})\enspace Art\'{\i}stica\par
  \hspace*{10mm}(\coppe@marcatipo{tecnologica})\enspace Tecnol\'ogica\par
  \hspace*{10mm}(\coppe@marcatipo{tecnica})\enspace T\'ecnica\par
  \vspace{5mm}
  \noindent Projeto de pesquisa vinculado \`a produ\c c\~ao intelectual?\par
  \vspace{1mm}
  \hspace*{10mm}(\coppe@marcavinc{sim})\enspace Sim\par
  \hspace*{10mm}(\coppe@marcavinc{nao})\enspace N\~ao\par
  \vspace{5mm}
  \noindent Nome do projeto de pesquisa:\par
  \vspace{1mm}
  \noindent\coppe@campo{\coppe@nomeprojeto}\par
  \vspace{5mm}
  \noindent \'Area de concentra\c c\~ao da produ\c c\~ao intelectual:\par
  \vspace{1mm}
  \noindent\coppe@campo{\coppe@areaconc}\par
  \vspace{5mm}
  \noindent Ag\^encia(s) de fomento financiadora(s) da produ\c c\~ao
  intelectual:\par
  \vspace{1mm}
  \ifthenelse{\value{coppeagencias}=0}{%
    \noindent\hrulefill\par}{%
    \count1=0
    \@whilenum\count1<\value{coppeagencias}\do{%
      \noindent\hspace*{10mm}\csname CoppeAgencia:\the\count1\endcsname
      \ (\csname CoppeAgenciaSigla:\the\count1\endcsname)\par
      \advance\count1 by 1}}%
  \vspace{9mm}
  \begin{center}
    {\large\bfseries Ficha catalogr\'afica}\par
    \vspace{4mm}
    \ifthenelse{\equal{\coppe@fichafile}{}}{%
      \if@copperascunho
        \makecatalog
      \else
        \framebox[125mm][c]{\parbox[c][62mm][c]{115mm}{\centering\footnotesize
          Espa\c co reservado \`a ficha catalogr\'afica.\\[1ex]
          Gere-a em \texttt{fichacatalografica.sibi.ufrj.br} e inclua o
          arquivo com \texttt{\string\fichacatalografica\{arquivo.pdf\}},
          ou solicite-a \`a biblioteca do seu Programa.}}%
      \fi}{%
      \includegraphics[page=\coppe@fichapage,width=125mm]{\coppe@fichafile}}%
  \end{center}
  \par}}
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
    \local@monthname/\coppe@docyear
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
  \vspace*{7mm}}{%
  \coppe@printkeywords{\coppemainstring{keywordsname}}%
    {CoppeKeyword:}{\value{keywords}}%
  \vspace*{\fill}}
\newenvironment{foreignabstract}{%
  \cleardoublepage
  \thispagestyle{plain}
  \begin{otherlanguage}{\coppe@foreignlang}
  \foreignabstract@toptext\par
  \vspace*{8.6mm}
  \begin{center}
    \sloppy\nohyphens{\MakeUppercase\foreign@title}\par
    \vspace*{13.2mm}
    \@authname\ \@authsurn \par
    \vspace*{7mm}
    \foreign@monthname/\coppe@docyear
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
  \ifnum\value{foreignkeywords}>0
    \coppe@printkeywords{\coppeforeignstring{keywordsname}}%
      {CoppeForeignKeyword:}{\value{foreignkeywords}}%
  \else
    \coppe@printkeywords{\coppeforeignstring{keywordsname}}%
      {CoppeKeyword:}{\value{keywords}}%
  \fi
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
\newenvironment{brazilianabstract}{%
  \cleardoublepage
  \thispagestyle{plain}
  \begin{otherlanguage}{brazilian}
  \abstract@toptext\par
  \vspace*{8.6mm}
  \begin{center}
    \sloppy\nohyphens{\MakeUppercase\local@title}\par
    \vspace*{13.2mm}
    \@authname\ \@authsurn \par
    \vspace*{7mm}
    \local@monthname/\coppe@docyear
  \end{center}\par
  \vspace*{1.5cm}
  \noindent%
  \begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
    \local@advisorstring: &
    \count1=0
    \toks@={}
    \@whilenum \count1<\@advisor \do{%
    \ifcase\count1
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
  \vspace*{7mm}}{%
  \ifnum\value{braziliankeywords}>0
    \coppe@printkeywords{\coppestring{keywordsname}}%
      {CoppeBrazilianKeyword:}{\value{braziliankeywords}}%
  \else
    \coppe@printkeywords{\coppestring{keywordsname}}%
      {CoppeKeyword:}{\value{keywords}}%
  \fi
  \end{otherlanguage}
  \vspace*{\fill}}
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
  \ltx@ifpackageloaded{hyperref}{%
    \def\coppe@bibEnd{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{bib:end}}%
          {{}{\number\c@page}{}{\detokenize{page.}\number\c@page}{}}}}%
    \def\coppe@bibBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{bib:begin}}%
          {{}{\number\c@page}{}{\detokenize{page.}\number\c@page}{}}}}%
    \def\coppe@mainBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{front:pageno}}%
          {{}{\Roman{page}}{}{\detokenize{page.}\romannumeral\c@page}{}}}}%
    \def\coppe@hasLof{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{cat:lofflag}}%
          {{}{\detokenize{:~il.;}}{}{\detokenize{page.}\romannumeral\c@page}{}}}}%
  }{%
    \def\coppe@bibEnd{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{bib:end}}{{}{\number\c@page}{}}}}%
    \def\coppe@bibBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{bib:begin}}{{}{\number\c@page}{}}}}%
    \def\coppe@mainBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{\detokenize{front:pageno}}{{}{\Roman{page}}{}}}}%
    \def\coppe@hasLof{%
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
\newcommand\listabbreviationname{\coppemainstring{listabbreviation}}
\newcommand\listsymbolname{\coppemainstring{listsymbol}}
\newcommand\glossaryname{\coppemainstring{glossary}}
\newcommand\local@advisorstring{Orientador}
\newcommand\foreign@advisorstring{Advisor}
\ifthenelse{\boolean{maledoc}}{%
  \newcommand\local@approvedname{\coppemainstring{approvedmale}}%
}{%
  \newcommand\local@approvedname{\coppemainstring{approvedfemale}}%
}
\ifthenelse{\boolean{maledoc}}{%
  \newcommand\local@approvedonname{\coppemainstring{approvedonmale}}%
}{%
  \newcommand\local@approvedonname{\coppemainstring{approvedonfemale}}%
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
  \local@degname\ em \local@deptname.}%
  \ifthenelse{\equal{\coppe@areaconc}{}}{}{%
    \par\vspace{1ex}%
    \sloppy\nohyphens{\'Area de concentra{\c c}{\~ a}o: \coppe@areaconc.}}%
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
  {\MakeUppercase\local@monthname\ DE \coppe@docyear}
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
\RequirePackage{setspace}
\if@coppedoublespace\doublespacing\else\onehalfspacing\fi
\RequirePackage{hyperref}
\if@coppenumeric
  \RequirePackage[backend=biber,datamodel=coppe,%
    bibstyle=coppe-numeric,citestyle=coppe-numeric,natbib=true]{biblatex}
\else
  \RequirePackage[backend=biber,datamodel=coppe,%
    bibstyle=coppe,citestyle=coppe,natbib=true]{biblatex}
\fi
\defbibheading{bibliography}{%
  \chapter*{\coppestring{references}}%
  \addcontentsline{toc}{chapter}{\coppestring{references}}}
\AtBeginBibliography{\coppe@bibBegin}
\let\coppe@orig@printbibliography\printbibliography
\renewcommand\printbibliography[1][]{%
  \coppe@orig@printbibliography[#1]%
  \coppe@bibEnd}
\newcommand{\annex}{
    \renewcommand{\appendixname}{\coppestring{annex}}%
    \appendix
    \@coppeannextrue
}
%% 
%%
%% End of file `coppe.cls'.
