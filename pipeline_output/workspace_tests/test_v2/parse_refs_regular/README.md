# Parse-Refs Regular (Regex)

## Command
```bash
parser parse-refs <research_document> -o parse_refs_regular
```

## Results
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

## Output Files
| File | Description |
|------|-------------|
| `references.json` | Structured JSON with all references |
| `references.md` | Human-readable markdown list |

## Reference Breakdown

### GitHub (4)
- pytorch/pytorch
- huggingface/transformers
- microsoft/Swin-Transformer
- meta-llama/llama3

### arXiv (3)
- 2303.08774 (GPT-4)
- 2407.21783 (Llama 3)
- 2302.13971 (LLaMA)

### DOI (4)
- 10.1038/s41586-020-2649-2
- 10.1038/nature14539
- 10.18653/v1/N19-1423
- 10.1109/ICCV48922.2021.00986

### Papers (10)
- An Image is Worth 16x16 Words
- Array programming with NumPy
- And 8 more...

## Characteristics
- **Fast**: Milliseconds to process
- **Basic metadata**: Only extracts identifiers
- **No context**: Doesn't understand citation context
- **Pattern-based**: May miss non-standard formats

## Status: ✅ PASS
