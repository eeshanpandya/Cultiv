# Cultiv

Daily agrochem industry news and insights, in plain language, installable as a phone app.

- The app is a static web app served by GitHub Pages (`index.html`, `manifest.webmanifest`, `sw.js`, `icons/`).
- Every edition in `data/` is encrypted (AES-256-GCM, key derived from a passcode with PBKDF2-SHA256). Without the passcode the files are unreadable.
- A scheduled task writes a new edition each morning and publishes it with `tools/publish.py`.

To read Cultiv, open the site, enter the passcode once, then use your browser's "Install app" or "Add to Home screen".
