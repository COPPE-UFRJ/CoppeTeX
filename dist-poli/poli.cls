%%
%% This is file `poli.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% ufrj-poli.dtx  (with options: `compat')
%% 
%% This is the `ufrj-poli' unit style of the `ufrj' document class -- the data
%% and texts of the Escola Politecnica (POLI) of the Federal University of Rio
%% de Janeiro, for its undergraduate projects -- and the `poli' compatibility
%% class, which loads the `ufrj' class with this style. Both are generated from
%% ufrj-poli.dtx by docstrip; edit the .dtx source, not these files.
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
\NeedsTeXFormat{LaTeX2e}[2020/10/01]
\ProvidesClass{poli}[2026/09/23 v5.0 CoppeTeX compatibility class: ufrj with ufrj-poli]
\ClassWarningNoLine{poli}{A classe poli agora e a classe ufrj com o estilo\MessageBreak
  ufrj-poli. Este documento compila como esta, mas troque\MessageBreak
  \string\documentclass[grad]{poli} por\MessageBreak
  \string\documentclass[grad]{ufrj} e acrescente\MessageBreak
  \string\usepackage{ufrj-poli} logo abaixo}
\DeclareOption{pdftex}{}
\DeclareOption{dvips}{}
\DeclareOption{dvipdfm}{}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ufrj}}
\ProcessOptions\relax
\LoadClass{ufrj}
\RequirePackage{ufrj-poli}
\let\ufrjpoli@advisor\advisor
\renewcommand\advisor[4]{\ufrjpoli@advisor[#1]{#2}{#3}{#4}{}}
\let\ufrjpoli@coadvisor\coadvisor
\renewcommand\coadvisor[4]{\ufrjpoli@coadvisor[#1]{#2}{#3}{#4}{}}
\newif\if@ufrjpoliavisoexaminador \@ufrjpoliavisoexaminadortrue
\let\ufrjpoli@examiner\examiner
\renewcommand\examiner[3]{%
  \if@ufrjpoliavisoexaminador
    \ClassWarningNoLine{poli}{A forma antiga do \string\examiner\space nao tem
      instituicao,\MessageBreak e a 3.1.2.1.3(e) a pede: escreva\MessageBreak
      \string\examiner{Nome Sobrenome}{D.Sc.}{UFRJ}}%
    \@ufrjpoliavisoexaminadorfalse
  \fi
  \ufrjpoli@examiner{#1\ #2}{#3}{}}
%% 
%%
%% End of file `poli.cls'.
