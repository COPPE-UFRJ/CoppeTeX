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
%% \CheckSum{1681}
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
\def\filedate{2025/10/18}
\NeedsTeXFormat{LaTeX2e}[2023/11/01]
\ProvidesClass{Coppe}[\filedate\ \fileversion\ Coppe Dissertations and Thesis]
\LoadClass[12pt,a4paper,twoside]{book}
\RequirePackage{hyphenat}   % Hyphenation control (e.g., \hyp{} and disabling hyphenation in words)
\RequirePackage{lastpage}   % Provides label/anchor for the last page (e.g., page X of \pageref{LastPage})
\RequirePackage{ifthen}     % Basic conditional logic (\ifthenelse) for simple class/package switches
\RequirePackage{graphicx}   % Graphics inclusion and scaling (\includegraphics, rotation, clipping)
\RequirePackage{setspace}   % Line spacing control (\singlespacing, \onehalfspacing, \doublespacing)
\RequirePackage{tabularx}   % Tables with automatic column width (X column) and full-width tabulars
\RequirePackage{etoolbox}   % Robust programming tools: toggles, conditionals, patching (\apptocmd, \pretocmd)
\RequirePackage{eqparbox}   % Equal-width boxes for aligned text blocks across lines/columns
\RequirePackage{ltxcmds}    % Low-level LaTeX kernel helpers used by other packages and internal code
\RequirePackage{expl3}      % LaTeX3 programming layer (token lists, properties, sequences, etc.)
\RequirePackage{xparse}     % High-level interface to define commands/environments (\NewDocumentCommand)
\RequirePackage[spanish,english,brazilian]{babel} % Languages!
\ExplSyntaxOn               % Enable LaTeX3 (expl3) syntax for subsequent definitions
\RequirePackage[T1]{fontenc} % CHECK LuaLaTeX compatibility
\RequirePackage{kvoptions} % Drop traditional options
\SetupKeyvalOptions{family=Coppe, prefix=Coppe@}
\DeclareStringOption[br]{lang}   % br | en | es |
\DeclareStringOption[msc]{degree}% msc | phd | qual | proposal
\DeclareStringOption[number]{bibtype} % number | alpha
\DeclareBoolOption[false]{doublespacing} % oneandhalfspace | doublespace
\ProcessKeyvalOptions*

\newcommand*\bindingoffset{0mm}
\newcommand*\setbindingoffset[1]{\renewcommand*\bindingoffset{#1}}
\RequirePackage[a4paper, % Brazilian standard
bindingoffset=\bindingoffset, % There are no instructions for binding offset, but we have to make a command to change this
%%vcentering=true,%
top=3cm,
bottom=2cm,
inner=3.0cm,
outer=2.0cm]{geometry}
\def\CoppeTeX{{\rm C\kern-.05em{\sc o\kern-.025em p\kern-.025em
p\kern-.025em e}}\kern-.08em
T\kern-.1667em\lower.5ex\hbox{E}\kern-.125emX\spacefactor1000}
\onehalfspacing   % UFRJ/ABNT require 1.5 lines
\ifCoppe@doublespacing % can make it easer to comment
\doublespacing
\fi
\AtBeginEnvironment{quotation}{\singlespacing\small}
\AtEndEnvironment{quotation}{\onehalfspacing\normalsize}
\AtBeginEnvironment{quote}{\singlespacing\small}
\AtEndEnvironment{quote}{\onehalfspacing\normalsize}
\AtBeginEnvironment{figure}{\singlespacing\small}
\AtEndEnvironment{figure}{\onehalfspacing\normalsize}
\AtBeginEnvironment{table}{\singlespacing\small}
\AtEndEnvironment{table}{\onehalfspacing\normalsize}
\AtBeginEnvironment{thebibliography}{\singlespacing}
\AtEndEnvironment{thebibliography}{\onehalfspacing}


\newboolean{maledoc}
\setboolean{maledoc}{false}

\ExplSyntaxOn

\cs_new:Npn \Coppe_degperson_main:
{
\bool_if:NTF \maledoc
{ \Coppe_str_get:nn { degperson / \Coppe@degree / m } { \l_Coppe_lang_main_tl } }
{ \Coppe_str_get:nn { degperson / \Coppe@degree / f } { \l_Coppe_lang_main_tl } }
}

\let\local@degname\Coppe_degperson_main:

\ExplSyntaxOff
\ExplSyntaxOn
\tl_new:N \l_Coppe_lang_main_tl
\tl_new:N \l_Coppe_lang_second_tl
\tl_set:Nn \l_Coppe_lang_main_tl { \Coppe@lang }
\cs_new_protected:Npn \Coppe_set_secondary_lang:
{
\str_case:nnF { \Coppe@lang }
{
{br}{ \tl_set:Nn \l_Coppe_lang_second_tl { en } }
{en}{ \tl_set:Nn \l_Coppe_lang_second_tl { br } }
{es}{ \tl_set:Nn \l_Coppe_lang_second_tl { br } }
}{ \tl_set:Nn \l_Coppe_lang_second_tl { en } }
}
\Coppe_set_secondary_lang:
\cs_new:Npn \Coppe_title_main:
{
\str_case:nnF { \l_Coppe_lang_main_tl }
{ {br}{\local@title} {pt}{\local@title} {en}{\foreign@title} {es}{\foreign@title} }
{\local@title}
}
\cs_new:Npn \Coppe_title_second:
{
\str_case:nnF { \l_Coppe_lang_second_tl }
{ {br}{\local@title} {pt}{\local@title} {en}{\foreign@title} {es}{\foreign@title} }
{\foreign@title}
}


\str_case:nnF { \Coppe@lang }
{
{br}{\selectlanguage{brazilian}}
{en}{\selectlanguage{english}}
{es}{\selectlanguage{spanish}}
}{\selectlanguage{brazilian}} % default

\prop_new:N \g_Coppe_strings_prop
\prop_new:N \g_Coppe_dept_prop

\cs_new_protected:Npn \Coppe_str_set:nnn #1#2#3
{ % #1 = key (e.g., doctype/msc), #2 = lang (br|en|es), #3 = value
\prop_gput:Nnx \g_Coppe_strings_prop { #1 / #2 } { #3 } }
\cs_new_protected:Npn \Coppe_dept_set:nnn #1#2#3
{ % #1 = PESC, #2 = lang, #3 = localized name
\prop_gput:Nnx \g_Coppe_dept_prop { #1 / #2 } { #3 } }

\cs_new:Npn \Coppe_str_get:nn #1#2
{ \prop_item:Nn \g_Coppe_strings_prop { #1 / #2 } }
\cs_new:Npn \Coppe_dept_get:nn #1#2
{ \prop_item:Nn \g_Coppe_dept_prop   { #1 / #2 } }

\cs_new:Npn \Coppe_str_main:n   #1 { \Coppe_str_get:nn  { #1 } { \l_Coppe_lang_main_tl } }
\cs_new:Npn \Coppe_str_second:n #1 { \Coppe_str_get:nn  { #1 } { \l_Coppe_lang_second_tl } }
\cs_new:Npn \Coppe_dept_main:n  #1 { \Coppe_dept_get:nn { #1 } { \l_Coppe_lang_main_tl } }
\cs_new:Npn \Coppe_dept_second:n#1 { \Coppe_dept_get:nn { #1 } { \l_Coppe_lang_second_tl } }

\NewDocumentCommand{\CoppeString}{m}{\Coppe_str_main:n{#1}}
\NewDocumentCommand{\CoppeStringSecond}{m}{\Coppe_str_second:n{#1}}

\NewDocumentCommand{\department}{m}{
\global\def\local@deptname   {\Coppe_dept_main:n{#1}}
\global\def\foreign@deptname {\Coppe_dept_second:n{#1}}
}

\ExplSyntaxOff
\InputIfFileExists{Coppe-lang-br.def}{}{\ClassWarning{Coppe}{Coppe-lang-br.def not found}}
\InputIfFileExists{Coppe-lang-en.def}{}{\ClassWarning{Coppe}{Coppe-lang-en.def not found}}
\InputIfFileExists{Coppe-lang-es.def}{}{\ClassWarning{Coppe}{Coppe-lang-es.def not found}}
\ExplSyntaxOn
\cs_new_protected:Npn \Coppe_setup_degree_strings:
{
\tl_gset:Nx \g_Coppe_degreename_tl
{ \Coppe_str_get:nn { degname / \Coppe@degree } { \l_Coppe_lang_main_tl } }
\tl_gset:Nx \g_Coppe_degreename_second_tl
{ \Coppe_str_get:nn { degname / \Coppe@degree } { \l_Coppe_lang_second_tl } }

\tl_gset:Nx \g_Coppe_doctype_tl
{ \Coppe_str_get:nn { doctype / \Coppe@degree } { \l_Coppe_lang_main_tl } }
\tl_gset:Nx \g_Coppe_doctype_second_tl
{ \Coppe_str_get:nn { doctype / \Coppe@degree } { \l_Coppe_lang_second_tl } }

\tl_gset_eq:NN \@degreename \g_Coppe_degreename_tl
\tl_gset_eq:NN \local@doctype \g_Coppe_doctype_tl
}

\cs_new:Npn \Coppe_month_main:
{
\monthname % in whatever language is currently selected (we selected main above)
}
\cs_new_protected:Npn \Coppe_month_second:
{
\begingroup
\str_case:nnF { \l_Coppe_lang_second_tl }
{ {br}{\selectlanguage{brazilian}}
{en}{\selectlanguage{english}}
{es}{\selectlanguage{spanish}} }
{ \selectlanguage{english} }
\monthname
\endgroup
}

\cs_new:Npn \local@monthname   { \Coppe_month_main: }
\cs_new:Npn \foreign@monthname { \Coppe_month_second: }

\cs_new:Npn \Coppe_listabbrev_main:   { \Coppe_str_main:n   { listabbreviationname } }
\cs_new:Npn \Coppe_listsymbols_main:  { \Coppe_str_main:n   { listsymbolname } }
\cs_new:Npn \Coppe_glossary_main:     { \Coppe_str_main:n   { glossaryname } }

\cs_new:Npn \Coppe_advisor_label_main:
{
\int_compare:nNnTF { \@advisor } > { 1 }
{ \Coppe_str_main:n { advisors_label } } % plural
{ \Coppe_str_main:n { advisor_label } }  % singular
}
\cs_new:Npn \Coppe_advisor_label_second:
{
\int_compare:nNnTF { \@advisor } > { 1 }
{ \Coppe_str_second:n { advisors_label } }
{ \Coppe_str_second:n { advisor_label } }
}

\cs_new:Npn \listabbreviationname { \Coppe_listabbrev_main: }
\cs_new:Npn \listsymbolname       { \Coppe_listsymbols_main: }
\cs_new:Npn \glossaryname         { \Coppe_glossary_main: }
\cs_new:Npn \local@advisorstring  { \Coppe_advisor_label_main: }
\cs_new:Npn \foreign@advisorstring{ \Coppe_advisor_label_second: }

\cs_new:Npn \Coppe_approved_main:
{
\Coppe_str_main:n { approved_by }
}

\AtBeginDocument{\Coppe_setup_degree_strings:}

\ExplSyntaxOff


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
  \setcounter{page}{2}
  \makefrontpage
  \clearpage
  \pagestyle{plain}
  \makecatalog%
}
\renewcommand\mainmatter{%
  \Coppe@mainBegin
  \cleardoublepage
  \@mainmattertrue
  \pagestyle{plain}
  \pagenumbering{arabic}}
\renewcommand\backmatter{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi}
\renewcommand\maketitle{%
  \pagenumbering{alph}
  \ltx@ifpackageloaded{hyperref}{\Coppe@hypersetup}{}%
  \begin{titlepage}
  \begin{flushleft}
  \vspace*{1.5mm}
  \setlength\baselineskip{0pt}
  \setlength\parskip{1mm}
  \makebox[20mm][c]{\hspace{4.8cm}\includegraphics{Coppe-logo}}
  \end{flushleft}
  \vspace{1.05cm}
  \begin{center}
\nohyphens{\MakeUppercase{\Coppe_title_main:}}\par
\str_if_eq:VnF \l_Coppe_lang_second_tl {\l_Coppe_lang_main_tl}
{ \vspace{2mm}\nohyphens{\MakeUppercase{\Coppe_title_second:}}\par }
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
\sloppy\nohyphens{\MakeUppercase{\Coppe_title_main:}}\par
\str_if_eq:VnF \l_Coppe_lang_second_tl {\l_Coppe_lang_main_tl}
{ \vspace{2mm}\sloppy\nohyphens{\MakeUppercase{\Coppe_title_second:}}\par }
\vspace*{7mm}
{\@authname\ \@authsurn}\par
\end{center}\par
\vspace*{4mm}
\frontpage@maintext
\vspace*{16mm}
\vspace*{20mm}
\noindent\begin{tabularx}{\textwidth}[b]{@{}l@{ }>{\raggedright\arraybackslash}X@{}}
\Coppe_approved_main:  & % <-- i18n “Approved by”
\count1=0
\toks@={}
\@whilenum \count1<\@examiner \do{%
\ifcase\count1
\toks@=\expandafter{\csname CoppeExaminer:\the\count1\endcsname\\}
\else
\toks@=\expandafter\expandafter\expandafter{%
\expandafter\the\expandafter\toks@
\expandafter&\expandafter\space
\csname CoppeExaminer:\the\count1\endcsname\\
}%
\fi
\advance\count1 by 1}
\the\toks@
\end{tabularx}\par

  \vspace*{\fill}
  \frontpage@bottomtext}
\newcommand\Coppe@hypersetup{%
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
  pdfsubject={\local@doctype\ de \@degreename\ em \local@deptname\ da Coppe/UFRJ},
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
      UFRJ/Coppe, \number\year.}\par
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
      UFRJ/Coppe/Programa de \local@deptname, \number\year.}\par
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
      II. \local@universityname, Coppe, Programa de \local@deptname.
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
  \clearpage
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
  \vspace*{\fill}
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
\clearpage
\thispagestyle{plain}
\begingroup
\str_case:nnF { \l_Coppe_lang_second_tl }
{ {br}{\selectlanguage{brazilian}} {en}{\selectlanguage{english}} {es}{\selectlanguage{spanish}} }
{ \selectlanguage{english} }
\foreignabstract@toptext\par
\vspace*{8.6mm}
\begin{center}
\sloppy\nohyphens{\MakeUppercase{\Coppe_title_second:}}\par
\vspace*{13.2mm}
\@authname\ \@authsurn \par
\vspace*{7mm}
\foreign@monthname/\number\year
\end{center}\par
\vspace*{\fill}
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
  \end{tabularx}
  \vspace*{2mm}
  \noindent\foreign@deptstring: \foreign@deptname\par
  \vspace*{7mm}}{%
  \endgroup % restore original language
\vspace*{\fill}
}
\renewcommand\listoffigures{%
    \Coppe@hasLof
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
    \def\Coppe@bibEnd{%
      \immediate\write\@auxout{%
        \string\newlabel{bib:end}{{}{\arabic{page}}{}{page.\arabic{page}}{}}}}%
    \def\Coppe@bibBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{bib:begin}{{}{\arabic{page}}{}{page.\arabic{page}}{}}}}%
    \def\Coppe@mainBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{front:pageno}{{}{\Roman{page}}{}{page.\roman{page}}{}}}}%
    \def\Coppe@hasLof{%
      \immediate\write\@auxout{%
        \string\newlabel{cat:lofflag}{{}{:~il.;}{}{page.\roman{page}}{}}}}%
  }{%
    \def\Coppe@bibEnd{%
      \immediate\write\@auxout{%
      \string\newlabel{bib:end}{{}{\arabic{page}}{}}}}%
    \def\Coppe@bibBegin{%
      \immediate\write\@auxout{%
      \string\newlabel{bib:begin}{{}{\arabic{page}}{}}}}%
    \def\Coppe@mainBegin{%
      \immediate\write\@auxout{%
        \string\newlabel{front:pageno}{{}{\Roman{page}}{}}}}%
    \def\Coppe@hasLof{%
      \immediate\write\@auxout{%
        \string\newlabel{cat:lofflag}{{}{:~il.;}{}}}}%
  }%
}
\newdimen\bibindent%
\setlength\bibindent{1.5em}%
\renewenvironment{thebibliography}[1]%
     {\onehalfspacing%
      \chapter*{\bibname}%
      \addcontentsline{toc}{chapter}{\bibname}%
      \Coppe@bibBegin
      \list{\@biblabel{\@arabic\c@enumiv}}%
           {\setlength{\labelwidth}{0ex}%
            \setlength{\leftmargin}{9.0ex}%
            \setlength{\itemindent}{-9.0ex}%
            \advance\leftmargin\labelsep%
            \@openbib@code%
            \usecounter{enumiv}%
            \let\p@enumiv\@empty%
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
      \sloppy%
      \clubpenalty4000%
      \@clubpenalty \clubpenalty%
      \widowpenalty4000%
      \sfcode`\.\@m}%
     {\def\@noitemerr%
       {\@latex@warning{Empty `thebibliography' environment}}%
       \Coppe@bibEnd
      \endlist}
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
  Coppe, da \local@universityname, como parte dos requisitos
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
  \sloppy\nohyphens{{\` a} Coppe/UFRJ como parte dos requisitos
  necess{\' a}rios para a obten{\c c}{\~ a}o do grau de
  \local@degname\ em Ci{\^ e}ncias (\@degree)}
}
\newcommand\foreignabstract@toptext{%
  \noindent \sloppy\nohyphens{Abstract of \foreign@doctype\ presented to
  Coppe/UFRJ as a partial fulfillment of the requirements for the
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
