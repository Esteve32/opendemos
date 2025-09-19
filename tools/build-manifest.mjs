#!/usr/bin/env node
import { promises as fs } from 'node:fs';
import path from 'node:path';
import url from 'node:url';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const demosRoot = path.join(repoRoot, 'demos');
const manifestPath = path.join(repoRoot, 'demos.json');

function log(...args) { console.log('[build-manifest]', ...args); }

async function exists(p) {
  try { await fs.access(p); return true; } catch { return false; }
}

async function readJSON(p) {
  const raw = await fs.readFile(p, 'utf8');
  return JSON.parse(raw);
}

async function main() {
  if (!await exists(demosRoot)) {
    log(`No demos directory found at ${demosRoot}`);
    process.exit(0);
  }

  const entries = await fs.readdir(demosRoot, { withFileTypes: true });
  const dirs = entries.filter(e => e.isDirectory()).map(e => e.name);

  const manifest = [];
  for (const dir of dirs) {
    const demoDir = path.join(demosRoot, dir);
    const metaFile = path.join(demoDir, 'meta.json');
    const indexHtml = path.join(demoDir, 'index.html');

    if (!await exists(indexHtml)) {
      log(`Skipping ${dir}: missing index.html`);
      continue;
    }

    let meta = {};
    if (await exists(metaFile)) {
      try { meta = await readJSON(metaFile); }
      catch (e) { log(`Warning: failed to parse meta.json in ${dir}:`, e.message); }
    }

    // find a thumbnail if present
    const thumbs = ['png','jpg','jpeg','webp','gif'].map(ext => path.join(demoDir, `thumbnail.${ext}`));
    let thumbRel = '';
    for (const t of thumbs) {
      if (await exists(t)) { thumbRel = path.relative(repoRoot, t).replace(/\\/g, '/'); break; }
    }

    manifest.push({
      id: dir,
      title: meta.title || dir,
      description: meta.description || '',
      path: path.posix.join('demos', dir, 'index.html'),
      thumbnail: thumbRel,
      tags: Array.isArray(meta.tags) ? meta.tags : []
    });
  }

  // Sort by title for consistent ordering
  manifest.sort((a, b) => a.title.localeCompare(b.title, undefined, { sensitivity: 'base' }));

  await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
  log(`Wrote ${manifest.length} demo(s) to ${path.relative(repoRoot, manifestPath)}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});