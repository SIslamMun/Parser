# Parser

**Download academic papers automatically from multiple sources.**

Got a list of papers you need? This tool will find and download PDFs from open access sources, convert DOIs to BibTeX, verify citations, and optionally access papers through your university's subscription.

## What It Does

1. You give it a DOI, arXiv ID, or title
2. It searches multiple sources (Unpaywall, arXiv, PubMed Central, etc.)
3. It downloads the PDF to your computer

Also includes: DOI to BibTeX conversion, citation verification, citation graphs, reference extraction, and batch processing.

---

## Installation

```bash
# Clone and install
git clone <repo-url>
cd parser

# Using uv (recommended)
uv sync
```

---

## Quick Start

### 1. Create a config file

```bash
cp config.yaml.example config.yaml
```

Or initialize interactively:
```bash
parser init
```

### 2. Add your email

Edit `config.yaml` and set your email (required by APIs for polite access):

```yaml
user:
  email: "your.email@university.edu"
```

### 3. Download a paper

```bash
# By DOI
parser retrieve --doi "10.1038/nature12373"

# By arXiv ID
parser retrieve arXiv:1706.03762

# By title
parser retrieve --title "Attention Is All You Need"

# Specify where to save
parser retrieve --doi "10.1038/nature12373" -o ./papers

# Verbose output
parser retrieve --doi "10.1038/nature12373" -v
```

That's it! The PDF will be saved to `./downloads/` (or wherever you specify).

---

## Batch Processing

Have a list of papers? Put them in a file:

**Option 1: Text file (one identifier per line)**
```
10.1038/nature12373
10.1145/3292500.3330919
arXiv:1706.03762
```

**Option 2: CSV file**
```csv
doi,title
10.1038/nature12373,
,Attention Is All You Need
10.1145/3292500.3330919,
```

**Option 3: JSON file**
```json
[
  {"doi": "10.1038/nature12373"},
  {"title": "Attention Is All You Need"},
  {"doi": "10.1145/3292500.3330919"}
]
```

Then run:
```bash
parser batch papers.txt -o ./downloads
parser batch papers.csv -o ./downloads
parser batch papers.json -o ./downloads -n 5  # 5 concurrent downloads
```

The tool will download all papers, skipping any you've already got.

---

## DOI to BibTeX

Convert DOIs and arXiv IDs to BibTeX citations:

```bash
# Single DOI
parser doi2bib 10.1038/nature12373

# arXiv ID
parser doi2bib arXiv:1706.03762

# Short arXiv format
parser doi2bib 1706.03762

# Save to file
parser doi2bib 10.1038/nature12373 -o reference.bib

# Different formats
parser doi2bib 10.1038/nature12373 --format json
parser doi2bib 10.1038/nature12373 --format markdown

# Process multiple from file
parser doi2bib -i dois.txt -o references.bib
```

**Output formats:**
- `bibtex` (default): Standard BibTeX format
- `json`: Full metadata as JSON
- `markdown`: Formatted citation with YAML frontmatter

---

## Citation Verification

Verify BibTeX entries against CrossRef and arXiv:

```bash
# Verify a .bib file
parser verify references.bib -o ./verified

# Verify a directory of .bib files
parser verify citations_dir/ -o ./output

# Skip specific entries (websites, manual entries, etc.)
parser verify refs.bib --skip-keys "website1,manual2"

# Skip entries from a file
parser verify refs.bib --skip-keys-file skip.txt

# Use pre-verified manual entries
parser verify refs.bib --manual manual.bib

# Dry run (don't write files)
parser verify refs.bib --dry-run -v
```

**Output:**
```
verified/
├── verified.bib    # Successfully verified
├── failed.bib      # Need manual attention
└── report.md       # Summary report with details
```

---

## Citation Graphs

Get papers that cite or are referenced by a given paper:

```bash
# Get both citations and references
parser citations "10.1038/nature12373" --direction both

# Get only papers that cite this paper
parser citations "10.1038/nature12373" --direction citations

# Get only papers referenced by this paper
parser citations "10.1038/nature12373" --direction references

# Limit results
parser citations "arXiv:2005.11401" -n 100

# Output as BibTeX
parser citations "10.1038/nature12373" --format bibtex -o refs.bib

# Output as JSON
parser citations "10.1038/nature12373" --format json -o citations.json
```

**Data source:** Semantic Scholar API (use `--s2-key` for higher rate limits)

---

## Parse References

Extract DOIs, arXiv IDs, and URLs from research documents:

```bash
# Parse references from a markdown file
parser parse-refs research_report.md

# Output to directory
parser parse-refs report.md -o ./refs

# Output formats
parser parse-refs report.md --format json
parser parse-refs report.md --format md
parser parse-refs report.md --format both
```

**What it extracts:**
- DOIs (e.g., `10.1038/nature12373`)
- arXiv IDs (e.g., `arXiv:1706.03762`, `1706.03762`)
- URLs to papers
- Semantic Scholar links
- PubMed/PMC IDs

---

## Sources (What Gets Searched)

The tool tries these sources in order:

| Priority | Source | What It Has |
|----------|--------|-------------|
| 1 | **Unpaywall** | Legal open access versions from publishers & repositories |
| 2 | **arXiv** | Preprints in physics, math, CS, quantitative biology |
| 3 | **PubMed Central** | Open access biomedical literature |
| 4 | **bioRxiv/medRxiv** | Biology and medical preprints |
| 5 | **Semantic Scholar** | Academic papers with open access PDFs |
| 6 | **OpenAlex** | Open access aggregator |
| 7 | **Institutional** | IEEE, ACM, Elsevier via your university (optional) |
| 8 | **Sci-Hub** | Gray area source (disabled by default) |
| 9 | **LibGen** | Gray area source (disabled by default) |
| 10 | **Web Search** | Google Scholar fallback (disabled by default) |

Check your current source status:
```bash
parser sources
```

You can enable/disable sources and change priorities in `config.yaml`.

---

## University/Institutional Access

If you have a university subscription, you can download papers from IEEE, ACM, Elsevier, and other publishers.

### Two Options

**Option A: VPN Mode (Recommended)**

If your university provides VPN access, simply connect to it and enable VPN mode:

```yaml
institutional:
  enabled: true
  vpn_enabled: true
```

That's it! Once connected to your university VPN, papers download directly.

If you want to automate VPN connection, create a script:

```bash
# Example: scripts/vpn-connect.sh
#!/bin/bash
# Your VPN connection command here
# Examples:
# openconnect vpn.youruni.edu
# sudo openvpn --config ~/vpn/university.ovpn
# nmcli connection up "University VPN"
```

Then configure it:

```yaml
institutional:
  enabled: true
  vpn_enabled: true
  vpn_script: "./scripts/vpn-connect.sh"
  vpn_disconnect_script: "./scripts/vpn-disconnect.sh"  # optional
```

Run authentication to connect:
```bash
parser auth
```

**Option B: EZProxy Mode (No VPN needed)**

If you can't use VPN, use your university's EZProxy:

```yaml
institutional:
  enabled: true
  vpn_enabled: false
  proxy_url: "https://ezproxy.gl.iit.edu/login?url="  # Your university's URL
```

Then authenticate once:
```bash
parser auth
```

This opens a browser where you log in through your university. Your session is saved for future use.

### Finding Your Proxy URL

Your proxy URL usually looks like:
- `https://ezproxy.youruni.edu/login?url=`
- `https://proxy.library.youruni.edu/login?url=`

Ask your library or check your library's website for "off-campus access" instructions.

---

## Configuration Reference

### Full config.yaml example

```yaml
# Required: Your email for API access
user:
  email: "you@university.edu"
  name: ""  # Optional

# Optional: API keys for higher rate limits
api_keys:
  ncbi: null              # Get from https://www.ncbi.nlm.nih.gov/account/settings/
  semantic_scholar: null  # Get from https://www.semanticscholar.org/product/api
  crossref_plus: null     # If you have institutional access

# Sources: Enable/disable and set priority (lower = tried first)
sources:
  unpaywall:
    enabled: true
    priority: 1
  arxiv:
    enabled: true
    priority: 2
  pmc:
    enabled: true
    priority: 3
  biorxiv:
    enabled: true
    priority: 4
  semantic_scholar:
    enabled: true
    priority: 5
  openalex:
    enabled: true
    priority: 6
  institutional:
    enabled: false  # Enable if you have university access
    priority: 7
  scihub:
    enabled: false  # Gray area - use at your own risk
    priority: 8
  libgen:
    enabled: false  # Gray area - use at your own risk
    priority: 9
  web_search:
    enabled: false
    priority: 10

# Institutional access settings
institutional:
  enabled: false
  vpn_enabled: false
  vpn_script: null              # e.g., "./scripts/vpn-connect.sh"
  vpn_disconnect_script: null
  proxy_url: null               # e.g., "https://ezproxy.youruni.edu/login?url="
  cookies_file: ".institutional_cookies.pkl"
  university: ""                # For reference

# Unofficial sources (require explicit opt-in)
unofficial:
  disclaimer_accepted: false    # Must set to true to enable scihub/libgen
  scihub:
    enabled: false
    proxy: null                 # SOCKS5 proxy if needed
  libgen:
    enabled: false
    mirror: "li"                # LibGen mirror: "li", "is", "rs", "st"

# Where to save PDFs
download:
  output_dir: "./downloads"
  filename_format: "{first_author}_{year}_{title_short}.pdf"
  max_title_length: 50
  create_subfolders: false
  skip_existing: true

# Rate limiting (don't change unless you know what you're doing)
rate_limits:
  global_delay: 1.0
  per_source_delays:
    crossref: 0.5
    unpaywall: 0.1
    arxiv: 3.0
    pmc: 0.34
    semantic_scholar: 3.0
    biorxiv: 1.0
    scihub: 5.0
    libgen: 3.0

# Batch processing
batch:
  max_concurrent: 3
  retry_failed: true
  max_retries: 2
  save_progress: true
  progress_file: ".retrieval_progress.json"

# Logging
logging:
  level: "INFO"   # DEBUG, INFO, WARNING, ERROR
  file: null      # e.g., "parser.log"
```

### Environment Variables

You can also set these via environment variables:

| Variable | Purpose |
|----------|---------|
| `PAPER_EMAIL` | Your email (overrides config) |
| `NCBI_API_KEY` | PubMed/PMC API key |
| `S2_API_KEY` | Semantic Scholar API key |
| `GITHUB_TOKEN` | For config sync (needs gist scope) |

---

## CLI Commands Reference

```bash
# Show help
parser --help

# Use specific config file
parser -c /path/to/config.yaml retrieve ...

# Download a single paper
parser retrieve --doi "10.1038/nature12373"
parser retrieve --title "Paper Title"
parser retrieve -d "10.1038/nature12373" -o ./papers -e you@email.com -v
parser retrieve arXiv:1706.03762 -o ./papers
parser retrieve --no-skip-existing  # Force re-download

# Download multiple papers
parser batch papers.txt -o ./downloads
parser batch papers.csv -o ./downloads
parser batch papers.json -o ./downloads -n 5 -v  # 5 concurrent, verbose

# Convert DOI to BibTeX
parser doi2bib 10.1038/nature12373
parser doi2bib arXiv:1706.03762
parser doi2bib 10.1038/nature12373 --format json
parser doi2bib 10.1038/nature12373 --format markdown
parser doi2bib -i dois.txt -o references.bib

# Verify citations
parser verify references.bib -o ./verified
parser verify citations_dir/ -o ./output
parser verify refs.bib --skip-keys "website1,manual2"
parser verify refs.bib --skip-keys-file skip.txt
parser verify refs.bib --manual manual.bib
parser verify refs.bib --dry-run -v

# Citation graph
parser citations "10.1038/nature12373" --direction both
parser citations "arXiv:2005.11401" --direction citations -n 100
parser citations "10.1038/nature12373" --format bibtex -o refs.bib

# Parse references from documents
parser parse-refs research_report.md -o ./refs
parser parse-refs report.md --format json

# Show available sources and status
parser sources

# Initialize config file
parser init

# Authenticate with your university
parser auth

# Sync config across machines (requires GITHUB_TOKEN)
parser config push     # Upload config to private gist
parser config pull     # Download config from gist
```

---

## Troubleshooting

### "Email required" error

Add your email to `config.yaml` under `user.email` or use the `-e` flag:
```bash
parser retrieve -d "10.1038/nature12373" -e you@email.com
```

### Paper not found

The tool only searches open access sources by default. If the paper is behind a paywall:
1. Enable institutional access (see above)
2. Or try the paper's arXiv preprint (many papers have one)
3. Enable Sci-Hub as a fallback (gray area)

### Rate limiting

If you're getting blocked, the tool is making requests too fast. Increase delays in `config.yaml`:

```yaml
rate_limits:
  global_delay: 2.0  # Increase this
```

### Institutional auth not working

1. Make sure your `proxy_url` is correct
2. Clear old cookies: delete `.institutional_cookies.pkl`
3. Run `parser auth` again
4. Complete the login fully before pressing Enter

### bioRxiv downloads fail

bioRxiv uses Cloudflare protection that blocks automated downloads. Try:
- Connect to university VPN (sometimes helps)
- Download manually from browser

### Verification fails for valid entries

Some reasons verification might fail:
- DOI is incorrect or misformatted
- Entry has no DOI (add one manually)
- CrossRef has different metadata (check the report.md)

Use `--skip-keys` for entries you've manually verified.

---

## Limitations & Known Issues

### Sources That Don't Work

| Source | Status | Why |
|--------|--------|-----|
| **ScienceDirect/Elsevier** | Not supported | Aggressive bot detection (Incapsula/Imperva). Use institutional access. |
| **Springer** | Not supported | No public API for PDF access. Requires institutional subscription. |
| **Wiley** | Not supported | Same as Springer. |
| **Taylor & Francis** | Not supported | No public PDF API. |

### Sources With Caveats

| Source | Issue | Workaround |
|--------|-------|------------|
| **Semantic Scholar** | Aggressive rate limiting (429 errors) | Use 3+ second delays. Get an API key for higher limits. |
| **bioRxiv/medRxiv** | Cloudflare protection | Often blocked. Use VPN or download manually. |
| **Institutional** | Requires active session | Re-run `parser auth` if cookies expire. VPN mode is more reliable. |
| **LibGen** | Often blocked by universities | May not work on university networks. |

### What This Means

For paywalled papers not in open access repositories, you'll need:
1. **Institutional access** via VPN or EZProxy (if your university provides it)
2. **Check arXiv** - many papers have preprint versions
3. **Email the authors** - most are happy to share PDFs directly
4. **Interlibrary loan** - your library can usually get any paper

### Gray Area Sources

Sci-Hub and LibGen clients exist but are disabled by default. These sources operate in legal gray areas depending on jurisdiction. Enable at your own discretion:

```yaml
unofficial:
  disclaimer_accepted: true  # Must accept to enable

sources:
  scihub:
    enabled: true  # Use at your own risk
  libgen:
    enabled: true  # Use at your own risk
```

---

## Rate Limits

The tool respects API rate limits to avoid getting blocked:

| Source | Rate Limit | Notes |
|--------|------------|-------|
| CrossRef | 50 req/sec (shared pool) | Uses polite pool with email |
| Unpaywall | 100,000/day | Very permissive |
| arXiv | 1 request/3 sec | Official limit |
| PubMed Central | 3 req/sec (10 with key) | Get API key for more |
| Semantic Scholar | 100 req/5 min | Free API key available |
| bioRxiv | ~1 req/sec | No official limit |
| Sci-Hub | Be careful | Use 5+ second delays |
| LibGen | ~1 req/3 sec | No official limit |

---

## Development

```bash
git clone <repo-url>
cd parser
uv sync --extra dev
uv run pytest
```

---

## License

MIT
