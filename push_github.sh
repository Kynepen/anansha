#!/bin/bash
# 安安虾 GitHub 推送脚本
# 运行前请确保已登录 GitHub 并有仓库创建权限

set -e

REPO_NAME="anansha"
GITHUB_USER="kyne1127"

echo "🦞 安安虾 GitHub 推送工具"
echo "=========================="
echo ""

# 检查是否在正确的目录
if [ ! -f "README.md" ]; then
    echo "❌ 请在 anansha 项目目录中运行此脚本"
    exit 1
fi

# 方式 1: 尝试使用 gh CLI
if command -v gh &> /dev/null; then
    echo "✅ 检测到 GitHub CLI"
    
    # 检查登录状态
    if gh auth status &> /dev/null; then
        echo "✅ 已登录 GitHub"
        
        echo "📦 创建 GitHub 仓库..."
        gh repo create "$REPO_NAME" --public --description="安安虾 - 币安智能交易助手" --homepage="" || true
        
        echo "🚀 推送代码..."
        git remote remove origin 2>/dev/null || true
        git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
        git branch -M main
        git push -u origin main
        
        echo ""
        echo "🎉 推送成功！"
        echo "📱 访问: https://github.com/$GITHUB_USER/$REPO_NAME"
        exit 0
    else
        echo "⚠️ 请先登录 GitHub CLI: gh auth login"
    fi
else
    echo "⚠️ 未检测到 GitHub CLI"
fi

# 方式 2: 使用 HTTPS + Token
echo ""
echo "📋 手动推送指南："
echo "=================="
echo ""
echo "方式 1: 使用 GitHub CLI (推荐)"
echo "------------------------------"
echo "1. 安装 GitHub CLI:"
echo "   sudo apt install gh  # Ubuntu/Debian"
echo "   brew install gh      # macOS"
echo ""
echo "2. 登录 GitHub:"
echo "   gh auth login"
echo ""
echo "3. 创建仓库并推送:"
echo "   gh repo create anansha --public --source=. --remote=origin --push"
echo ""
echo ""
echo "方式 2: 使用 HTTPS + Personal Access Token"
echo "-------------------------------------------"
echo "1. 创建 GitHub Token:"
echo "   访问: https://github.com/settings/tokens/new"
echo "   勾选 'repo' 权限，点击 Generate token"
echo "   复制生成的 token (只显示一次！)"
echo ""
echo "2. 配置远程仓库:"
echo "   git remote remove origin 2>/dev/null || true"
echo "   git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "   git branch -M main"
echo ""
echo "3. 推送 (会提示输入密码，输入 Token):"
echo "   git push -u origin main"
echo ""
echo ""
echo "方式 3: 使用 SSH (最方便后续使用)"
echo "----------------------------------"
echo "1. 复制 SSH 公钥:"
echo "   cat ~/.ssh/id_ed25519.pub"
echo ""
echo "2. 添加到 GitHub:"
echo "   访问: https://github.com/settings/ssh/new"
echo "   粘贴公钥，点击 Add SSH key"
echo ""
echo "3. 配置远程仓库:"
echo "   git remote remove origin 2>/dev/null || true" 
echo "   git remote add origin git@github.com:$GITHUB_USER/$REPO_NAME.git"
echo "   git branch -M main"
echo ""
echo "4. 推送:"
echo "   git push -u origin main"
echo ""
