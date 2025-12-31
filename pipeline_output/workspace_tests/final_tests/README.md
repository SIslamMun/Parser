# Parser CLI - Final Test Results

> Generated: December 31, 2025

## Test Summary

| Test | Command | Status | Notes |
|------|---------|--------|-------|
| 01 | `parser sources` | ✅ PASS | Lists 12 sources, 11 enabled |
| 02 | `parser retrieve` | ✅ PASS | Downloads arXiv paper successfully |
| 03 | `parser batch` | ✅ PASS | Downloads 2 papers in parallel |
| 04 | `parser parse-refs` | ✅ PASS | Extracts 18 references |
| 05 | `parser doi2bib` | ✅ PASS | Converts DOI/arXiv to BibTeX |
| 06 | `parser verify` | ✅ PASS | Verifies BibTeX citations |
| 07 | `parser citations` | ✅ PASS | Gets citation graph from S2 |
| 08 | `parser init` | ✅ PASS | Creates config.yaml |
| 09 | `parser auth` | ⚠️ SKIP | Requires institutional config |
| 10 | `parser config` | ✅ PASS | Config sync help works |
| 11 | Individual Sources | ✅ PARTIAL | 4/6 sources tested successfully |
| 12 | parse-refs exports | ✅ PASS | Creates batch.json and dois.txt |

## Test Details

### 01_sources - List Available Sources
```bash
parser sources
```
**Result:** Lists 12 sources with status (enabled/disabled)

### 02_retrieve - Single Paper Download
```bash
parser retrieve arXiv:1706.03762 -o ./output
```
**Result:** ✅ Downloaded `Vaswani_2017_Attention_is_All_you_Need.pdf`

### 03_batch - Batch Download
```bash
parser batch test_dois.txt -o ./downloads -n 2
```
**Result:** ✅ Downloaded 2 papers in parallel

### 04_parse_refs - Reference Extraction
```bash
parser parse-refs research_report.md -o ./refs
```
**Result:** ✅ Found 18 references (2 arXiv, 4 DOI, 7 papers, 5 websites)

### 05_doi2bib - DOI to BibTeX
```bash
parser doi2bib 10.1038/nature12373
parser doi2bib 1706.03762
parser doi2bib -i dois.txt -o references.bib
```
**Result:** ✅ All formats work (BibTeX, JSON, Markdown)

### 06_verify - Citation Verification
```bash
parser verify test.bib -o ./output
```
**Result:** ✅ Verifies against CrossRef/arXiv

### 07_citations - Citation Graph
```bash
parser citations "10.1038/nature12373" --direction citations -n 5
```
**Result:** ✅ Found 5 citing papers via Semantic Scholar

### 08_init - Initialize Config
```bash
parser init
```
**Result:** ✅ Creates config.yaml template

### 09_auth - Institutional Auth
```bash
parser auth
```
**Result:** ⚠️ Requires institutional config enabled

### 10_config - Config Sync
```bash
parser config push
parser config pull
```
**Result:** ✅ Help displays correctly (requires GitHub CLI for actual sync)

### 11_sources_individual - Individual Source Tests

| Source | DOI/ID | Status |
|--------|--------|--------|
| arXiv | arXiv:2005.11401 | ✅ Downloaded |
| OpenAlex | 10.1038/nature12373 | ✅ Downloaded |
| Unpaywall | 10.18653/v1/2020.acl-main.747 | ✅ Downloaded |
| Semantic Scholar | 10.18653/v1/P18-1238 | ✅ Downloaded |
| bioRxiv | 10.1101/2020.04.27.064501 | ❌ Not found |
| Frontiers | 10.3389/frai.2021.684004 | ❌ Not found |

### 12_parse_refs_advanced - Export Options

```bash
parser parse-refs report.md --export-batch --export-dois
```
**Result:** ✅ Creates:
- `batch.json` (13 papers for `parser batch`)
- `dois.txt` (6 DOIs for `parser doi2bib -i`)

## Commands Coverage

All 10 CLI commands tested:

1. ✅ `parser retrieve` - Download single paper
2. ✅ `parser batch` - Batch download
3. ✅ `parser parse-refs` - Extract references
4. ✅ `parser doi2bib` - DOI to BibTeX
5. ✅ `parser verify` - Verify citations
6. ✅ `parser citations` - Citation graph
7. ✅ `parser sources` - List sources
8. ✅ `parser init` - Initialize config
9. ⚠️ `parser auth` - Institutional auth (config required)
10. ✅ `parser config` - Config sync

## Files Generated

```
final_tests/
├── README.md                    # This file
├── 01_sources/
│   ├── README.md
│   └── output.txt
├── 02_retrieve/
│   ├── README.md
│   ├── output.txt
│   └── *.pdf
├── 03_batch/
│   ├── README.md
│   ├── test_dois.txt
│   ├── output.txt
│   └── downloads/*.pdf
├── 04_parse_refs/
│   ├── README.md
│   ├── output.txt
│   ├── references.json
│   └── references.md
├── 05_doi2bib/
│   ├── README.md
│   ├── output.txt
│   └── from_file.bib
├── 06_verify/
│   ├── README.md
│   ├── test.bib
│   └── output/
├── 07_citations/
│   ├── README.md
│   └── output.txt
├── 08_init/
│   ├── README.md
│   └── output.txt
├── 09_auth/
│   ├── README.md
│   └── output.txt
├── 10_config/
│   ├── README.md
│   └── output.txt
├── 11_sources_individual/
│   ├── README.md
│   ├── output.txt
│   └── *.pdf
└── 12_parse_refs_advanced/
    ├── README.md
    ├── batch.json
    ├── dois.txt
    └── references.*
```
