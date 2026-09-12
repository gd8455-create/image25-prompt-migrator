---
name: image25-prompt-migrator
description: Convert an existing prompt from an older image model, another image AI, or an unknown source for GPT Image 2.5 while preserving intent. Requires a source prompt; use for conversion, optional fair baselines, or repair of a failed converted prompt, never prompt creation from scratch.
---

# GPT Image 2.5 Prompt Migrator

## Outcome and boundary

Convert an existing `source_prompt` into a prompt for GPT Image 2.5. The source may come from an older image model, another image AI, or an unknown tool. GPT Image 2.5 is always the target.

This skill requires the source prompt itself. If it is missing, request it and do not synthesize a replacement. Preserve the user's visual intent, explicit constraints, reference-image roles, and required rendered text. Do not use this skill as a general prompt writer, an idea generator, or an image generator.

## Keep roles and surfaces separate

The current Codex agent performs the migration and QA planning. GPT Image 2.5 is the downstream image model that receives the converted prompt. Do not put agent configuration in the image prompt.

Keep visual instructions in the converted prompt. Keep model choice, quality, dimensions, background, output format, and other exposed controls in request settings. A source tool's flags, node settings, weights, model add-ons, or UI controls are not GPT Image 2.5 prompt syntax.

## Select the migration path

- **Default conversion:** use `migration_convert` in [workflow modes](references/workflow-modes.md). Read [source adapters](references/source-adapters.md) for the identified or unknown source, then use [conversion patterns](references/prompting-patterns.md) only as needed.
- **Optional fair comparison:** use `migration_baseline` only when the user requests a comparison or the task needs evidence that conversion helps. The baseline keeps the source prompt unchanged and does not replace the converted deliverable.
- **Repair after a failed conversion:** use `migration_repair` only when a converted prompt has produced a documented failure. Base every repair on the original source prompt, the converted prompt, and the observed failure.
- **Optional realism profile:** read [Physical Realism v2](references/physical-realism-v2.md) only when a realism-oriented conversion profile is requested or clearly useful. Disclose its use and keep an unprofiled migration traceable.
- **Dense, JSON-like, or measured scene prompts:** read [structured scene audit](references/structured-scenes.md) to retain useful detail, check conflicts, and distinguish author claims from evidence.
- **Claims about models, platforms, or source syntax:** consult [evidence boundaries](references/evidence.md).
- **Before delivery:** apply the [output contract and completion conditions](references/output-contract.md).

## Migration invariants

Preserve the complete source prompt and classify its origin as an older image model, another image AI, or unknown. Record a more specific source product only when the user, supplied artifact, or authoritative documentation establishes it.

Translate visual meaning rather than copying tool-specific control syntax. Map proprietary syntax only when its source and meaning are explicit. If no direct GPT Image 2.5 equivalent exists, record that limitation. Never guess what an unfamiliar flag, token, weight, node, preset, or hidden platform control means.

An older GPT Image prompt that is already clear and compatible may pass through unchanged with `changes: []`. Do not expand it merely to demonstrate migration.

Register every required rendered string exactly, including case, punctuation, count, location, style, and relative size. Scope broad exclusions so they do not cancel required names, labels, signatures, or scene text. Do not invent reference images, identities, scene details, or unsupported target settings.

Ask one focused question only when missing source context or ambiguous syntax would materially change the result. Otherwise complete the migration and mark non-equivalent or unresolved source controls explicitly.
