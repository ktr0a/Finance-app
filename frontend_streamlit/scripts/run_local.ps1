$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FrontDir = Resolve-Path (Join-Path $ScriptDir "..")
$RootDir = Resolve-Path (Join-Path $FrontDir "..")

Set-Location $RootDir
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts\run_api.py"

Set-Location $FrontDir
streamlit run app.py
