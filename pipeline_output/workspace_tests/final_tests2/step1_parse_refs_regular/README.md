# Step 1: Parse References (Regular/Regex)

## Command
```bash
parser parse-refs "research document/research_report.md" \
  -o step1_parse_refs_regular \
  --export-batch --export-dois
```

## Input
| Property | Value |
|----------|-------|
| File | `research document/research_report.md` |
| Size | 17,737 bytes |
| Topic | Transformer Architecture and Attention Mechanisms |

## Output Files
| File | Description |
|------|-------------|
| `references.json` | Structured reference data (JSON) |
| `references.md` | Human-readable reference list |
| `batch.json` | 17 papers for batch download |
| `dois.txt` | 7 DOI/arXiv identifiers |
| `output.txt` | Command output log |

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

## Reference Breakdown

### GitHub Repositories (4)
- pytorch/pytorch
- huggingface/transformers
- tensorflow/tensorflow
- google-research/bert

### arXiv Papers (3)
- arXiv:2303.08774 (GPT-4 Technical Report)
- arXiv:2407.21783 (Llama 3 Herd of Models)
- arXiv:2302.13971 (LLaMA)

### DOIs (4)
- 10.1038/s41586-020-2649-2 (NumPy)
- 10.1038/nature14539 (Deep Learning)
- 10.18653/v1/N19-1423 (BERT)
- 10.1109/ICCV48922.2021.00986 (Swin Transformer)

### Papers (10)
- Attention Is All You Need
- BERT: Pre-training of Deep Bidirectional Transformers
- GPT-4 Technical Report
- LLaMA: Open and Efficient Foundation Language Models
- And more...

### YouTube Videos (3)
- Educational videos on transformers/attention

### Websites (6)
- Documentation and blog posts

## Analysis
- **Strong academic extraction**: DOIs, arXiv IDs, and paper titles well detected
- **Multi-format support**: Handles various reference styles
- **Deduplication**: Automatically applied to remove duplicates
- **Export ready**: Generated batch.json and dois.txt for next steps

## Status: ✅ PASS
