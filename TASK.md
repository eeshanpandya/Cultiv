# Cultiv daily edition: instructions for the scheduled run

You are writing today's edition of **Cultiv**, a daily agrochemical-industry intelligence app for Ishan Pandya (Growth Office, International Business Division, Indofil Industries Ltd, Mumbai).

Cultiv has two front ends that show the same data:

- **(a)** a claude.ai artifact whose content lives in its database: https://claude.ai/artifact/CK8NwcnhSRB3vojAffG9Wa
- **(b)** this repository (eeshanpandya/Cultiv), an installable web app on GitHub Pages that reads encrypted copies of the same documents.

Do NOT republish or edit the artifact page itself; only write its database documents with the ArtifactData tool (load it first with ToolSearch query `select:ArtifactData`). Today's date is the current date in Asia/Kolkata (YYYY-MM-DD).

The passcode used to encrypt editions is given in the scheduled task's prompt. Never write it into any file in this repository.

## Writing style (most important)

The reader wants news that is EASY TO UNDERSTAND and makes them want to tap. Stories appear as cards showing a plain headline, a one-line explainer and one big number; tapping opens the full story. Every number tile and chart on the front page also opens the story behind it, so link them (see `kpis.item` and `charts.items`).

- Write clear, specific, curiosity-worthy headlines (no clickbait, no exaggeration).
- Use short sentences and everyday words. Explain who a company is the first time it appears ("Rallis, a Tata company").
- Avoid unexplained jargon; when a technical term is unavoidable, add it to the glossary.
- Plain, concise English; Indian conventions for ₹ (crore); no emoji.
- Keep short fields short: kpi delta ≤22 characters, kpi label ≤26 characters, stat value ≤12 characters.

## Step 1: Load context

- ArtifactData get `meta/index` (collection `meta`, doc_id `index`). Its `dates` array lists past editions, newest first.
- ArtifactData get the newest edition (collection `editions`, doc_id = newest date) and save it with `out_dir` so you can read it. It is the exact JSON template for today's document: same keys, same shapes.
- ArtifactData list collection `threads` (story threads with timelines). Note each doc's version.
- If an edition for today already exists, update it rather than creating a duplicate.

## Step 2: Research (WebSearch then WebFetch the articles; 15–25 searches)

Cover news since the previous edition (usually the last 24–48 hours; on Mondays include the weekend). Search separately for:

- agrochemical / crop protection industry news
- results and deals (UPL, PI Industries, Sharda, Dhanuka, Rallis, Bayer, Syngenta, ADAMA, Corteva, FMC, BASF, Nufarm, Sumitomo, Crystal, Coromandel, Best Agrolife, Bharat Rasayan, Dharmaj, Meghmani, etc.)
- Indian domestic news specifically (CIB&RC, state agriculture departments, crop sowing, Indian company announcements, farmer demand, GST and subsidies)
- China pesticide technical prices and export data
- mancozeb / dithiocarbamates / fungicide markets
- regulation (EU approvals and MRLs, India's Pesticides Management Bill, Brazil MAPA/ANVISA/Ibama, US EPA, DGTR anti-dumping)
- trade policy and tariffs (India–US, China, Brazil)
- weather and crop progress (ENSO/NOAA CPC, IMD, India rabi/kharif sowing, Brazil/Argentina planting via Conab/AgRural, Europe and Australia seasons)
- tech (biologicals, new actives, drones, AI spraying, digital distribution)
- M&A chatter and unconfirmed reports

Aim for a healthy mix of domestic (India) and international stories. Prefer original sources dated in the window. Every item must come from a page you fetched or a search result in this run. Never invent figures, dates or quotes; if a number is uncertain, leave it out. Paraphrase; no quote longer than 15 words.

## Step 3: Write the edition document (collection `editions`, doc_id = today's date)

Follow the template's schema exactly:

- `date`, `generatedAt` (ISO, +05:30), `headline` (≤12 plain words, the day's main point), `dek` (2 plain sentences), `mood` {score -1..1, label, note (2 short plain sentences)}.
- `kpis`: exactly 6 tiles {label, value, unit, delta, dir up|down|flat, bad (true if "up" is bad), note, item (id of the story this number comes from; required)}.
- `items`: {top, financial, regulatory, political, weather, tech, rumors}; each an array of {id, title (plain, specific headline), simple (1–2 sentences, what happened in everyday words; a non-specialist must understand it), stat {value, label} (the single most telling number from the story, shown big on the card, e.g. `{"value":"−19%","label":"Q2 revenue"}`; label ≤6 words; it must appear in the source), summary (3–5 sentences with the figures; shown under "The details"), why (why it matters, in plain words), scope ("domestic" for India-only, "international" for outside India, "both" if it clearly affects both), region, company?, date (event date YYYY-MM-DD), sentiment -1..1, impact 1–5, tags[], threads[] (thread ids), source, url}.
  - top: 4–6 biggest stories (top[0] is the lead). Other sections 2–6 items each (fewer if there is genuinely nothing).
  - rumors items also need status ("Unconfirmed", "Open process", "Market chatter", "Opinion"…) and credibility 1–5, and must be real reported speculation or open processes, clearly labelled.
  - Item ids unique within the edition (t1…, f1…, r1…, p1…, w1…, x1…, m1…).
  - Don't repeat a story from earlier editions unless there is a new development; then say what changed.
- `domestic`: {summary (2–3 plain sentences on India today), points [3 short bullets]}; `international`: {summary, points [3]}.
- `glossary`: 12–25 entries {term, match [lower-case words/phrases that should trigger it], def (one plain sentence)} covering every technical term used in today's stories. Reuse and extend the previous edition's glossary.
- `charts`: 4–10 infographics with real numbers from today's sources, each {id, section (top|financial|regulatory|political|weather|tech|rumors), type, title, note, unit, source, url?, items [ids of the stories the chart is about; required]} plus data by type:
  - "bars": data [{label, value, sub?, tone? pos|neg|acc|leaf|mute|mix}] (signed: true for +/-)
  - "compare": data [{label, a, b}] with legend [a-label, b-label]
  - "progress": data [{label, value 0–100, ref?}] with refLabel
  - "gauge": {value, min, max, ticks[], bands[{from,to,tone,label}]}
  - Put 1–2 charts in "top" and at least one in financial and weather. Keep bar labels short (≤24 characters). Chart titles and notes in plain words.
- `insights`: 3–6 {title, body, confidence high|medium|low, horizon, threads[]}. These must CONNECT today's news with earlier editions and thread timelines (name the earlier development and its date), spot patterns, second-order effects and contradictions, still in plain words.
- `indofil`: {summary (2–3 sentences, net read), exposure [{area, score -5..5, note}] (6–9 areas), impacts [{title, body, direction positive|negative|mixed, magnitude 1–5, horizon "0-3m"|"3-12m"|"12m+", area, action (a concrete next step for the Growth Office), items[ids from today], threads[]}] (5–9 impacts)}.
  - Indofil context: fungicide-led Indian manufacturer with mancozeb as its anchor molecule (global leader in that molecule; mancozeb is not approved in the EU since 2020/21 and Indofil's court challenge failed in 2025); export-focused international business; Growth Office priorities are Brazil (distributor landscape, partnership terms), Europe (portfolio gap analysis, biologicals acquisition targets), Australia/market access, India, molecule prioritisation across India/Brazil/EU/Australia, and buy-side M&A screening; Indofil has no in-house herbicide manufacturing plant.
  - Do not name confidential deal targets or advisors; describe workstreams generically.
- `digest`: {tldr [4–6 one-sentence plain bullets], numbers [{value, label}] (6), watch [{when, event}] (upcoming dated events; mark unconfirmed dates as such)}.

Keep the document under 150 KB. Write it to a local JSON file outside the repository (e.g. `/tmp/cultiv-out/edition.json`) and use `file_path`. Before writing, check with a short script that every `kpis.item`, `charts.items`, `impacts.items` and threads id you reference exists.

## Step 4: Update story threads (collection `threads`, doc_id = thread id)

For each thread touched today, add timeline entries {date, text (one plain sentence), url} for today's developments, update `summary`, `status` (escalating|developing|cooling|resolved), `updated` = today, and keep `indofil` relevance (high|medium|low). Mark expected future events with `"future": true` and remove future entries that have now happened. Create a new thread (kebab-case id) when a story is likely to recur; give it 2–4 back-dated entries from your research so it connects to the past. Keep each timeline to the most relevant 15 entries.

## Step 5: Update the index

Set `meta/index` `dates` = [{date, headline, mood label}] with today's entry first, followed by all earlier entries unchanged; `updated` = today.

Write steps 3–5 in ONE ArtifactData `batch` call (≤50 writes) using `file_path` entries, passing `if_version` (from your reads) for every document that already exists. If the batch reports a version conflict, re-read that document, merge, and retry once.

## Step 6: Publish to the app (this repository)

1. After the batch succeeds, save the FINAL versions outside the repository (e.g. under `/tmp/cultiv-out/`): today's edition JSON (`edition.json`), the index JSON (`index.json`), and ALL threads (ArtifactData list collection `threads` with `out_dir`, then one file per thread named `<thread id>.json` holding only the document fields, without the id/version wrapper).
2. In this repository's clone, make sure you are on `main` (`git checkout main`, `git pull --ff-only origin main`). Commits must go to `main`, not a `claude/` branch, because GitHub Pages serves `main`.
3. Backfill missing editions: list `data/editions/*.json`. For every date in `meta/index` `dates` (other than today) with no `data/editions/<date>.json`, ArtifactData get collection `editions`, doc_id `<date>` with `out_dir`, unwrap it to the document fields, and add it as an extra `--edition` argument below.
4. Run (install `cryptography` with `pip install --break-system-packages cryptography` if missing):

   ```
   CULTIV_PASSCODE='<passcode from the task prompt>' python3 tools/publish.py --site . \
     --edition /tmp/cultiv-out/edition.json [--edition /tmp/cultiv-out/<missing date>.json ...] \
     --threads /tmp/cultiv-out/threads --index /tmp/cultiv-out/index.json
   ```

   The script refuses to write if the passcode does not match the site. Never change the passcode or delete `data/meta.json`.
5. `git add -A`, commit `Edition <date>` (mention any backfilled dates) with the trailer line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, then `git push origin main`. If the push is refused, report the exact error and send a push notification about it; the artifact is already updated.
6. Never commit unencrypted edition, thread or index JSON, or the passcode, to this repository.

## Step 7: Verify and report

Re-read `editions/<today>` once to confirm it saved, and confirm the push succeeded. Finish with a 3-line summary: the headline, the single biggest Indofil impact, and the count of domestic and international stories filed (plus "App updated", any backfilled dates, or the push error).
