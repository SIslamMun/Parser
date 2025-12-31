# Step 2: Parse References (Agent - Claude)

## Command
```bash
parser parse-refs "research document/research_report.md" \
  -o step2_parse_refs_agent --agent claude
```

## Status: ⚠️ SKIPPED

## Reason
Claude CLI rate limit hit (resets at 12pm America/Chicago timezone).

The `--agent claude` option uses:
- **Claude Agent SDK** for intelligent reference parsing
- **Claude Pro subscription** via CLI (no API key required)
- **Enhanced extraction** with semantic understanding

## Error Message
```
Rate limit error - Claude CLI usage limit exceeded
Please wait until 12pm America/Chicago for limit reset
```

## How Agent Parsing Works
1. Sends document to Claude via Agent SDK
2. Claude analyzes text semantically (not just regex)
3. Extracts references with full metadata
4. Returns structured JSON output

## Benefits of Agent Parsing
- **Better context understanding**: Catches implicit references
- **Metadata extraction**: Extracts authors, years, venues
- **Disambiguation**: Resolves incomplete citations
- **Quality over regex**: Understands academic writing patterns

## To Retry Later
```bash
# After 12pm Chicago time
parser parse-refs "research document/research_report.md" \
  -o step2_parse_refs_agent --agent claude
```

## Expected Output (When Working)
```
Found N references (agent):
  arxiv: X
  doi: Y
  paper: Z
  ...
```

## Status: ⚠️ SKIPPED (Rate Limited)
