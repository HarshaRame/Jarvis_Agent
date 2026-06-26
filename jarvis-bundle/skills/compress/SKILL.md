---
name: compress
description: >
  Compress natural language memory files into caveman format
  to save input tokens. Preserves code, URLs, and structure.
---

# Caveman Compress

Compress natural language files (CLAUDE.md, todos, preferences) into caveman-speak to reduce input tokens.

## Trigger

`/caveman:compress <filepath>` or when user asks to compress a memory file.

## Compression Rules

### Remove
- Articles: a, an, the
- Filler: just, really, basically, actually, simply, essentially, generally
- Pleasantries: "sure", "certainly", "of course", "happy to", "I'd recommend"
- Hedging: "it might be worth", "you could consider"
- Redundant phrasing: "in order to" → "to", "make sure to" → "ensure"

### Preserve EXACTLY
- Code blocks (fenced ``` and indented) — copy EXACTLY
- Inline code (`backtick content`) — copy EXACTLY  
- URLs and links (full URLs, markdown links)
- File paths (`/src/components/...`, `./config.yaml`)
- Commands (`npm install`, `git commit`, `docker build`)
- Technical terms (library names, API names, protocols)
- Proper nouns (project names, people, companies)
- Dates, version numbers, numeric values
- Environment variables (`$HOME`, `NODE_ENV`)

### Preserve Structure
- All markdown headings (keep exact heading text, compress body below)
- Bullet point hierarchy (keep nesting level)
- Numbered lists (keep numbering)
- Tables (compress cell text, keep structure)
- Frontmatter/YAML headers

### Compress
- Use short synonyms: "big" not "extensive", "fix" not "implement a solution for", "use" not "utilize"
- Fragments OK: "Run tests before commit" not "You should always run tests before committing"
- Drop "you should", "make sure to", "remember to" — just state the action

## Boundaries

- ONLY compress natural language files (.md, .txt)
- NEVER modify: .py, .js, .ts, .json, .yaml, .yml, .toml, .env, .lock, .css, .html, .xml, .sql, .sh
- If file has mixed content (prose + code), compress ONLY prose sections
- Original backed up as FILE.original.md before overwriting
- Never compress FILE.original.md (skip it)
