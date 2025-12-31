# Test 05: DOI2BIB

## Commands
```bash
# Single DOI
parser doi2bib 10.1038/nature12373

# arXiv ID
parser doi2bib 1706.03762

# From file
parser doi2bib -i dois.txt -o references.bib
```

## Description
Converts DOIs and arXiv IDs to BibTeX citations.

## Expected Output
- BibTeX formatted citation
- Metadata from CrossRef/Semantic Scholar

## Result
✅ **PASS**

## Output - Single DOI
```bibtex
@article{kucsko2013nanometrescale,
  title = {Nanometre-scale thermometry in a living cell},
  author = {G. Kucsko and P. Maurer and N. Yao and ...},
  year = {2013},
  journal = {Nature},
  doi = {10.1038/nature12373},
  eprint = {1304.1068},
  archiveprefix = {arXiv},
  url = {https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4221854}
}
```

## Output - arXiv ID
```bibtex
@misc{vaswani2017attention,
  title = {Attention Is All You Need},
  author = {Ashish Vaswani and Noam Shazeer and ...},
  year = {2017},
  doi = {10.48550/arXiv.1706.03762},
  eprint = {1706.03762},
  archiveprefix = {arXiv},
  primaryclass = {cs.CL},
  url = {https://arxiv.org/pdf/1706.03762.pdf}
}
```

## Output - From File
```
Processing 6 identifiers...
  arXiv:1409.0473...
  arXiv:2009.06732...
  10.5555/3295222.3295349...
    ✗ Failed
  10.18653/v1/N19-1423...
  10.1145/3530811...
  10.1162/neco.1997.9.8.1735...

✓ Wrote 5 entries to from_file.bib
✗ Failed: 1 identifiers
```

## Files Generated
- `output.txt` - Single DOI output
- `output2.txt` - Alternative DOI output
- `from_file.bib` - Batch conversion result
- `output_from_file.txt` - Batch processing log

## Formats Supported
- `bibtex` (default)
- `json` - Full metadata
- `markdown` - Formatted citation

## Notes
- Uses CrossRef API for DOI lookup
- Uses arXiv API for arXiv IDs
- Semantic Scholar as fallback
