# Won Myunghee 0.9.2 release receipt

Date: 2026-08-19 Asia/Seoul

## Scope and version

- Repository: `https://github.com/devninjadev/TheEasygoingSageoftheEconomicResearchClub`
- Previously published latest release: `v0.9.1`
- Release version: `0.9.2`
- Behavior change commit: `5a162c49267f47f000aff30fcb646affd9778e7c`
- Git skill-tree object: `27a032887320aec956eff560a4e0c7bf05ce7cd9`

Version `0.9.2` restores a compact, topic-indexed supplied-canon bank for Warren Buffett and Ray Dalio and routes materially relevant investment or life-planning questions through it even when the user did not explicitly ask for a famous investor. At most one perspective is woven into the decision as `current issue -> investor perspective -> Myunghee's interpretation -> current evidence`; authority never replaces evidence.

## Package identity

- Archive: `won-myunghee-0.9.2.zip`
- Archive SHA-256: `5e1721cbfa005d5e0efbf3ec7e4412746b6a539649531b4253fbfffbf0cde0fa`
- Layout: one top-level `won-myunghee/` directory.
- Build input: tracked `skills/won-myunghee` tree only.
- Reproducibility: file order is sorted, entry times are normalized to 1980-01-01, and ZIP extended attributes are omitted.

## Behavior verification

- A fresh-context long-horizon valuation probe naturally used one Buffett perspective and connected it to Myunghee's own interpretation and current evidence.
- Buffett and Dalio remain Myunghee's representative voices; Hayoung's Soros and Druckenmiller canon remains disjoint.
- Precise wording, timing, publication, or decision-critical use still requires primary-source verification.

## Pre-publication verification

- Source suite: 22 tests, 0 failures.
- Official skill validation on source: `Skill is valid!`.
- ZIP CRC: no compressed-data errors.
- The release candidate was generated from the recorded tracked skill tree and will be revalidated after public download.

## Publication and installation gate

Publish only if remote `main` and the annotated `v0.9.2` tag resolve to the intended release commit and the GitHub Release is non-draft and non-prerelease. After publication, download the public ZIP and checksum into fresh staging, repeat checksum, CRC, validation, tests, and source parity checks, then replace `/Users/jundochang/.codex/skills/won-myunghee` from that verified public extraction.
