#!/usr/bin/env bash
rm doc.md 2> /dev/null
for f in docs/desc.md docs/rf.md docs/csu*.md; do (cat "${f}"; echo -e "\n\\pagebreak\n";) >> doc.md; done
# pandoc -s --pdf-engine=xelatex -V geometry:margin=1in -o doc.pdf doc.md
pandoc -o doc.tex doc.md
rm doc.md
