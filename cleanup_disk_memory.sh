#!/bin/bash
#
# Disk and Memory Cleanup Script
# 清理磁盘空间和使用过的内存
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   Disk and Memory Cleanup Script${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# 函数：显示磁盘使用情况
show_disk_usage() {
    echo -e "${YELLOW}[1] 当前磁盘使用情况:${NC}"
    echo ""
    df -h / /home /data 2>/dev/null | column -t
    echo ""
}

# 函数：显示内存使用情况
show_memory_usage() {
    echo -e "${YELLOW}[2] 当前内存使用情况:${NC}"
    echo ""
    free -h
    echo ""
}

# 函数：清理系统缓存（释放 buff/cache）
cleanup_system_cache() {
    echo -e "${BLUE}[3] 清理系统内存缓存...${NC}"
    echo "  这会释放 Linux 的 page cache、dentry 和 inode 缓存，不会删除实际数据"
    read -p "  是否清理系统缓存? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -n "  需要 sudo 权限，请输入密码..."
        sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
        echo -e "  ${GREEN}✓ 系统缓存已清理${NC}"
    else
        echo "  跳过系统缓存清理"
    fi
    echo ""
}

# 函数：清理 apt 缓存
cleanup_apt() {
    echo -e "${BLUE}[4] 清理 apt 包管理器缓存...${NC}"
    if [ -d /var/cache/apt ]; then
        local size=$(du -sh /var/cache/apt 2>/dev/null | cut -f1)
        echo "  当前 apt 缓存大小：${size}"
        read -p "  是否清理 apt 缓存? (y/N): " -n 1 -recho
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo apt clean
            sudo apt autoclean
            sudo apt autoremove -y
            echo -e "  ${GREEN}✓ apt 缓存已清理${NC}"
        else
            echo "  跳过 apt 缓存清理"
        fi
    else
        echo "  apt 缓存目录不存在"
    fi
    echo ""
}

# 函数：清理 journal 日志
cleanup_journal() {
    echo -e "${BLUE}[5] 清理系统日志 (journal)...${NC}"
    if [ -d /var/log/journal ]; then
        local size=$(du -sh /var/log/journal 2>/dev/null | cut -f1)
        echo "  当前 journal 日志大小：${size}"
        echo "  建议保留最近 2 周的日志"
        read -p "  是否清理旧的 journal 日志? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo journalctl --vacuum-time=14d
            echo -e "  ${GREEN}✓ Journal 日志已清理${NC}"
        else
            echo "  跳过 journal 日志清理"
        fi
    else
        echo "  Journal 日志目录不存在"
    fi
    echo ""
}

# 函数：清理用户缓存
cleanup_user_cache() {
    echo -e "${BLUE}[6] 清理用户缓存目录...${NC}"
    local cache_dir="$HOME/.cache"
    if [ -d "$cache_dir" ]; then
        echo "  当前缓存目录内容:"
        du -sh "$cache_dir"/* 2>/dev/null | sort -h | tail -5
        echo ""
        echo "  选项:"
        echo "  1) 清理 pip 缓存"
        echo "  2) 清理 npm/yarn 缓存"
        echo "  3) 清理 node-gyp 缓存"
        echo "  4) 清理 playwright 缓存（会删除已安装的浏览器）"
        echo "  5) 清理所有缓存"
        read -p "  选择清理哪些缓存 (1-5, 或直接回车跳过): " -n 1 -r
        echo
        case $REPLY in
            1)
                echo "  清理 pip 缓存..."
                rm -rf "$cache_dir"/pip
                echo -e "  ${GREEN}✓ pip 缓存已清理${NC}"
                ;;
            2)
                echo "  清理 npm/yarn 缓存..."
                rm -rf "$cache_dir"/npm "$cache_dir"/yarn
                echo -e "  ${GREEN}✓ npm/yarn 缓存已清理${NC}"
                ;;
            3)
                echo "  清理 node-gyp 缓存..."
                rm -rf "$cache_dir"/node-gyp
                echo -e "  ${GREEN}✓ node-gyp 缓存已清理${NC}"
                ;;
            4)
                echo "  警告：这会删除所有已安装的 Playwright 浏览器!"
                read -p "  确认删除 playwright 缓存? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm -rf "$cache_dir"/ms-playwright
                    echo -e "  ${GREEN}✓ Playwright 缓存已清理${NC}"
                else
                    echo "  跳过"
                fi
                ;;
            5)
                echo "  清理所有缓存..."
                rm -rf "$cache_dir"/*
                echo -e "  ${GREEN}✓ 所有用户缓存已清理${NC}"
                ;;
            *)
                echo "  跳过用户缓存清理"
                ;;
        esac
    else
        echo "  用户缓存目录不存在"
    fi
    echo ""
}

# 函数：清理 Hermes 相关缓存
cleanup_hermes() {
    echo -e "${BLUE}[7] 清理 Hermes 相关数据...${NC}"
    local hermes_home="${HERMES_HOME:-$HOME/.hermes}"
    
    if [ -d "$hermes_home" ]; then
        echo "  Hermes 目录大小:"
        du -sh "$hermes_home"/* 2>/dev/null | sort -h | tail -5
        echo ""
        echo "  选项:"
        echo "  1) 清理会话记录（保留最近的数据）"
        echo "  2) 清理临时文件"
        echo "  3) 删除旧的 session 导出文件"
        read -p "  选项 (1-3, 或回车跳过): " -n 1 -r
        echo
        case $REPLY in
            1)
                echo "  保留最近 30 天的会话，删除更旧的..."
                find "$hermes_home/sessions" -type f -mtime +30 -delete 2>/dev/null || true
                echo -e "  ${GREEN}✓ 旧会话已清理${NC}"
                ;;
            2)
                echo "  清理临时文件..."
                find "$hermes_home" -name "*.tmp" -o -name "*.temp" -o -name "*~" | xargs rm -f 2>/dev/null || true
                echo -e "  ${GREEN}✓ 临时文件已清理${NC}"
                ;;
            3)
                echo "  删除旧的导出文件 (超过 90 天)..."
                find "$hermes_home" -name "*.md" -o -name "*.txt" -o -name "*.json" | xargs find {} -mtime +90 -delete 2>/dev/null || true
                echo -e "  ${GREEN}✓ 旧导出文件已清理${NC}"
                ;;
            *)
                echo "  跳过 Hermes 数据清理"
                ;;
        esac
    else
        echo "  Hermes 目录不存在"
    fi
    echo ""
}

# 函数：清理大文件
cleanup_large_files() {
    echo -e "${BLUE}[8] 查找并清理大文件...${NC}"
    echo "  搜索超过 500MB 的文件:"
    echo ""
    find /data /home "$HOME" -type f -size +500M 2>/dev/null | head -20 | while read file; do
        size=$(du -h "$file" 2>/dev/null | cut -f1)
        echo "    $size  $file"
    done
    echo ""
    read -p "  是否删除这些大文件? (高风险，y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  警告：请仔细确认不要误删重要文件!"
        read -p "  继续删除? (等待 5 秒后输入 yes 确认): " -r
        echo "  5..."
        sleep 1
        echo "  4..."
        sleep 1
        echo "  3..."
        sleep 1
        echo "  2..."
        sleep 1
        echo "  1..."
        sleep 1
        echo "  删除中..."
        find /data /home "$HOME" -type f -size +500M -mtime +30 -delete 2>/dev/null || true
        echo -e "  ${GREEN}✓ 大文件清理完成${NC}"
    else
        echo "  跳过大文件清理"
    fi
    echo ""
}

# 函数：显示清理后的状态
show_summary() {
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}   清理完成!${NC}"
    echo -e "${GREEN}=========================================${NC}"
    echo ""
    show_disk_usage
    show_memory_usage
    echo ""
    echo -e "${BLUE}提示:${NC}"
    echo "  - 可以定期运行此脚本保持系统整洁"
    echo "  - 建议每周清理一次缓存和日志"
    echo "  - 对于长期未使用的项目，考虑归档或删除"
    echo ""
}

# 主执行流程
main() {
    clear
    show_disk_usage
    show_memory_usage
    
    echo -e "${YELLOW}请选择要执行的清理操作 (通过数字组合，如 '124' 表示执行 1,2,4):${NC}"
    echo "  1 - 清理系统内存缓存"
    echo "  2 - 清理 apt 包管理器缓存"
    echo "  3 - 清理系统日志 (journal)"
    echo "  4 - 清理用户缓存"
    echo "  5 - 清理 Hermes 相关数据"
    echo "  6 - 查找并清理大文件"
    echo "  a - 执行所有安全清理 (1-5)"
    echo "  d - 执行所有清理 (包括大文件)"
    echo "  q - 取消退出"
    echo ""
    read -p "  你的选择: " -r
    echo ""
    
    case $REPLY in
        a)
            cleanup_system_cache
            cleanup_apt
            cleanup_journal
            cleanup_user_cache
            cleanup_hermes
            ;;
        d)
            cleanup_system_cache
            cleanup_apt
            cleanup_journal
            cleanup_user_cache
            cleanup_hermes
            cleanup_large_files
            ;;
        1*|*1*)
            [[ $REPLY == *1* ]] && cleanup_system_cache
            [[ $REPLY == *2* ]] && cleanup_apt
            [[ $REPLY == *3* ]] && cleanup_journal
            [[ $REPLY == *4* ]] && cleanup_user_cache
            [[ $REPLY == *5* ]] && cleanup_hermes
            [[ $REPLY == *6* ]] && cleanup_large_files
            ;;
        q|Q)
            echo "  取消清理"
            exit 0
            ;;
        *)
            # 单个数字
            case $REPLY in
                1) cleanup_system_cache ;;
                2) cleanup_apt ;;
                3) cleanup_journal ;;
                4) cleanup_user_cache ;;
                5) cleanup_hermes ;;
                6) cleanup_large_files ;;
                *) echo "  无效选择"; exit 1 ;;
            esac
            ;;
    esac
    
    show_summary
}

# 检查是否以 root 权限运行
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}注意: 部分清理操作需要 sudo 权限${NC}"
    echo -e "${YELLOW}脚本会在需要时提示输入密码${NC}"
    echo ""
fi

# 运行主函数
main