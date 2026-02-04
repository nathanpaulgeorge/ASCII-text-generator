# ASCII Art Generator

Self-contained ASCII text generator with a CLI and a static web UI.

Features
- Pure Python CLI (no external deps) with size presets: small/medium/large/huge (scales 1/2/4/8)
- Static web UI (works offline) using the same built-in 5x7 font
- Change site title and defaults via docs/site-config.json
- Choose draw character (e.g., '#', '*', '█'), spacing, and custom scale

Quick start — CLI
1. Make the script executable:
   chmod +x ascii_generator.py
2. Render:
   ./ascii_generator.py "Hello World" --size huge --char "█"
3. Save to file:
   ./ascii_generator.py "Hello" -o hello.txt
4. From stdin:
   echo "Pipe me" | ./ascii_generator.py --stdin

Quick start — Web UI
1. Put the site files in the `docs/` folder at repo root (docs/index.html, docs/style.css, docs/script.js, docs/site-config.json).
2. Enable GitHub Pages: Settings → Pages → Branch: main, Folder: /docs.
3. Visit the Pages URL (https://<your-username>.github.io/<repo-name>), type text, click Render.
4. Use Copy (adds attribution) or Download (file includes attribution).

Publishing to GitHub Pages (recommended)
- Use the included publish.sh script (requires GitHub CLI `gh` and git) or upload files using the GitHub web UI.

License
This project is licensed under the MIT License (see LICENSE).
