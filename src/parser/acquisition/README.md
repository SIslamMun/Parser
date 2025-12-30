# Parser Acquisition Module

> Paper retrieval with multi-source fallback

This module handles downloading scientific papers from multiple sources.

**See the main [README.md](../../../README.md) for full documentation.**

## Quick Reference

### CLI Commands

```bash
# Single paper
parser retrieve --doi "10.1038/nature12373"
parser retrieve --title "Attention Is All You Need"
parser retrieve arXiv:1706.03762

# Batch download
parser batch papers.csv -o ./output

# Check sources
parser sources

# Configure institutional access
parser auth --proxy-url "https://ezproxy.university.edu/login?url="
```

### Python API

```python
from parser.acquisition import PaperRetriever, Config

config = Config.load()
retriever = PaperRetriever(config)

result = await retriever.retrieve("10.1038/nature12373", output_dir="./papers")
```

## Module Structure

```
acquisition/
├── __init__.py         # Public exports
├── config.py           # Configuration handling
├── retriever.py        # Main PaperRetriever class
├── identifier.py       # DOI/arXiv ID resolution
└── clients/            # API clients
    ├── base.py         # BaseClient with rate limiting
    ├── arxiv.py        # arXiv API
    ├── crossref.py     # CrossRef API
    ├── unpaywall.py    # Unpaywall API
    ├── semantic_scholar.py
    ├── openalex.py
    ├── pmc.py          # PubMed Central
    ├── biorxiv.py      # bioRxiv/medRxiv
    ├── institutional.py # EZProxy/VPN support
    ├── scihub.py       # Sci-Hub (disabled by default)
    ├── libgen.py       # LibGen (disabled by default)
    └── web_search.py   # Google Scholar fallback
```

## Configuration

See [config.yaml](../../../config.yaml) for full configuration options.

Key settings:
- `sources.<name>.enabled` - Enable/disable each source
- `sources.<name>.delay` - Rate limit delay in seconds
- `output.filename_format` - PDF naming format
- `retrieval.skip_existing` - Skip already downloaded papers
