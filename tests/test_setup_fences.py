"""Setup-page prose translates while Pandoc division syntax stays literal."""
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import translation_core as core


BARE_DIV_SETUP = '''---
title: Setup
---

### You are running Windows

<br>

:::::::::::::::  solution

## If you already have R and RStudio installed

- Open RStudio and check for updates.

:::::::::::::::::::::::::
'''

ATTRIBUTE_DIV_SETUP = '''---
title: Setup
---

::: {.solution #windows-setup data-label="Do not translate"}

## If you already have R and RStudio installed

Open `RStudio` and read [the guide](https://example.org/setup).

  ::::: {.callout-note #package-note collapse="true" title="Keep English"}

Install the packages below.

```r
# Keep this code comment in English.
install.packages(c("BiocManager", "remotes"))
```

  :::::

:::
'''


def spanish_setup(source):
    document = core.extract_document(source, "learners/setup.md")
    replacements = {
        "Setup": "Preparación",
        "You are running Windows": "Si utiliza Windows",
        "If you already have R and RStudio installed": "Si ya tiene R y RStudio instalados",
        "Open RStudio and check for updates.": "Abra RStudio y compruebe si hay actualizaciones.",
        "Open ": "Abra ",
        " and read ": " y lea ",
        "the guide": "la guía",
        "Install the packages below.": "Instale los paquetes siguientes.",
    }
    translations = {}
    for unit in document.units:
        text = unit.masked
        for english, spanish in replacements.items():
            text = text.replace(english, spanish)
        translations[core.unit_key(unit)] = text
    return document, core.render_document(document, translations)


def colon_lines(source):
    return [line for line in source.splitlines(keepends=True)
            if re.match(r"^[ \t]*:{3,}", line)]


class SetupFencedDivisionTests(unittest.TestCase):
    def test_bare_solution_fences_are_excluded_from_translation(self):
        document, translated = spanish_setup(BARE_DIV_SETUP)
        self.assertEqual(colon_lines(translated), colon_lines(BARE_DIV_SETUP))
        self.assertIn("### Si utiliza Windows", translated)
        self.assertIn("## Si ya tiene R y RStudio instalados", translated)
        self.assertIn("- Abra RStudio y compruebe si hay actualizaciones.", translated)
        self.assertFalse(any("solution" in unit.source or ":" * 3 in unit.masked
                             for unit in document.units))
        self.assertIn("<br>\n", translated)

    def test_nested_division_attributes_and_code_are_literal(self):
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=repr(newline)):
                source = ATTRIBUTE_DIV_SETUP.replace("\n", newline)
                document, translated = spanish_setup(source)
                self.assertEqual(colon_lines(translated), colon_lines(source))
                self.assertIn("Instale los paquetes siguientes.", translated)
                self.assertIn("Abra `RStudio` y lea [la guía](https://example.org/setup).", translated)
                code = ('```r\n# Keep this code comment in English.\n'
                        'install.packages(c("BiocManager", "remotes"))\n```\n')
                self.assertIn(code.replace("\n", newline), translated)
                for literal in (".solution", "windows-setup", "Do not translate",
                                ".callout-note", "package-note", "Keep English",
                                "Keep this code comment"):
                    self.assertFalse(any(literal in unit.source or literal in unit.masked
                                         for unit in document.units), literal)
                core.validate_document(source, translated, "learners/setup.md")

    def test_validator_rejects_changes_to_division_markers_and_attributes(self):
        _, translated = spanish_setup(ATTRIBUTE_DIV_SETUP)
        mutations = {
            "class": (".solution", ".solucion"),
            "identifier": ("#windows-setup", "#configuracion-windows"),
            "attribute value": ('title="Keep English"', 'title="Traducido"'),
            "opening delimiter": ("::: {.solution", ":::: {.solution"),
            "closing delimiter": ("\n:::\n", "\n::::\n"),
            "indentation": ("  :::::\n", " :::::\n"),
        }
        for label, (before, after) in mutations.items():
            with self.subTest(label=label):
                self.assertIn(before, translated)
                with self.assertRaises(ValueError):
                    core.validate_document(ATTRIBUTE_DIV_SETUP,
                                           translated.replace(before, after, 1),
                                           "learners/setup.md")


if __name__ == "__main__":
    unittest.main()
