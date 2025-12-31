# Test 10: Config

## Commands
```bash
parser config push
parser config pull
```

## Description
Syncs configuration across machines using GitHub Gists.

## Expected Output
- Push: Creates/updates private gist with config
- Pull: Downloads config from gist

## Result
✅ **PASS** (help works)

## Output (Help)
```
Usage: parser config [OPTIONS] COMMAND [ARGS]...

  Manage configuration sync across machines.

Options:
  --help  Show this message and exit.

Commands:
  pull  Pull config from a private GitHub gist.
  push  Push config to a private GitHub gist.
```

## Prerequisites
1. Install GitHub CLI: `brew install gh` or `apt install gh`
2. Authenticate: `gh auth login`
3. Grant gist scope

## Usage

### Push Config
```bash
# First time - creates new gist
parser config push

# Update existing gist
parser config push --gist-id <gist_id>
```

### Pull Config
```bash
parser config pull --gist-id <gist_id>
```

## Notes
- Uses private gists (only you can see)
- Requires GitHub CLI (`gh`) installed and authenticated
- Useful for syncing config across multiple machines
