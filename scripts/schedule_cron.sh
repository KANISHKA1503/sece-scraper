#!/bin/bash
# Weekly SECE scraper scheduler for Linux/Unix
# Usage: ./scripts/schedule_cron.sh [install|run|check|remove]

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SPIDER_SCRIPT="$PROJECT_DIR/scripts/run_spider.py"
LOG_FILE="$PROJECT_DIR/logs/weekly_schedule.log"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 [install|run|check|remove]"
    echo "  install - Install cron job for weekly execution"
    echo "  run     - Run scraper immediately"
    echo "  check   - Check if cron job is installed"
    echo "  remove  - Remove cron job"
}

install_cron() {
    echo "Installing cron job..."
    
    # Create cron entry
    CRON_JOB="0 0 * * 0 cd $PROJECT_DIR && /usr/bin/python3 $SPIDER_SCRIPT --clean >> $LOG_FILE 2>&1"
    
    # Check if job already exists
    if crontab -l 2>/dev/null | grep -q "sece_deep_crawl"; then
        echo -e "${YELLOW}Cron job already installed. Removing old entry...${NC}"
        crontab -l 2>/dev/null | grep -v "sece_deep_crawl" | crontab -
    fi
    
    # Install new job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Cron job installed successfully!${NC}"
        echo "Schedule: Every Sunday at 00:00 (midnight)"
        echo "Command: python3 $SPIDER_SCRIPT --clean"
        echo "Logs: $LOG_FILE"
    else
        echo -e "${RED}✗ Failed to install cron job${NC}"
        exit 1
    fi
}

run_scraper() {
    echo "Running SECE scraper..."
    mkdir -p "$PROJECT_DIR/logs"
    
    cd "$PROJECT_DIR"
    python3 "$SPIDER_SCRIPT" --clean >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Scraper completed successfully!${NC}"
    else
        echo -e "${RED}✗ Error occurred during scraping${NC}"
        echo "Check log file: $LOG_FILE"
        exit 1
    fi
}

check_cron() {
    echo "Checking installed cron jobs..."
    
    if crontab -l 2>/dev/null | grep -q "sece_deep_crawl"; then
        echo -e "${GREEN}✓ Cron job is installed${NC}"
        echo ""
        echo "Details:"
        crontab -l 2>/dev/null | grep "sece_deep_crawl"
    else
        echo -e "${RED}✗ Cron job is not installed${NC}"
        exit 1
    fi
}

remove_cron() {
    echo "Removing cron job..."
    
    if crontab -l 2>/dev/null | grep -q "sece_deep_crawl"; then
        crontab -l 2>/dev/null | grep -v "sece_deep_crawl" | crontab -
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Cron job removed successfully!${NC}"
        else
            echo -e "${RED}✗ Failed to remove cron job${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Cron job not found${NC}"
    fi
}

# Main logic
case "$1" in
    install)
        install_cron
        ;;
    run)
        run_scraper
        ;;
    check)
        check_cron
        ;;
    remove)
        remove_cron
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
