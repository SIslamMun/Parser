# Test 11: Individual Sources

## Commands
```bash
# arXiv
parser retrieve arXiv:2005.11401 -o ./output

# OpenAlex
parser retrieve --doi "10.1038/nature12373" -o ./output

# ACL Anthology  
parser retrieve --doi "10.18653/v1/2020.acl-main.747" -o ./output

# bioRxiv
parser retrieve --doi "10.1101/2020.04.27.064501" -o ./output

# Semantic Scholar
parser retrieve --doi "10.18653/v1/P18-1238" -o ./output

# Frontiers
parser retrieve --doi "10.3389/frai.2021.684004" -o ./output
```

## Description
Tests individual acquisition sources for paper retrieval.

## Results

| Source | DOI/ID | Status | Notes |
|--------|--------|--------|-------|
| arXiv | arXiv:2005.11401 | ✅ PASS | RAG paper downloaded |
| OpenAlex | 10.1038/nature12373 | ✅ PASS | Via OpenAlex |
| Unpaywall | 10.18653/v1/2020.acl-main.747 | ✅ PASS | ACL paper via Unpaywall |
| Unpaywall | 10.18653/v1/P18-1238 | ✅ PASS | Another ACL paper |
| bioRxiv | 10.1101/2020.04.27.064501 | ❌ FAIL | Not found |
| Frontiers | 10.3389/frai.2021.684004 | ❌ FAIL | Not found |

## Files Generated
- `Lewis_2020_Retrieval-Augmented_Generation_for_Knowledge-Inten.pdf`
- `Kucsko_2013_Nanometre-scale_thermometry_in_a_living_cell.pdf`
- `Conneau_2020_Unsupervised_Cross-lingual_Representation_Learning.pdf`
- `Sharma_2018_Conceptual_Captions_A_Cleaned_Hypernymed_Image_Alt.pdf`

## Source Priority
1. unpaywall - Legal open access
2. arxiv - Preprints
3. pmc - Biomedical
4. biorxiv - Biology preprints (with Selenium fallback)
5. semantic_scholar - Academic papers
6. acl_anthology - NLP papers
7. openalex - Open access aggregator
8. frontiers - Gold OA (with Selenium fallback)
9. institutional - Via university (if configured)
10. scihub - Gray area (disabled by default)
11. libgen - Gray area (disabled by default)
12. web_search - Google Scholar (disabled)

## Notes
- Some sources have bot protection (Selenium fallback used)
- bioRxiv/Frontiers may fail due to Cloudflare
- Use VPN for better success rates
- 4/6 sources tested successfully (67%)
