#!/usr/bin/env node
"use strict";
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const INPUT_DIR = path.resolve(__dirname, '..', 'mermaid_blocks');
const OUTPUT_DIR = path.resolve(__dirname, '..', 'generated_images');

// Determine output format from command line (--format svg|png). Default svg
let format = 'svg';
for (let i = 2; i < process.argv.length; i++) {
  const arg = process.argv[i];
  if ((arg === '--format' || arg === '-f') && process.argv[i+1]) {
    format = process.argv[i+1];
    i++;
  }
}
if (!['svg', 'png'].includes(format)) {
  console.error(`Unsupported format: ${format}`);
  process.exit(1);
}

if (!fs.existsSync(INPUT_DIR)) {
  console.error(`Input directory not found: ${INPUT_DIR}`);
  process.exit(1);
}

fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const files = fs.readdirSync(INPUT_DIR).filter(f => f.endsWith('.mmd'));

if (files.length === 0) {
  console.log('No .mmd files found in', INPUT_DIR);
  process.exit(0);
}

for (const file of files) {
  const inputPath = path.join(INPUT_DIR, file);
  const outName = file.replace(/\.mmd$/, `.${format}`);
  const outputPath = path.join(OUTPUT_DIR, outName);

  const result = spawnSync('mmdc', ['-i', inputPath, '-o', outputPath], {
    stdio: 'inherit'
  });

  if (result.status === 0) {
    console.log(`Converted ${file} -> ${outName}`);
  } else {
    console.error(`Failed to convert ${file}`);
  }
}
