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
- **AI chat panel** — the chat surface. A message you send renders as a
  bubble hugging the right edge of the chat area (the "backwall");
  assistant and system messages render as flat full-width rows
  (`src/components/AI/chatBubbles.ts`). Every message carries a wall-clock
  timestamp for display and a ritual tick for causal order.

## In the terminal

The `lucifer` command set, routed by the terminal
(`src/utils/commandRouter.ts`, `LUCIFERAI_COMMANDS`):

`help` · `plan` · `fix` · `fixnet` · `llm` · `build` · `create` ·
`workflow` · `tokens` · `history` · `agent`

When the plugin is active and idle, the terminal shows the heartbeat —
`🩸 Idle • Awaiting Commands...` (cycling red ↔ purple,
`src/components/Terminal/heartbeatLogic.ts`, `Heartbeat.tsx`) — and the
fangs drip while an AI-chat generation or a LuciferAI plugin task is
running (`src/components/Synth/blood.ts`, `shouldDrip`).

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
