# JGTML Agent Guide

This guide introduces the major capabilities provided by **jgtml**. Each section describes how to generate datasets, perform analysis, and automate workflows with the included CLIs.

## Quick Command Reference
```bash
# Data Generation & Analysis
jgtmlcli -i EUR/USD -t D1 --full --fresh
mxcli -i EUR/USD -t D1 --fresh
python -m jgtml.alligator_cli -i EUR/USD -t D1 -d B --type all

# Trading Operations
jgtapp fxaddorder -i EUR/USD -n 0.1 -r 1.0950 -d B -x 1.0900

# Documentation
guidecli_jgtml --list    # Show available sections
```

## Core Sections
- [Overview](overview.md) — Architecture and data layout
- [CLI Tools](cli_tools.md) — Commands for analysis and trading
- [Automation](automation.md) — Offline dataset generation

Use `guidecli_jgtml --section <name>` to display a page or `--all` to print them in sequence. Combine these docs with `CLI_HELP.md` for a deeper dive into each option.
