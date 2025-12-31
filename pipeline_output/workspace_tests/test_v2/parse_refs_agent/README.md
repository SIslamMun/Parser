# Parse-Refs Agent (Claude)

## Command
```bash
parser parse-refs <research_document> -o parse_refs_agent --agent claude
```

## Results
Found 30+ references with rich metadata including:
- Paper titles
- Authors
- Years
- URLs
- Citation context

## Output Files
| File | Description |
|------|-------------|
| `references.json` | Processed references |
| `references.md` | Human-readable list |
| `agent_raw_response.txt` | Full agent response with context |
| `agent_result.json` | Raw agent JSON output |

## Sample Output
```json
{
  "type": "paper",
  "value": "Attention Is All You Need",
  "title": "Attention Is All You Need",
  "authors": "Vaswani et al.",
  "year": "2017",
  "url": "https://papers.nips.cc/paper/2017/hash/3f5ee243...",
  "context": "The publication of 'Attention Is All You Need' by Vaswani et al. in 2017..."
}
```

## Advantages Over Regex
| Feature | Regex | Agent |
|---------|-------|-------|
| **Metadata extraction** | ❌ IDs only | ✅ Full metadata |
| **Author detection** | ❌ No | ✅ Yes |
| **Year extraction** | ❌ No | ✅ Yes |
| **Context preservation** | ❌ No | ✅ Yes |
| **Semantic understanding** | ❌ No | ✅ Yes |
| **URL inference** | ❌ Explicit only | ✅ Inferred |

## Reference Types Found
- **paper**: 14 academic papers with full metadata
- **website**: 8 URLs with descriptions
- **doi**: 4 DOIs linked to paper metadata
- **arxiv**: 3 arXiv papers with titles/authors
- **pdf**: 2 direct PDF links
- **github**: 4 repositories
- **youtube**: 3 educational videos

## Requirements
- Claude CLI installed (`claude --version`)
- Claude Pro subscription (no API key needed)
- May hit rate limits during heavy use

## Status: ✅ PASS
