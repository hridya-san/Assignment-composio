<#
Create and push repository to GitHub using a local Personal Access Token.
USAGE (PowerShell):
  $env:GITHUB_TOKEN = 'ghp_xxx'
  ./create_and_push_github.ps1 -Owner 'your-username' -Repo 'Assignment-composio' -Visibility 'public'

This script will:
 - Check if the repo exists under the given owner
 - Create the repo if missing
 - Initialize a local git repo (if needed), commit, add remote, and push to GitHub

Do NOT paste tokens to anyone. Run locally where your credentials are secure.
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$Owner,
    [Parameter(Mandatory=$true)]
    [string]$Repo,
    [ValidateSet('public','private')]
    [string]$Visibility = 'public'
)

function ExitWithError($msg){ Write-Error $msg; exit 1 }

if (-not $env:GITHUB_TOKEN) { ExitWithError 'GITHUB_TOKEN environment variable is not set. Export it first.' }

$token = $env:GITHUB_TOKEN
$headers = @{ Authorization = "token $token"; 'User-Agent' = 'assignment-script' }

$repoApiUrl = "https://api.github.com/repos/$Owner/$Repo"
$exists = $false

try {
    $resp = Invoke-RestMethod -Uri $repoApiUrl -Headers $headers -Method Get -ErrorAction Stop
    if ($resp -and $resp.full_name) { Write-Host "Repo $Owner/$Repo already exists."; $exists = $true }
} catch {
    if ($_.Exception.Response -ne $null -and $_.Exception.Response.StatusCode.Value__ -eq 404) {
        $exists = $false
    } else {
        Write-Warning "Could not check repo existence: $_"
    }
}

if (-not $exists) {
    Write-Host "Creating repo $Owner/$Repo..."
    $body = @{ name = $Repo; private = ($Visibility -eq 'private') } | ConvertTo-Json
    try {
        $createResp = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $headers -Method Post -Body $body -ContentType 'application/json' -ErrorAction Stop
        Write-Host "Created repo: $($createResp.full_name)"
    } catch {
        ExitWithError "Failed to create repository: $_"
    }
}

# Prepare local git repo
if (-not (Test-Path -Path .git)) {
    Write-Host "Initializing local git repository..."
    git init
}

# Ensure there's at least one commit
$hasCommit = $false
try {
    $hasCommit = git rev-parse --verify HEAD 2>$null
} catch {
    $hasCommit = $false
}

if (-not $hasCommit) {
    git add -A
    try {
        git commit -m "Initial commit: research agent and site" -q
    } catch {
        Write-Host "No changes to commit or commit failed."
    }
}

# Add remote and push
$remote = git remote get-url origin 2>$null
if (-not $remote) {
    $remoteUrl = "https://github.com/$Owner/$Repo.git"
    git remote add origin $remoteUrl
} else {
    Write-Host "Remote 'origin' already set to $remote"
}

Write-Host "Pushing to GitHub..."
# Ensure branch name is main
git branch -M main

# Use HTTPS push - token will be used by git credential helper if configured. We use direct API to set remote with token temporarily to push.
$pushUrlWithToken = "https://$($token)@github.com/$Owner/$Repo.git"

# Temporarily set remote URL with token for push then restore
git remote set-url origin $pushUrlWithToken
try {
    git push -u origin main --force
    Write-Host "Pushed to https://github.com/$Owner/$Repo"
} catch {
    ExitWithError "Push failed: $_"
} finally {
    # Restore remote to tokenless URL
    git remote set-url origin "https://github.com/$Owner/$Repo.git"
}

Write-Host "Done. Repo available at: https://github.com/$Owner/$Repo"
Write-Host "Next: In Render, create a Static Site and connect this GitHub repo. Set build command: 'python research_agent.py' and publish directory: 'site'"
