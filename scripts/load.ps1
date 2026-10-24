# Фоновая нагрузка на DemoApi для лабораторных по мониторингу. Остановка: Ctrl+C
# Запуск: pwsh ./scripts/load.ps1
# Строки вывода латиницей: так скрипт работает и в Windows PowerShell 5.1
param(
    [string]$BaseUrl = 'http://localhost:8088',
    [ValidateRange(0,60000)][int]$DelayMs = 300,
    [ValidateRange(0,100000)][int]$Iterations = 0
)

$json = 'application/json'
$ErrorActionPreference = 'Stop'
$project = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/projects" -ContentType $json `
    -Body (@{ name = "load-$(Get-Date -Format 'yyyyMMdd-HHmmss')" } | ConvertTo-Json)
Write-Host "Project $($project.id). Load on $BaseUrl, press Ctrl+C to stop"

$i = 0
$failed = 0
while ($Iterations -eq 0 -or $i -lt $Iterations) {
    $i++
    try {
        $task = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/tasks" -ContentType $json `
            -Body (@{ projectId = $project.id; title = "Load task $i" } | ConvertTo-Json)
        Invoke-RestMethod -Method Patch -Uri "$BaseUrl/api/tasks/$($task.id)/status" -ContentType $json `
            -Body (@{ status = 'InProgress' } | ConvertTo-Json) | Out-Null
        Invoke-RestMethod -Uri "$BaseUrl/api/tasks?projectId=$($project.id)&status=Todo" | Out-Null
        if ($i % 20 -eq 0) { Write-Host "iterations: $i" }
    }
    catch {
        $failed++
        Write-Host "error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    Start-Sleep -Milliseconds $DelayMs
}
Write-Host "completed: $i; failed: $failed; project: $($project.id)"
if ($failed -gt 0) { exit 1 }
