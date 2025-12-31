# Test 03: Batch

## Command
```bash
parser batch test_dois.txt -o ./downloads -n 2
```

## Description
Downloads multiple papers from a file with parallel processing.

## Input File (test_dois.txt)
```
10.1038/nature14539
1706.03762
```

## Expected Output
- Both papers downloaded
- Parallel processing (up to 2 concurrent)
- Progress tracking

## Result
✅ **PASS**

## Output
```
Found 2 papers to retrieve:
  - 2 with title/DOI (metadata search)
  - 0 direct PDF URLs

Results:
  ✓ Downloaded: 2
```

## Files Generated
- `downloads/*.pdf` - Two paper PDFs

## Notes
- Input formats: TXT, CSV, JSON
- Supports concurrent downloads (-n flag)
- Skips existing files by default
- Resumes interrupted batches
