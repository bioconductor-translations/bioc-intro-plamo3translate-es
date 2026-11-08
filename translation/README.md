# Updating the Spanish translation

Run these commands from the repository root. The translator reads English Rmd
files from a Git revision and writes Spanish Rmd files under `episodes/`.
It reads the source revision without checking it out or merging it into the
working tree.

## Requirements

New translations use Python 3.12, [uv](https://docs.astral.sh/uv/), and an Apple
silicon Mac. Dependencies are declared in `scripts/translate.py` and locked in
`scripts/translate.py.lock`; `uv run --locked` creates the required Python
environment automatically.

The model is
[`pfnet/plamo-3-translate-8b-MLX-4bit`](https://huggingface.co/pfnet/plamo-3-translate-8b-MLX-4bit),
pinned to revision `9d87684408bdf34500b7d6115c257d83350c1fe5`. Its first download
uses about 6 GB. The distribution includes custom model and tokenizer code,
loaded with `trust_remote_code=True` from that pinned revision. The default
downloader is recommended. To use `--model-dir /path/to/model`, retain the
matching Hugging Face revision metadata and the PLaMo 8B 4-bit configuration.
Supported copies include a Hugging Face cache snapshot directory named by the
revision, or an `hf download --local-dir` directory with its `.cache/`
metadata intact. The target language is Spanish (`es`); the Japanese-only
`form` setting is omitted.

Cached replay and planning work with Python 3.12 alone, on any platform, without
loading MLX or downloading weights. The Spanish translation memory includes
instructor notes in HTML comments.

## Preview an upstream update

If this clone has no `english` remote, add it once:

```sh
git remote add english https://github.com/carpentries-incubator/bioc-intro.git
```

The separate `english` remote avoids using a translation fork that may already
be configured as `upstream`.

Fetch the English revision and inspect the translation plan:

```sh
git fetch english main
uv run --locked scripts/translate.py --source-ref english/main --dry-run
```

The dry run reports what can be reused and what needs translation. The script
performs no model inference or lesson-file writes in this mode. To avoid even
setting up the MLX environment for a plan, use `python3.12` instead of `uv run`.
The optional `--fetch` flag performs the same `git fetch english main` step.

## Translate, review, and build

Apply the update and save new translation memory and source provenance for
review:

```sh
uv run --locked scripts/translate.py --source-ref english/main --update-memory
git diff -- episodes translation
Rscript scripts/build.R
```

Unchanged passages reuse the available translation memory. New or changed prose is sent to
the pinned model. Review new Spanish text for technical terminology, exercise
conditions, and meaning before committing the lesson and memory changes.
The tool does not commit or push changes.

To check whether the available memory reproduces the current files, without
loading the model or changing files:

```sh
python3.12 scripts/translate.py --source-ref english/main --check
```

This check requires every source passage to be cached. If upstream has new
uncached prose, it reports that translation is needed. Use `--cache-only` for a
normal update that must also be completed entirely from memory.

## Protecting local edits and lesson structure

The translator checks output hashes against the supplied baseline and the last
successful run. It stops before replacing an edited Spanish lesson. Review or
save those edits first; `--overwrite` explicitly permits replacing edited
outputs.

Carpentries colon fences, full code blocks, commented-out code, inline code,
link destinations, identifiers, and other protected syntax are kept out of the model's
translation text. All planned lessons are validated before output replacement.
Missing or altered placeholders and unsupported structural changes stop the
update for review.

Four separately recorded build adaptations in `patches.json` are reapplied
only when their exact English source guards and translated text still match:

- A stable heading ID for the `data.frame` section.
- A link to the vector-generation section.
- A figure link and anchor for the painter model.
- The existing `blue_theme()` call corrected to use the saved theme object.

The last adaptation is the only code edit. Its guard matches the complete
original chunk, so it will not overwrite a changed upstream example. Use
`--no-patches` to omit all four adaptations and retain upstream code exactly.
Review skipped adaptations when upstream changes their source excerpts.

## Sources, outputs, and memory

Use a local English episode directory instead of a Git revision when needed:

```sh
uv run --locked scripts/translate.py --source-dir /path/to/english/episodes --output-dir /path/to/spanish/episodes
```

Choose separate directory trees: the input and output directories must differ
and must not be nested inside each other.

`--output-dir` defaults to this repository's `episodes/`. Runtime cache and
output-state records use the ignored `.cache/translation/` directory; change
that location with `--cache-dir`. Runtime cache contents and model weights do not belong
in Git.

The versioned resources in this directory are:

- `config.json`: model revision, source remote, prompt settings, and resource
  paths. Use `--config /path/to/config.json` to select another configuration.
- `seed-cache.json`: reusable Spanish translations, keyed by normalized
  masked source text and unit kind, and restricted to their episode filenames.
- `glossary.json`: shared English-to-Spanish terminology.
- `reviewed-context.json`: disambiguation and glossary overrides selected by
  exact source keys and filenames, rather than paragraph numbers.
- `source-manifest.json`: English revision, model provenance, and file hashes.
- `patches.json`: the guarded local build adaptations described above.

`--update-memory` saves new records and provenance in the versioned resources
for review and commit. The ignored runtime cache supports interrupted runs and
subsequent updates without repeating completed inference.

Memory is scoped to its source and target languages. Changing the target language
never reuses records from another language, even when they are reviewed.

After reviewing a new record, change its `review_status` from `machine` to
`reviewed` to retain it across model or glossary changes. For a per-episode
variant, change the status in that variant. A preservation error stops the
update; inspect the runtime cache and the reported source passage, then add a
reviewed translation or refine its context/glossary before rerunning.

Generated memory records retain the profile of the model, prompt, glossary,
and context settings used to create them. Changing those settings requires
fresh generation for those machine records. Reviewed records in the same source
and target languages remain stable for matching source text in their original
episodes. The same
English text can have separate translations in different episodes, so adding a
translation in one chapter does not replace another chapter's wording.

The translator updates Rmd lessons only. Synchronize upstream images, datasets,
and other supporting files separately. Review `config.yaml` episode ordering
when chapters are added or removed. To remove a previously managed episode that
has disappeared upstream, use `--prune`; edited outputs remain protected. Files
outside the translator's managed lesson set are not pruned.
