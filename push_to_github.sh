#!/bin/bash
# 安安虾 GitHub 推送脚本

echo "🦞 安安虾 GitHub 推送指南"
echo "=========================="
echo ""

# 检查是否已配置 GitHub
if ! git remote get-url origin 2>/dev/null | grep -q github; then
    echo "📋 步骤 1: 在 GitHub 创建新仓库"
    echo "   1. 访问 https://github.com/new"
    echo "   2. 仓库名称: anansha"
    echo "   3. 选择公开 (Public)"
    echo "   4. 不要初始化 README (我们已经有了)"
    echo "   5. 点击 Create repository"
    echo ""
    
    echo "📋 步骤 2: 配置远程仓库"
    echo "   运行以下命令:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/anansha.git"
    echo ""
    
    echo "   或者使用 SSH (推荐):"
    echo "   git remote add origin git@github.com:YOUR_USERNAME/anansha.git"
    echo ""
    
    echo "📋 步骤 3: 推送代码"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    
    echo "📋 备选方案: GitHub CLI"
    echo "   如果安装了 gh:"
    echo "   gh repo create anansha --public --source=. --remote=origin --push"
else
    echo "✅ 远程仓库已配置"
    echo "🚀 直接推送: git push -u origin main"
fi

echo ""
echo "📱 推送完成后，访问:"
echo "   https://github.com/YOUR_USERNAME/anansha"
echo ""
echo "🎉 安安虾即将上线 GitHub！"
