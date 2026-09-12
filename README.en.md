# GPT Image 2.5 Prompt Migrator

[繁體中文](README.md)

[![Validate public skill](https://github.com/gd8455-create/image25-prompt-migrator/actions/workflows/ci.yml/badge.svg)](https://github.com/gd8455-create/image25-prompt-migrator/actions/workflows/ci.yml)

**Old prompts → GPT Image 2.5: a Skill for migration, audit, and prompt repair.**

GPT Image 2.5 Prompt Migrator works with image prompts you **already have** from older models or other AI tools. It audits conflicting instructions and incompatible syntax, migrates the prompt while preserving intent, and repairs the converted prompt when actual generation results reveal a failure. The source, reasons for changes, and acceptance criteria remain traceable.

| Capability | What it does |
| --- | --- |
| **Migration** | Convert an existing prompt from an older image model, another image tool, or another AI assistant into prompt text and settings for GPT Image 2.5. |
| **Audit** | Check positive/negative conflicts, source-tool syntax, false numerical precision, reference roles, and required rendered text; record what is preserved, changed, or unresolved. |
| **Prompt repair** | Use the source prompt, prior conversion, and observed failure evidence to correct omissions, ambiguity, or drift in the converted prompt. A new generation and review are required to establish success. |

All three capabilities work from the same existing prompt. Repair applies to **prompt text**. The core Skill delivers text and QA; it does not call an image-generation API or directly repair image pixels.

It accepts prompts written for earlier GPT Image models, prompts from other image tools, and existing image prompts produced by other AI assistants. It does not start from a blank brief or write a new prompt from scratch. It also does not assume that every prompt needs rewriting: when the source is already suitable for GPT Image 2.5, it passes the prompt through unchanged and returns `changes: []`.

> v1.0.0 · MIT licensed · An independently maintained, publicly installable image-workflow Skill. It is not an official OpenAI product.

## Why this exists

Creators often have a library of working prompts when a model or tool changes. Those prompts may mix older-model habits, tool-specific syntax, negative-prompt blocks, weight notation, or text from another AI assistant that has not been adapted for GPT Image 2.5. Rewriting each prompt by hand can lose the original intent and makes it hard to see what actually changed.

This Skill provides an inspectable migration path. It retains the source prompt, identifies source syntax, separates visual instructions from request settings, and delivers a migrated prompt, change record, preserved requirements, and human-reviewable QA. The user can adopt, reject, or continue testing the conversion with a visible audit trail.

## Accepted sources

| Source | Treatment |
| --- | --- |
| An existing generation or editing prompt for an earlier GPT Image model | Preserve intent, clean up obsolete or mixed conventions, and prepare a GPT Image 2.5 migration candidate. |
| An existing prompt for another image-generation or editing tool | Translate identifiable visual intent into GPT Image 2.5 instructions without pretending that tool-specific controls have one-to-one equivalents. |
| An existing image prompt produced by another AI assistant | Check whether it still uses older-model or cross-tool conventions, then convert only what is needed. |
| A prompt already suitable for GPT Image 2.5 | Pass it through unchanged with `changes: []`; do not rewrite it merely to demonstrate activity. |

These are common source categories, not a claim of complete compatibility with every third-party tool, version, or syntax. Source tokens that cannot be interpreted reliably remain under `Unresolved` for the user to decide. See [source-adapter guidance](skills/image25-prompt-migrator/references/source-adapters.md) for the boundaries around flags, weights, negative prompts, and source settings.

## Scope

The input must include an existing image-generation or image-editing prompt. The Skill can:

- Retain the source prompt and non-drifting requirements for subjects, identity, products, composition, rendered text, and reference-image roles.
- Remove or restate syntax that only has meaning in the source tool, while recording each material change.
- Separate visual instructions from request settings such as `model`, `quality`, pixel size, background, and output format.
- Define a migration baseline, repetition plan, and human-reviewable QA for the before-and-after comparison.
- Replace vague quality-token stacks in photorealistic source prompts with concrete relationships among material, gravity, contact, moisture, light, and what the camera sees.

It does not ideate from a blank brief or write a wholly new image prompt, and it does not guarantee that the migrated image will be better. Use a general prompt-writing or creative-production workflow when no source prompt exists.

## Migration workflow

1. Preserve the source prompt, known source tool or model, and known request settings.
2. Decide whether conversion is needed. If the prompt is already suitable, pass it through with `changes: []`.
3. When conversion is needed, change only what is relevant to GPT Image 2.5 migration while preserving creative intent and required constraints.
4. Record source syntax with no reliable target mapping as removed, provenance-only, or `Unresolved`; do not invent an equivalent parameter.
5. Deliver the migrated prompt, change record, request settings, and post-generation QA.
6. If generation with the converted prompt has produced an observed failure, compare it with the original requirements, repair the relevant prompt text, and plan another review.

Model comparisons should begin with a saved baseline. The first pass can change only the selected model while keeping the prompt, references, dimensions, format, and quality setting fixed. Controlled prompt changes come after that baseline. This follows the official GPT Image 2.5 migration guidance to use representative inputs, fixed comparison conditions, and complete result checks.

## Structured source prompts

Long prompts and JSON-like scene descriptions are supported as existing source material. The [structured scene audit](skills/image25-prompt-migrator/references/structured-scenes.md) checks anchors, positive/negative conflicts, reference roles and unverifiable measurements without treating JSON or greater length as proof of quality or model compatibility.

## Installation

Invoke `$skill-installer` in Codex and pass the Skill folder URL:

```text
$skill-installer https://github.com/gd8455-create/image25-prompt-migrator/tree/main/skills/image25-prompt-migrator
```

The URL targets `skills/image25-prompt-migrator/` directly. If you have cloned the repository, you can also use the included installer:

```powershell
python -X utf8 scripts/install.py
```

Pass `--destination <skills-directory>` to test an installation in a temporary or custom skills directory. The installer stops if that destination already contains a Skill with the same name; replacement occurs only when you explicitly add `--force`.

## Example requests

Legacy-prompt conversion:

```text
Use $image25-prompt-migrator to migrate the following older image-generation prompt to GPT Image 2.5. Preserve the subject, composition, and rendered-text requirements. List every change; if no change is needed, return the source unchanged with changes: [].
```

Cross-AI conversion:

```text
Use $image25-prompt-migrator to convert this existing image prompt produced by another AI assistant for GPT Image 2.5. Separate source-tool parameters and do not assume that every parameter has a one-to-one mapping.
```

Migration baseline:

```text
Use $image25-prompt-migrator to prepare a GPT Image 2.5 migration baseline for this existing prompt. Do not rewrite the prompt in the first pass. List fixed settings, repetitions, and evaluation criteria.
```

Audit an existing prompt:

```text
Use $image25-prompt-migrator to audit this older prompt for GPT Image 2.5 migration. Identify conflicts, source-specific syntax, and requirements to preserve. Do not rewrite compatible content merely to show activity.
```

Repair a failed conversion:

```text
Use $image25-prompt-migrator with the source prompt, prior conversion, and generated image or actual failure description I provide. Repair only the parts connected to the failure, explain the changes, and mark untested results as pending validation.
```

See [migration and repair modes](skills/image25-prompt-migrator/references/workflow-modes.md) for input requirements.

## Examples

[`examples/`](examples/) contains three text deliverables and one real, single-run image evaluation:

- [Legacy-prompt conversion](examples/01-legacy-conversion.md)
- [Migration baseline and unchanged pass-through](examples/02-migration-baseline.md)
- [Cross-AI prompt conversion](examples/03-cross-ai-conversion.md)
- [Single-run visual check of the conversion workflow](examples/04-built-in-generation-evaluation.md)

The fourth report did run each prompt once through Codex's built-in image-generation tool. The tool did not expose its exact backend model, seed, or sampling settings. The report therefore evaluates the visible result of this particular “source prompt → migrated prompt → follow-up correction” workflow. It is not a controlled GPT Image 2.5 API benchmark and does not show that a migrated prompt is generally superior to its source.

## Repository structure

```text
image25-prompt-migrator/
├─ skills/image25-prompt-migrator/
│  ├─ SKILL.md
│  ├─ LICENSE
│  ├─ agents/openai.yaml
│  └─ references/
├─ examples/
│  └─ assets/
├─ scripts/
│  ├─ install.py
│  └─ validate_repo.py
├─ tests/
├─ .github/workflows/
├─ README.md
├─ README.en.md
├─ CHANGELOG.md
├─ LICENSE
└─ SECURITY.md
```

The public installation entry point is `skills/image25-prompt-migrator/`. `examples/` contains migration-behavior and visual-review examples. `scripts/` contains a single-Skill installer and repository validator. `tests/` and GitHub Actions check the public package, Skill structure, and accidental inclusion of private material.

## Validation

Run from the repository root:

```powershell
python -X utf8 scripts/validate_repo.py
python -X utf8 -m unittest discover -s tests -v
```

You can also run Codex's built-in Skill structure validator:

```powershell
python -X utf8 "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "skills\image25-prompt-migrator"
```

Structural validation does not mean that GPT Image 2.5 generated an image and passed visual review. Migration quality, rendered-text accuracy, identity preservation, latency, and cost still require repeated tests with matched inputs.

## Limitations

- The core Skill produces prompt text, request settings, change records, and QA. It does not call an image-generation API by itself.
- Third-party prompt syntax varies by version. An unverified source token is not presented as an equivalent GPT Image 2.5 setting.
- A prompt cannot guarantee pixel-identical preservation. Use a mask, compositing, or another deterministic post-production method when unchanged pixels are required.
- API models and controls may differ from the ChatGPT interface. This project does not present one interface's settings as guarantees for another.
- A single output is evidence only for that run. Adoption should be based on representative inputs, repeated tests, and the user's acceptance criteria.

## Sources

Model names, parameter boundaries, and migration-test principles are grounded primarily in official OpenAI documentation:

- [GPT Image 2.5 prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)
- [Image generation API guide](https://developers.openai.com/api/docs/guides/image-generation)
- [GPT Image 2.5 Flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)
- [GPT Image 2.5 Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)

## License

[MIT License](LICENSE). Use, modification, redistribution, and commercial use are permitted with the copyright and permission notices retained. The Skill folder includes the same license so standalone installations retain these notices.
