# Test 04: Parse-Refs

## Command
```bash
parser parse-refs research_report.md -o ./refs
```

## Description
Extracts references from a research document using regex patterns.

## Expected Output
- JSON and Markdown output files
- Categorized references by type
- Deduplicated results

## Result
✅ **PASS**

## Output
```
============================================================
Running REGULAR (regex-based) parsing...
============================================================
✓ JSON: references.json
✓ Markdown: references.md

Found 18 references (regular):
  arxiv: 2
  doi: 4
  paper: 7
  website: 5
```

## Files Generated
- `references.json` - Structured data
- `references.md` - Human-readable list

## What It Extracts
- DOIs (e.g., `10.1038/nature12373`)
- arXiv IDs (e.g., `arXiv:1706.03762`)
- GitHub repositories
- YouTube videos
- Paper citations (Author et al., Year)
- URLs and websites

## Notes
- Automatic deduplication across types
- Academic paper URLs skipped (already counted as papers)
- Wikipedia URLs handled correctly
