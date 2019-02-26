#!/bin/bash
#
# Compile a French document to PDF and HTML
#

name=astro2019
#doconce ipynb2doconce $name.ipynb

options="--encoding=utf-8"

function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}

function common_replacements {
  filename=$1
  # Replace English phrases
  # __Summary.__ is needed for identifying the abstract
  doconce replace Summary Résumé $1
  doconce replace Notice Remarque $1
  doconce replace "Table of contents" "Table des matières" $1
  doconce replace Contents Contenu $1
  doconce replace "Project" "Projet" $1
  doconce replace "Example" "Exemple" $1
}

doconce pygmentize $name.do.txt perldoc
system doconce format pdflatex $name --latex_code_style=pyg-gray $options --latex_font=palatino --latex_admon=grayicon
# Tips: http://folk.uio.no/tobiasvl/latex.html
system common_replacements $name.tex

doconce replace '10pt]{' '10pt,french]{' $name.tex
# package [norsk]{label} requires texlive-lang-norwegian package
doconce subst '% insert custom LaTeX commands...' '\usepackage[french]{babel}\n\n% insert custom LaTeX commands...' $name.tex
system pdflatex -shell-escape $name
#system bibtex $name
system makeindex $name
pdflatex -shell-escape $name
pdflatex -shell-escape $name

# LaTeX Beamer slides
beamertheme=red_shadow
system doconce format pdflatex $name --latex_title_layout=beamer --latex_admon_title_no_period -DBEAMER
editfix ${name}.p.tex
system doconce ptex2tex $name envir=minted
system doconce slides_beamer $name --beamer_slide_theme=$beamertheme
cp $name.tex ${name}-beamer.tex
system common_replacements ${name}-beamer.tex
system pdflatex -shell-escape ${name}-beamer
system pdflatex -shell-escape ${name}-beamer


system doconce format html $name --html_style=bootstrap $options --latex_admon=grayicon
common_replacements $name.html

# Jupyter notebook
doconce format ipynb $name
common_replacements $name.ipynb
# Publish
# Publish
dest=../pub/$name
if [ ! -d $dest ]; then
mkdir $dest
fi
cp -r *.pdf *.html figs $dest
