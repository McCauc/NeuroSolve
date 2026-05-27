# GitNexus Analyze 60% LadybugDB Regression

## Summary

This note documents a real regression we hit after updating GitNexus.

Symptom:

- `gitnexus analyze` stopped progressing at `60% | Loading into LadybugDB...`
- In non-interactive runs, the command exited early instead of finishing
- The failure reproduced even on a fresh scratch `.lbug` database

Effective fix:

- Pin GitNexus's bundled `@ladybugdb/core` dependency to `0.15.3`

Why we fixed it this way:

- `@ladybugdb/core 0.15.4` crashed while loading the `fts` extension on this Windows machine
- `@ladybugdb/core 0.15.3` and `0.15.2` both worked
- GitNexus `1.6.4-rc.24` declared `@ladybugdb/core` as `^0.15.2`, so a normal reinstall/update could silently pull in the broken `0.15.4`

## Environment Where This Happened

- Repo: `Global-Governance`
- OS: Windows x64
- GitNexus: `1.6.4-rc.24`
- Node: `v25.9.0`

## What We Observed

The command appeared stuck at:

```text
60% | Loading into LadybugDB...
```

But the deeper issue was not a slow repo scan. The actual failure happened while GitNexus initialized LadybugDB and tried to load the `fts` extension.

## Investigation Findings

### 1. The repo pipeline was not the problem

Running the shared analysis path showed that:

- file scanning completed
- parsing completed
- community detection completed
- process detection completed
- the failure happened only after the pipeline reached the LadybugDB phase

So the problem was not caused by code parsing or repository size.

### 2. Basic LadybugDB usage still worked

These operations worked:

- open a fresh LadybugDB database
- create a connection
- run a simple query like `RETURN 1 AS n`
- run GitNexus schema creation queries

That narrowed the fault to extension loading, not database creation in general.

### 3. The exact breaking operation was `LOAD EXTENSION fts`

This direct repro failed with `@ladybugdb/core 0.15.4`:

```js
await conn.query('LOAD EXTENSION fts');
```

The process died immediately after that call.

`LOAD EXTENSION VECTOR` also failed the same way in the broken version.

By contrast, unrelated extension behavior was normal. For example, `httpfs` produced a normal "not installed" error instead of crashing the process.

### 4. This was not specific to this repo

The failure reproduced on a fresh scratch `.lbug` database, which means:

- the repo contents were not the root cause
- the existing `.gitnexus/lbug` files were not the root cause
- the issue was in the runtime/dependency layer

### 5. Reinstalling the FTS extension cache did not fix it

We tested a cache refresh under:

- `C:\Users\Nakko\.lbdb\extension\0.15.0\win_amd64\fts\`

Reinstalling the cached extension changed the binary on disk, but `LOAD EXTENSION fts` still crashed under `@ladybugdb/core 0.15.4`.

So the problem was not just a stale cached extension file.

## Version Comparison That Identified the Root Cause

We tested LadybugDB versions directly outside the normal GitNexus CLI flow.

Results:

- `@ladybugdb/core 0.15.2`: `LOAD EXTENSION fts` worked
- `@ladybugdb/core 0.15.3`: `LOAD EXTENSION fts` worked
- `@ladybugdb/core 0.15.4`: `LOAD EXTENSION fts` crashed

This strongly suggests a Windows regression in `@ladybugdb/core 0.15.4` related to extension loading.

## Temporary Workaround

Before the dependency pin, the following workaround allowed analysis to complete:

```powershell
$env:GITNEXUS_LBUG_EXTENSION_INSTALL='never'
gitnexus analyze . --force
```

Why this worked:

- GitNexus skipped extension loading
- LadybugDB still initialized
- the graph loaded successfully
- analysis completed

Tradeoff:

- optional FTS-backed behavior may be degraded

This workaround is useful if a future update reintroduces the problem before a cleaner fix is applied.

## Clean Fix We Applied

We changed the installed global GitNexus package to use `@ladybugdb/core 0.15.3`.

Location:

- `C:\nvm4w\nodejs\node_modules\gitnexus`

Command used:

```powershell
npm install @ladybugdb/core@0.15.3 --save-exact
```

What this changed:

- `gitnexus/package.json` now pins `@ladybugdb/core` to `0.15.3`
- the installed `@ladybugdb/core` package resolved to `0.15.3`
- the installed `@ladybugdb/core-win32-x64` package resolved to `0.15.3`

## Verification After the Fix

After pinning to `0.15.3`, all of these worked:

### Direct extension load

```js
await conn.query('LOAD EXTENSION fts');
```

This succeeded.

### Normal GitNexus analyze flow

```powershell
gitnexus analyze . --force
```

This completed successfully without the workaround env var.

## Why Future Updates Might Break Again

GitNexus `1.6.4-rc.24` declared:

```json
"@ladybugdb/core": "^0.15.2"
```

That means a reinstall or update can silently pull a newer compatible-in-range version, including one with a regression.

If GitNexus is updated again and this issue returns, check whether:

- `@ladybugdb/core` was upgraded back to `0.15.4` or newer
- `gitnexus analyze` is again stalling or dying at `60% | Loading into LadybugDB...`
- direct `LOAD EXTENSION fts` tests start failing again

## Important Path Pitfall Found Later

We later discovered this machine had **two global GitNexus installs**:

- `C:\Users\Nakko\AppData\Roaming\npm\node_modules\gitnexus`
- `C:\nvm4w\nodejs\node_modules\gitnexus`

And `where gitnexus` showed the roaming install first:

- `C:\Users\Nakko\AppData\Roaming\npm\gitnexus.cmd`
- `C:\nvm4w\nodejs\gitnexus.cmd`

That mattered because the earlier LadybugDB pin was applied to the `nvm4w` copy, but the terminal was actually running the roaming copy after reinstalling GitNexus.

So the old fix was still present in one location, but the command on PATH was executing a different install that still had:

- `@ladybugdb/core 0.15.4`

This is why the issue appeared to "come back" after reopening the terminal.

### What proved the active install path

These commands identified the live global location:

```powershell
where gitnexus
npm config get prefix
npm root -g
```

On this machine they resolved to:

- global prefix: `C:\Users\Nakko\AppData\Roaming\npm`
- global node_modules: `C:\Users\Nakko\AppData\Roaming\npm\node_modules`

### What fixed it the second time

We pinned the **active** install here:

```powershell
cd C:\Users\Nakko\AppData\Roaming\npm\node_modules\gitnexus
npm install @ladybugdb/core@0.15.3 --save-exact
```

After that:

- direct `LOAD EXTENSION fts` succeeded again
- `gitnexus analyze . --force` completed successfully again

## Recommended Recovery Procedure For Future LLMs

If this regression happens again, use this order:

1. Confirm the symptom:

```powershell
gitnexus analyze . --force
```

2. Identify which GitNexus install is actually being executed:

```powershell
where gitnexus
npm config get prefix
npm root -g
```

3. Check the installed LadybugDB version in the **active** GitNexus install:

```powershell
Get-Content '<active-global-node_modules>\\gitnexus\\node_modules\\@ladybugdb\\core\\package.json'
```

4. If the installed version is `0.15.4` or another suspect newer version, test direct FTS load:

```powershell
node -e "(async()=>{ const lbug=require('<active-global-node_modules>/gitnexus/node_modules/@ladybugdb/core'); const db=new lbug.Database('tmp-test.lbug'); const conn=new lbug.Connection(db); await conn.query('LOAD EXTENSION fts'); console.log('ok'); })()"
```

5. If that crashes or dies, apply the temporary unblock:

```powershell
$env:GITNEXUS_LBUG_EXTENSION_INSTALL='never'
gitnexus analyze . --force
```

6. Then reapply the cleaner dependency pin to the **active** install:

```powershell
cd <active-global-node_modules>\gitnexus
npm install @ladybugdb/core@0.15.3 --save-exact
```

7. Re-verify:

```powershell
gitnexus analyze . --force
gitnexus status
```

## Notes

- `gitnexus doctor` was not sufficient to catch this issue by itself because it reported capabilities optimistically and did not prove that `LOAD EXTENSION fts` actually succeeded.
- The root problem behaved like a native runtime crash, not a normal JavaScript exception.
- If upstream GitNexus later pins a fixed LadybugDB release, prefer the upstream-supported version over a local manual pin.
