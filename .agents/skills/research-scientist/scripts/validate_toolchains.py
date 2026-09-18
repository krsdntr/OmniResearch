#!/usr/bin/env python3
"""
OmniResearch Toolchain Validator
Zero-dependency CLI tool to audit installed compilers, interpreters, package managers,
and publication engines on the researcher's system.
Compatible with Windows, Linux, and macOS.
"""

import shutil
import subprocess
import sys
from pathlib import Path

TOOLCHAINS = [
    {"name": "Python", "bin": "python", "args": ["--version"], "domain": "General Data Science / ML"},
    {"name": "uv (Fast Python)", "bin": "uv", "args": ["--version"], "domain": "Python Package Management"},
    {"name": "R Script", "bin": "Rscript", "args": ["--version"], "domain": "Biostatistics / Econometrics"},
    {"name": "Julia", "bin": "julia", "args": ["--version"], "domain": "Scientific Computing / ODE"},
    {"name": "GCC / G++", "bin": "g++", "args": ["--version"], "domain": "C++ High Performance"},
    {"name": "Clang", "bin": "clang", "args": ["--version"], "domain": "C/C++ LLVM"},
    {"name": "Typst", "bin": "typst", "args": ["--version"], "domain": "Modern Typesetting / Papers"},
    {"name": "Quarto", "bin": "quarto", "args": ["--version"], "domain": "Scientific Publishing / Reports"},
    {"name": "Pandoc", "bin": "pandoc", "args": ["--version"], "domain": "Document Conversion"},
    {"name": "Git", "bin": "git", "args": ["--version"], "domain": "Version Control & Lineage"},
    {"name": "Docker", "bin": "docker", "args": ["--version"], "domain": "Containerized Reproducibility"}
]

def check_tool(tool: dict) -> tuple[bool, str]:
    bin_path = shutil.which(tool["bin"])
    if not bin_path:
        return False, "Not Found"
    try:
        res = subprocess.run(
            [bin_path] + tool["args"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5
        )
        first_line = res.stdout.strip().split("\n")[0] if res.stdout else "Available"
        return True, first_line[:40]
    except Exception as e:
        return True, "Found (version check timed out)"

def main():
    print("=" * 75)
    print(" " * 20 + "OmniResearch Toolchain Audit")
    print("=" * 75)
    print(f"{'Tool / Compiler':<18} | {'Status':<10} | {'Domain / Usage':<25} | {'Version Details'}")
    print("-" * 75)

    ready_count = 0
    for t in TOOLCHAINS:
        found, details = check_tool(t)
        status_str = "[READY]" if found else "[MISSING]"
        if found:
            ready_count += 1
        print(f"{t['name']:<18} | {status_str:<10} | {t['domain']:<25} | {details}")

    print("=" * 75)
    print(f"Summary: {ready_count}/{len(TOOLCHAINS)} toolchains detected.")
    if ready_count < len(TOOLCHAINS):
        print("\nNote: Missing toolchains are only required if your specific project uses them.")
        print("  - For Biostatistics/Econometrics: Install R (https://cran.r-project.org/)")
        print("  - For High-Performance ODE: Install Julia (https://julialang.org/)")
        print("  - For Fast Python Management: Install uv (https://github.com/astral-sh/uv)")
        print("  - For Modern Papers: Install Typst (https://typst.app/)")

if __name__ == "__main__":
    main()
