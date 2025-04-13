param([string[]]$Args)
$loadingLines = @(
    "Hallucination loading...",
    "Consulting the AI oracle...",
    "Reality distortion field online...",
    "Assembling a plausible reply...",
    "Routing through linguistic chaos..."
    "Unleashing artificial intelligence...",
    "Fabricating answers with confidence...",
    "Conjuring plausible realities...",
    "Plausibility matrix engaged...",
    "Hallucination seeding complete. Executing..."
)
Write-Host ($loadingLines | Get-Random)

$Assistant = $Args[0]
$Prompt = $Args[1..($Args.Length - 1)] -join " "

$Body = @{
    prompt    = $Prompt
    assistant = $Assistant
}

$response = Invoke-RestMethod -Method Post -Uri "http://localhost:5000/ask" `
    -Body ($Body | ConvertTo-Json -Depth 2) `
    -ContentType "application/json"

$response.response
