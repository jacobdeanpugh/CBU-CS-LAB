# Firefox Policies Configuration

## Overview
This folder contains the `policies.json` file, which defines organizational policy settings that should be deployed across all Firefox installations within the lab environment.

## Installation

The installation location varies by operating system. Ensure Firefox is closed before placing the policy file, and create any missing directories in the path.

### Linux (DGX Sparks)
```
/etc/firefox/policies/policies.json
```

### Windows
```
C:\Program Files\Mozilla Firefox\distribution\policies.json
```

### macOS
```
/Applications/Firefox.app/Contents/Resources/distribution/policies.json
```

## Deployment Steps

1. **Locate or create the appropriate directory** for your operating system
2. **Copy `policies.json`** to the directory path shown above
3. **Restart Firefox** for the policies to take effect
4. **Verify** the policies are active by navigating to `about:policies` in Firefox

## Troubleshooting

- If policies don't apply, verify the file is named exactly `policies.json` (case-sensitive on Linux/macOS)
- Ensure the file has appropriate read permissions for all users
- Check Firefox version compatibility with the policies defined

## Additional Resources

For more information on Firefox policies, visit the [official Mozilla documentation](https://github.com/mozilla/policy-templates).