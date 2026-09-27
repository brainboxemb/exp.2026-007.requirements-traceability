# Agent guidance

This repository is the implementation/evidence owner for Experiment 007.

Before changing the experiment:

1. read `README.md`;
2. read the numbered documents in `docs/` in order;
3. read the current experiment issue/PR;
4. use `brainboxemb/brainboxemb.meta` as the cross-project coordination source;
5. use the current reference project as source of truth for real engineering
   documentation examples.

Shared workflow and ownership guidance comes from
[`brainboxemb.meta/AGENTS.md`](https://github.com/brainboxemb/brainboxemb.meta/blob/main/AGENTS.md).

## Local experiment rules

- Do not select a documentation/traceability product merely because it is the
  first candidate.
- Start from the target user experience and explicit qualification questions.
- Keep the existing event-timing Markdown source unchanged unless a later
  adoption track explicitly authorizes a production experiment there.
- Prefer small reproducible fixtures over copying the complete event-timing
  documentation.
- Distinguish the engineering knowledge model from the UI/view technology.
- A failed candidate is useful evidence; do not weaken the target to make a
  tool fit.
- Keep generated output and experimental evidence out of authored source unless
  the experiment deliberately tests an authored-source representation.
