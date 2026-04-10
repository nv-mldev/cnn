# LLM Wiki — Setup Plan for `desktop-local`

Based on Karpathy's LLM Wiki pattern. Build a persistent, compounding knowledge base for the CNN tutorial series, served as a browser UI from `desktop-local`'s public IP.

---

## Goal

- Wiki lives on `desktop-local` as a directory of markdown files
- Claude Code on `desktop-local` reads/writes the wiki (agent is the programmer, wiki is the codebase)
- MkDocs serves the wiki as a static site, auto-reloading on changes
- Nginx reverse proxies it to the public IP so you can browse from anywhere

---

## Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Wiki files | Markdown in `~/projects/cnn/wiki/` | The persistent knowledge base |
| Static site | MkDocs + Material theme | Renders markdown → browser UI |
| Reverse proxy | Nginx | Exposes MkDocs on public IP |
| Agent | Claude Code | Writes and maintains the wiki |
| Auth | Nginx basic auth | Protects wiki behind a password |

---

## Directory Layout

```
~/projects/cnn/
├── wiki/
│   ├── index.md                  # MkDocs home page + wiki catalog
│   ├── log.md                    # Append-only ingest/query history
│   ├── concepts/
│   │   ├── gaussian_noise.md
│   │   ├── normalisation.md
│   │   ├── dot_product.md
│   │   └── ...
│   ├── notebooks/
│   │   ├── 00_digital_images.md
│   │   ├── 01a_probability.md
│   │   ├── 01b_linear_algebra.md
│   │   └── 02_why_not_pixels.md
│   └── synthesis/
│       └── cs231n_prerequisites.md
├── mkdocs.yml                    # MkDocs config
├── raw/                          # Immutable source documents (existing DIP3E images etc.)
└── CLAUDE.md                     # Already exists — extend with wiki schema section
```

---

## Step 1 — Install Dependencies

```bash
pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin
```

Or with uv (preferred):
```bash
uv add mkdocs mkdocs-material mkdocs-awesome-pages-plugin
```

---

## Step 2 — MkDocs Config

Create `~/projects/cnn/mkdocs.yml`:

```yaml
site_name: CNN Tutorial Wiki
site_description: Personal knowledge base for CNN tutorial series
docs_dir: wiki
site_dir: site

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.highlight
    - content.code.copy
  palette:
    scheme: slate          # dark mode — easier on eyes

plugins:
  - search
  - awesome-pages

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.arithmatex:       # LaTeX math rendering
      generic: true
  - admonition
  - toc:
      permalink: true

extra_javascript:
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js
```

---

## Step 3 — Run MkDocs (dev mode with live reload)

```bash
cd ~/projects/cnn
mkdocs serve --dev-addr=0.0.0.0:8000
```

To run as a background service (systemd):

```ini
# /etc/systemd/system/mkdocs-wiki.service
[Unit]
Description=MkDocs Wiki Server
After=network.target

[Service]
User=nithin
WorkingDirectory=/home/nithin/projects/cnn
ExecStart=/home/nithin/.venv/bin/mkdocs serve --dev-addr=0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mkdocs-wiki
sudo systemctl start mkdocs-wiki
```

---

## Step 4 — Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/wiki
server {
    listen 80;
    server_name <your-public-ip>;   # or a domain if you have one

    # Basic auth — protects the wiki from public access
    auth_basic "Wiki";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";   # needed for mkdocs live reload websocket
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/wiki /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Set up password:
```bash
sudo apt install apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd nithin
# enter password when prompted
```

Access: `http://<public-ip>/`

---

## Step 5 — Extend CLAUDE.md with Wiki Schema

Add this section to `~/projects/cnn/CLAUDE.md` on `desktop-local`:

```markdown
## Wiki

The wiki at `wiki/` is a persistent knowledge base maintained by Claude Code.
You (Claude) own this layer entirely — create pages, update them, maintain cross-references.

### Directory conventions
- `wiki/concepts/` — one page per concept (gaussian_noise.md, normalisation.md, etc.)
- `wiki/notebooks/` — one summary page per tutorial notebook
- `wiki/synthesis/` — cross-cutting analysis, comparisons, the "big picture"
- `wiki/index.md` — catalog of all pages with one-line summaries (keep updated)
- `wiki/log.md` — append-only log, format: `## [YYYY-MM-DD] <operation> | <title>`

### On ingest (new source or notebook draft)
1. Read the source
2. Write a summary page in the appropriate subdirectory
3. Update `wiki/index.md` with a new entry
4. Update any related concept pages with new connections or contradictions
5. Append an entry to `wiki/log.md`

### On query
1. Read `wiki/index.md` to find relevant pages
2. Read those pages
3. Synthesize an answer with citations to wiki pages
4. If the answer is non-trivial and reusable, file it as a new page in `wiki/synthesis/`

### On lint (periodic health check)
Check for: contradictions between pages, stale claims, orphan pages (no inbound links),
concepts mentioned but lacking their own page, missing cross-references.

### Page frontmatter (YAML)
Every wiki page should start with:
\`\`\`yaml
---
tags: [concept|notebook|synthesis]
notebook_refs: [00, 01a, 01b, 02]   # which notebooks reference this
last_updated: YYYY-MM-DD
---
\`\`\`
```

---

## Step 6 — Seed the Wiki

Once the server is running, ask Claude Code on `desktop-local` to seed the wiki from existing notebooks:

```
Ingest all existing tutorial notebooks in tutorials/ into the wiki.
For each notebook: write a summary page in wiki/notebooks/, extract key concepts
into wiki/concepts/, update wiki/index.md, and append to wiki/log.md.
```

---

## Access Summary

| From | How |
|------|-----|
| Browser (anywhere) | `http://<public-ip>/` + password |
| Terminal (anywhere) | `ssh desktop-local` then `claude` in `~/projects/cnn` |
| VS Code | Remote SSH to `desktop-local`, open `~/projects/cnn` |

---

## Optional Later

- **HTTPS** — add a domain + Let's Encrypt (`certbot --nginx`)
- **Search** — MkDocs Material has built-in search, good enough for hundreds of pages
- **Git history** — wiki is just files, `git log wiki/` gives you full edit history
- **qmd** — local BM25/vector search CLI if wiki grows beyond ~200 pages
