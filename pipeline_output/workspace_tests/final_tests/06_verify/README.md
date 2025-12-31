# Test 06: Verify

## Command
```bash
parser verify test.bib -o ./output
```

## Description
Verifies BibTeX citations against CrossRef and arXiv.

## Input File (test.bib)
```bibtex
@article{test2023,
  title = {Test Paper},
  author = {Test Author},
  year = {2023},
  doi = {10.1038/nature12373}
}
```

## Expected Output
- Verified entries separated from failed
- Report generated
- Summary statistics

## Result
✅ **PASS**

## Output
```
============================================================
Citation Verification (Single File Mode)
============================================================
Input: test.bib
Output: ./output

Results:
  Verified: 0
  arXiv: 0
  Searched: 0
  Website: 0
  Manual: 0
  Failed: 1

Total verified: 0
Total failed: 1

Output written to: ./output
```

## Files Generated
- `output/verified.bib` - Successfully verified entries
- `output/failed.bib` - Entries needing attention
- `output/report.md` - Summary report

## Options
- `--skip-keys` - Skip specific entries
- `--skip-keys-file` - Skip entries from file
- `--manual` - Use pre-verified entries
- `--dry-run` - Preview without writing

## Notes
- Checks DOI against CrossRef
- Validates arXiv IDs
- Reports mismatched metadata
