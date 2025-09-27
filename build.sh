#!/bin/bash

echo "🚀 Building MINI FIRE with Kivy Docker..."

# Build image
docker build -t minifire-kivy .

# Run build
docker run --rm \
  -v $(pwd):/app \
  -v minifire-kivy-cache:/root/.buildozer \
  minifire-kivy

echo "✅ Build complete! Check bin/ directory."
