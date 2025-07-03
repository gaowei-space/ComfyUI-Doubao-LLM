# ComfyUI 豆包大模型节点开发文档

## 项目概述

本项目是一个为 ComfyUI 开发的自定义节点包，用于集成火山引擎豆包大模型API。该节点支持文本生成和视觉理解功能，提供了灵活的参数配置和安全的API密钥管理。

## 技术架构

### 核心组件

1. **API客户端层** (`DoubaoAPI`)
   - 负责与豆包API的HTTP通信
   - 处理认证和错误处理
   - 支持环境变量配置

2. **配置管理层** (`DoubaoConfig`)
   - 使用Pydantic进行参数验证
   - 支持多种模型配置
   - 提供合理的默认值

3. **消息处理层** (`DoubaoMessage`)
   - 统一的消息格式
   - 支持文本和多模态消息
   - 自动处理图像编码

4. **节点接口层** (ComfyUI节点类)
   - 符合ComfyUI规范的节点定义
   - 类型安全的输入输出
   - 用户友好的参数界面

### 数据流

```
用户输入 → ComfyUI节点 → 消息构建 → API调用 → 响应处理 → 输出结果
```

## 文件结构

```
comfyui-doubao-llm/
├── __init__.py          # 包初始化，导出节点映射
├── nodes.py             # 核心节点实现
├── requirements.txt     # 项目依赖
├── README.md           # 用户文档
├── DEVELOPMENT.md      # 开发文档（本文件）
└── examples/           # 示例工作流（可选）
```

## 核心实现详解

### 1. API客户端实现

```python
class DoubaoAPI:
    def __init__(self, api_key: str = None, endpoint: str = None):
        # API密钥优先级：参数 > 环境变量
        self.api_key = api_key or os.getenv('DOUBAO_API_KEY')
        self.endpoint = endpoint or "https://ark.cn-beijing.volces.com/api/v3"
        
    def chat_completions(self, messages: List[DoubaoMessage], config: DoubaoConfig) -> str:
        # 构建请求、发送API调用、处理响应
```

**设计要点：**
- 支持环境变量配置，提高安全性
- 统一的错误处理和重试机制
- 清晰的API接口设计

### 2. 配置管理

```python
class DoubaoConfig(BaseModel):
    model: str = Field(default="doubao-pro-4k")
    max_tokens: int = Field(default=1000, ge=1, le=4000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    stream: bool = Field(default=False)
```

**设计要点：**
- 使用Pydantic进行参数验证
- 提供合理的默认值和范围限制
- 支持流式和非流式输出

### 3. 消息处理

```python
class DoubaoMessage(BaseModel):
    role: MessageRole
    content: Union[str, List[Dict[str, Any]]]
    
    @classmethod
    def create_text_message(cls, role: MessageRole, text: str):
        # 创建纯文本消息
        
    @classmethod
    def create_multimodal_message(cls, role: MessageRole, text: str, image_base64: str):
        # 创建多模态消息
```

**设计要点：**
- 统一的消息格式，支持文本和多模态
- 自动处理图像编码转换
- 符合豆包API的消息格式要求

### 4. ComfyUI节点实现

每个节点都遵循ComfyUI的标准模式：

```python
class DoubaoTextChatNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": ("STRING", {"multiline": True}),
                "doubao_api": ("DOUBAO_API",),
                "doubao_config": ("DOUBAO_CONFIG",),
            },
            "optional": {
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "chat"
    CATEGORY = "Doubao"
    
    def chat(self, user_prompt, doubao_api, doubao_config, system_prompt=""):
        # 节点执行逻辑
```

**设计要点：**
- 清晰的输入输出类型定义
- 合理的参数分组（必需/可选）
- 用户友好的界面配置

## 开发规范

### 代码风格

1. **命名规范**
   - 类名使用PascalCase
   - 函数和变量使用snake_case
   - 常量使用UPPER_CASE

2. **类型注解**
   - 所有函数参数和返回值都要有类型注解
   - 使用Union、Optional等类型提示

3. **文档字符串**
   - 所有公共方法都要有docstring
   - 使用Google风格的文档字符串

### 错误处理

1. **API错误**
   ```python
   try:
       response = requests.post(url, json=data, headers=headers)
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       raise Exception(f"豆包API调用失败: {str(e)}")
   ```

2. **参数验证**
   ```python
   if not self.api_key:
       raise ValueError("API密钥未设置，请设置环境变量DOUBAO_API_KEY或在节点中输入")
   ```

3. **模型兼容性检查**
   ```python
   if config.model not in doubao_vision_models:
       raise ValueError(f"模型 {config.model} 不支持视觉理解功能")
   ```

### 测试策略

1. **单元测试**
   - 测试API客户端的各种场景
   - 测试配置验证逻辑
   - 测试消息构建功能

2. **集成测试**
   - 测试完整的API调用流程
   - 测试不同模型的兼容性
   - 测试错误处理机制

3. **ComfyUI集成测试**
   - 在实际ComfyUI环境中测试节点
   - 验证工作流的正确性
   - 测试用户界面的友好性

## 扩展开发

### 添加新模型

1. 更新模型列表：
   ```python
   doubao_models = [
       "doubao-pro-4k",
       "doubao-pro-32k",
       # 添加新模型
       "doubao-new-model",
   ]
   ```

2. 如果是视觉模型，同时更新：
   ```python
   doubao_vision_models = [
       "doubao-pro-vision",
       "doubao-lite-vision",
       # 添加新的视觉模型
       "doubao-new-vision",
   ]
   ```

### 添加新功能节点

1. 定义新的节点类
2. 实现INPUT_TYPES和执行方法
3. 更新NODE_CLASS_MAPPINGS
4. 添加相应的测试

### 优化建议

1. **性能优化**
   - 实现请求缓存机制
   - 支持批量处理
   - 异步API调用

2. **用户体验优化**
   - 添加进度指示器
   - 提供更详细的错误信息
   - 支持预设配置模板

3. **功能扩展**
   - 支持流式输出
   - 添加对话历史管理
   - 支持更多的API参数

## 发布准备

### 版本管理

1. 使用语义化版本号（Semantic Versioning）
2. 维护CHANGELOG.md文件
3. 为每个版本创建Git标签

### 文档完善

1. 确保README.md内容完整
2. 提供详细的使用示例
3. 创建视频教程（可选）

### 社区发布

1. **GitHub发布**
   - 创建详细的Release说明
   - 提供安装包下载
   - 设置Issue和PR模板

2. **ComfyUI社区**
   - 在ComfyUI Manager中注册
   - 在相关论坛和社区分享
   - 收集用户反馈

## 维护指南

### 定期维护任务

1. **依赖更新**
   - 定期检查和更新依赖包
   - 测试兼容性

2. **API兼容性**
   - 关注豆包API的更新
   - 及时适配新的API版本

3. **ComfyUI兼容性**
   - 跟进ComfyUI的版本更新
   - 确保节点接口的兼容性

### 问题排查

1. **常见问题**
   - API密钥配置问题
   - 网络连接问题
   - 模型兼容性问题

2. **调试工具**
   - 启用详细日志
   - 使用API测试工具
   - 检查ComfyUI控制台输出

## 贡献指南

### 提交代码

1. Fork项目仓库
2. 创建功能分支
3. 编写代码和测试
4. 提交Pull Request

### 代码审查

1. 检查代码风格
2. 验证功能正确性
3. 确保测试覆盖率
4. 检查文档完整性

---

本文档将随着项目的发展持续更新，欢迎开发者贡献和完善。