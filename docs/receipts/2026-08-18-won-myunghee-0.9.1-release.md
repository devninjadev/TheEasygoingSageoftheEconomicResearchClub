# Won Myunghee 0.9.1 release receipt

Date: 2026-08-18 Asia/Seoul

## Scope and version

- Repository: `https://github.com/devninjadev/TheEasygoingSageoftheEconomicResearchClub`
- Previously published latest release: `v0.9.0`
- Release version: `0.9.1`
- Behavior change commit: `2d32341a185855264187349c46766f22ce9642d8`
- Git skill-tree object: `0a312e7e5ccf1001d09cfde8e1d499746745aaa5`

Version `0.9.1` restores the original GPTs persona's calm, warm, slightly old-fashioned senior-to-junior informal speech as an explicit runtime contract. Myunghee keeps this speech level when the user writes politely and when she explains investments, tax, insurance, retirement, or other professional topics. A semantic pre-output check distinguishes narration, Myunghee's user-directed dialogue, and third-party speech before repairing any drift into generic polite financial-adviser language.

## Package identity

- Archive: `won-myunghee-0.9.1.zip`
- Archive SHA-256: `84c0035773b04053b93a001828f51b00c68739091c28f3482c3c9b750e3c79c1`
- Layout: one top-level `won-myunghee/` directory.
- Build input: tracked `skills/won-myunghee` tree only.
- Reproducibility: archive entry times normalized to 1980-01-01 and ZIP extended attributes omitted.

## Behavior verification

- Baseline symptom: a substantive market-mindset question produced polite endings such as `-해요` and `-답니다` in Myunghee's dialogue.
- Fresh-context probe after the change: the same question produced user-directed endings such as `-거야`, `-해야 해`, `-뿐이야`, and `-하지 마` without polite-adviser drift.
- The user requested an instruction-first correction; because the fresh-context probe passed, no additional regression test was added in this patch release.

## Pre-publication verification

- Source suite: 20 tests, 0 failures.
- Fresh tracked-source extraction suite: 20 tests, 0 failures.
- Official skill validation on source and extraction: `Skill is valid!`.
- ZIP CRC: no compressed-data errors.
- Candidate worktree archive and tracked-source archive SHA-256: identical.
- Tracked source-to-extraction sorted file list and per-file SHA-256: identical.

## Publication and installation gate

Publish only if remote `main` and the new annotated `v0.9.1` tag resolve to the intended release commit and the GitHub Release is non-draft and non-prerelease. After publication, download the public ZIP and checksum into fresh staging, repeat CRC, validation, tests, and source parity checks, then replace `/Users/jundochang/.codex/skills/won-myunghee` from that verified public extraction. The public extraction and personal installation must match file-for-file and hash-for-hash.
