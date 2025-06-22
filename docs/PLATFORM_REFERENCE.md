# Platform Reference Guide

This guide provides quick reference for platform-specific commands and paths when working with docx-processor.

## Environment Paths

| Platform | Project Path | Archive Path |
|----------|-------------|--------------|
| Windows (Claude Desktop) | `D:\Users\alexp\dev\docx-processor` | `D:\Users\alexp\dev\docx-processor\archive` |
| WSL2 (Claude Code) | `/mnt/d/Users/alexp/dev/docx-processor` | `/mnt/d/Users/alexp/dev/docx-processor/archive` |

## Virtual Environment Activation

### Windows (PowerShell)

```powershell
cd "D:\Users\alexp\dev\docx-processor"
.\docx-processor-env\Scripts\Activate.ps1
```

### WSL2/Linux (Bash)

```bash
cd /mnt/d/Users/alexp/dev/docx-processor
source docx-processor-env/bin/activate
```

## Setup Scripts

### Windows

```powershell
.\scripts\setup.ps1
```

### WSL2/Linux

```bash
./scripts/setup.sh
# or
bash scripts/setup.sh
```

## File Operations

### Archiving Files

**Windows (PowerShell)**

```powershell
Copy-Item -Path "src\file.py" -Destination "archive\file_2025-06-22.py"
```

**WSL2/Linux (Bash)**

```bash
cp src/file.py archive/file_2025-06-22.py
```

## Desktop-Commander Usage

### Windows

```python
desktop-commander:execute_command(
    command='Copy-Item -Path "..." -Destination "..."',
    shell="powershell",
    timeout_ms=5000
)
```

### WSL2/Linux

```python
desktop-commander:execute_command(
    command='cp source destination',
    shell="bash",
    timeout_ms=5000
)
```

## Key Differences

1. **Path Separators**: Windows accepts both `\` and `/`, Linux requires `/`
2. **Shell**: Windows uses PowerShell, Linux uses Bash
3. **Scripts**: `.ps1` for Windows, `.sh` for Linux
4. **Permissions**: Windows uses `icacls`, Linux uses `chmod`

## WSL2 Special Notes

- WSL2 accesses Windows drives through mount points (`/mnt/c/`, `/mnt/d/`, etc.)
- File changes in WSL2 are immediately visible in Windows and vice versa
- Use Windows paths when working with Windows tools, WSL2 paths when in Linux environment
