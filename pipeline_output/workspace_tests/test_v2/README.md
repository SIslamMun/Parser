# test_v2 - Transformer Research Document Tests

> Research File: test_v2 research document (Transformer Architecture)
> Date: December 2025

## Contents

| Folder | Description | Status |
|--------|-------------|--------|
| `parse_refs_regular/` | Regex-based reference extraction | ✅ Complete |
| `parse_refs_agent/` | Claude agent reference extraction | ✅ Complete |
| `undirected_1/` | Undirected research output 1 | ✅ Complete |
| `undirected_2/` | Undirected research output 2 | ✅ Complete |
| `undirected_2_retry/` | Retry of undirected 2 | ✅ Complete |
| `undirected_advanced/` | Advanced undirected research | ✅ Complete |
| `undirected_full_categories/` | Full category research | ✅ Complete |

---

## Parse-Refs Comparison

### Regular (Regex) Results
```
Found 31 references:
  github: 4
  arxiv: 3
  doi: 4
  paper: 10
  pdf: 1
  youtube: 3
  website: 6
```

### Agent (Claude) Results
```
Found 30+ references with enhanced metadata:
  paper: 14 (with titles, authors, years)
  website: 8 (with context)
  doi: 4 (linked to papers)
  arxiv: 3 (with metadata)
  pdf: 2 (direct links)
  github: 4
  youtube: 3
```

### Key Differences
| Aspect | Regular | Agent |
|--------|---------|-------|
| **Metadata** | Minimal (IDs only) | Rich (title, authors, year, context) |
| **Accuracy** | Pattern-based | Semantic understanding |
| **Context** | None | Includes citation context |
| **Dedup** | Basic | Smart (understands same paper) |

---

## Files

### parse_refs_regular/
- `references.json` - 31 references (basic metadata)
- `references.md` - Human-readable list

### parse_refs_agent/
- `references.json` - 30+ references (rich metadata)
- `references.md` - Human-readable list
- `agent_raw_response.txt` - Full agent response with context
- `agent_result.json` - Processed agent output
