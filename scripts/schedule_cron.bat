@echo off
REM Weekly SECE scraper scheduler for Windows
REM Usage: schedule_cron.bat [install|run]

setlocal enabledelayexpansion

set PROJECT_DIR=%~dp0..
set SPIDER_SCRIPT=%PROJECT_DIR%\scripts\run_spider.py
set LOG_FILE=%PROJECT_DIR%\logs\weekly_schedule.log

if "%1"=="install" (
    echo Installing scheduled task...
    REM Create a scheduled task that runs every Sunday at midnight
    schtasks /create /tn "SECE-WebScraper-Weekly" /tr "python %SPIDER_SCRIPT% --clean" /sc weekly /d SUN /st 00:00 /f
    echo Scheduled task installed successfully!
    echo Task: SECE-WebScraper-Weekly
    echo Schedule: Weekly, Sunday at 00:00 (midnight)
    exit /b 0
)

if "%1"=="run" (
    echo Running SECE scraper...
    cd /d %PROJECT_DIR%
    python scripts/run_spider.py --clean >> "%LOG_FILE%" 2>&1
    if !errorlevel! equ 0 (
        echo Scraper completed successfully!
    ) else (
        echo Error occurred during scraping. Check log file for details.
    )
    exit /b !errorlevel!
)

echo Usage: schedule_cron.bat [install^|run]
echo   install - Install as Windows scheduled task
echo   run     - Run scraper immediately
