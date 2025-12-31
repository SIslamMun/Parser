# Test 08: Init

## Command
```bash
parser init
```

## Description
Initializes a configuration file with default settings.

## Expected Output
- Creates `config.yaml` with template
- Prompts to overwrite if exists

## Result
✅ **PASS**

## Output
```
config.yaml exists. Overwrite? [y/N]: y
Created config.yaml
Please edit the file and set your email address.
```

## Files Generated
- `config.yaml` - Configuration template

## Configuration Sections
```yaml
user:
  email: "your.email@university.edu"

api_keys:
  ncbi: null
  semantic_scholar: null

institutional:
  enabled: false
  vpn_enabled: false
  proxy_url: null

sources:
  unpaywall:
    enabled: true
    priority: 1
  # ... more sources

download:
  output_dir: "./downloads"
  filename_format: "{first_author}_{year}_{title_short}.pdf"

rate_limits:
  global_delay: 1.0
  # ... per-source delays

batch:
  max_concurrent: 3

agent:
  anthropic:
    api_key: null
  gemini:
    api_key: null
```

## Notes
- Must set email for API access
- Sources can be enabled/disabled
- Rate limits respect API guidelines
