# voice.md

How I write, written down well enough that an agent can fake it.

Agents writing PRs, reviews and issues sound like agents. "Be concise" doesn't
fix that - examples do. So this is a doc of how I actually write, with real
examples next to what a model would write by default.

- [`VOICE.md`](./VOICE.md) - my voice. Code, commits, reviews, issues, status
  updates, docs and chat.
- [`spec.md`](./spec.md) - the shape of a voice doc, if you want to write your
  own.
- [`skills/build-voice/`](./skills/build-voice) - a Claude Code skill that
  builds one for you, from your own GitHub, Linear, docs and chat.

## Using it

Point your agent at `VOICE.md` before it writes anything as you. The
[`voice`](./skills/voice) skill does that, install it with:

```sh
./scripts/install.sh
```

It symlinks the skill into `~/.claude/skills`, so there's only ever one copy.
To use it from another skill, symlink `VOICE.md` in directly:

```sh
ln -s ~/path/to/voice.md/VOICE.md ~/.claude/skills/<skill>/references/voice.md
```

## Making your own

Install the skills with `./scripts/install.sh`, then ask Claude to build your
voice.

It'll ask for your sources, check that what you give it was _actually_ written
by you (a voice built from AI text is just the model again), and write a
`VOICE.md` that follows the spec.

Then test it: give a fresh agent only your `VOICE.md` and a few prompts based
on things you've written that aren't in the doc, and compare. See the end of
`spec.md`.
