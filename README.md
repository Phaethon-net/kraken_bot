# Kraken Quant Bot (POC)

Free-tier friendly proof-of-concept crypto trading bot for **Kraken**.
- Paper mode and live mode (spot only)
- Minute-level quant scaffold (momentum/mean-reversion + regime filter stubs)
- Logs to CSV and SQLite
- Windows-friendly scripts (install/run/service via NSSM)

## Quick start
### 1) Install deps
```
scripts\install.bat
```

### 2) Configure
- Copy `.env.example` → `.env` and fill in keys after Kraken KYC.
- Edit `config.yaml` for pair/timeframes/risk.

### 3) Run paper mode
```
scripts\run_paper.bat
```

### 4) Run live mode (after testing)
```
scripts\run_live.bat
```

### 5) Optional: install as Windows service (NSSM)
```
scripts\nssm_install.bat
```

## GitHub push (after unzipping here)
```
cd C:\kraken_bot
git add -A
git commit -m "Initial skeleton"
git branch -M main
git remote remove origin 2>NUL
git remote add origin https://github.com/phaethon-net/kraken_bot.git
git push -u origin main
```

