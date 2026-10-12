# Voice spec

Agents write like agents. If we want them writing PRs, reviews and issues as
_us_, they need something better to copy than "be concise". A voice doc is
that: how one person actually writes, with enough examples that someone else
could fake it.

Everyone's voice is different, so the content is up to you. This is just the
shape, so we can all point the same tooling at them.

## The doc

One markdown file, first person, written as you.

It should read like you wrote it, because you did. No numbered sections, no
lists of rules, no "always" / "never" checklists - if something sounds like a
rule, it should really be a habit you can point at. And it follows its own
advice: if you write short, the doc is short.

Leave out where it came from - no "derived from 700 comments". Keep it safe to
publish too: Alice, Bob and Charlie instead of real people, and anything
private (repos, components, customers) swapped for something similar sounding,
so the example still reads naturally.

Start with a couple of sentences on what it is and how to read the examples,
then one section per register.

## Registers

A register is anywhere your writing changes. Start with one section for the
stuff that's true everywhere, then one per register where you sound noticeably
different.

Some ideas:

- Everywhere - length, hedging, punctuation, humour, emoji
- Code - comments, naming, API shape
- Commits - commit messages, PR descriptions
- Reviews
- Issues
- Documents
- Chat

Don't do all of these! Skip anything you don't write, and anything where you
don't sound any different. Add your own if there's something missing.

Sub-registers are `###` subsections, for when part of a register has its own
shape - design docs inside Documents, say. Most differences are a paragraph,
not a subsection, so use these sparingly.

Inside a register, a paragraph is one habit. A sentence or two on what you do,
and why if it isn't obvious. Then the example.

## Examples

The examples matter more than the prose - when in doubt, an agent should copy
these. So every habit gets one, straight after the paragraph, not saved up for
a section at the end.

They're always a pair, in a quote block:

```markdown
> ❌ This logic is non-obvious and would benefit from an explanatory comment.
>
> ✅ This needs an explanation of _why_ it's done like this. I had to spend
> quite a chunk of time trying to decipher why we needed this.
```

The ❌ is what a model writes by default - polished, padded, hedging
everything. Make it believable though, the kind of thing you've actually seen
in an AI-written PR. A strawman teaches nothing.

The ✅ is what you'd write. Use real ones wherever you can, pulled straight out
of your own PRs, reviews, issues and chat. Don't tidy them up - the typos and
missing full stops are part of the voice 🙂 If you have to make one up, keep it
close to something real.

Examples teach _how often_, not just _how_. If most of your ✅s have an emoji,
an agent will put one on everything, even if you only use them now and then.
So keep the plain ones in proportion, and when a habit is rare, say so in the
prose.

Small habits are easy to miss and easy to recognise - tag questions ("right?"),
how you open a status update, whether a list is fragments or sentences. If
it's something people would notice was missing, it gets a paragraph and an
example.

Anything multi-line (code, commits, markdown) goes in a fenced block, with the
❌ / ✅ on its own line above it:

````markdown
> ❌
>
> ```go
> // Check if the organization has reached its node limit.
> if len(org.Nodes) >= org.NodeLimit {
> ```
>
> ✅
>
> ```go
> if len(org.Nodes) >= org.NodeLimit {
> ```
````

Short stuff - titles, flags, names - can just go inline in backticks.

## Testing it

Give an agent _only_ your voice doc and a handful of prompts, built from real
things you've written that aren't quoted in the doc - a review comment, a
commit, an issue, the start of a doc. Then compare what it writes against what
you actually wrote. Whatever it gets wrong in the same way more than once is
something the doc is teaching badly.
