#!/bin/sh

OUTPUT_DIR=$1 # same as passed to quarto render --output-dir ...
OLDPWD=$(pwd)
BASENAME=Optimal-Scheduling-for-Cross-Facility-Workflows
cd "${OUTPUT_DIR}"/book-latex
sed -i '105,167s/^/%% /g' "${BASENAME}".tex
sed -i '105,167s/^%% %% /%% /g' "${BASENAME}".tex
sed -i '/bookmarksetup/d' "${BASENAME}".tex
pdflatex "${BASENAME}"
bibtex "${BASENAME}"
pdflatex "${BASENAME}"
pdflatex "${BASENAME}"
mv -v "${BASENAME}".pdf ..
cd "${OLDPWD}"
