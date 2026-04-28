$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$logsDir = Join-Path $scriptDir "logs"
New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
$startLog = Join-Path $logsDir "start.log"

function Write-Log($message) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "$timestamp | $message"
    
    # Retry logic for file locking issues
    $maxRetries = 3
    $retryCount = 0
    
    while ($retryCount -lt $maxRetries) {
        try {
            Add-Content -Path $startLog -Value $logEntry -Encoding UTF8 -ErrorAction Stop
            Write-Host $logEntry
            break
        }
        catch {
            $retryCount++
            if ($retryCount -lt $maxRetries) {
                Start-Sleep -Milliseconds 100
            }
            else {
                Write-Host "WARNING: Could not write to log file: $_" -ForegroundColor Yellow
                Write-Host $logEntry
            }
        }
    }
}

function Clear-Port($port) {
    $conns = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($procId in $conns) {
        if ($procId) {
            Write-Log "Stopping process $procId on port $port"
            Stop-Process -Id $procId -Force
        }
    }
}

if (-not (Test-Path (Join-Path $scriptDir ".venv"))) {
    Write-Log "Creating virtual environment"
    & python -m venv .venv 2>&1 | Out-File -FilePath $startLog -Append -Encoding UTF8
}

$venvPython = Join-Path $scriptDir ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Virtual environment Python not found at $venvPython"
}

Write-Log "Installing Python dependencies"
& $venvPython -m pip install --upgrade pip --disable-pip-version-check -q 2>&1 |
    Out-File -FilePath $startLog -Append -Encoding UTF8
& $venvPython -m pip install -r requirements.txt --disable-pip-version-check -q 2>&1 |
    Out-File -FilePath $startLog -Append -Encoding UTF8

# Install Node.js dependencies for React frontend
Write-Log "Installing Node.js dependencies"
$frontendDir = Join-Path $scriptDir "alz-frontend-main"
$nodeModules = Join-Path $frontendDir "node_modules"
if (-not (Test-Path $nodeModules)) {
    Write-Log "Running: npm install in $frontendDir"
    Set-Location $frontendDir
    & npm install --loglevel=warn 2>&1 | Out-File -FilePath $startLog -Append -Encoding UTF8
    Set-Location $scriptDir
    Write-Log "Node.js dependencies installed"
} else {
    Write-Log "Node modules already installed, skipping npm install"
}

Clear-Port 5000
Clear-Port 3000

Write-Log "Starting API on port 5000"
$apiProcess = Start-Process -NoNewWindow -FilePath $venvPython -ArgumentList @(
    "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"
) -WorkingDirectory $scriptDir -PassThru

Write-Log "Starting React UI on port 3000"
$frontendDir = Join-Path $scriptDir "alz-frontend-main"
$uiProcess = Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList @(
    "/c", "cd /d `"$frontendDir`" && npm run dev"
) -PassThru

Write-Log "Opening browsers"
Start-Process "http://localhost:5000/health"
Start-Process "http://localhost:3000"
Write-Log "Startup complete!"
