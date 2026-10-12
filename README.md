# voice.md

How I write, written down well enough that an agent can fake it.

Agents writing PRs, reviews and issues sound like agents. "Be concise" doesn't
fix that - examples do. So this is a doc of how I actually write, with real
examples next to what a model would write by default.

- [`VOICE.md`](./VOICE.md) - my voice. Code, commits, reviews, issues, status
  updates, docs and chat.
- [`spec.md`](./spec.md) - the shape of a voice doc, if you want to write your
  own.
- [`build-voice/`](./build-voice) - a Claude Code skill that builds one for you,
  from your own GitHub, Linear, docs and chat.

## Using it

Point your agent at `VOICE.md` before it writes anything as you. I symlink it
into my skills, so there's only ever one copy:

```sh
ln -s ~/path/to/voice.md/VOICE.md ~/.claude/skills/<skill>/references/voice.md
```

## Making your own

Symlink the skill in, then ask Claude to build your voice:

```sh
ln -s ~/path/to/voice.md/build-voice ~/.claude/skills/build-voice
```

It'll ask for your sources, check that what you give it was _actually_ written
by you (a voice built from AI text is just the model again), and write a
`VOICE.md` that follows the spec.

Then test it: give a fresh agent only your `VOICE.md` and a few prompts based
on things you've written that aren't in the doc, and compare. See the end of
`spec.md`.
