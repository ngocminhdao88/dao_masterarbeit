PDFLATEX=pdflatex.exe
LATEXMK=latexmk.exe
PDF_VIEWER=start "SumatraPDF.exe"

# name of the main tex file
MAIN=main
PREAMBLE=preamble
TEXS=$(wildcard ./chapters/*.tex)
TABLES=$(wildcard ./tables/*.*)
FIGURES=$(wildcard ./images/*.*)
BIBTEX=$(wildcard ./literatures/*.bib)
ALL=$(MAIN).tex $(PREAMBLE).fmt $(TEXS) $(FIGURES) $(TABLES) $(BIBTEX)

.PHONY: all clean view debug

all: $(MAIN).pdf

# rule for create the main file using latexmk and pdflatex
$(MAIN).pdf : $(ALL)
	$(LATEXMK) -bibtex -pdf -pdflatex="$(PDFLATEX) -fmt=$(PREAMBLE) -synctex=1 -interaction=nonstopmode" $<

# rule for create compiled preamble file
$(PREAMBLE).fmt : $(PREAMBLE).tex
	$(PDFLATEX) -ini -jobname="$(PREAMBLE)" "&pdflatex $(PREAMBLE).tex\dump"

# clean all the file
clean:
	$(LATEXMK) -C

# view the pdf file
view: $(MAIN).pdf
	$(PDF_VIEWER) -reuse-instance $<

debug: $(MAIN).tex $(PREAMBLE).fmt $(TEXS) $(FIGURES)
	$(PDFLATEX) -fmt=$(PREAMBLE) -file-line-error $<
