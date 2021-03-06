PDFLATEX=pdflatex
LATEXMK=latexmk

# name of the main tex file
MAIN=main
PREAMBLE=preamble
TEXS=$(wildcard ./chapters/*.tex)
TABLES=$(wildcard ./tables/*.*)
FIGURES=$(wildcard ./images/*.*)
BIBTEX=$(wildcard ./literatures/*.bib)
ALL=$(MAIN).tex $(PREAMBLE).fmt $(TEXS) $(FIGURES) $(TABLES) $(BIBTEX)

.PHONY: all clean debug

all: $(MAIN).pdf

# rule for create the main file using latexmk and pdflatex
$(MAIN).pdf : $(ALL)
	$(LATEXMK) -bibtex -pdf -pdflatex="$(PDFLATEX) -shell-escape -fmt=$(PREAMBLE) -interaction=nonstopmode -synctex=1" $<

# rule for create compiled preamble file
$(PREAMBLE).fmt : $(PREAMBLE).tex
	$(PDFLATEX) -ini -jobname="$(PREAMBLE)" "&pdflatex $(PREAMBLE).tex\dump"

# clean all the file
clean:
	$(LATEXMK) -C

debug: $(MAIN).tex $(PREAMBLE).fmt $(TEXS) $(FIGURES)
	$(PDFLATEX) -fmt=$(PREAMBLE) -file-line-error $<
