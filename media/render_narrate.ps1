param(
    [string]$OutputDirectory = ".\deliverables",
    [int]$SpeechRate = 0,
    [switch]$RenderOnly
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path $OutputDirectory).Path
$manifest = Get-Content (Join-Path $root 'workshop-manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$images = Join-Path $root 'slides'
$audio = Join-Path $root 'audio'
[void][IO.Directory]::CreateDirectory($images)
[void][IO.Directory]::CreateDirectory($audio)
$app = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
    $deck = $app.Presentations.Open((Join-Path $root 'advanced-github-copilot-workshop.pptx'), $(if ($RenderOnly) { -1 } else { 0 }), 0, 0)
    if ($deck.Slides.Count -ne $manifest.slides) { throw 'Rendered slide count differs from manifest.' }
    $adjustments = @()
    foreach ($slide in $deck.Slides) {
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                $range = $shape.TextFrame.TextRange
                $before = $range.Font.Size
                while ($range.BoundHeight -gt ($shape.Height + 0.5) -or $range.BoundWidth -gt ($shape.Width + 0.5)) {
                    if ($range.Font.Size -le 10) { throw "Slide $($slide.SlideIndex) needs structural text reflow: $($shape.Name)" }
                    $range.Font.Size = $range.Font.Size - 1
                }
                if ($range.Font.Size -ne $before) {
                    $adjustments += [pscustomobject]@{slide=$slide.SlideIndex; shape=$shape.Name; before=$before; after=$range.Font.Size}
                }
            }
        }
    }
    if (-not $RenderOnly) {
        $deck.Save()
        $adjustments | ConvertTo-Json -Depth 3 | Set-Content (Join-Path $root 'text-fit-adjustments.json') -Encoding UTF8
    }
    for ($i = 1; $i -le $deck.Slides.Count; $i++) {
        $deck.Slides.Item($i).Export((Join-Path $images ('slide-{0:D2}.png' -f $i)), 'PNG', 1280, 720)
    }
    if (-not $RenderOnly) { $deck.SaveAs((Join-Path $root 'advanced-github-copilot-workshop.pdf'), 32) }
    Write-Output "Rendered $($deck.Slides.Count) slides."
}
finally {
    if ($deck) { $deck.Close() }
    $app.Quit()
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($app)
}
if ($RenderOnly) { return }
$voice = New-Object -ComObject SAPI.SpVoice
$zira = @($voice.GetVoices() | Where-Object { $_.GetDescription() -like '*Zira*' })
if ($zira.Count -eq 0) { throw 'Local Microsoft Zira voice is unavailable. Install a local voice or explicitly select another.' }
$voice.Voice = $zira[0]
$voice.Rate = $SpeechRate
$voice.Volume = 100
for ($i = 0; $i -lt $manifest.slides_data.Count; $i++) {
    $path = Join-Path $audio ('slide-{0:D2}.wav' -f ($i + 1))
    $hashPath = "$path.sha256"
    $inputBytes = [Text.Encoding]::UTF8.GetBytes("$SpeechRate`n$($zira[0].GetDescription())`n$($manifest.slides_data[$i].narration)")
    $sha = [Security.Cryptography.SHA256]::Create()
    try { $inputHash = ($sha.ComputeHash($inputBytes) | ForEach-Object { $_.ToString('x2') }) -join '' } finally { $sha.Dispose() }
    if ((Test-Path $path) -and (Test-Path $hashPath) -and ((Get-Content $hashPath -Raw).Trim() -eq $inputHash)) { continue }
    $stream = New-Object -ComObject SAPI.SpFileStream
    $stream.Format.Type = 22
    try {
        $stream.Open($path, 3, $false)
        $voice.AudioOutputStream = $stream
        [void]$voice.Speak($manifest.slides_data[$i].narration)
    }
    finally {
        $stream.Close()
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($stream)
    }
    Set-Content $hashPath $inputHash -Encoding ASCII
    Write-Output ('Narrated {0}/{1}: {2}' -f ($i + 1), $manifest.slides, $manifest.slides_data[$i].title.Replace("`n", ' '))
}
[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($voice)
