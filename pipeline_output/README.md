# Pipeline Test Output

All test results consolidated from various test runs.

## Directory Structure

```
pipeline_output/
├── workspace_tests/       # Tests from workspace
│   ├── test_v2/          # Parse refs comparison (agent vs regular)
│   ├── test_output/      # Institutional access tests
│   ├── final_tests/      # First batch of final tests
│   ├── final_tests2/     # Step-by-step pipeline tests
│   ├── test_results/     # Various feature tests
│   └── claude_test_report/  # Claude agent test reports
│
└── tmp_tests/            # Tests from /tmp (batch downloads)
    ├── final_test/       # 13 PDFs (before fixes)
    ├── final_test2/      # 14 PDFs (after some fixes)
    ├── fix_test/         # 14 PDFs (with DOI validation)
    ├── fix_test2/        # 14 PDFs (with title mismatch detection)
    ├── final_fix_test/   # 15 PDFs (all fixes applied)
    └── comprehensive_test/  # 6 PDFs (comprehensive source test)
```

## Test Status Summary

### /tmp Tests (Batch Downloads)

| Test | PDFs | Status | Notes |
|------|------|--------|-------|
| `comprehensive_test` | 6 | ✓ Pass | Multi-source test |
| `final_fix_test` | 15 | ✓ Pass | **Best result** - all fixes applied |
| `final_test` | 13 | ✗ Failed | 3 failures (before fixes) |
| `final_test2` | 14 | ✓ Pass | Improved with fixes |
| `fix_test` | 14 | ✓ Pass | DOI validation working |
| `fix_test2` | 14 | ✓ Pass | Title mismatch detection working |

### Workspace Tests

| Test | PDFs | Markdown | JSON | Purpose |
|------|------|----------|------|---------|
| `claude_test_report` | 0 | 8 | 0 | Agent test documentation |
| `final_tests` | 7 | 16 | 4 | Initial pipeline tests |
| `final_tests2` | 14 | 10 | 4 | Step-by-step pipeline |
| `test_output` | 10 | 1 | 4 | Institutional access |
| `test_results` | 32 | 10 | 21 | Feature tests |
| `test_v2` | 0 | 13 | 11 | Parse refs comparison |

## Key Fixes Applied

1. **Metadata Resolution Order**: Peer-reviewed (CrossRef) first, preprints (arXiv) last
2. **DOI Validation**: Skip peer reviews, book chapters, datasets
3. **Title Matching**: Substring + subset + Jaccard similarity
4. **Title Mismatch Detection**: Catches llama/LLaMA, falcon/Falcon, bert/BERT confusion

## Test Date

December 31, 2025
