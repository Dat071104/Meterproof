# Local development bootstrap

This project baseline uses Python 3.13 through `uv`, immutable container image digests, and a local Docker Compose lab. It makes no provider or cloud calls. Do not install a host JDK or system Python packages for this baseline.

## Prerequisites

- Git
- `uv` 0.11.20
- Docker Desktop with the Linux engine running
- The image digests listed in [`TOOLCHAIN_PINS.md`](../architecture/TOOLCHAIN_PINS.md)

The `java` executable on the host is not used. The owner’s Oracle Java 23 path shim timed out during diagnosis; the Maven and Flink containers carry the pinned Java 17 runtime.

## First-time setup (PowerShell)

Run from the repository root:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:MYPY_CACHE_DIR = Join-Path $env:TEMP "meterproof-mypy-cache"
if (-not $env:UV_CACHE_DIR) { $env:UV_CACHE_DIR = Join-Path $env:TEMP "meterproof-uv-cache" }
if (-not $env:UV_PROJECT_ENVIRONMENT) { $env:UV_PROJECT_ENVIRONMENT = Join-Path $env:TEMP "meterproof-venv" }
$env:METERPROOF_POSTGRES_PORT = "55432"
$env:METERPROOF_DATABASE_URL = "postgresql+psycopg://meterproof_local:meterproof_local_only@127.0.0.1:55432/meterproof"
uv sync --locked --all-groups
uv run --locked python -c "import sys; print(sys.executable); print(sys.version)"
uv run --locked dbt --version
```

Pull the lab and secret-scan images explicitly before using `--pull never`:

```powershell
docker compose -f infra/compose/compose.yaml --profile full pull
docker pull zricethezav/gitleaks:v8.30.1@sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f
```

Validate the Python baseline and the four configured Compose profiles:

```powershell
uv run --locked ruff check tests tools/meterproof
uv run --locked ruff format --check tests tools/meterproof
uv run --locked mypy --cache-dir $env:MYPY_CACHE_DIR tests tools/meterproof
uv run --locked pytest tests/contracts tests/unit -q
uv run --locked python tools/meterproof/validate_overlay.py --target .
uv run --locked python ai-agent-workspace-pack/_agent_ops/tools/check_repo_hygiene.py --root . --warn-only-artifacts
uv run --locked python tools/meterproof/check_adr_scores.py --root .
foreach ($profile in @("db", "cdc", "stream", "full")) {
    docker compose -f infra/compose/compose.yaml --profile $profile config --quiet
}
```

The lab smoke checks are intentionally separate from the contract/unit suite. Run each profile serially and tear it down before starting the next:

```powershell
foreach ($profile in @("db", "cdc", "stream")) {
    docker compose -f infra/compose/compose.yaml --profile $profile up -d --wait --pull never
    uv run --locked python tools/meterproof/lab_smoke.py --profile $profile
    docker compose -f infra/compose/compose.yaml --profile $profile down -v --remove-orphans
}
```

The P0.4 resource measurement is one run of the `full` profile (no object-store service). It passed on the measured host with five services at about 2.20 GiB total from rounded Docker stats; see the receipt. Do not repeat the resource measurement as part of the clean-checkout verification.

```powershell
docker compose -f infra/compose/compose.yaml --profile full up -d --wait --pull never
uv run --locked python tools/meterproof/lab_smoke.py --profile full
docker stats --no-stream
docker compose -f infra/compose/compose.yaml --profile full down -v --remove-orphans
```

For the database migration smoke, set the flag only while running the opt-in integration test:

```powershell
$env:METERPROOF_DB_SMOKE = "1"
docker compose -f infra/compose/compose.yaml --profile db up -d --wait --pull never
uv run --locked pytest tests/integration/test_migration_smoke.py -q
docker compose -f infra/compose/compose.yaml --profile db down -v --remove-orphans
Remove-Item Env:\METERPROOF_DB_SMOKE
```

Gitleaks uses [`.gitleaks.toml`](../../.gitleaks.toml), which extends the default rules and allowlists only 64-character lowercase hex values under the exact pack-manifest path. Do not add `.gitleaksignore` fingerprints, disable rules, or widen the path.

The A1-6 negative control uses a temporary Git repository outside the project. The following creates a token-shaped non-hex manifest value and the source manifest's digest under `api_token` in another file, commits only in the temporary repository, and verifies that the configured scan reports both findings. It prints no matched values and removes the temporary repo:

```powershell
$controlRoot = Join-Path $env:TEMP ("meterproof-gitleaks-control-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $controlRoot | Out-Null
try {
    git -C $controlRoot init -q
    $packDir = Join-Path $controlRoot "ai-agent-workspace-pack"
    New-Item -ItemType Directory -Path $packDir | Out-Null
    $digest = (Get-Content -LiteralPath "ai-agent-workspace-pack/PACK_MANIFEST.json" -Raw | ConvertFrom-Json).files.'harness/TOKEN_RISK_MATRIX.md'
    $tokenText = "ghp_" + ([guid]::NewGuid().ToString("N") + "abcd")
    $utf8 = [System.Text.UTF8Encoding]::new($false)
    $packJson = ConvertTo-Json -InputObject ([ordered]@{ files = [ordered]@{ "harness/TOKEN_RISK_MATRIX.md" = $tokenText } }) -Depth 4 -Compress
    $apiJson = ConvertTo-Json -InputObject ([ordered]@{ api_token = $digest }) -Compress
    [System.IO.File]::WriteAllText((Join-Path $packDir "PACK_MANIFEST.json"), $packJson, $utf8)
    [System.IO.File]::WriteAllText((Join-Path $controlRoot "other.json"), $apiJson, $utf8)
    Copy-Item -LiteralPath ".gitleaks.toml" -Destination (Join-Path $controlRoot ".gitleaks.toml")
    git -C $controlRoot add -- .gitleaks.toml ai-agent-workspace-pack/PACK_MANIFEST.json other.json
    git -C $controlRoot -c "user.name=Meterproof Synthetic Probe" -c "user.email=probe@example.invalid" commit -q -m "A1-6 synthetic controls"
    $image = "zricethezav/gitleaks:v8.30.1@sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f"
    $report = docker run --rm --network none -v "${controlRoot}:/repo:ro" -w /repo $image git --config .gitleaks.toml --no-banner --log-level error --redact=100 --exit-code 1 --report-format json --report-path - . 2>&1
    $scanExit = $LASTEXITCODE
    $findings = ConvertFrom-Json -InputObject (@($report | ForEach-Object { $_.ToString() }) -join "`n")
    $manifestHit = @($findings | Where-Object { $_.File -eq "ai-agent-workspace-pack/PACK_MANIFEST.json" -and $_.RuleID -eq "github-pat" }).Count -eq 1
    $apiTokenHit = @($findings | Where-Object { $_.File -eq "other.json" -and $_.RuleID -eq "generic-api-key" }).Count -eq 1
    Write-Output "negative_control_exit=$scanExit findings=$(@($findings).Count) manifest_nonhex=$manifestHit other_api_token_digest=$apiTokenHit"
    if ($scanExit -ne 1 -or @($findings).Count -ne 2 -or -not $manifestHit -or -not $apiTokenHit) { throw "A1-6 negative control failed" }
} finally {
    if (Test-Path -LiteralPath $controlRoot) {
        $base = (Resolve-Path -LiteralPath $env:TEMP).Path
        $target = (Resolve-Path -LiteralPath $controlRoot).Path
        if (-not $target.StartsWith($base + '\', [System.StringComparison]::OrdinalIgnoreCase)) { throw "Refusing cleanup outside temp root: $target" }
        Remove-Item -LiteralPath $target -Recurse -Force
    }
}
```

Then scan both the project's full Git history and working tree:

```powershell
docker run --rm -v "${PWD}:/repo:ro" -w /repo zricethezav/gitleaks:v8.30.1@sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f git --config .gitleaks.toml --redact=100 --exit-code 1 .
docker run --rm -v "${PWD}:/repo:ro" -w /repo zricethezav/gitleaks:v8.30.1@sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f dir --config .gitleaks.toml --redact=100 --exit-code 1 .
```

Record the image digest and each process exit code in the P0.4 receipt. Do not print or retain a real secret value.

## Offline re-run

After the first-time setup has cached the locked wheels and the explicitly pinned images, a clean checkout should reproduce the baseline without network access. Reuse the same external `UV_CACHE_DIR` and set `UV_PROJECT_ENVIRONMENT` to a new temporary venv path for the clean checkout:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:MYPY_CACHE_DIR = Join-Path $env:TEMP "meterproof-mypy-cache"
if (-not $env:UV_CACHE_DIR) { $env:UV_CACHE_DIR = Join-Path $env:TEMP "meterproof-uv-cache" }
if (-not $env:UV_PROJECT_ENVIRONMENT) { $env:UV_PROJECT_ENVIRONMENT = Join-Path $env:TEMP "meterproof-offline-venv" }
$env:METERPROOF_POSTGRES_PORT = "55432"
$env:METERPROOF_DATABASE_URL = "postgresql+psycopg://meterproof_local:meterproof_local_only@127.0.0.1:55432/meterproof"
uv sync --locked --offline --all-groups
uv run --offline --locked python -c "import sys; print(sys.executable); print(sys.version)"
uv run --offline --locked ruff check tests tools/meterproof
uv run --offline --locked ruff format --check tests tools/meterproof
uv run --offline --locked mypy --cache-dir $env:MYPY_CACHE_DIR tests tools/meterproof
uv run --offline --locked pytest tests/contracts tests/unit -q
uv run --offline --locked python tools/meterproof/validate_overlay.py --target .
uv run --offline --locked python ai-agent-workspace-pack/_agent_ops/tools/check_repo_hygiene.py --root . --warn-only-artifacts
uv run --offline --locked python tools/meterproof/check_adr_scores.py --root .
foreach ($profile in @("db", "cdc", "stream", "full")) {
    docker compose -f infra/compose/compose.yaml --profile $profile config --quiet
}
docker compose -f infra/compose/compose.yaml --profile db up -d --wait --pull never
$env:METERPROOF_DB_SMOKE = "1"
uv run --offline --locked pytest tests/integration/test_migration_smoke.py -q
docker compose -f infra/compose/compose.yaml --profile db down -v --remove-orphans
Remove-Item Env:\METERPROOF_DB_SMOKE
if (@(docker ps -a --filter "label=com.docker.compose.project=meterproof" --format "{{.ID}}").Count -ne 0) { throw "Meterproof containers remain" }
if (@(docker volume ls --filter "label=com.docker.compose.project=meterproof" --format "{{.Name}}").Count -ne 0) { throw "Meterproof volumes remain" }
```

The verification receipt must report skipped integration tests as skipped, never as passed. The offline clean-checkout run must set `METERPROOF_DB_SMOKE=1` and show the migration smoke actually ran.

The hygiene helper currently treats the required `infra/compose/.env.example` as a filesystem artifact because its scan matches `.env.*` without honoring the `.gitignore` exception. The documented `--warn-only-artifacts` invocation still fails on forbidden tracked files and reports the warning; verify that the warning list contains only this placeholder file and that no generated files are tracked.

## Teardown

After each profile, confirm `docker ps -a --filter label=com.docker.compose.project=meterproof` and `docker volume ls --filter label=com.docker.compose.project=meterproof` return no rows. If needed, from the repository root:

```powershell
docker compose -f infra/compose/compose.yaml --profile full down -v --remove-orphans
```

Do not change Docker Desktop CPU or memory settings. The P0.4 receipt records the observed allocation and lab footprint. The allocation was 20 CPUs and 8,171,610,112 bytes of memory. The single full-lab run, excluding an object store, used about 2.20 GiB across the five Meterproof containers from the sum of rounded Docker stats values; global Docker disk totals were unchanged before/after teardown.

## Troubleshooting

- **Host `java -version` hangs:** do not use or repair the host shim. The project uses JDK 17 inside pinned containers; see the Java diagnosis in the pin manifest.
- **Pytest loads an unrelated user plugin:** set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`; the environment in this runbook does this before pytest.
- **Python creates caches in the checkout:** keep `PYTHONDONTWRITEBYTECODE=1`, use `-p no:cacheprovider` from `pyproject.toml`, and place the mypy cache under `%TEMP%`.
- **Windows reports path-length errors:** configure `git config --global core.longpaths true` only if the owner chooses to change that host setting; it is not needed to run the documented commands unless Git reports a path-length failure.
- **Docker cannot bind PostgreSQL port 55432:** the runbook uses this loopback port because Windows denied the Compose default 54329 on the measured host. Choose another available port through `METERPROOF_POSTGRES_PORT` and set `METERPROOF_DATABASE_URL` to the same port. This changes only the Compose process environment, not host or Docker settings.
- **A profile cannot become healthy:** capture the service health/logs and Docker allocation, tear down with `down -v --remove-orphans`, and record the failing service. Do not increase Docker Desktop limits as part of this work order.

## Artifacts profile

The artifacts profile is `NOT_PINNED` and omitted from `full` under Amendment 01 A1-1. MinIO OSS is unmaintained; the maintained official AIStor successor requires vendor licensing terms, and no license request is authorized. The artifact-store choice moves to P3. Any full-lab memory measurement therefore excludes an object store. See [`TOOLCHAIN_PINS.md`](../architecture/TOOLCHAIN_PINS.md) and the P0.4 receipt.
