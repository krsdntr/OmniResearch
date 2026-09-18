#!/usr/bin/env bash
# OmniResearch Universal Installer for Linux and macOS
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/krsdntr/OmniResearch/main/install.sh | bash

set -e

REPO_URL="https://github.com/krsdntr/OmniResearch.git"
GLOBAL_GEMINI_DIR="$HOME/.gemini/config/skills/research-scientist"

echo "========================================================"
echo "    OmniResearch Scientist Workbench Installer          "
echo "========================================================"

TARGET_MODE="global"
TARGET_DIR="$GLOBAL_GEMINI_DIR"

if [ "$1" == "--local" ]; then
    TARGET_MODE="local"
    TARGET_DIR="./.agents/skills/research-scientist"
fi

echo "[+] Target Installation: $TARGET_MODE ($TARGET_DIR)"

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "[+] Fetching latest OmniResearch Skill..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR/omni" > /dev/null 2>&1

mkdir -p "$TARGET_DIR"
cp -r "$TEMP_DIR/omni/.agents/skills/research-scientist/"* "$TARGET_DIR/"

# If local mode, also copy bridges
if [ "$TARGET_MODE" == "local" ]; then
    cp "$TEMP_DIR/omni/GEMINI.md" ./ 2>/dev/null || true
    cp "$TEMP_DIR/omni/CLAUDE.md" ./ 2>/dev/null || true
    cp "$TEMP_DIR/omni/AGENTS.md" ./ 2>/dev/null || true
    cp "$TEMP_DIR/omni/.cursorrules" ./ 2>/dev/null || true
fi

echo "[✔] OmniResearch successfully installed to: $TARGET_DIR"
echo ""
echo "How to use in Google Antigravity:"
echo "  - Simply open any research workspace and ask:"
echo "    'Initialize an OmniResearch scientific study for my project.'"
echo "========================================================"
