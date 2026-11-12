# LuciferAI on Lucid — the living embodiment

LuciferAI now lives and runs as a plugin inside **Lucid Terminal**
([GareBear99/lucid-terminal](https://github.com/GareBear99/lucid-terminal)).
That is where LuciferAI works today. This repo is the original standalone
Python system it grew out of — preserved here as the origin — and the Lucid
plugin is the embodiment it advanced into.

Lucid's own README puts it plainly: *"Lucid integrates
[LuciferAI](https://github.com/GareBear99/LuciferAI_Local) as its native
execution engine"* and *"LuciferAI isn't an add-on; it's the core execution
layer."*

## What LuciferAI is on Lucid

The 3rd anchored plugin, id `lucifer`, the first and only entry in the
plugin-shell registry (`src/types/synth.ts`, `PLUGIN_SHELLS`), and the
default plugin (`DEFAULT_PLUGIN_ID = 'lucifer'`). It is embodied as
**Lucifer the Sentinel** — classification `Sentinel`, role
`synth-embodiment` (`LUCIFER_EMBODIMENT`, same file) — mounted into the
shell at `public/synth/matrix-synth-v67.html`.

It has **two surfaces, one plugin** (`src/data/toolbarPlugins.ts`:
*"two buttons for the same plugin, not two plugins"*):

- **Synth view** — the plugin shell, where the Sentinel lives.
- **Blood drop terminal** — the creation place. Both blood drops (the
  toolbar one and the prompt-bar one) open the same creation place
  (`src/data/toolbarPlugins.ts`, Gary 2026-11-07).

The **AI chat panel is not a LuciferAI surface any more** (Gary,
2026-11-07): it is **Lucid AI, its own plugin**, unmounted from
LuciferAI and mounted as a top-level panel. Its model is the ping server
(Llama 3.2 1B via Cloudflare), an API key, or a local model — never
LuciferAI — so it works with the plugin on or off, on every view, and no
gate on the panel may read the plugin. The backwall-bubble rendering
(a message you send hugging the right edge, assistant and system
messages as flat full-width rows, `src/components/AI/chatBubbles.ts`)
now belongs to Lucid AI's chat, not to LuciferAI.

## On, off, and silenced — three states

- **On:** the plugin is active; the terminal shows the heartbeat
  (`🩸 Idle • Awaiting Commands...`, cycling red ↔ purple) while idle,
  and the fangs drip while an AI-chat generation or a LuciferAI plugin
  task is running.
- **Off:** the terminal is a plain terminal, zero residue — no blood
  drop, no heartbeat, no Sentinel face, and LuciferAI words go to the
  shell (`src/components/Terminal/Terminal.tsx`, "off = plain terminal,
  zero residue").
- **Silenced:** the blood drop greys and holds causal order while the
  runtime and ticks keep running; the heartbeat is gone (it renders
  only when the plugin is available, on the active tab, and not
  silenced), and `lucifer` commands are not accepted while silenced.

The FixNet line in the status bar still renders with LuciferAI off:
LucidCore is initialised at startup (`src/App.tsx`), so FixNet stats
and the online indicator are there either way.

## In the terminal

The `lucifer` command set, routed by the terminal
(`src/utils/commandRouter.ts`, `LUCIFERAI_COMMANDS`):

`help` · `plan` · `fix` · `fixnet` · `llm` · `build` · `create` ·
`workflow` · `tokens` · `history` · `agent`

## The model

The plugin ships no model of its own. Lucid's AI layer provides the
model — a local model or an API key — and the plugin is the surface that
talks to it. The plugin loads and reports its own status even with no
model configured.

## Running it

```bash
git clone https://github.com/GareBear99/lucid-terminal.git
cd lucid-terminal
npm install
npm run dev      # development build
npm run build    # distributable build
```

## What this repo is now

- **The original standalone system** (`lucifer.py`, `core/`, the FixNet
  code, `docs/`) — the Python terminal assistant LuciferAI started as.
  It is preserved here, not deleted, and its old claims are corrected in
  the [README](../README.md) rather than presented as live (the "72%
  offline" figure was an unmeasured docs assertion; the "100% local"
  wording overstated a system that syncs FixNet state and runs a WiFi
  check on startup).
- **The living embodiment is Lucid** — the plugin described above. New
  work on LuciferAI happens there.
