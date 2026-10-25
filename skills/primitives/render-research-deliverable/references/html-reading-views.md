# Interactive local reading companions and replies

Use when a table, chart, result passage or revision is easier to inspect in a browser. This is an executable presentation mode of `render-research-deliverable`, not a new research pipeline or a substitute for a thesis's LaTeX source and compiled PDF.

## Source and content

Resolve the workspace through the parent skill's contract. Read the pinned table/data, units, provenance and selected prose. Preserve the canonical files; write the HTML and its preparation input as derived exports in the owning artifact's export location. Record source identities and export readback through the existing artifact/index, outside scholarly prose and the learner-facing page.

Use `scripts/render_reading_view.py`, with `assets/reading-view.html` retained at its packaged relative location. It uses only Python's standard library. Prepare UTF-8 JSON with:

- `title`, `summary`: a recognizable title and a short explanation entailed by the actual sources; no template result numbers.
- `sources`: one or more `{label, note, url?}` descriptions. Explain provider, version/period, transformations and scope in ordinary research language. URLs are optional HTTP(S) source links, never automatic resource loads.
- `table`: `{title, columns, rows}`. Each column has unique `key`, human-readable `label`, `type` (`text` or `number`), and an explicit numeric `unit`; optional `decimals` controls display only. Use `null` or an absent cell for missing values, never invented zeros. An empty `rows` list is a valid empty state. Numeric raw strings/JSON numbers retain original precision; sorting uses exact-decimal ranks.
- Optional `chart`: `{title, label_key, value_key}` referencing existing columns. The value column must be numeric. The chart uses the same filtered/sorted observations; missing values are labelled rather than plotted as zero.
- Optional `excerpt`: `{title, text, highlights: [literal strings]}` from the actual source passage. Highlights do not rewrite it.
- Optional `revision`: `{title, before, after}` using two real versions. Omit when they are unavailable; never invent an earlier draft. Identical versions show that no text changed.

Keep code identifiers, paths, checksums and operation logs in the technical record, not in these human-readable labels. The JSON keys are implementation metadata and are not exposed as UI labels.

```sh
python <installed-render-skill>/scripts/render_reading_view.py \
  --input <pinned-reading-input.json> --output <new-reading.html>
```

The renderer refuses to overwrite a file and rejects invalid numeric columns, nonfinite values and unsafe source URLs. Its HTML has no external dependencies, network fetches, remote fonts/images or executable data markup. Data is encoded safely and inserted as text. Do not bypass this encoding by adding `innerHTML`, arbitrary scripts or unverified resource URLs.

## Verify actual use

Open the produced file with the host's supported file/browser surface. Test the actual reply link, table sorting and filtering, provided chart/excerpt/revision tabs and return links. Repeated actions must preserve observations; empty filters and missing values must be distinguishable from zero. Inspect readable numbers and full text on desktop and a narrow viewport when changing the renderer. A real anchor/hash target or event handler owns every navigation action. Do not substitute a cursor animation, timed visibility change, screenshot or source-code check for a browser action.

## Capture for tutorials

When producing a tutorial, prefer actual full-Windows screenshots if a formally supported, authorised desktop-capture tool is available and the required context is safe to capture. Read-only screenshot capability and app control are separate: neither proves the other is available. Keep unknown desktop capability unknown until the official surface confirms it; do not promise that the current host can capture the desktop. If only browser capture is available, use genuine browser screenshots and name that scope. Never substitute shell/OS screenshot calls, another control surface or changed security permissions to bypass a tool restriction. Do not capture unrelated private or sensitive windows; select an authorised surface or stop that capture when it cannot be bounded safely.

Preserve each original capture unedited in the existing operation evidence, with its observed capture time, actual action/step, tool/surface and related artifact version. Do not invent a precise timestamp or missing action when the record lacks one. Keep cropped, zoomed, redacted or annotated derivatives separately and retain their original-image pointer and changed region. Cropping and emphasis may clarify real operations; overlays must remain distinguishable from the captured interface. Never add a link, button, response, changed number or click that did not actually occur, or hide a failure to create a success narrative. A screenshot establishes visible content, not an unrecorded click or skill invocation. Keep the provenance detail outside the learner-facing view.

## Reply contract and link verification

Generate the artifact first. Then use `scripts/build_reading_reply.py` to build the reply from its actual title and summary:

```sh
python <installed-render-skill>/scripts/build_reading_reply.py \
  --artifact <existing-reading.html> --next-step '<concrete next research action>' \
  --output <new-reply.md>
```

It checks an existing reading artifact and emits three user-facing parts: a short explanation, a titled clickable artifact link, and the next step. The local path is only a local-file link. For an already authorised temporary loopback preview, optionally supply `--url http://127.0.0.1:<actual-port>/<actual-file>`; the helper fetches that exact local target and compares its bytes before returning a link. It does not start a server, follow redirects, publish, or connect to another host. `--response-html` can save a readable copy of the same actual reply with a real anchor for browser acceptance; label that test as a saved reply, not native Codex chat interaction.

Use the host's supported clickable Markdown/local-file format or the exact returned attachment link. Do not invent Library/download URLs, convert a Windows path into a public URL, or promise another device can access localhost. Cross-device delivery requires an already authorised supported attachment route; a local export is not evidence it was delivered. Keep internal verification in the technical record.

If generation fails, the artifact is missing, the link returns different bytes, or no supported delivery surface exists, state the actual failure and next recovery action. Do not say “created”, emit a placeholder link, manufacture a button or claim a click. A valid file with an unavailable delivery channel is a partial delivery, not a failed research result. Forward the generated reply only after checking its summary against the sources; the helper verifies identity/access, not research validity. Never present a separately written illustrative exchange as the actual reply.

For acceptance, retain the actual skill reads, renderer/reply commands, source/output identities and real browser action results separately from user-facing content. State exactly which layer passed; this feature does not prove native skill discovery or fix unrelated repository failures.
