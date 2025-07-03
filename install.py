#!/usr/bin/env python3
"""
豆包大模型节点安装脚本
自动安装所需依赖并验证安装
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """运行命令并处理错误"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    print("✅ Python版本符合要求")
    return True

def install_dependencies():
    """安装依赖包"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt文件不存在")
        return False
    
    # 安装依赖
    cmd = f"{sys.executable} -m pip install -r {requirements_file}"
    return run_command(cmd, "安装依赖包")

def verify_installation():
    """验证安装"""
    print("\n正在验证安装...")
    
    try:
        # 尝试导入主要模块
        import requests
        import pydantic
        from PIL import Image
        print("✅ 核心依赖导入成功")
        
        # 运行基础测试（如果存在）
        test_file = Path(__file__).parent / "test_basic.py"
        if test_file.exists():
            print("\n运行基础功能测试...")
            cmd = f"{sys.executable} {test_file}"
            if run_command(cmd, "基础功能测试"):
                print("✅ 所有测试通过")
            else:
                print("⚠️ 部分测试失败，但核心功能应该可用")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        return False

def show_usage_info():
    """显示使用说明"""
    print("\n" + "="*60)
    print("🎉 豆包大模型节点安装完成！")
    print("="*60)
    
    print("\n📋 使用步骤:")
    print("1. 重启ComfyUI")
    print("2. 在节点菜单中找到 'Doubao LLM' 分类")
    print("3. 配置API密钥（推荐使用环境变量）:")
    print("   export DOUBAO_API_KEY='your_api_key_here'")
    print("4. 开始使用豆包节点！")
    
    print("\n🔧 可用节点:")
    print("• 豆包 API 配置 - 配置API密钥和端点")
    print("• 豆包模型配置 - 选择模型和参数")
    print("• 豆包文本对话 - 纯文本对话")
    print("• 豆包视觉对话 - 图像理解对话")
    
    print("\n📚 更多信息:")
    print("• README.md - 详细使用说明")
    print("• DEVELOPMENT.md - 开发文档")
    print("• examples/ - 示例工作流")
    
    print("\n🆘 如遇问题:")
    print("• 检查API密钥配置")
    print("• 查看ComfyUI控制台错误信息")
    print("• 参考README.md中的故障排除部分")
    
    print("\n" + "="*60)

def main():
    """主安装流程"""
    print("豆包大模型ComfyUI节点安装程序")
    print("="*40)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        print("\n❌ 依赖安装失败，请手动安装:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # 验证安装
    if not verify_installation():
        print("\n⚠️ 安装验证失败，但可能仍然可用")
        print("请尝试在ComfyUI中使用节点")
    
    # 显示使用说明
    show_usage_info()

if __name__ == "__main__":
    main()