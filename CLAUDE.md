# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Parser** is a Python CLI tool for academic paper acquisition, DOI/arXiv to BibTeX conversion, citation verification, and reference extraction from research documents. It aggregates multiple open access sources (Unpaywall, arXiv, PubMed Central, Semantic Scholar, etc.) with fallback support for institutional access and gray-area sources.

## Development Commands

### Setup
```bash
# Clone and install dependencies
uv sync

# Install with dev dependencies
uv sync --extra dev

# Install with all AI agent support
uv sync --extra agents
```

### Running the CLI
```bash
# The CLI is available via the `parser` command
parser --help

# Use specific config file
parser -c /path/to/config.yaml <command>

# Common commands
parser retrieve --doi "10.1038/nature12373"
parser batch papers.txt -o ./downloads
parser doi2bib 10.1038/nature12373
parser verify references.bib -o ./verified
parser parse-refs research_report.md
parser citations "10.1038/nature12373" --direction both
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run tests requiring network access
uv run pytest -m network

# Run specific test file
uv run pytest tests/test_parser.py
```

Note: There is currently no `tests/` directory in the repository. Tests should be created in a `tests/` directory when added.

### Code Quality
```bash
# Lint with ruff
uv run ruff check .

# Format with ruff
uv run ruff format .

# Type checking with mypy
uv run mypy src/parser
```

### Configuration
```bash
# Initialize config file interactively
parser init

# Copy example config
cp config.yaml.example config.yaml

# Authenticate with institutional access
parser auth
```

## Architecture

### High-Level Structure

The codebase is organized into four main modules:

1. **`acquisition/`** - Multi-source paper PDF retrieval system
2. **`doi2bib/`** - DOI/arXiv to BibTeX conversion and citation verification
3. **`agent/`** - AI-powered reference extraction (Claude SDK, Anthropic API, Google Gemini)
4. **`parser.py`** - Regex-based reference extraction from documents

### Key Design Patterns

#### 1. Client-Based Architecture (`acquisition/clients/`)

All paper sources implement the `BaseClient` abstract class from `acquisition/clients/base.py`:

```python
class BaseClient(ABC):
    @abstractmethod
    async def get_paper_metadata(self, identifier: str) -> dict[str, Any] | None:
        """Get metadata for a paper by identifier."""
        pass
```

**Source clients** (each in `acquisition/clients/`):
- `UnpaywallClient` - Open access aggregator (priority 1)
- `ArxivClient` - arXiv preprints (priority 2)
- `PMCClient` - PubMed Central (priority 3)
- `BioRxivClient` - bioRxiv/medRxiv preprints with Selenium fallback (priority 4)
- `SemanticScholarClient` - Academic search (priority 5)
- `ACLAnthologyClient` - NLP conference papers (priority 6)
- `OpenAlexClient` - Open access aggregator (priority 7)
- `FrontiersClient` - Frontiers publisher with Selenium fallback (priority 8)
- `InstitutionalClient` - University proxy/VPN access (priority 9, disabled by default)
- `SciHubClient` - Gray area source (priority 10, disabled by default)
- `LibGenClient` - Gray area source (priority 11, disabled by default)

All clients include built-in rate limiting via the `RateLimiter` class.

#### 2. Orchestration via `PaperRetriever`

The `acquisition/retriever.py` module contains `PaperRetriever`, which:
- Initializes all enabled clients based on `config.yaml`
- Tries sources in priority order (lowest priority number first)
- Returns `RetrievalResult` with status, source, PDF path, and metadata
- Handles batch processing with concurrency control
- Maintains retrieval progress for resume capability

#### 3. Identifier Resolution (`doi2bib/resolver.py`)

The `PaperIdentifier` system normalizes various identifier formats:
- DOI: `10.1234/example` or `https://doi.org/10.1234/example`
- arXiv: `arXiv:2301.12345`, `2301.12345`, or arXiv URLs
- Semantic Scholar: 40-char hex IDs or S2 URLs
- OpenAlex: `W1234567890` or OpenAlex URLs
- PubMed/PMC: `PMID:12345678` or `PMC1234567`
- PDF URLs, titles, or unknown formats

All identifiers are normalized through regex patterns before being passed to clients.

#### 4. Configuration Management (`acquisition/config.py`)

Config loading follows this precedence (highest to lowest):
1. Environment variables (`PAPER_EMAIL`, `NCBI_API_KEY`, `S2_API_KEY`, etc.)
2. Specified config file path (`-c/--config`)
3. `./config.yaml` (current directory)
4. `./parser.yaml`
5. `~/.config/parser/config.yaml`
6. `~/.parser.yaml`
7. Defaults

Config is passed to all clients and controls:
- Source enable/disable and priority order
- Rate limits per source
- Batch processing concurrency
- Institutional access settings
- Download paths and file naming

#### 5. AI Agent System (`agent/`)

Three agent implementations for enhanced reference extraction:

**Factory pattern** (`agent/factory.py`):
```python
def create_agent(agent_type: str, config: dict, model: str | None) -> AgentParser
```

**Agent types**:
- `claude-sdk` - Uses Claude Agent SDK (NO API key needed, uses Claude Code CLI auth)
- `anthropic` - Direct Anthropic API (falls back to SDK if available)
- `gemini` - Google Generative AI
- `google-adk` - Google ADK framework

All agents implement `AgentParser` base class and return `AgentParseResult` with:
- Extracted references
- Raw LLM response
- Token usage
- Model and agent metadata

Agents use structured prompts from `agent/base.py` to extract references in JSON format.

#### 6. CLI Structure (`cli.py`)

Click-based CLI with command groups:
- **Paper acquisition**: `retrieve`, `batch`, `sources`, `auth`
- **DOI/BibTeX**: `doi2bib`, `verify`
- **Reference parsing**: `parse-refs`, `citations`
- **Config management**: `init`, `config push/pull`

All commands accept:
- `-c/--config` for custom config file path
- `-v/--verbose` for detailed output
- `-o/--output` for output directory

### Data Flow

**Paper Retrieval Flow**:
```
User Input (DOI/arXiv/Title)
    ↓
Identifier Resolution (doi2bib/resolver.py)
    ↓
PaperRetriever.retrieve()
    ↓
Try sources by priority (acquisition/clients/*)
    ↓
Download PDF (acquisition/downloader.py)
    ↓
Save with configured filename format
    ↓
Return RetrievalResult
```

**Reference Parsing Flow**:
```
Document Input (.md, .txt, .pdf)
    ↓
Choose parsing method:
    - ResearchParser (regex-based, fast)
    - AgentParser (AI-based, more accurate)
    ↓
Extract references by type (DOI, arXiv, GitHub, etc.)
    ↓
Output as JSON, Markdown, or BibTeX
```

**Citation Verification Flow**:
```
BibTeX file(s)
    ↓
Parse entries (doi2bib/verifier.py)
    ↓
Query CrossRef/arXiv for canonical metadata
    ↓
Compare and detect mismatches
    ↓
Output: verified.bib, failed.bib, report.md
```

## Important Implementation Details

### Rate Limiting
Each client has its own rate limiter configured in `config.yaml` under `rate_limits.per_source_delays`. The `RateLimiter` class in `acquisition/clients/base.py` uses `asyncio.sleep()` to enforce delays. Never reduce rate limits below the configured values - they respect API guidelines.

### Selenium Fallback
`BioRxivClient` and `FrontiersClient` automatically fall back to Selenium (headless Chrome) when direct HTTP downloads are blocked by Cloudflare. This requires Chrome to be installed but ChromeDriver is managed automatically via `webdriver-manager`.

### Institutional Access
Two modes available:
1. **VPN mode**: Set `institutional.vpn_enabled: true` when connected to university VPN
2. **EZProxy mode**: Set `institutional.proxy_url` and run `parser auth` for browser-based login

Cookies are saved to `.institutional_cookies.pkl` and reused for subsequent requests.

### Async Architecture
The entire acquisition system is async-first using `httpx.AsyncClient` and `asyncio`. CLI commands use `asyncio.run()` to execute async functions. When adding new features, maintain async patterns throughout.

### Error Handling
Clients return `None` for not-found or failed requests rather than raising exceptions. The retriever aggregates all attempts in `RetrievalResult.attempts` for debugging. Status is tracked via `RetrievalStatus` enum.

### File Naming
PDFs are saved using the format string from `download.filename_format`:
```python
"{first_author}_{year}_{title_short}.pdf"
```
Variables available: `first_author`, `year`, `title_short`, `doi`, `arxiv_id`

## Common Patterns

### Adding a New Source Client

1. Create new file in `src/parser/acquisition/clients/`
2. Inherit from `BaseClient`
3. Implement `get_paper_metadata()` and `download_pdf()`
4. Add rate limit config to `config.yaml.example`
5. Register in `acquisition/clients/__init__.py`
6. Add initialization in `retriever.py:_init_clients()`
7. Add source config to `config.yaml.example` with priority

### Adding a New CLI Command

1. Add `@cli.command()` decorated function in `cli.py`
2. Import required modules within the command function (not at top level)
3. Load config with `Config.load(ctx.obj.get("config_path"))`
4. Use Click options for all parameters
5. Handle errors with try/except and `click.echo()` for user messages

### Working with Config

Always load config through `Config.load()` which handles:
- Multiple search paths
- Environment variable overrides
- Default values
- YAML parsing

Access nested config via dict syntax:
```python
config.api_keys.get("semantic_scholar")
config.sources.get("arxiv", {}).get("enabled", True)
```

### Testing Network Clients

Use pytest markers:
```python
@pytest.mark.network
async def test_arxiv_client():
    """Test arXiv client (requires network)."""
```

Run with: `pytest -m network`

## External Dependencies

### Critical APIs
- **CrossRef**: Requires polite pool (email in user-agent), 50 req/sec shared pool
- **Unpaywall**: 100k requests/day, email required
- **arXiv**: 1 request/3 seconds strictly enforced
- **PubMed Central**: 3 req/sec (10 req/sec with API key)
- **Semantic Scholar**: 100 req/5 min (higher with API key)

### Optional Dependencies
- `anthropic` - Direct Anthropic API (requires `ANTHROPIC_API_KEY`)
- `google-generativeai` - Gemini API (requires `GOOGLE_API_KEY`)
- `google-adk` - Google ADK framework
- `claude-agent-sdk` - Claude SDK (NO API key needed!)
- `selenium` + `webdriver-manager` - For Cloudflare-protected sites

### Development Tools
- `pytest` + `pytest-asyncio` - Testing framework
- `ruff` - Linting and formatting
- `mypy` - Type checking
- `uv` - Fast Python package installer

## Configuration Locations

1. **Project config**: `./config.yaml` (git-ignored)
2. **Example config**: `./config.yaml.example` (version-controlled)
3. **User config**: `~/.config/parser/config.yaml` or `~/.parser.yaml`
4. **Institutional cookies**: `.institutional_cookies.pkl` (git-ignored)
5. **Batch progress**: `.retrieval_progress.json` (git-ignored)

## Known Limitations

### Sources That Don't Work
- ScienceDirect/Elsevier: Aggressive bot detection (Incapsula/Imperva)
- Springer: No public API for PDF access
- Wiley: Same as Springer
- Taylor & Francis: No public PDF API

These require institutional access via VPN/EZProxy.

### Legal Gray Areas
`SciHubClient` and `LibGenClient` are included but disabled by default. Users must:
1. Set `unofficial.disclaimer_accepted: true` in config
2. Enable the specific source
3. Understand legal implications in their jurisdiction

## Python Version

Requires Python 3.11+ (uses modern type hints like `str | None` and `dict[str, Any]`).
