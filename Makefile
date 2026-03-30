# KairuAI · Makefile

.PHONY: install install-ts install-py run predict signal trading polymarket clean help

help:
	@echo ""
	@echo "  KairuAI — Autonomous AI Trading Agent"
	@echo ""
	@echo "  Setup:"
	@echo "    make install       Install all dependencies (Python + Node)"
	@echo "    make install-py    Install Python dependencies only"
	@echo "    make install-ts    Install TypeScript dependencies only"
	@echo ""
	@echo "  Run:"
	@echo "    make run           Launch KairuAI interactive menu"
	@echo "    make predict       Launch Prediction Agent"
	@echo "    make signal        Launch Signal Agent"
	@echo "    make trading       Launch Trading Agent (TypeScript)"
	@echo "    make polymarket    Launch Polymarket Agent (TypeScript)"
	@echo ""
	@echo "    make clean         Remove cache files"
	@echo ""

install: install-py install-ts

install-py:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

install-ts:
	@echo "Installing TypeScript dependencies..."
	npm install

run:
	python kairu.py

predict:
	python kairu.py predict

signal:
	python kairu.py signal

trading:
	cd agents/trading && npm run dev

polymarket:
	cd agents/polymarket && npm run dev

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.tsbuildinfo" -delete 2>/dev/null || true
	@echo "Cache cleared."
