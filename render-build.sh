#!/usr/bin/env bash
set -e  # Exit immediately if any command fails

echo "==> Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "==> Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "==> Build complete!"
