#!/usr/bin/env python3
"""
基础功能测试脚本
测试豆包节点的基本功能，不依赖ComfyUI环境
"""

import os
import sys
from unittest.mock import Mock, patch

# 模拟torch模块
sys.modules['torch'] = Mock()
sys.modules['torch.nn'] = Mock()
sys.modules['torch.nn.functional'] = Mock()

# 导入我们的模块
from nodes import (
    DoubaoConfig, 
    DoubaoMessage, 
    MessageRole,
    DoubaoAPI,
    doubao_models,
    doubao_vision_models,
    NODE_CLASS_MAPPINGS,
    NODE_DISPLAY_NAME_MAPPINGS
)

def test_config():
    """测试配置类"""
    print("测试DoubaoConfig...")
    
    # 测试默认配置
    config = DoubaoConfig()
    assert config.model == "doubao-seed-1.6-flash-250615"
    assert config.max_tokens == 1000
    assert config.temperature == 0.7
    assert config.top_p == 0.9
    assert config.stream == False
    print("✓ 默认配置测试通过")
    
    # 测试自定义配置
    config = DoubaoConfig(
        model="doubao-pro-vision",
        max_tokens=2000,
        temperature=0.5,
        top_p=0.8
    )
    assert config.model == "doubao-pro-vision"
    assert config.max_tokens == 2000
    assert config.temperature == 0.5
    assert config.top_p == 0.8
    print("✓ 自定义配置测试通过")

def test_message():
    """测试消息类"""
    print("\n测试DoubaoMessage...")
    
    # 测试文本消息
    msg = DoubaoMessage.create_text_message(MessageRole.user, "Hello")
    assert msg.role == MessageRole.user
    assert isinstance(msg.content, list)
    assert len(msg.content) == 1
    assert msg.content[0]["type"] == "text"
    assert msg.content[0]["text"] == "Hello"
    print("✓ 文本消息测试通过")
    
    # 测试多模态消息
    msg = DoubaoMessage.create_multimodal_message(
        MessageRole.user, 
        "描述这张图片", 
        "base64_image_data"
    )
    assert msg.role == MessageRole.user
    assert isinstance(msg.content, list)
    assert len(msg.content) == 2
    assert msg.content[0]["type"] == "text"
    assert msg.content[1]["type"] == "image_url"
    print("✓ 多模态消息测试通过")

def test_api_client():
    """测试API客户端"""
    print("\n测试DoubaoAPI...")
    
    # 测试初始化
    api = DoubaoAPI(api_key="test_key", endpoint="https://test.com")
    assert api.api_key == "test_key"
    assert api.endpoint == "https://test.com"
    print("✓ API客户端初始化测试通过")
    
    # 测试环境变量
    with patch.dict(os.environ, {'DOUBAO_API_KEY': 'env_key'}):
        api = DoubaoAPI()
        assert api.api_key == "env_key"
    print("✓ 环境变量测试通过")
    
    # 测试缺少API密钥的情况
    with patch.dict(os.environ, {}, clear=True):
        try:
            api = DoubaoAPI()
            assert False, "应该抛出异常"
        except ValueError as e:
            assert "API key not set" in str(e)
    print("✓ API密钥验证测试通过")
    
    # 测试模型格式验证
    with patch.dict(os.environ, {'DOUBAO_API_KEY': 'test_key'}):
        api = DoubaoAPI()
        
        # 测试无效的模型格式
        invalid_config = DoubaoConfig(model="invalid-model-id")
        try:
            api.chat_completions([], invalid_config)
            assert False, "应该抛出ValueError"
        except ValueError as e:
            assert "Invalid model format" in str(e)
            
        # 测试有效的Endpoint ID格式
        valid_endpoint_config = DoubaoConfig(model="ep-20241201123456-abcde")
        try:
            # 由于没有真实的API密钥，这会失败，但不会因为格式问题失败
            api.chat_completions([], valid_endpoint_config)
        except Exception as e:
            # 确保不是格式验证错误
            assert "Invalid model format" not in str(e)
            
        # 测试有效的Model ID格式
        valid_model_config = DoubaoConfig(model="doubao-seed-1.6-250615")
        try:
            # 由于没有真实的API密钥，这会失败，但不会因为格式问题失败
            api.chat_completions([], valid_model_config)
        except Exception as e:
            # 确保不是格式验证错误
            assert "Invalid model format" not in str(e)
    
    print("✓ 模型格式验证测试通过")

def test_models():
    """测试模型列表"""
    print("\n测试模型列表...")
    
    # 测试最新的豆包1.6系列模型
    assert "doubao-seed-1.6-250615" in doubao_models
    assert "doubao-seed-1.6-flash-250615" in doubao_models
    assert "doubao-seed-1.6-thinking-250615" in doubao_models
    
    # 测试视觉模型
    assert "doubao-seed-1.6-250615" in doubao_vision_models
    assert "doubao-1.5-thinking-vision-pro-250428" in doubao_vision_models
    
    # 测试兼容性模型
    assert "doubao-1.5-pro-32k" in doubao_models
    assert "doubao-1.5-vision-pro-32k" in doubao_vision_models
    
    assert len(doubao_models) > 0
    assert len(doubao_vision_models) > 0
    print(f"✓ 文本模型数量: {len(doubao_models)}")
    print(f"✓ 视觉模型数量: {len(doubao_vision_models)}")
    print(f"✓ 最新推荐模型: doubao-seed-1.6-250615")

def test_node_mappings():
    """测试节点映射"""
    print("\n测试节点映射...")
    
    expected_nodes = [
        "DoubaoAPI",
        "DoubaoConfig", 
        "DoubaoTextChat",
        "DoubaoVisionChat"
    ]
    
    for node in expected_nodes:
        assert node in NODE_CLASS_MAPPINGS
        assert node in NODE_DISPLAY_NAME_MAPPINGS
    
    print(f"✓ 节点类映射: {list(NODE_CLASS_MAPPINGS.keys())}")
    print(f"✓ 节点显示名称: {list(NODE_DISPLAY_NAME_MAPPINGS.values())}")

def test_node_input_types():
    """测试节点输入类型定义"""
    print("\n测试节点输入类型...")
    
    # 测试DoubaoAPI节点
    api_node = NODE_CLASS_MAPPINGS["DoubaoAPI"]
    input_types = api_node.INPUT_TYPES()
    assert "required" in input_types
    # DoubaoAPI节点没有optional字段，这是正常的
    print("✓ DoubaoAPI输入类型定义正确")
    
    # 测试DoubaoConfig节点
    config_node = NODE_CLASS_MAPPINGS["DoubaoConfig"]
    input_types = config_node.INPUT_TYPES()
    assert "required" in input_types
    print("✓ DoubaoConfig输入类型定义正确")
    
    # 测试DoubaoTextChat节点
    text_chat_node = NODE_CLASS_MAPPINGS["DoubaoTextChat"]
    input_types = text_chat_node.INPUT_TYPES()
    assert "required" in input_types
    assert "optional" in input_types
    print("✓ DoubaoTextChat输入类型定义正确")
    
    # 测试DoubaoVisionChat节点
    vision_chat_node = NODE_CLASS_MAPPINGS["DoubaoVisionChat"]
    input_types = vision_chat_node.INPUT_TYPES()
    assert "required" in input_types
    assert "optional" in input_types
    print("✓ DoubaoVisionChat输入类型定义正确")

def main():
    """运行所有测试"""
    print("开始测试豆包节点基础功能...\n")
    
    try:
        test_config()
        test_message()
        test_api_client()
        test_models()
        test_node_mappings()
        test_node_input_types()
        
        print("\n🎉 所有测试通过！")
        print("\n节点功能验证：")
        print("✅ 配置管理正常")
        print("✅ 消息处理正常")
        print("✅ API客户端正常")
        print("✅ 模型列表完整")
        print("✅ 节点映射正确")
        print("✅ 输入类型定义正确")
        
        print("\n🚀 豆包节点已准备就绪，可以在ComfyUI中使用！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()