# Step 3: Comparison (Regular vs Agent)

## Purpose
Compare reference extraction results between:
- **Regular (Regex)**: Pattern-based extraction
- **Agent (Claude)**: AI-powered semantic extraction

## Status: ⚠️ SKIPPED

## Reason
No agent results available for comparison (Step 2 was skipped due to rate limit).

## What This Step Would Show

### Metrics Comparison
| Metric | Regular | Agent | Difference |
|--------|---------|-------|------------|
| Total References | 31 | ? | ? |
| GitHub | 4 | ? | ? |
| arXiv | 3 | ? | ? |
| DOI | 4 | ? | ? |
| Paper | 10 | ? | ? |
| YouTube | 3 | ? | ? |
| Website | 6 | ? | ? |

### Quality Analysis
- **Precision**: How many extracted refs are valid
- **Recall**: How many actual refs were found
- **Metadata Quality**: Completeness of author/year/venue

### Expected Differences
1. Agent typically finds more implicit references
2. Agent extracts better metadata (authors, years)
3. Regex may have false positives on partial matches
4. Agent understands context (e.g., "as shown by Smith et al.")

## To Run Comparison Later
```bash
# First, run agent parsing
parser parse-refs "research document/research_report.md" \
  -o step2_parse_refs_agent --agent claude

# Then compare outputs manually or with diff:
diff step1_parse_refs_regular/references.json \
     step2_parse_refs_agent/references.json
```

## Current Data (Regular Only)
```
Regular extraction found 31 references:
  github: 4
  arxiv: 3
  doi: 4
  paper: 10
  pdf: 1
  youtube: 3
  website: 6
```

## Status: ⚠️ SKIPPED (No Agent Data)
