# bibtex_corrector
A few Python codes to correct the bibtex downloaded from Google Scholar
## add_url.py
Some BibTeX may not contain the "url" field, the hyperlink to access the references. One can of course add these links manually, which is very time-consuming for a lot of references. 
This Python script first finds the BibTeX blocks where the URL fields are missing. Then, for each of them, it performs a Google search about the title and appends the first URL link of the search to the BibTeX blocks. It will print out all these links and please double-check them!
### Dependency
Based on googlesearch, which can be installed by 
```pip install googlesearch-python```
## capital_letters_in_title.py
Some bib styles default the titles to be purely lowercase letters except for the first letter. For example, chemical formulas like YBaCuO will appear as ybacuo. This script is doing a very simple thing to correct this: it adds a pair of braces "{}" to the "title" field. 
## remove_repeat_bib.py
Sometimes we have a lot of repeated BibTex blocks in our .bib file, particularly when we combine two .bib files together. This script helps to remove all the repeated BibTex blocks. If it finds repeated BibTex blocks, the convention is to keep only the last one. 
