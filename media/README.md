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

The live workshop is **180 minutes**: 60 minutes of instruction/demos, then
30/35/40/15-minute labs. The self-paced video's playback length is independent
of the live schedule. The long-form notes are narration, **not a script to read
verbatim during the 60-minute live segment**.

The video is an original narrated slide lesson with explained code examples,
not a recording of live Copilot UI interaction. The current edition uses
**Microsoft Foundry `gpt-audio-1.5`, Alloy voice**. Only the workshop narration
is submitted to the specified Foundry endpoint; credentials stay in process
environment variables, never files or source control. Generation incurs normal
Azure inference charges. Captions use phrase-level proportional timing anchored
to measured audio chunks, not word-level forced alignment.

## Rebuild on Windows

Prerequisites: Python 3.11+, installed PowerPoint, the supplied reference deck
if rebuilding the presentation, and permission to invoke the Foundry deployment.
Node is required separately for the labs. Use an explicitly supplied service
principal; the generator does not fall back to your Azure CLI identity.
The request shape follows the
[official Azure OpenAI audio completions quickstart](https://learn.microsoft.com/azure/foundry/openai/audio-completions-quickstart).

```powershell
python -m pip install -r .\media\requirements.txt
.\media\render_narrate.ps1 -RenderOnly
$env:AZURE_TENANT_ID = "<tenant ID>"
$env:AZURE_CLIENT_ID = "<application ID>"
$env:AZURE_CLIENT_SECRET = [Net.NetworkCredential]::new(
    "", (Read-Host "Client secret" -AsSecureString)
).Password
try {
    python .\media\generate_foundry_narration.py --endpoint "https://<resource>.services.ai.azure.com/openai/v1"
    if ($LASTEXITCODE -ne 0) { throw "Narration generation failed." }
} finally {
    $env:AZURE_CLIENT_SECRET = $null
    $env:AZURE_CLIENT_ID = $null
    $env:AZURE_TENANT_ID = $null
}
python .\media\build_video.py
python .\media\verify_media.py
python -m unittest discover -s .\media -p test_foundry_narration.py
```

The bundled `imageio-ffmpeg` executable supplies the encoder; no separate global
FFmpeg installation is needed. `-RenderOnly` renders the existing presentation
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
The final Foundry voice track is loudness-normalized for consistent listening.
Failed attempts may consume Azure usage; the manifest totals accepted clips,
not an invoice.

Audio and video caches are content-hashed. A complete narration manifest is
required before remixing Foundry audio. Keep `deliverables/narration-chunks/`
and other build intermediates out of Git. Regeneration and media verification
require those intermediate audio/render files or a fresh rebuild.

The original deck is not redistributed. Its actual theme is copied into the
output, and the measured near-black/white/cyan/purple-blue formatting is adapted
with original text and diagrams. No legacy presenter affiliation is copied.

After committing the workshop source and final media, create distributable
archives with `python .\media\package_workshop.py --repo .`.
The complete archive includes the media. The lightweight app/labs archive
excludes large media and Git metadata; initialize Git and commit a baseline
before its worktree exercises.
