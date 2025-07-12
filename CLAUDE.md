# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is Ethan Swan's personal website built with Hugo and styled with Tailwind CSS. The site includes a blog, teaching materials, speaking engagements, and various content sections. It's deployed on Cloudflare with automatic builds.

## Architecture

- **Static Site Generator**: Hugo (configured via `hugo.yaml`)
- **Styling**: Tailwind CSS (configured in `tailwind/` directory)
- **Content**: Markdown files in `content/` directory organized by section
- **Layouts**: Hugo templates in `layouts/` directory
- **Assets**: Images and static files in `assets/` and `static/` directories
- **Testing**: Python-based test suite in `test-suite/` directory

## Development Commands

### Local Development
To run the site locally, you need both Hugo and Tailwind running simultaneously:

**Terminal 1 (from repository root):**
```bash
hugo serve
```

**Terminal 2 (from tailwind/ directory):**
```bash
cd tailwind/
npm run watch
```

This setup allows Tailwind to rebuild CSS when content or layout files change, which Hugo then picks up automatically.

### Tailwind CSS Commands
```bash
cd tailwind/
npm run build    # Build CSS for production
npm run watch    # Watch for changes and rebuild CSS
```

### Testing
The test suite uses Python with pytest and is managed with UV:

```bash
cd test-suite/
uv venv                           # First time setup
. .venv/bin/activate             # Activate environment
uv pip install -e ".[dev]"      # Install dependencies
pytest                           # Run tests
```

To test against a local development server:
```bash
ES_SITE_URL=http://localhost:1313 pytest
```

## Content Structure

- **Blog posts**: `content/posts/YYYY/` organized by year
- **Teaching materials**: `content/courses/` and `content/teaching/`
- **Speaking engagements**: `content/speaking/`
- **Coffee shop ratings**: `content/coffee_shop_ratings/`
- **Running blog**: `content/running-blog/`

## Key Files

- `hugo.yaml`: Hugo configuration
- `tailwind/package.json`: Tailwind dependencies and build scripts
- `tailwind/tailwind.config.js`: Tailwind configuration
- `layouts/`: Custom Hugo templates and partials
- `static/css/tailwind-style.css`: Generated Tailwind CSS (committed to repo)

## Deployment

The site is deployed on Cloudflare. The `static/css/tailwind-style.css` file must be committed since Cloudflare doesn't run the Tailwind build process.

## Testing Strategy

The Python test suite in `test-suite/` includes:
- Smoke tests to verify site functionality
- Dead link detection
- Site structure validation

Tests can run against both the live site and local development instances.