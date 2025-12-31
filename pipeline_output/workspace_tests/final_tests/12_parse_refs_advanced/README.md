# Test 12: Parse-Refs Advanced

## Command
```bash
parser parse-refs report.md -o ./output --export-batch --export-dois
```

## Description
Tests parse-refs with export options for pipeline integration.

## Expected Output
- Standard references.json and references.md
- batch.json for `parser batch`
- dois.txt for `parser doi2bib -i`

## Result
✅ **PASS**

## Output
```
============================================================
Running REGULAR (regex-based) parsing...
============================================================
✓ JSON: references.json
✓ Markdown: references.md
✓ Batch export (13 papers): batch.json
  Use with: parser batch batch.json -o ./papers
✓ DOI export (6 identifiers): dois.txt
  Use with: parser doi2bib -i dois.txt -o references.bib

Found 18 references (regular):
  arxiv: 2
  doi: 4
  paper: 7
  website: 5
```

## Files Generated
- `references.json` - All extracted references
- `references.md` - Human-readable list
- `batch.json` - Papers with DOIs/arXiv/PDFs for batch download
- `dois.txt` - DOI/arXiv IDs only for doi2bib

## Export Format - batch.json
```json
[
  {"doi": "10.1038/nature12373", "title": "Paper Title"},
  {"arxiv_id": "1706.03762", "title": "arXiv Paper"},
  {"pdf_url": "https://example.com/paper.pdf"}
]
```

## Export Format - dois.txt
```
10.1038/nature12373
arXiv:1706.03762
10.5555/3295222.3295349
```

## Pipeline Integration
```bash
# Step 1: Extract references
parser parse-refs report.md --export-batch --export-dois

# Step 2: Download papers
parser batch batch.json -o ./papers

# Step 3: Get BibTeX
parser doi2bib -i dois.txt -o references.bib
```

## Notes
- batch.json only includes downloadable papers (with DOI/arXiv/PDF)
- dois.txt only includes DOI and arXiv IDs
- Website URLs and paper titles (without DOI) not included in exports
