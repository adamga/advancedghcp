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
The original PowerPoint, handouts, app and labs remain unchanged. The video's
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
itself, use `build_deck.py --template "C:\path\to\reference.pptx"` first.
Do not use ordinary `render_narrate.ps1` for the Foundry edition: that explicitly
selects the legacy local Zira narration.

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

After committing the workshop source and final media, create distributable
archives with `python .\media\package_workshop.py --repo .`.
Use `--compact-media` for attachment delivery: the full video and core workshop
materials remain in the ZIP; optional audio-only and preview files are separate
downloads. `build_video.py --reuse-video` remasters previously verified visuals
without rerendering them, then the normal verification must run again.
The complete archive includes the media. The lightweight app/labs archive
excludes large media and Git metadata; initialize Git and commit a baseline
before its worktree exercises.
