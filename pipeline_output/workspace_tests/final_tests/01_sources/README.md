# Test 01: Sources

## Command
```bash
parser sources
```

## Description
Lists all available paper acquisition sources and their status.

## Expected Output
- Lists 12 sources with enabled/disabled status
- Shows institutional access configuration
- Shows unofficial sources status

## Result
✅ **PASS**

## Output
```
Available sources:

  1. unpaywall: enabled
  2. arxiv: enabled
  3. pmc: enabled
  4. biorxiv: enabled
  5. semantic_scholar: enabled
  6. acl_anthology: enabled
  7. openalex: enabled
  8. frontiers: enabled
  9. institutional: enabled
  10. scihub: enabled
  11. libgen: enabled
  12. web_search: disabled

Institutional access:
  Mode: EZProxy
  Proxy URL: https://ezproxy.gl.iit.edu/login?url=

Unofficial sources enabled
```

## Notes
- 11 of 12 sources enabled
- web_search is disabled by default
- Institutional access configured with EZProxy
