#!/bin/bash
#
# Disk and Memory Cleanup Script (Non-Interactive / Cron-Friendly)
# 清理磁盘空间和使用过的内存 — 全自动版本，适合 cron 定时任务
#
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

LOG_FILE="/data/hermes/workspace/MyDocuments/logs/cleanup_log_$(date +%Y%m%d_%H%M%S).txt"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo -e "$msg" | tee -a "$LOG_FILE"
}

section() {
    log ""
    log "${BLUE}--- $1 ---${NC}"
}

# 显示初始状态
show_initial_state() {
    section "初始磁盘使用情况"
    df -h / /home /data 2>/dev/null | column -t >> "$LOG_FILE" 2>/dev/null || df -h / >> "$LOG_FILE"
    
    section "初始内存使用情况"
    free -h >> "$LOG_FILE" 2>/dev/null
    
    section "根目录大目录 TOP 10"
    du -sh /data/* /home/* /* 2>/dev/null | sort -rh | head -10 >> "$LOG_FILE" 2>/dev/null || true
}

# 1. 清理系统内存缓存（释放 buff/cache）
cleanup_system_cache() {
    section "清理系统内存缓存 (drop_caches)"
    sync
    if [ "$(id -u)" -eq 0 ]; then
        echo 3 > /proc/sys/vm/drop_caches 2>/dev/null && log "${GREEN}✓ 系统缓存已清理${NC}" || log "${YELLOW}⚠ 无法写入 drop_caches（可能不需要）${NC}"
    else
        echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null 2>&1 && log "${GREEN}✓ 系统缓存已清理${NC}" || log "${YELLOW}⚠ 无 sudo 权限，跳过 drop_caches${NC}"
    fi
}

# 2. 清理 apt 缓存
cleanup_apt() {
    section "清理 apt 包管理器缓存"
    if [ -d /var/cache/apt ]; then
        local before=$(du -sm /var/cache/apt 2>/dev/null | awk '{print $1}' || echo 0)
        before=${before//[^0-9]/}; before=${before:-0}
        log "清理前 apt 缓存: ${before}MB"
        apt clean 2>/dev/null && apt autoclean 2>/dev/null && apt autoremove -y 2>/dev/null || true
        local after=$(du -sm /var/cache/apt 2>/dev/null | awk '{print $1}' || echo 0)
        after=${after//[^0-9]/}; after=${after:-0}
        local freed=$((before - after))
        log "${GREEN}✓ apt 缓存清理完成，释放 ~${freed}MB${NC}"
    else
        log "apt 缓存目录不存在，跳过"
    fi
}

# 3. 清理 journal 日志
cleanup_journal() {
    section "清理系统日志 (journal)"
    if command -v journalctl &>/dev/null && [ -d /var/log/journal ]; then
        local before=$(du -sm /var/log/journal 2>/dev/null | awk '{print $1}' || echo 0)
        before=${before//[^0-9]/}; before=${before:-0}
        log "清理前 journal 日志: ${before}MB"
        journalctl --vacuum-time=7d 2>/dev/null || true
        local after=$(du -sm /var/log/journal 2>/dev/null | awk '{print $1}' || echo 0)
        after=${after//[^0-9]/}; after=${after:-0}
        local freed=$((before - after))
        log "${GREEN}✓ Journal 日志已清理，释放 ~${freed}MB${NC}"
    else
        log "Journal 日志目录不存在，跳过"
    fi
}

# 4. 清理用户缓存
cleanup_user_cache() {
    section "清理用户缓存"
    local cache_dir="${HOME}/.cache"
    if [ -d "$cache_dir" ]; then
        local before=$(du -sm "$cache_dir" 2>/dev/null | awk '{print $1}' || echo 0)
        before=${before//[^0-9]/}; before=${before:-0}
        log "清理前用户缓存: ${before}MB"
        
        # 安全清理常见缓存子目录
        rm -rf "$cache_dir"/pip 2>/dev/null || true
        rm -rf "$cache_dir"/npm "$cache_dir"/yarn 2>/dev/null || true
        rm -rf "$cache_dir"/node-gyp 2>/dev/null || true
        rm -rf "$cache_dir"/thunderbird 2>/dev/null || true
        rm -rf "$cache_dir"/fontconfig 2>/dev/null || true
        rm -rf "$cache_dir"/Trash 2>/dev/null || true
        
        local after=$(du -sm "$cache_dir" 2>/dev/null | awk '{print $1}' || echo 0)
        after=${after//[^0-9]/}; after=${after:-0}
        local freed=$((before - after))
        log "${GREEN}✓ 用户缓存已清理，释放 ~${freed}MB${NC}"
    else
        log "用户缓存目录不存在，跳过"
    fi
}

# 5. 清理 Hermes 相关数据
cleanup_hermes() {
    section "清理 Hermes 相关数据"
    local hermes_home="${HERMES_HOME:-$HOME/.hermes}"
    if [ -d "$hermes_home" ]; then
        # 清理过期会话 (>30天)
        # local deleted_sessions=$(find "$hermes_home/sessions" -type f -mtime +30 2>/dev/null | wc -l || echo 0)
        # find "$hermes_home/sessions" -type f -mtime +30 -delete 2>/dev/null || true
        # log "${GREEN}✓ 清理了 ${deleted_sessions} 个过期会话文件${NC}"
        
        # 清理临时文件
        local deleted_tmp=$(find "$hermes_home" \( -name "*.tmp" -o -name "*.temp" -o -name "*~" \) -mtime +1 2>/dev/null | wc -l || echo 0)
        find "$hermes_home" \( -name "*.tmp" -o -name "*.temp" -o -name "*~" \) -mtime +1 -delete 2>/dev/null || true
        log "${GREEN}✓ 清理了 ${deleted_tmp} 个临时文件${NC}"
        
        # 清理旧的音频/语音缓存
        if [ -d "$hermes_home/audio_cache" ]; then
            local deleted_audio=$(find "$hermes_home/audio_cache" -type f -mtime +7 2>/dev/null | wc -l || echo 0)
            find "$hermes_home/audio_cache" -type f -mtime +7 -delete 2>/dev/null || true
            log "${GREEN}✓ 清理了 ${deleted_audio} 个过期音频缓存${NC}"
        fi
        
        # 清理旧的截图
        if [ -d "$hermes_home/screenshots" ]; then
            local deleted_ss=$(find "$hermes_home/screenshots" -type f -mtime +14 2>/dev/null | wc -l || echo 0)
            find "$hermes_home/screenshots" -type f -mtime +14 -delete 2>/dev/null || true
            log "${GREEN}✓ 清理了 ${deleted_ss} 个过期截图${NC}"
        fi
    else
        log "Hermes 目录不存在，跳过"
    fi
}

# 6. 清理 Docker 垃圾
cleanup_docker() {
    section "清理 Docker 垃圾"
    if command -v docker &>/dev/null; then
        local before=$(docker system df --format "{{.Size}}" 2>/dev/null | tail -1 || echo "unknown")
        log "清理前 Docker 占用: ${before}"
        docker system prune -af --volumes 2>/dev/null || true
        log "${GREEN}✓ Docker 垃圾已清理${NC}"
    else
        log "Docker 未安装，跳过"
    fi
}

# 7. 清理 Python venv 缓存
cleanup_python() {
    section "清理 Python 缓存"
    find /data /home "$HOME" -type d -name "__pycache__" -empty -exec rmdir {} \; 2>/dev/null || true
    find /data /home "$HOME" -type f -name "*.pyc" -delete 2>/dev/null || true
    find /data /home "$HOME" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find /data /home "$HOME" -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
    log "${GREEN}✓ Python 缓存已清理${NC}"
}

# 8. 清理临时目录
cleanup_tmp() {
    section "清理临时文件"
    find /tmp -type f -atime +3 -delete 2>/dev/null || true
    find /var/tmp -type f -atime +7 -delete 2>/dev/null || true
    rm -rf /tmp/* 2>/dev/null || true
    log "${GREEN}✓ 临时文件已清理${NC}"
}

# 清理日志文件自身（保留最近 5 个）
rotate_logs() {
    section "日志轮转"
    local log_dir="/data/hermes/workspace/MyDocuments"
    if [ -d "$log_dir" ]; then
        local count=$(ls -1 "$log_dir"/cleanup_log_*.txt 2>/dev/null | wc -l || echo 0)
        if [ "$count" -gt 5 ]; then
            ls -1t "$log_dir"/cleanup_log_*.txt 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true
            log "${GREEN}✓ 已轮转旧日志文件，保留最近 5 个${NC}"
        fi
    fi
}

# 显示最终状态
show_final_state() {
    section "清理后磁盘使用情况"
    df -h / /home /data 2>/dev/null | column -t >> "$LOG_FILE" 2>/dev/null || df -h / >> "$LOG_FILE"
    
    section "清理后内存使用情况"
    free -h >> "$LOG_FILE" 2>/dev/null
    
    section "根目录大目录 TOP 10 (清理后)"
    du -sh /data/* /home/* /* 2>/dev/null | sort -rh | head -10 >> "$LOG_FILE" 2>/dev/null || true
}

# ========== 主流程 ==========
main() {
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}   Disk & Memory Cleanup (Auto Mode)${NC}"
    echo -e "${BLUE}   $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
    
    show_initial_state
    
    cleanup_system_cache
    cleanup_apt
    cleanup_journal
    cleanup_user_cache
    cleanup_hermes
    cleanup_docker
    cleanup_python
    cleanup_tmp
    
    show_final_state
    rotate_logs
    
    log ""
    log "${GREEN}============================================${NC}"
    log "${GREEN}   清理全部完成！${NC}"
    log "${GREEN}   日志保存在: ${LOG_FILE}${NC}"
    log "${GREEN}============================================${NC}"
}

main
