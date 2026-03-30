#!/usr/bin/env bash
# KairuAI — One-line installer
# Usage: bash install.sh

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}  KairuAI — Autonomous AI Trading Agent${NC}"
echo -e "${CYAN}  \$KAIRUAI · Built on Solana${NC}"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}Error: Python 3.11+ is required.${NC}"
  exit 1
fi
echo -e "  ${GREEN}✓${NC} Python $(python3 --version) detected"

# Check Node
if ! command -v node &>/dev/null; then
  echo -e "${RED}Error: Node.js 18+ is required.${NC}"
  exit 1
fi
echo -e "  ${GREEN}✓${NC} Node.js $(node --version) detected"

# Python deps
echo "  Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo -e "  ${GREEN}✓${NC} Python dependencies installed"

# Node deps
echo "  Installing TypeScript dependencies..."
npm install --silent
echo -e "  ${GREEN}✓${NC} TypeScript dependencies installed"

# Setup .env
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo -e "  ${GREEN}✓${NC} .env created from template"
  echo ""
  echo -e "  ${CYAN}Next:[/cyan] Open .env and add your API keys"
else
  echo -e "  ${GREEN}✓${NC} .env already exists"
fi

echo ""
echo -e "  ${GREEN}Setup complete.${NC}"
echo ""
echo "  Run KairuAI:"
echo "    python kairu.py"
echo ""
