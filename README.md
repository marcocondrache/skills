# Skills

These are the agent skills I use in my main engineering work. Some I run every day, others I'm still testing, and any of them can change or disappear once it stops helping. They're plain Markdown, so any agent harness that loads skills can use them.

The repo is personal. It follows how I work and makes no promise of stability to anyone else. Take whatever is useful.

## Skills

| Skill | Use it to |
| --- | --- |
| `how` | Explain how a part of the code works before you change it |
| `why` | Find the reasons behind the code's current shape in git history, PRs, and docs |
| `sweep` | Review a whole codebase instead of a diff and rank what looks off |
| `no-comments` | Send the Comment Sicko subagent after needless comments and delete them |
| `retro` | Look back at a session and change the agent's setup so the next one goes better |
| `steering` | Decide where an instruction for an agent should live and at what scope |
| `technical-writing` | Write or review docs, RFCs, and READMEs |
| `unslop` | Strip AI tells from any writing |
| `design-eng` | Build or review UI motion and interaction details |
| `i-have-adhd` | Shape replies for a reader with ADHD, with the next action first |
| `bro` | Restate the last reply in plain language |

## Inspiration

- [pstack](https://github.com/cursor/plugins) by Lauren Tan is where this repo started. `how`, `why`, `no-comments`, `technical-writing`, `unslop`, `bro`, and the Comment Sicko subagent came from it. `how` and `why` are much shorter now, and the rest are close to the original.
- [mattpocock/skills](https://github.com/mattpocock/skills) is the base for `retro`.
- [emilkowalski/skills](https://github.com/emilkowalski/skills) is the base for `design-eng`.
- [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) is the base for `i-have-adhd`.
- Anthropic's article [Steering Claude Code](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more) is the base for `steering`.
- [Diátaxis](https://diataxis.fr), the [Google developer documentation style guide](https://developers.google.com/style), [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org), and John Kohl's *The Global English Style Guide* are the four layers of `technical-writing`.

`sweep` is my own.

## License

MIT, see [LICENSE](LICENSE). `design-eng` and `i-have-adhd` keep their original MIT licenses in their own directories.
