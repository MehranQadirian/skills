# Skills

A collection of ready-to-use [Claude](https://claude.ai) skills, grouped by category. Drop one in and Claude gets a new ability.

## Categories

| Category | Skills |
|---|---|
| [**Documents**](documents/) | [PDF Atelier](documents/pdf-atelier/): beautiful themed PDFs with RTL support |

## Quick start

1. Open a category and pick a skill.
2. **Claude.ai:** zip the skill folder and upload it in Settings > Capabilities > Skills.
3. **Claude Code:** copy the skill folder into `~/.claude/skills/`.

## Layout

```
skills/
└── <category>/
    ├── README.md
    └── <skill>/
        ├── SKILL.md
        └── README.md
```

Every skill has a `SKILL.md` (instructions for Claude) and a `README.md` (instructions for humans).

## Contributing

Add your skill under the right category, link it in that category's README, and open a pull request.
