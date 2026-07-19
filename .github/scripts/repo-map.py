#!/usr/bin/env python3
"""Deterministic repo map generator (Aider-style, dependency-free).

Walks a repo and emits a compact markdown map: directory tree + the key
exported symbols per file (functions, classes, types, components, SQL
objects), trimmed to a line budget. Agents read this instead of exploring
with dozens of Read/Grep calls.

Usage: repo-map.py <repo-root> [--max-lines 400]
"""

import argparse
import os
import re
import sys

SKIP_DIRS = {
    ".git", "node_modules", ".next", "dist", "build", "out", "coverage",
    "__pycache__", ".venv", "venv", ".turbo", ".vercel", "vendor",
}
EXTS = {
    ".ts", ".tsx", ".js", ".jsx", ".py", ".sql", ".rb", ".go", ".rs",
    ".sh", ".md", ".yml", ".yaml",
}

PATTERNS = [
    # ts/js exports
    re.compile(
        r"^export\s+(?:default\s+)?(?:async\s+)?"
        r"(function|class|const|interface|type|enum)\s+([A-Za-z0-9_$]+)"
    ),
    # python defs/classes (top-level only)
    re.compile(r"^(def|class)\s+([A-Za-z0-9_]+)"),
    # sql objects
    re.compile(
        r"^\s*CREATE\s+(?:OR\s+REPLACE\s+)?"
        r"(TABLE|FUNCTION|VIEW|TRIGGER|POLICY|INDEX)\s+"
        r"(?:IF\s+NOT\s+EXISTS\s+)?[\"']?([A-Za-z0-9_.]+)",
        re.IGNORECASE,
    ),
    # go/rust
    re.compile(r"^(?:pub\s+)?(fn|func|struct|impl|trait)\s+([A-Za-z0-9_]+)"),
    # shell functions
    re.compile(r"^(?:(function)\s+)?([A-Za-z0-9_]+)\(\)\s*\{"),
    # markdown h2 headings (doc section index)
    re.compile(r"^(##)\s+(.{1,60}?)\s*$"),
]


def symbols(path):
    out = []
    try:
        with open(path, errors="replace") as f:
            for line in f:
                if len(out) >= 12:
                    out.append("…")
                    break
                for pat in PATTERNS:
                    m = pat.match(line)
                    if m:
                        kind = (m.group(1) or "fn").lower()
                        kind = "\u00a7" if kind == "##" else kind
                        out.append(f"{kind} {m.group(2)}")
                        break
    except OSError:
        pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--max-lines", type=int, default=400)
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    entries = []  # (rel_path, [symbols])
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
        )
        for fn in sorted(filenames):
            ext = os.path.splitext(fn)[1]
            if ext not in EXTS and ext != "":
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            entries.append((rel, symbols(full)))

    print("## Repo map (generated — do not edit by hand)")
    print()
    dirs = {os.path.dirname(rel) or "." for rel, _ in entries}
    budget = args.max_lines - len(dirs)
    # degrade gracefully so no file is ever omitted: one line per file with
    # symbols when it fits, else name-only files grouped 6 per line
    symbol_cap = 12 if budget >= len(entries) else 0
    cur_dir = None
    row = []
    for rel, syms in entries:
        d = os.path.dirname(rel) or "."
        if d != cur_dir:
            if row:
                print("- " + ", ".join(row))
                row = []
            print(f"**{d}/**")
            cur_dir = d
        name = os.path.basename(rel)
        shown = syms[:symbol_cap]
        if shown:
            extra = f" (+{len(syms) - len(shown)})" if len(syms) > len(shown) else ""
            print(f"- {name} — {'; '.join(shown)}{extra}")
        elif symbol_cap:
            print(f"- {name}")
        else:
            row.append(name)
            if len(row) >= 6:
                print("- " + ", ".join(row))
                row = []
    if row:
        print("- " + ", ".join(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
