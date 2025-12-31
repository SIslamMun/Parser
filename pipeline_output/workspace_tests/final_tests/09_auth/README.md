# Test 09: Auth

## Command
```bash
parser auth
```

## Description
Authenticates with institutional access (VPN or EZProxy).

## Expected Output
- Opens browser for EZProxy login
- Saves session cookies

## Result
⚠️ **SKIP** - Requires institutional config

## Output
```
Error: Institutional access not enabled

Add the following to your config.yaml:
  institutional:
    enabled: true
    proxy_url: "https://ezproxy.your-university.edu/login?url="
```

## Prerequisites
Configure in `config.yaml`:
```yaml
institutional:
  enabled: true
  # Option A: VPN Mode
  vpn_enabled: true
  vpn_script: "./scripts/vpn-connect.sh"
  
  # Option B: EZProxy Mode
  proxy_url: "https://ezproxy.gl.iit.edu/login?url="
```

## Modes

### VPN Mode
1. Connect to university VPN
2. Set `vpn_enabled: true`
3. Papers download through VPN

### EZProxy Mode
1. Set `proxy_url` to your university's EZProxy URL
2. Run `parser auth`
3. Complete login in browser
4. Session saved for future use

## Notes
- Cookies stored in `.institutional_cookies.pkl`
- Re-run `parser auth` if session expires
- VPN mode is more reliable than EZProxy
