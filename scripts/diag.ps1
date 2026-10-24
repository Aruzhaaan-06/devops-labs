#requires -Version 7.0
<#
.SYNOPSIS
    Read-only container evidence for laboratory 6: state, health, memory, logs, events.
.DESCRIPTION
    Does not start, stop, recreate or modify a container. Omits Config.Env.
    Docker retains only a bounded recent event buffer; this is not a log archive.
.EXAMPLE
    pwsh -File scripts/diag.ps1 devops-labs-api-1
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0)]
    [ValidatePattern('^[a-zA-Z0-9][a-zA-Z0-9_.-]*$')]
    [string]$Container
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false

function Invoke-DockerRead {
    param([string[]]$DockerArguments)
    $result = & docker @DockerArguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker $($DockerArguments[0]) failed for '$Container': $($result -join [Environment]::NewLine)"
    }
    return $result -join [Environment]::NewLine
}

function Protect-LogText {
    param([string]$Text)
    # Application logs can include connection strings even though inspect omits Env.
    $Text = $Text -replace '(?i)((?:password|pwd|token|secret)\s*[=:]\s*)[^;\s,"}]+', '$1[REDACTED]'
    return $Text -replace '\b(?:gh[opusr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})', '[REDACTED]'
}

try {
    $format = '{"id":{{json .Id}},"state":{{json .State}},"restartCount":{{json .RestartCount}},"memoryLimitBytes":{{json .HostConfig.Memory}},"restartPolicy":{{json .HostConfig.RestartPolicy.Name}}}'
    $snapshot = Invoke-DockerRead -DockerArguments @('inspect', '--format', $format, $Container) | ConvertFrom-Json
    $health = if ($null -ne $snapshot.state.Health) { $snapshot.state.Health.Status } else { 'not configured' }
    Write-Output "Container: $Container"
    Write-Output "ID: $($snapshot.id)"
    Write-Output "Status: $($snapshot.state.Status); Health: $health"
    Write-Output "ExitCode: $($snapshot.state.ExitCode); OOMKilled: $($snapshot.state.OOMKilled)"
    Write-Output "RestartCount: $($snapshot.restartCount); RestartPolicy: $($snapshot.restartPolicy)"
    Write-Output "Memory limit bytes: $($snapshot.memoryLimitBytes)"

    Write-Output "`nMemory/CPU now (docker stats --no-stream):"
    if ($snapshot.state.Running) {
        Invoke-DockerRead -DockerArguments @('stats', '--no-stream', '--format', '{{json .}}', $Container)
    } else {
        Write-Output 'Unavailable: container is not running.'
    }

    Write-Output "`nLast 20 log lines (Docker timestamps):"
    Protect-LogText (Invoke-DockerRead -DockerArguments @('logs', '--timestamps', '--tail', '20', $Container))

    Write-Output "`nDie/OOM events during last 15 minutes (bounded Docker buffer):"
    $events = Invoke-DockerRead -DockerArguments @('events', '--since', '15m', '--until', '0s',
        '--filter', "container=$Container", '--filter', 'event=die', '--filter', 'event=oom', '--format', '{{json .}}')
    if ([string]::IsNullOrWhiteSpace($events)) {
        Write-Output 'No matching events retained.'
    } else {
        Protect-LogText $events
    }
} catch {
    Write-Error (Protect-LogText $_.Exception.Message)
    exit 1
}
