% Template for COPPE/UFRJ presentations with LaTeX beamer.
% Adapted from the LUT beamer template.
%
% by Aleksei Mashlakov, mashlakov@gmail.com
%
% Inspired by the template for SINTEF presentations by Federico Zenith,
% which was derived (through several iterations) from Håvard Berland's
% beamerthementnu class.
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

\ProvidesClass{coppebeamer}[2026/01/30]

\RequirePackage{etoolbox}
\newcommand{\@DashColor}{coppeAccent}
\newcommand{\@DashHeight}{1.5mm}

\newcommand{\testcolor}[1]{\colorbox{#1}{\textcolor{#1}{test}} \texttt{#1}}
\newcommand{\hrefcol}[2]{\textcolor{coppeAccent}{\href{#1}{#2}}}


\newbool{COPPEdark}
\PassOptionsToClass{aspectratio=169}{beamer} % Default, may be overridden
\DeclareOption{cyandash}{\renewcommand{\@DashColor}{coppeAccent}}
\DeclareOption{nodash}{\renewcommand{\@DashHeight}{0mm}}
\DeclareOption{light}{\boolfalse{COPPEdark}}
\DeclareOption{dark}{\booltrue{COPPEdark}}
\newcommand{\COPPEtitlepagestyle}{simpletitlepage} % default

\DeclareOption{simpletitlepage}{\renewcommand{\COPPEtitlepagestyle}{simpletitlepage}}
\DeclareOption{backgroundpicturetitlepage}{\renewcommand{\COPPEtitlepagestyle}{backgroundpicturetitlepage}}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax
\LoadClass{beamer}

\usepackage{caladea,carlito}
\renewcommand{\familydefault}{\sfdefault}

\RequirePackage{graphicx,coppecolor,ifthen}
\RequirePackage{tikz}

% Following commands will not be activated for article mode.
\mode<presentation>

% No navigation symbols
\setbeamertemplate{navigation symbols}{}

% phantom items 
\setbeamercovered{transparent} % invisible

% nomenclature
\usepackage[symbols,nomain,acronyms,makeindex,section=subsection]{glossaries-extra}
\newglossary{latin}{lat}{latout}{Latin alphabet}
\newglossary{greek}{grk}{grkout}{Greek alphabet}
\newglossary{sub}{sub}{subout}{Subscripts}
\newglossary{sup}{sup}{supout}{Superscripts}
\newglossary{dimless}{diml}{dimlout}{Dimensionless numbers}
\newglossary{notation}{not}{notout}{Notation}
\glsnoexpandfields
\glstocfalse
% \makeglossaries
\input{nomenclature.tex}

% packages
\usepackage{amsfonts,amsmath,oldgerm}
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\minimize}{minimize} % minimize operator
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{subfig}
\usepackage{tikz}
\usepackage{verbatim}


% line spacing
\linespread{1.1}\selectfont % <---

% item spacing
% \let\tempone\itemize
% \let\temptwo\enditemize
% \renewenvironment{itemize}{\tempone\addtolength{\itemsep}{0.35\baselineskip}}{\temptwo}

% bibliography style
\usepackage[style=numeric,backend=bibtex]{biblatex}
% \usepackage[autocite=footnote,style=authortitle,backend=bibtex]{biblatex} 
\addbibresource{references.bib}

% Set colours (COPPE palette)
\setbeamercolor{alerted text}{fg=coppeWine}
\setbeamercolor{headline}{fg=white,bg=coppeWine}
\setbeamercolor{author}{fg=coppeGraphite}
\setbeamercolor{example text}{fg=coppeAccent,bg=coppeLightGray}
\setbeamercolor{block title}{fg=white,bg=coppeWine}
\setbeamercolor{block body}{fg=coppeGraphite,bg=coppeLightGray}
\setbeamercolor{block body example}{fg=coppeGraphite,bg=coppeLightGray}
\setbeamercolor{caption name}{fg=coppeGraphite}
\newcommand{\@COPPElogo}{logos/COPPE-LOGO-PNG}
\ifbool{COPPEdark}{
    \setbeamercolor{normal text}{fg=white}
    \setbeamercolor{background canvas}{bg=coppeGraphite}
    \setbeamercolor{structure}{fg=coppeAccent}
    \setbeamercolor{frametitle}{fg=white,bg=coppeGraphite}
    \setbeamercolor{title}{fg=white,bg=coppeGraphite}
    \setbeamercolor{footline}{fg=white}
    \setbeamercolor{itemize items}{fg=coppeAccent}
    \renewcommand{\@COPPElogo}{logos/COPPE-LOGO-WHITE-PNG}
}{
    \setbeamercolor{normal text}{fg=coppeGraphite}
    \setbeamercolor{background canvas}{bg=white}
    \setbeamercolor{frametitle}{fg=coppeGraphite,bg=white}
    \setbeamercolor{structure}{fg=coppeAccent}
    \setbeamercolor{footline}{fg=coppeGraphite}
    \setbeamercolor{itemize items}{fg=coppeAccent}
    \renewcommand{\@COPPElogo}{logos/COPPE-LOGO-PNG}
}

% font sizes
\usefonttheme[onlymath]{serif}
\setbeamerfont{author}{size=\footnotesize}
\setbeamerfont{date}{size=\scriptsize}
\setbeamerfont{caption}{size=\scriptsize}
\setbeamerfont{normal text}{size=\footnotesize}
\setbeamerfont{equation}{size=\footnotesize}
\setbeamerfont{subsection in toc}{size=\footnotesize}
\setbeamerfont{section in toc}{size=\normalsize}
\renewcommand*{\bibfont}{\footnotesize}
\setbeamertemplate{itemize/enumerate body begin}{\footnotesize}
\setbeamertemplate{itemize/enumerate subbody begin}{\scriptsize}

% Code to get prettier boxes
\setbeamertemplate{blocks}[rounded][shadow=true]

% Bullets in several levels
\setbeamertemplate{itemize item}{\textbf{\normalsize\guillemotright}}
\setbeamertemplate{itemize subitem}{\normalsize\textendash}
\setbeamertemplate{itemize subsubitem}{\normalsize\textbullet}

% pink squares and triangle for items
\newcommand{\redsquareitem}{\item[\textcolor{coppeWine}{\tiny$\blacksquare$}]}
\newcommand{\redtriangleitem}{\item[\textcolor{coppeWine}{$\blacktriangleright$}]}

% to have a separate numbering for back-up slides 
\usepackage{appendixnumberbeamer}

% table of content in itemize style
\setbeamertemplate{section in toc}[square]
\setbeamertemplate{subsection in toc}[default]

% Define frame title and subtitle layout
\setbeamertemplate{frametitle}
{   \hbox{%
    \begin{beamercolorbox}[wd=.75\paperwidth,ht=17mm,dp=0mm, left]{frametitle}
        \usebeamerfont{frametitle}\MakeUppercase{\insertframetitle}\\
        \vspace{0.1ex}{\textcolor{\@DashColor}{\rule[0ex]{1cm}{\@DashHeight}} 
        \usebeamerfont{framesubtitle}\insertframesubtitle~\vphantom{phantomText}}\\
    \end{beamercolorbox}% 
    \begin{beamercolorbox}[wd=.25\paperwidth,ht=15mm,dp=2mm, left]{frametitle}
    \hfill{\vspace{1.5ex}\includegraphics[height=4ex]{\@COPPElogo} \hspace*{2em}}
    \end{beamercolorbox}
    }%
    \vskip0pt%
}

% 
\makeatletter
\def\COPPE@department{}
% \department prints the current department, but if used as \department{...} it sets it.
\newcommand{\department}{\@ifnextchar\bgroup\COPPE@setdepartment\COPPE@department}
\newcommand{\COPPE@setdepartment}[1]{\def\COPPE@department{#1}}
\newcommand{\setdepartment}[1]{\COPPE@setdepartment{#1}}

% Title background image hook (used by backgroundpicturetitlepage)
\newcommand{\titlebackground}{}
\newcommand{\settitlebackground}[1]{\def\titlebackground{#1}}

\makeatother

\titlegraphic{\includegraphics[height=5ex]{\@COPPElogo}}

% Define the title page

% ---------------------------
% Title page templates
% ---------------------------

% Simple title page (no background picture)
\defbeamertemplate*{title page}{simpletitlepage}{
  \hbox{%
   \begin{beamercolorbox}[wd=0.74\paperwidth,sep=8pt,left]{institute}
      \usebeamerfont{institute}{\department\par \insertinstitute}
    \end{beamercolorbox}
    \begin{beamercolorbox}[wd=0.2\paperwidth,sep=8pt,left]{institute}
      \hfill\includegraphics[height=10mm]{logos/COPPE-LOGO-PNG}
    \end{beamercolorbox}
  }%
  \begin{centering}
    \begin{beamercolorbox}[sep=8pt,left]{title}
      \usebeamerfont{title}\MakeUppercase{\inserttitle}\par%
      {\color{coppeAccent}\rule[0ex]{1cm}{1.2pt}}
    \end{beamercolorbox}%
    \begin{beamercolorbox}[sep=8pt,left]{subtitle}
      \ifx\insertsubtitle\@empty%
      \else%
        \vskip0em%
        {\usebeamerfont{subtitle}\usebeamercolor[fg]{subtitle}\MakeUppercase{\insertsubtitle}\par}%
      \fi%     
    \end{beamercolorbox}
    \vskip0em\par
    \begin{beamercolorbox}[sep=8pt,left]{author}
        \usebeamerfont{author}{Presented by \insertauthor}
    \end{beamercolorbox}
    \begin{beamercolorbox}[sep=8pt,left]{date}
      \usebeamerfont{date}{\insertdate}
    \end{beamercolorbox}%\vskip0.5em
    \end{centering}
}


% Background picture title page (full-bleed image + overlay text + white logo)
\defbeamertemplate*{title page}{backgroundpicturetitlepage}{
  \begin{tikzpicture}[remember picture,overlay]
    \ifx\titlebackground\empty
      % fallback if no background was set
      \path[fill=coppeWine] (current page.south west) rectangle (current page.north east);
    \else
      \node[inner sep=0pt,anchor=center] at (current page.center) {%
        \includegraphics[width=\paperwidth,height=\paperheight]{\titlebackground}%
      };
      % readability overlay
      \path[fill=black,opacity=0.35] (current page.south west) rectangle (current page.north east);
    \fi

    % White COPPE logo (top-left)
    % \node[anchor=north west,xshift=8mm,yshift=-6mm] at (current page.north west) {%
    %   \includegraphics[height=10mm]{logos/COPPE-LOGO-WHITE-PNG}%
    % };

    % White COPPE logo (top-right)
    \node[anchor=north east,xshift=-8mm,yshift=-6mm] at (current page.north east) {%
    \includegraphics[height=10mm]{logos/COPPE-LOGO-WHITE-PNG}%
    };

    % Text block (bottom-left)
    \node[anchor=south west,xshift=10mm,yshift=12mm, text width=0.84\paperwidth] at (current page.south west) {%
      \color{white}%
      {\usebeamerfont{title}\fontsize{22}{26}\selectfont\inserttitle\par}%
      \vspace{2mm}%
      {\usebeamerfont{subtitle}\fontsize{14}{18}\selectfont\insertsubtitle\par}%
      \vspace{4mm}%
      {\usebeamerfont{author}\fontsize{11}{14}\selectfont\insertauthor\par}%
      \vspace{1mm}%
      {\usebeamerfont{institute}\fontsize{10}{13}\selectfont\insertinstitute\par}%
      \vspace{1mm}%
      {\usebeamerfont{date}\fontsize{10}{13}\selectfont\insertdate\par}%
    };
  \end{tikzpicture}
}

% Activate selected title page style (default: simpletitlepage)
\setbeamertemplate{title page}[\COPPEtitlepagestyle]



% Define the bottom of each standard frame
\setbeamertemplate{footline}{
    % bottom bar
    \begin{beamercolorbox}[wd=\paperwidth, ht=10pt, dp=1pt]{footline}
    \usebeamerfont{footline}
    
    \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=south west, 
          xshift=10mm, 
          yshift=.4mm] 
         at (current page.south west) 
         {\insertdate}; 
    \end{tikzpicture}
    
    \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=south west, 
          xshift=35mm, 
          yshift=.4mm] 
          at (current page.south west) 
         {\insertauthor,~\department,~\insertshortinstitute}; 
    \end{tikzpicture}
    
    \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=south east, 
          xshift=-5mm, 
          yshift=0.5mm] 
         at (current page.south east) 
         {\insertframenumber \,/\, \inserttotalframenumber};
    \end{tikzpicture}
    
    \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=south east, 
          xshift=-15mm, 
          yshift=0.4mm] 
          at (current page.south east) 
         {\insertshorttitle}; 
    \end{tikzpicture}
    
    \end{beamercolorbox}
}

% add navigation symbols
\ifbool{COPPEdark}{\setbeamercolor{mycolor}{fg=white}}{\setbeamercolor{mycolor}{fg=coppeGraphite}}
\addtobeamertemplate{footline}{
    \leavevmode%
    \hbox{%
    \begin{beamercolorbox}[wd=\paperwidth,ht=2.75ex,dp=.5ex,right,rightskip=5mm]{mycolor}%
    \usebeamercolor[fg]{navigation symbols}\insertslidenavigationsymbol%
                                           \insertframenavigationsymbol%
                                           \insertsubsectionnavigationsymbol%
                                           \insertsectionnavigationsymbol%
                                           \insertdocnavigationsymbol%
                                           \insertbackfindforwardnavigationsymbol%
    \end{beamercolorbox}%
    }%
    \vskip0.5pt%
}{}

\mode<all>
