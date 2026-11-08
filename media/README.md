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

The live workshop is **180 minutes**: 60 minutes of instruction/demos, then
30/35/40/15-minute labs. The self-paced video's playback length is independent
of the live schedule. The long-form notes are narration, **not a script to read
verbatim during the 60-minute live segment**.

The video is an original narrated slide lesson with explained code examples,
not a recording of live Copilot UI interaction. It uses local Microsoft Zira
speech synthesis; no attendee or repository data is uploaded to a voice service.
Captions use phrase-level proportional timing anchored to measured audio
durations, not word-level forced alignment.

## Rebuild on Windows

Prerequisites: Python 3.11+, installed PowerPoint, a local Microsoft Zira SAPI
voice, and the supplied reference deck. Node is required separately for the labs.

```powershell
python -m pip install -r .\media\requirements.txt
python .\media\build_deck.py --template "C:\path\to\reference.pptx"
.\media\render_narrate.ps1
python .\media\build_video.py
python .\media\verify_media.py
```

The bundled `imageio-ffmpeg` executable supplies the encoder; no separate global
FFmpeg installation is needed. PowerPoint renders every slide and exports the
PDF, so the video uses the actual deck rendering, not an approximation.
Generated audio and video segments are resumable with content hashes. Narration
changes invalidate affected audio; image/duration changes invalidate video
segments. PowerPoint measures actual text bounds, adjusts overflowing text
within a minimum readable size, saves the editable deck, and then renders it.

The original deck is not redistributed. Its actual theme is copied into the
output, and the measured near-black/white/cyan/purple-blue formatting is adapted
with original text and diagrams. No legacy presenter affiliation is copied.

After committing the workshop source and final media, create distributable
archives with `python .\media\package_workshop.py --repo .`.
The complete archive includes the media. The lightweight app/labs archive
excludes large media and Git metadata; initialize Git and commit a baseline
before its worktree exercises.
