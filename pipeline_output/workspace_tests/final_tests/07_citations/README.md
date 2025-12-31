# Test 07: Citations

## Command
```bash
parser citations "10.1038/nature12373" --direction citations -n 5
```

## Description
Gets citation graph for a paper from Semantic Scholar API.

## Expected Output
- List of papers citing this paper
- Paper metadata (title, authors, year, DOI)
- Formatted output

## Result
✅ **PASS**

## Output
```
Fetching citations for DOI:10.1038/nature12373...
  Found 5 citing papers
# Papers citing this work (5)

1. Linlin Li, Lingxuan Kong, Jingying Chen et al. (2026). 
   Charge compensation boosts luminous efficiency...
   DOI:10.1016/j.jlumin.2025.121725

2. Tao Hu, Kun Huang, Xinhui He et al. (2026). 
   Integrated portable dual-mode multimorphic...
   DOI:10.1016/j.measurement.2025.119628

3. Jia Su, Zenghao Kong, Fei Kong et al. (2025). 
   Double-Layered Silica-Engineered Fluorescent...

4. Dannareli Barron-Ortiz, Enric Pérez-Parets et al. (2025). 
   Internal 3D temperature mapping...
   DOI:10.3762/bjnano.16.159

5. H. Kono, H. Yukawa, Takeshi Hiromoto et al. (2025). 
   Quantum Life Science: A Paradigm...
   DOI:10.1021/acsnano.4c14828
```

## Options
- `--direction` - citations, references, or both
- `-n, --limit` - Maximum results
- `--format` - json, text, or bibtex
- `-o, --output` - Output file

## Formats
```bash
# Text (default)
parser citations "DOI" --format text

# JSON
parser citations "DOI" --format json -o citations.json

# BibTeX
parser citations "DOI" --format bibtex -o refs.bib
```

## Notes
- Uses Semantic Scholar API
- Use `--s2-key` for higher rate limits
- Both DOI and arXiv IDs supported
