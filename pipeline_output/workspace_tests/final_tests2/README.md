# Pipeline Test Report - Transformer Architecture Research Document

> Generated: December 31, 2025
> Input: `research document/research_report.md`
> Output: `final_tests2/`

## Pipeline Overview

| Step | Command | Status | Results |
|------|---------|--------|---------|
| 1 | `parse-refs` (regex) | ✅ PASS | 31 references found |
| 2 | `parse-refs --agent claude` | ⚠️ SKIPPED | Rate limit hit |
| 3 | Comparison | ⚠️ SKIPPED | No agent results |
| 4 | `batch` retrieve | ✅ PASS | 13/17 downloaded |
| 5 | `doi2bib` | ✅ PASS | 6/7 converted |
| 6 | `verify` | ✅ PASS | 6/6 verified |

---

## Step 1: Parse References (Regular/Regex)

### Command
```bash
parser parse-refs "research document/research_report.md" \
  -o step1_parse_refs_regular \
  --export-batch --export-dois
```

### Input
- **File:** `research document/research_report.md`
- **Size:** 17,737 bytes
- **Topic:** Transformer Architecture and Attention Mechanisms

### Output
| File | Description |
|------|-------------|
| `references.json` | Structured reference data |
| `references.md` | Human-readable list |
| `batch.json` | 17 papers for download |
| `dois.txt` | 7 DOI/arXiv identifiers |

### Results
```
Found 31 references (regular):
  github: 4
  arxiv: 3
  doi: 4
  paper: 10
  pdf: 1
  youtube: 3
  website: 6
```

### Analysis
- **Strong extraction** of academic references (DOIs, arXiv, papers)
- **GitHub repos detected:** pytorch/pytorch, huggingface/transformers, etc.
- **YouTube videos found:** 3 educational videos
- **Deduplication:** Applied automatically

---

## Step 2: Parse References (Agent - Claude)

### Command
```bash
parser parse-refs "research document/research_report.md" \
  -o step2_parse_refs_agent --agent claude
```

### Status: ⚠️ SKIPPED

### Reason
- Claude CLI rate limit hit (resets at 12pm America/Chicago)
- The `--agent claude` option uses Claude Agent SDK
- No API key required - uses Claude Pro subscription via CLI

### To Retry Later
```bash
parser parse-refs "research document/research_report.md" \
  -o step2_parse_refs_agent --agent claude
```

---

## Step 3: Comparison

### Status: ⚠️ SKIPPED

No agent results available for comparison.

### When Available
The comparison would show:
- Regular vs Agent reference counts
- Missing references in each
- Quality of metadata extraction
- Precision/recall analysis

---

## Step 4: Retrieve Papers

### Command
```bash
parser batch step1_parse_refs_regular/batch.json \
  -o step4_retrieve_papers -n 3
```

### Input
- **File:** `batch.json` (17 papers)
- **Concurrency:** 3 parallel downloads

### Results
```
✓ Downloaded: 13
⊘ Skipped: 1
✗ Failed: 3
```

### Downloaded Papers (13)
| Filename | Size |
|----------|------|
| Achiam_2023_GPT-4_Technical_Report.pdf | 5.2 MB |
| Devlin_2019_paper.pdf | 775 KB |
| Dubey_2024_The_Llama_3_Herd_of_Models.pdf | 9.8 MB |
| Harris_2020_Array_programming_with_NumPy.pdf | 1.2 MB |
| LeCun_2015_Deep_learning.pdf | 690 KB |
| Liu_2021_Swin_Transformer_Hierarchical_Vision_Transformer.pdf | 1.4 MB |
| Touvron_2023_LLaMA_Open_and_Efficient_Foundation.pdf | 727 KB |
| Unknown_XXXX_An_Image_is_Worth_16x16_Words.pdf | 3.3 MB |
| Unknown_XXXX_An_Image_is_Worth_16x16_Words_Transformers.pdf | 3.7 MB |
| Unknown_XXXX_BERT_Pre-training_of_Deep_Bidirectional.pdf | 775 KB |
| Unknown_XXXX_Deep_Learning.pdf | 690 KB |
| Unknown_XXXX_GPT-4_Technical_Report.pdf | 5.2 MB |
| Unknown_XXXX_LLaMA_Open_and_Efficient_Foundation.pdf | 727 KB |

### Failed Papers (3)
- `10.14293/s2199-1006.1.sor-uncat.a7759461.v1.raugfi` - Invalid DOI
- `10.1007/978-3-031-84300-6_13` - Springer paywalled
- `10.1016/b978-1-4377-2352-6.00004-3` - Elsevier paywalled

### Analysis
- **76% success rate** (13/17)
- Most failures due to paywalled content (Springer, Elsevier)
- Some duplicates downloaded (same paper via DOI and title)

---

## Step 5: DOI to BibTeX

### Command
```bash
parser doi2bib -i step1_parse_refs_regular/dois.txt \
  -o step5_doi2bib/references.bib
```

### Input
```
arXiv:2303.08774
arXiv:2407.21783
arXiv:2302.13971
10.1038/s41586-020-2649-2
10.1038/nature14539
10.18653/v1/N19-1423
10.1109/ICCV48922.2021.00986
```

### Results
```
✓ Wrote 6 entries to references.bib
✗ Failed: 1 identifier (10.1038/nature14539)
```

### Output Sample
```bibtex
@misc{achiam2023gpt4,
  title = {GPT-4 Technical Report},
  author = {Josh Achiam and Steven Adler and ...},
  year = {2023},
  eprint = {2303.08774},
  archiveprefix = {arXiv},
  primaryclass = {cs.CL},
  url = {https://arxiv.org/pdf/2303.08774.pdf}
}
```

---

## Step 6: Verify Citations

### Command
```bash
parser verify step5_doi2bib/references.bib -o step6_verify
```

### Results
```
Total verified: 6
Total failed: 0

Breakdown:
  Verified: 0 (CrossRef matches)
  arXiv: 6 (arXiv validated)
  Searched: 0
  Website: 0
  Manual: 0
  Failed: 0
```

### Output Files
| File | Content |
|------|---------|
| `verified.bib` | 6 verified entries |
| `failed.bib` | 0 entries |
| `report.md` | Verification report |

---

## Summary

### Pipeline Success Rate
| Metric | Value |
|--------|-------|
| References Extracted | 31 |
| Papers Downloaded | 13/17 (76%) |
| DOIs Converted | 6/7 (86%) |
| Citations Verified | 6/6 (100%) |

### Key Findings
1. **Regex parsing** works well for standard academic documents
2. **Institutional auth** enabled (EZProxy configured for IIT)
3. **Agent parsing** requires Claude CLI quota (rate limited today)
4. **Some duplicates** exist (same paper matched by DOI and title)
5. **Paywalled papers** require VPN or manual acquisition

### Files Structure
```
final_tests2/
├── research document/
│   ├── research_metadata.json
│   └── research_report.md          # INPUT
├── step1_parse_refs_regular/
│   ├── output.txt
│   ├── references.json
│   ├── references.md
│   ├── batch.json
│   └── dois.txt
├── step2_parse_refs_agent/
│   └── output.txt                  # SKIPPED
├── step3_comparison/
│   └── output.txt                  # SKIPPED
├── step4_retrieve_papers/
│   ├── output.txt
│   ├── *.pdf (13 files)
│   └── failed/
├── step5_doi2bib/
│   ├── output.txt
│   └── references.bib
├── step6_verify/
│   ├── output.txt
│   ├── verified.bib
│   ├── failed.bib
│   └── report.md
└── README.md                       # This file
```
