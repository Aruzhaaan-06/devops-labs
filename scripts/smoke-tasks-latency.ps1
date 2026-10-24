# Read-only latency gate for the local coursework deployment.
param(
    [ValidatePattern('^http://(?:127\.0\.0\.1|localhost):8088/?$')]
    [string]$BaseUrl = 'http://127.0.0.1:8088',
    [ValidateRange(100,10000)][int]$MaxMilliseconds = 1000,
    [ValidateRange(1,10)][int]$Samples = 3
)

$ErrorActionPreference = 'Stop'
$uri = "$($BaseUrl.TrimEnd('/'))/api/tasks?projectId=2147483647&status=Todo"
$results = for ($sample = 1; $sample -le $Samples; $sample++) {
    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    $response = Invoke-WebRequest -Uri $uri -TimeoutSec 5
    $watch.Stop()
    $milliseconds = [Math]::Round($watch.Elapsed.TotalMilliseconds, 3)
    Write-Host "Tasks/List sample $sample : HTTP $($response.StatusCode), $milliseconds ms (limit $MaxMilliseconds ms)"
    if ($response.StatusCode -ne 200) { throw 'Tasks/List did not return HTTP 200' }
    if ($milliseconds -ge $MaxMilliseconds) {
        throw "Tasks/List latency $milliseconds ms exceeds $MaxMilliseconds ms"
    }
    [pscustomobject]@{ sample = $sample; status = $response.StatusCode; milliseconds = $milliseconds }
}
[pscustomobject]@{ path = '/api/tasks'; maxMilliseconds = $MaxMilliseconds; samples = @($results) } | ConvertTo-Json -Depth 4
