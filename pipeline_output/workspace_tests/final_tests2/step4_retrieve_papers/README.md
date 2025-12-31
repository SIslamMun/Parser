# Step 4: Retrieve Papers (Batch Download)

## Command
```bash
parser batch step1_parse_refs_regular/batch.json \
  -o step4_retrieve_papers -n 3
```

## Input
| Property | Value |
|----------|-------|
| File | `batch.json` |
| Papers | 17 entries |
| Concurrency | 3 parallel downloads |

## Results Summary
```
✓ Downloaded: 13
⊘ Skipped: 1
✗ Failed: 3
```

**Success Rate: 76% (13/17)**

## Downloaded Papers (13)

| # | Filename | Size |
|---|----------|------|
| 1 | Achiam_2023_GPT-4_Technical_Report.pdf | 5.2 MB |
| 2 | Devlin_2019_paper.pdf | 775 KB |
| 3 | Dubey_2024_The_Llama_3_Herd_of_Models.pdf | 9.8 MB |
| 4 | Harris_2020_Array_programming_with_NumPy.pdf | 1.2 MB |
| 5 | LeCun_2015_Deep_learning.pdf | 690 KB |
| 6 | Liu_2021_Swin_Transformer_Hierarchical_Vision_Transformer.pdf | 1.4 MB |
| 7 | Touvron_2023_LLaMA_Open_and_Efficient_Foundation.pdf | 727 KB |
| 8 | Unknown_XXXX_An_Image_is_Worth_16x16_Words.pdf | 3.3 MB |
| 9 | Unknown_XXXX_An_Image_is_Worth_16x16_Words_Transformers.pdf | 3.7 MB |
| 10 | Unknown_XXXX_BERT_Pre-training_of_Deep_Bidirectional.pdf | 775 KB |
| 11 | Unknown_XXXX_Deep_Learning.pdf | 690 KB |
| 12 | Unknown_XXXX_GPT-4_Technical_Report.pdf | 5.2 MB |
| 13 | Unknown_XXXX_LLaMA_Open_and_Efficient_Foundation.pdf | 727 KB |

## Failed Papers (3) - Detailed Analysis

### 1. `10.14293/s2199-1006.1.sor-uncat.a7759461.v1.raugfi`
**Paper:** Review of "Array programming with NumPy"  
**Publisher:** ScienceOpen  
**Failure Reason:** This is a **peer review DOI**, not the actual paper DOI
- Unpaywall: No OA version found
- arXiv: Not an arXiv paper
- PMC: No PMC ID for this DOI
- Semantic Scholar: PDF download failed (review metadata, not paper)
- OpenAlex: PDF download failed

**Root Cause:** The DOI is for a peer review submission, not the NumPy paper itself. The actual NumPy paper DOI is `10.1038/s41586-020-2649-2` (which was downloaded successfully).

---

### 2. `10.1007/978-3-031-84300-6_13`
**Paper:** "Is Attention All You Need?" (Book chapter)  
**Publisher:** Springer  
**Failure Reason:** **Paywalled book chapter**
- Unpaywall: No OA version found
- arXiv: Not an arXiv paper (searched wrong title)
- PMC: No PMC ID
- Semantic Scholar: No open access PDF
- OpenAlex: No OA URL

**Root Cause:** This is a Springer book chapter (ISBN 978-3-031-84300-6), not the original "Attention Is All You Need" paper (arXiv:1706.03762). Book chapters are typically paywalled.

---

### 3. `10.1016/b978-1-4377-2352-6.00004-3`
**Paper:** "Camelid Herd Health and Nutrition"  
**Publisher:** Elsevier  
**Failure Reason:** **Wrong paper - title mismatch**
- Unpaywall: No OA version found
- arXiv: Searched "Camelid Herd Health" (not ML paper)
- PMC: No PMC ID
- Semantic Scholar: No open access PDF
- OpenAlex: No OA URL

**Root Cause:** This DOI was incorrectly matched. "Llama" in the context refers to Meta's language model, but this DOI is for a veterinary textbook about actual llamas (camelids). This is a **false positive from reference extraction**.

---

## Failure Summary

| DOI | True Cause | Category |
|-----|------------|----------|
| `10.14293/...` | Peer review DOI, not paper | Wrong identifier type |
| `10.1007/...` | Springer book chapter paywall | Paywalled content |
| `10.1016/...` | Wrong paper (llama animal vs LLaMA AI) | False positive |

## Skipped Papers (1)
- Already existed in output directory

## Acquisition Sources Used
1. **arXiv** - Open access preprints
2. **Unpaywall** - Legal open access versions
3. **Semantic Scholar** - Paper metadata and PDFs
4. **PMC** - PubMed Central open access
5. **OpenAlex** - Open scholarly metadata

## Notes
- Some duplicates exist (same paper via different identifiers)
- Paywalled content (Springer, Elsevier) requires VPN or manual download
- Institutional access (EZProxy) was configured but some papers still blocked

## Output Structure
```
step4_retrieve_papers/
├── output.txt              # Command log
├── *.pdf                   # Downloaded papers (13)
└── failed/                 # Failed download info
```

## Status: ✅ PASS (76% success rate)
