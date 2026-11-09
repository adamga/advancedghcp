# Deck and complete narrated explainer

The deck and video are generated from one original content source so the narration,
speaker notes, captions and slide topics stay aligned.

## Outputs

- `deliverables/advanced-github-copilot-workshop.pptx`: editable 42-slide deck.
- `deliverables/advanced-github-copilot-workshop.pdf`: printable slide handout.
- `deliverables/advanced-github-copilot-explainer.mp4`: complete narrated lesson,
  H.264 1280x720, AAC speech, embedded selectable English captions and chapters.
- `deliverables/advanced-github-copilot-explainer.srt` / `.vtt`: external captions.
- `deliverables/explainer-transcript.md`: full accessible narration.
- `deliverables/explainer-audio.m4a`: audio-only edition.
- `deliverables/video-chapters.txt`: timestamped navigation.
- `deliverables/source-ledger.md`: official sources, verification date and limits.
- `deliverables/narration-manifest.json`: voice provenance, verified chunk
  transcripts, measured timings and accepted-generation token usage.
- `deliverables/storyboard.json` / `video-script.md`: beginner-friendly visual
  teaching beats covering all 42 original topic areas.
- `deliverables/animation-manifest.json` / `animation-contact-sheet.jpg`: scene
  specification and overview of the 24 fps motion-graphics edition.
- `deliverables/audio-verification.json`: post-encoding loudness and true peak.
- `deliverables/animated-explainer-preview.mp4`: short laptop-playback sample.

The live workshop is **180 minutes**: 60 minutes of instruction/demos, then
30/35/40/15-minute labs. The self-paced video's playback length is independent
of the live schedule. The long-form notes are narration, **not a script to read
verbatim during the 60-minute live segment**.

The video is an original narrated slide lesson with explained code examples,
not a recording of live Copilot UI interaction. The current edition uses
**Microsoft Foundry `gpt-audio-1.5`, playful Coral voice**. It has a shorter,
beginner-friendly script and 126 teaching beats: animated roles, ownership,
dependency flows, worktrees, code highlighting, priority math and filtering.
The video narration was recorded for the first edition of the labs and has **not**
been re-narrated for Workshop 2. It still explains the concepts correctly; the
written labs in `workshop2/` are the source of truth for exact steps. The
PowerPoint's five practice-application and lab slides (35-39) and their speaker
notes were updated for Workshop 2; titles, sections and sources are unchanged,
so the video's 42 chapters still line up with the deck. The video's
script is separate from the PowerPoint's long-form teaching notes.
Only the workshop narration
is submitted to the specified Foundry endpoint; credentials stay in process
environment variables, never files or source control. Generation incurs normal
Azure inference charges. Captions use phrase-level proportional timing anchored
to measured audio chunks, not word-level forced alignment.

## Rebuild on Windows

Prerequisites: Python 3.11+, Windows Arial/Consolas fonts, and permission to invoke
the Foundry deployment. PowerPoint and the supplied reference deck are needed
only if rebuilding the presentation or its PDF, not the procedural animation.
Node is required separately for the labs. Use an explicitly supplied service
principal; the generator does not fall back to your Azure CLI identity.
The request shape follows the
[official Azure OpenAI audio completions quickstart](https://learn.microsoft.com/azure/foundry/openai/audio-completions-quickstart).

```powershell
python -m pip install -r .\media\requirements.txt
python .\media\animated_content.py --out .\deliverables
$env:AZURE_TENANT_ID = "<tenant ID>"
$env:AZURE_CLIENT_ID = "<application ID>"
$env:AZURE_CLIENT_SECRET = [Net.NetworkCredential]::new(
    "", (Read-Host "Client secret" -AsSecureString)
).Password
try {
    python .\media\generate_foundry_narration.py --endpoint "https://<resource>.services.ai.azure.com/openai/v1" --voice coral --style playful --target-wpm 155 --storyboard .\deliverables\storyboard.json
    if ($LASTEXITCODE -ne 0) { throw "Narration generation failed." }
} finally {
    $env:AZURE_CLIENT_SECRET = $null
    $env:AZURE_CLIENT_ID = $null
    $env:AZURE_TENANT_ID = $null
}
python .\media\build_video.py
python .\media\verify_media.py
python -m unittest discover -s .\media -p "test_*.py"
```

The bundled `imageio-ffmpeg` executable supplies the encoder; no separate global
FFmpeg installation is needed. Animation is rendered directly from the storyboard.
For the legacy static-slide edition, `-RenderOnly` renders the existing presentation
without changing its bytes or generating a local voice. To rebuild the deck
itself (for example after editing `workshop_content.py`), run
`build_deck.py --template "C:\path\to\reference.pptx" --out .\deliverables` and then
`.\media\render_narrate.ps1 -OutputDirectory .\deliverables -SkipNarration`. The second
command shrinks any overflowing text, saves the PPTX, and exports the PDF and slide
PNGs without any narration. Do not run `render_narrate.ps1` without `-SkipNarration` or
`-RenderOnly` for the Foundry edition: that selects the legacy local Zira narration.

Foundry generation uses short, resumable chunks and two bounded simultaneous
requests. Each returned transcript must match the source after punctuation,
whitespace and spoken-number normalization; missing words or negations fail
the check. This is not independent audio transcription. Every clip must contain
non-silent PCM audio and finish normally. Streaming WAV size sentinels are
finalized from actual PCM samples; truncated finite-size WAVs are rejected.
No partial narration or local-voice fallback is accepted as a complete video.
Cadence uses pitch-preserving time stretching, bounded to modest adjustments.
The actual speech rate is recorded and checked rather than inferred from a prompt.
The current quieter master targets about -22 LUFS, high-passes low rumble at
80 Hz, and reserves -6 dBTP before AAC encoding (72 kbps mono in the video,
96 kbps in the optional audio-only edition). Both encoded outputs
must measure no higher than -4 dBTP; extra attenuation is applied if needed.
No music or sound effects compete with the narration. This removes digital
overs but cannot guarantee performance at every laptop's hardware volume setting.
Failed attempts may consume Azure usage; the manifest totals accepted clips,
not an invoice.

Audio and video caches are content-hashed. A complete narration manifest is
required before remixing Foundry audio. Keep `deliverables/narration-chunks/`
and other build intermediates out of Git. Regeneration and media verification
require those intermediate audio/render files or a fresh rebuild.

For a short sample, use `generate_foundry_narration.py --limit-slides 2` with the
same voice/storyboard flags, then `build_video.py --preview-chapters 2`.
Preview files are explicitly labelled and cannot masquerade as a complete lesson.
Animation verification checks actual frame changes inside the teaching illustration
in every chapter, not merely a moving progress bar or a nominal frame rate.

The original deck is not redistributed. Its actual theme is copied into the
output, and the measured near-black/white/cyan/purple-blue formatting is adapted
with original text and diagrams. No legacy presenter affiliation is copied.

## Workshop 2 explainer videos (attendee and trainer)

Two newer, shorter, more playful videos cover the **Workshop 2** sample app, scenario,
approach and getting started. They are separate from the 42-chapter deck video above
and are built by the self-contained pipeline in `media/explainers/`.

| Video | Audience | Length | Chapters | Output |
|---|---|---|---|---|
| Attendee guide | People taking the labs: the app, the scenario, why, the approach, quick start, if you get stuck | about 5:40 | 15 | `deliverables/explainers/workshop2-attendee-guide.mp4` |
| Trainer briefing | The facilitator: all of the above plus pre-class setup, verification, the answer key, pacing and troubleshooting | about 11:24 | 24 | `deliverables/explainers/workshop2-trainer-briefing.mp4` |

Each has a matching `.srt` and `-poster.jpg`. Captions are also embedded as a soft
subtitle track, and every scene is a chapter.

How they are made:

- **Voice:** Microsoft Foundry `gpt-audio-1.5`, playful **Coral** voice at a brisk
  cadence (about 165 words per minute). Narration is generated once per scene by
  `generate_narration.py` and **cached** in `media/explainers/build/narration/`, with
  a manifest of the text each clip must match. Only the narration text is sent to Foundry.
- **Visuals:** 8 generated key-art images (`art/`) under a procedural motion-graphics
  renderer (`scenes_a.py`, `scenes_b.py`, `gfx.py`) written with Pillow only: 15 scene
  types, animated robots, a live board, score counters, terminals, confetti, a progress
  bar and a "CHAPTER n of N" intro card whenever a scene would otherwise open on an
  empty screen. Each on-screen item appears on the exact spoken phrase it illustrates
  (`timing.py` resolves every cue and fails loudly if a phrase is missing).
- **Sound:** synthesized sound effects plus a quiet music bed that ducks under speech
  (`sfx.py`). There is no stock audio.
- **Loudness:** both videos are mastered **quiet on purpose** to avoid laptop-speaker
  distortion: about -23 LUFS integrated with a true peak of -4 dBTP or lower.
- **Content:** scripts are in `storyboards.py`. All numbers (scoring weights, lab
  durations, test counts) come from the `workshop2/` documents; the videos do not
  show live Copilot UI.

```powershell
# Optional: regenerate narration (only needed if a script in storyboards.py changes).
# Use an explicitly supplied service principal; the script never falls back to your CLI login
# and never writes the secret to disk.
$env:AZURE_TENANT_ID = "<tenant ID>"
$env:AZURE_CLIENT_ID = "<application ID>"
$env:AZURE_CLIENT_SECRET = [Net.NetworkCredential]::new("", (Read-Host "Client secret" -AsSecureString)).Password
try {
    python .\media\explainers\generate_narration.py --endpoint "https://<resource>.services.ai.azure.com/openai/v1"
} finally {
    $env:AZURE_CLIENT_SECRET = $null; $env:AZURE_CLIENT_ID = $null; $env:AZURE_TENANT_ID = $null
}

# Render, mix, encode, master and mux (about 4 minutes for the attendee video, 9 for the trainer):
python .\media\explainers\make_videos.py all attendee --workers 7
python .\media\explainers\make_videos.py all trainer --workers 7

# Copy the finished MP4, SRT and poster into deliverables/explainers/:
python .\media\explainers\make_videos.py publish attendee
python .\media\explainers\make_videos.py publish trainer

# Check the published files and run the offline tests:
python .\media\explainers\verify_explainers.py
python -m unittest discover -s .\media\explainers -p "test_*.py"
```

Rendering needs only Python 3.11+, Pillow and the bundled `imageio-ffmpeg`
(see `requirements.txt`). Intermediate files live in the git-ignored
`media/explainers/build/`, **including the cached narration audio**. A fresh clone therefore
has the finished videos in `deliverables/explainers/` but must run the narration step
above (Foundry access required) before it can re-render. Any change to a scene, storyboard
or graphics source invalidates the cached video segments but never the cached narration.
Useful flags: `--only a04,a05` renders selected scenes, `--force` ignores caches, and
`--max-mib` changes the size budget (the defaults are 40 MiB for the attendee video and
60 MiB for the trainer video). `make_videos.py segments <video> --only ...` is a fast
way to preview a few scenes, and `all <video> --only ...` writes a short slice to
`build/<video>/slice/` that cannot be published as a complete video.
`verify_explainers.py` checks codec, size, chapters, caption coverage, decodes, frozen
stretches, loudness (-25 to -21 LUFS) and true peak (-4 dBTP or lower).
The Foundry-hosted narration incurs normal Azure inference charges; rendering does not.

After committing the workshop source and final media, create distributable
archives with `python .\media\package_workshop.py --repo .`.
Use `--compact-media` for attachment delivery: the full video and core workshop
materials remain in the ZIP; optional audio-only and preview files are separate
downloads. `build_video.py --reuse-video` remasters previously verified visuals
without rerendering them, then the normal verification must run again.
The complete archive includes the media. The lightweight app/labs archive
excludes large media and Git metadata; initialize Git and commit a baseline
before its worktree exercises.
