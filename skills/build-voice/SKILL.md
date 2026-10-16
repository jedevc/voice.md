---
name: build-voice
description: Build a VOICE.md for the user - a description of how they write, with paired examples - from a corpus of their own hand-written text (GitHub, Linear, Google Docs, Notion, chat). Use when the user wants to capture their writing voice, or asks to create/update a voice doc.
---

# Build a voice doc

The output is a `VOICE.md` that follows `spec.md`. Read the spec first - it's
at the root of the repo this skill lives in (`../../spec.md`). The skill is
usually symlinked in, so resolve the real path first (`readlink -f`). If it
isn't there, ask the user where it is. Don't base the result on anyone else's
voice doc, even if one is lying around: the only examples that belong in it are
the user's own.

## 1. Collect the corpus

Ask the user which sources to use, and for the details each one needs. Don't
go looking on your own beyond what they point you at.

- **GitHub** - their handle, the orgs to search, and a start date (six to
  twelve months is plenty). Check `gh auth status` works, then run
  `scripts/harvest-github.py OUT_DIR USER ORG[,ORG...] YYYY-MM-DD`. It pulls PR
  review comments, reviews, PR comments, authored PR bodies and commit
  messages. Search is rate limited, so it's slow - run it in the background.
- **Linear** - issues they created, comments, and project updates (via the
  Linear MCP, filtered to "me"), plus any specific issues or docs they link.
- **Google Docs / Notion** - links to docs they wrote. Ask which sections are
  theirs if the doc has several authors.
- **Chat** (Discord, Slack, etc) - ask them to paste a handful of their own
  messages. Ask whether any were typed on mobile, since autocorrect adds
  capitals and full stops that aren't part of their voice.
- **Anything else** - blog posts, talks, READMEs, design docs. Ask.

Aim for each register in the spec to have real material. If one has nothing,
ask for more or leave the register out - don't invent a voice for it.

Save everything as plain text in the session scratchpad, grouped by source.
None of it goes in the final doc except as quoted examples.

## 2. Check it was actually written by them

Lots of text with someone's name on it was written by an agent. A voice built
from that is just the model's voice again, which defeats the point.

Before using any source, ask the user directly whether they wrote it by hand,
and whether any of it was AI-assisted. Then check for yourself, and flag
anything that looks generated:

- Template structure: `## Summary` / `## Changes` / `## Test plan`, Problem /
  Proposed solution / Acceptance criteria.
- Em dashes, "comprehensive", "robust", "ensure", "leverage", bolded
  lead-ins on every bullet, perfectly parallel lists.
- A sudden jump in length or polish compared to the same person's other text.
- `Co-Authored-By` trailers on commits, or "generated with" footers.
- Code comments. These are very often AI-written even when the person's
  reviews aren't - lean on review comments for how they feel about code.
- Text by someone else that got swept up: co-authored docs, quoted replies,
  sections another person owns.

Show the user the suspect passages and let them say which are theirs. Anything
they don't confirm gets dropped. When a source is mixed, keep only the parts
they vouch for.

## 3. Hold some back

Before reading for habits, set aside 15-20 vetted pieces as an eval set, spread
across the registers you have: review comments, commits, PR descriptions,
issues, the opening of a doc or update, replies on their own PRs, chat, a bit
of code if you have any. Pick ordinary ones, not the most quotable.

For each, write two things, in separate files in the scratchpad:

- `eval/prompts.md` - the situation, with enough context to answer: the diff
  hunk, what the change does and why, who said what. The facts, never the
  wording.
- `eval/refs.md` - what they actually wrote.

These never get quoted in `VOICE.md`. If one turns out to be the perfect
example for a habit, use it, and swap a fresh piece into the eval set.

## 4. Find the habits

Read the corpus register by register and look for what _recurs_: length,
openings, how they hedge, how they disagree, how they praise, punctuation and
capitalisation, emphasis style, emoji and what each one means, recurring
phrases, what they leave out. A single occurrence isn't a habit.

Ask the user about anything you're unsure of, rather than guessing - e.g. "you
use 😭 a lot, is that only for frustration?". They'll know things the corpus
doesn't show.

Don't clean up their text. Typos, missing full stops and lowercase are part of
the voice, and "tightening" an example ruins it.

## 5. Write VOICE.md

Follow the spec for structure and the example format. For every habit:

- ✅ is a real quote from the corpus wherever possible, lightly trimmed but not
  reworded.
- ❌ is the same message written the way a model would by default. Make it
  believable, not a strawman.

Write the prose in the first person, as the user, and in _their_ voice - the
doc should pass its own test.

Then make it safe to publish:

- Real people become Alice, Bob, Charlie, etc.
- Private repos, components, customers and internal details become something
  similar sounding. Check repo visibility with `gh repo view OWNER/REPO --json
  visibility` - public ones can stay.
- No corpus stats or "derived from N comments".

Tell the user every translation you made, as a table, and anything you left in
that they might want to change.

## 6. Evaluate and refine

Test the doc the way it'll be used: a fresh agent, with nothing but the doc.

Spawn a new general-purpose subagent - not a fork, it mustn't inherit your
context. Tell it to read exactly two files, `VOICE.md` and `eval/prompts.md`,
and nothing else: no other files, no directory listings, no git, gh or web,
because `eval/refs.md` holds the answers. It writes what the person would post
for each prompt to `eval/outputs-N.md`, and nothing more.

Then compare each output against the reference. Don't score how good it is -
score how _similar_ it is:

- Length and shape: one line or several, prose or bullets, heading or none.
- How it opens, and how it ends.
- Hedging, questions, tag questions, how disagreement is softened.
- Emoji, punctuation, capitals, emphasis, dashes.
- Whether it added things the person wouldn't have said, or dropped what they
  would - an alternative named, a joke, an admission.

Look for patterns, not one-offs. Something wrong in the same direction across
several outputs is the doc teaching it badly. Count what you can count: how
many outputs have an emoji versus how many references do, and how many of the
doc's ✅ examples do.

Fix the cause in `VOICE.md`, not the symptom:

- A habit the outputs miss gets a paragraph and a real example.
- A habit they overdo usually comes from the examples, not the prose -
  examples teach _how often_. Say how rare it is, and rebalance the ✅s with
  equally real ones that don't have it.
- A rule they over-apply needs its limits spelled out, with an example of the
  other side.

Then run it again with another fresh agent, same prompts, a new outputs file.
Keep a short scoreboard per round (e.g. "emoji: 9/19 → 6/19, real: 1/19") so
it's obvious whether a change helped. Stop when a round stops improving, or
after three or four. Past that you're overfitting to the eval set - if you
want to keep going, add fresh held-out pieces.

If a lesson isn't about this person but about voice docs in general (like
"examples teach frequency"), propose it as a change to `spec.md` too, and
show the user the diff.

Show the user the scoreboard and the side-by-sides worth seeing. Not all of
them, just the ones that tell them something.

## 7. Iterate with the user

Show the user the draft and expect corrections - they will know when something
doesn't sound like them, and that beats any eval. Before every edit, re-read
the file: they will be editing it by hand too, and those edits shouldn't get
reverted. After a big round of changes, run the eval again.
