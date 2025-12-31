# Step 5: DOI to BibTeX Conversion

## Command
```bash
parser doi2bib -i step1_parse_refs_regular/dois.txt \
  -o step5_doi2bib/references.bib
```

## Input
**File:** `dois.txt`
```
arXiv:2303.08774
arXiv:2407.21783
arXiv:2302.13971
10.1038/s41586-020-2649-2
10.1038/nature14539
10.18653/v1/N19-1423
10.1109/ICCV48922.2021.00986
```

## Results
```
✓ Wrote 6 entries to references.bib
✗ Failed: 1 identifier
```

**Success Rate: 86% (6/7)**

## Successful Conversions (6)

| Identifier | Citation Key | Title |
|------------|--------------|-------|
| arXiv:2303.08774 | achiam2023gpt4 | GPT-4 Technical Report |
| arXiv:2407.21783 | dubey2024llama | The Llama 3 Herd of Models |
| arXiv:2302.13971 | touvron2023llama | LLaMA: Open and Efficient Foundation Language Models |
| 10.1038/s41586-020-2649-2 | harris2020array | Array programming with NumPy |
| 10.18653/v1/N19-1423 | devlin2019bert | BERT: Pre-training of Deep Bidirectional Transformers |
| 10.1109/ICCV48922.2021.00986 | liu2021swin | Swin Transformer |

## Failed Conversion (1)

| Identifier | Reason |
|------------|--------|
| `10.1038/nature14539` | DOI resolver error / metadata unavailable |

## Output Sample
```bibtex
@misc{achiam2023gpt4,
  title = {GPT-4 Technical Report},
  author = {Josh Achiam and Steven Adler and Sandhini Agarwal and ...},
  year = {2023},
  eprint = {2303.08774},
  archiveprefix = {arXiv},
  primaryclass = {cs.CL},
  url = {https://arxiv.org/pdf/2303.08774.pdf}
}

@article{harris2020array,
  title = {Array programming with NumPy},
  author = {Charles R. Harris and K. Jarrod Millman and ...},
  journal = {Nature},
  volume = {585},
  pages = {357--362},
  year = {2020},
  doi = {10.1038/s41586-020-2649-2}
}
```

## Sources Used
- **arXiv API** - For arXiv identifiers
- **CrossRef API** - For DOI metadata
- **Semantic Scholar** - Fallback for missing metadata

## Output Files
| File | Description |
|------|-------------|
| `references.bib` | 6 BibTeX entries |
| `output.txt` | Command execution log |

## Status: ✅ PASS (86% success rate)
