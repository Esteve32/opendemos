const state = {
  demos: [],
  filtered: [],
  activeTags: new Set(),
  search: ''
};

const els = {
  grid: document.getElementById('grid'),
  search: document.getElementById('search'),
  tags: document.getElementById('tags')
};

async function loadDemos() {
  try {
    const res = await fetch('demos.json', { cache: 'no-store' });
    if (!res.ok) throw new Error(`Failed to fetch demos.json: ${res.status}`);
    const data = await res.json();
    state.demos = Array.isArray(data) ? data : [];
    buildTagCloud();
    applyFilters();
  } catch (err) {
    console.error(err);
    els.grid.innerHTML = `<p>Could not load demos.json. Make sure it exists at the repo root.</p>`;
  }
}

function buildTagCloud() {
  const tagCounts = new Map();
  for (const d of state.demos) {
    (d.tags || []).forEach(t => tagCounts.set(t, (tagCounts.get(t) || 0) + 1));
  }
  const sorted = Array.from(tagCounts.entries()).sort((a,b)=>b[1]-a[1]).slice(0, 15);
  els.tags.innerHTML = '';
  for (const [tag] of sorted) {
    const btn = document.createElement('button');
    btn.className = 'tag';
    btn.type = 'button';
    btn.textContent = tag;
    btn.setAttribute('aria-pressed', state.activeTags.has(tag) ? 'true' : 'false');
    btn.addEventListener('click', () => {
      if (state.activeTags.has(tag)) state.activeTags.delete(tag);
      else state.activeTags.add(tag);
      btn.setAttribute('aria-pressed', state.activeTags.has(tag) ? 'true' : 'false');
      applyFilters();
    });
    els.tags.appendChild(btn);
  }
}

function applyFilters() {
  const q = state.search.toLowerCase().trim();
  const reqTags = state.activeTags;
  state.filtered = state.demos.filter(d => {
    const text = `${d.title} ${d.description} ${(d.tags||[]).join(' ')}`.toLowerCase();
    const matchesText = !q || text.includes(q);
    const matchesTags = reqTags.size === 0 || (d.tags || []).some(t => reqTags.has(t));
    return matchesText && matchesTags;
  });
  renderGrid();
}

function renderGrid() {
  if (state.filtered.length === 0) {
    els.grid.innerHTML = `<p>No demos match your filters.</p>`;
    return;
  }
  els.grid.innerHTML = state.filtered.map(cardHTML).join('');
}

function cardHTML(demo) {
  const safeThumb = demo.thumbnail || '';
  const safeHref = demo.path || '#';
  const tags = (demo.tags || []).map(t => `<span class="badge">${escapeHtml(t)}</span>`).join('');
  return `
  <a href="${escapeAttr(safeHref)}" class="card">
    ${safeThumb ? `<img class="thumb" src="${escapeAttr(safeThumb)}" alt="">` : `<div class="thumb" role="img" aria-label="Preview"></div>`}
    <div class="card-body">
      <strong class="card-title">${escapeHtml(demo.title || 'Untitled')}</strong>
      <p class="card-desc">${escapeHtml(demo.description || '')}</p>
      <div class="card-tags">${tags}</div>
    </div>
  </a>
  `;
}

function escapeHtml(s='') {
  return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));
}
function escapeAttr(s='') {
  return s.replace(/"/g, '&quot;');
}

els.search.addEventListener('input', (e) => {
  state.search = e.target.value || '';
  applyFilters();
});

loadDemos();