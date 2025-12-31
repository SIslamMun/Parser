# Test 02: Retrieve

## Command
```bash
parser retrieve arXiv:1706.03762 -o ./output
```

## Description
Downloads a single paper PDF by arXiv ID.

## Expected Output
- PDF file downloaded with metadata-based filename
- Source identified
- Title shown

## Result
✅ **PASS**

## Output
```
✓ Downloaded: Vaswani_2017_Attention_is_All_you_Need.pdf
  Source: arxiv
  Title: Attention is All you Need
```

## Files Generated
- `Vaswani_2017_Attention_is_All_you_Need.pdf` - The famous Transformer paper

## Notes
- Filename format: `{first_author}_{year}_{title_short}.pdf`
- Source priority: unpaywall → arxiv → pmc → ...
- arXiv source used directly for arXiv IDs
