# ComfyUI 豆包大模型节点

这是一个为 ComfyUI 开发的自定义节点包，用于集成火山引擎豆包大模型API，支持文本生成和视觉理解功能。

## 功能特性

- 🤖 **多模型支持**: 支持豆包系列的多个模型，包括文本和视觉理解模型
- 🖼️ **视觉理解**: 支持图像+文本的多模态输入
- ⚙️ **灵活配置**: 支持temperature、top_p、max_tokens等参数调节
- 🔒 **安全性**: API密钥支持环境变量配置，保护敏感信息
- 🎯 **易用性**: 简洁的节点设计，易于在工作流中使用

## 支持的模型

### 🔥 最新推荐模型（豆包1.6系列）
- `doubao-seed-1.6-250615` - **强烈推荐** 全新多模态深度思考模型，支持256K上下文，支持图文、视频理解 <mcreference link="https://www.volcengine.com/docs/82379/1330310" index="0">0</mcreference>
- `doubao-seed-1.6-flash-250615` - 极速版本，延迟极低，视觉理解能力比肩友商旗舰模型 <mcreference link="https://www.volcengine.com/docs/82379/1330310" index="0">0</mcreference>
- `doubao-seed-1.6-thinking-250615` - 深度思考强化版本，在编程、数学、逻辑推理等能力上大幅提升 <mcreference link="https://www.volcengine.com/docs/82379/1330310" index="0">0</mcreference>

### 豆包1.5系列模型
- `doubao-1.5-thinking-vision-pro-250428` - 支持深度思考的视觉理解模型
- `doubao-1.5-thinking-pro-250415` - 深度思考文本模型
- `doubao-1.5-vision-pro-250328` - 视觉理解模型
- `doubao-1.5-pro-32k` - 32K上下文文本模型
- `doubao-1.5-pro-256k` - 256K上下文文本模型
- `doubao-1.5-lite-32k` - 轻量版32K上下文

### DeepSeek系列模型
- `deepseek-r1-250528` - **推荐** 深度思考模型，能力比肩OpenAI o1 <mcreference link="https://www.volcengine.com/docs/82379/1330310" index="0">0</mcreference>
- `deepseek-r1-distill-qwen-32b-250120` - 32B参数蒸馏版本
- `deepseek-r1-distill-qwen-7b-250120` - 7B参数蒸馏版本

### 兼容性模型（旧版）
- `doubao-pro-32k` / `doubao-pro-256k` - 豆包专业版
- `doubao-lite-32k` / `doubao-lite-128k` - 豆包轻量版
- `doubao-vision-pro-32k` / `doubao-vision-lite-32k` - 旧版视觉模型

## 安装方法

### 方法一：Git克隆（推荐）

1. 进入ComfyUI的custom_nodes目录：
```bash
cd ComfyUI/custom_nodes
```

2. 克隆本项目：
```bash
git clone https://github.com/your-username/comfyui-doubao-llm.git
```

3. 安装依赖：
```bash
cd comfyui-doubao-llm
pip install -r requirements.txt
```

### 方法二：手动下载

1. 下载项目文件到 `ComfyUI/custom_nodes/comfyui-doubao-llm/` 目录
2. 安装依赖：`pip install -r requirements.txt`

## 快速开始

🔄 **重要更新：现在同时支持Model ID和Endpoint ID调用** 🔄

### 📖 详细设置指南

**建议阅读** [完整设置指南](SETUP_GUIDE.md)，其中包含：
- 获取API密钥的详细步骤
- 开通模型服务的完整流程
- 创建推理接入点的步骤（如需使用Endpoint ID）
- 常见问题解决方案

### 🚀 快速配置步骤

1. **获取API密钥**
   - 访问 [火山方舟控制台](https://console.volcengine.com/ark)
   - 在「API Key管理」中创建API Key

2. **选择调用方式**
   - **方式一：直接使用Model ID**（推荐，简单快捷）
     - 直接使用上面列出的模型ID（如 `doubao-seed-1.6-250615`）
   - **方式二：创建推理接入点**（可选，提供更多高级功能）
     - 开通所需的豆包模型服务
     - 在「在线推理」中创建推理接入点
     - 复制Endpoint ID（格式：`ep-xxxxxxxxxx-xxxxx`）

3. **配置环境变量**
   ```bash
   export DOUBAO_API_KEY="your-api-key-here"
   ```

4. **在ComfyUI中使用**
   - 重启ComfyUI
   - 添加Doubao节点到工作流
   - **在DoubaoConfig节点的model字段中输入Model ID或Endpoint ID**
   - 执行工作流

## 配置API密钥

### 方法一：环境变量（推荐）

设置环境变量：
```bash
export DOUBAO_API_KEY="your_api_key_here"
```

### 方法二：节点输入

直接在豆包API配置节点中输入API密钥（不推荐在生产环境使用）。

## 使用方法

### 基础文本对话

1. **添加豆包API配置节点**
   - 输入API密钥（或使用环境变量）
   - 设置API端点（默认为官方端点）

2. **添加豆包模型配置节点**
   - 选择模型（如 `doubao-pro-4k`）
   - 调整参数：
     - `max_tokens`: 最大输出长度（1-4000）
     - `temperature`: 随机性控制（0.0-2.0）
     - `top_p`: 核采样参数（0.0-1.0）

3. **添加豆包文本对话节点**
   - 连接API配置和模型配置
   - 输入用户提示词
   - 可选：设置系统提示词

### 视觉理解对话

1. **使用视觉理解模型**
   - 在模型配置中选择 `doubao-pro-vision` 或 `doubao-lite-vision`

2. **添加豆包视觉对话节点**
   - 连接图像输入
   - 连接API配置和模型配置
   - 输入关于图像的提示词
   - 可选：设置系统提示词

## 节点说明

### 豆包API配置 (DoubaoAPI)
**输入：**
- `api_key`: API密钥（可选，优先使用环境变量）
- `endpoint`: API端点地址

**输出：**
- `doubao_api`: API客户端实例

### 豆包模型配置 (DoubaoConfig)
**输入：**
- `model`: 输入模型ID（如 `doubao-seed-1.6-250615`）或Endpoint ID（如 `ep-xxxxxxxxxx-xxxxx`）
- `max_tokens`: 最大输出token数
- `temperature`: 温度参数（控制随机性）
- `top_p`: Top-p参数（控制多样性）

**输出：**
- `doubao_config`: 模型配置实例

### 豆包文本对话 (DoubaoTextChat)
**输入：**
- `user_prompt`: 用户提示词
- `doubao_api`: API客户端
- `doubao_config`: 模型配置
- `system_prompt`: 系统提示词（可选）
- `ignore_errors`: 忽略错误（可选，默认启用）- 启用时API错误将被忽略并返回空字符串而不是抛出异常

**输出：**
- `response`: AI生成的回复文本

### 豆包视觉对话 (DoubaoVisionChat)
**输入：**
- `image`: 图像输入
- `user_prompt`: 用户提示词
- `doubao_api`: API客户端
- `doubao_config`: 模型配置（推荐使用 `doubao-seed-1.6-250615` 等支持视觉的模型或视觉Endpoint ID）
- `system_prompt`: 系统提示词（可选）
- `ignore_errors`: 忽略错误（可选，默认启用）- 启用时API错误将被忽略并返回空字符串而不是抛出异常

**输出：**
- `response`: AI生成的回复文本

## 示例工作流

### 文本对话示例
```
豆包API配置 → 豆包模型配置 → 豆包文本对话 → 输出文本
```

### 图像理解示例
```
图像加载 → 豆包视觉对话 ← 豆包API配置
                ↑
            豆包模型配置（视觉模型）
```

## 参数调优建议

### Temperature（温度）
- `0.0-0.3`: 更确定性的输出，适合事实性问答
- `0.4-0.7`: 平衡创造性和准确性，适合一般对话
- `0.8-1.0`: 更有创造性的输出，适合创意写作
- `1.0+`: 高度随机，适合实验性用途

### Top-p（核采样）
- `0.1-0.5`: 更保守的输出
- `0.6-0.9`: 平衡的输出质量
- `0.9-1.0`: 更多样化的输出

### Max Tokens
- 根据需要的回复长度设置
- 注意API的token限制和计费

## 错误处理

常见错误及解决方案：

1. **API密钥错误**
   - 检查API密钥是否正确
   - 确认环境变量设置

2. **模型不支持视觉**
   - 确保使用视觉理解模型进行图像分析

3. **网络连接问题**
   - 检查网络连接
   - 确认API端点地址

4. **Token限制**
   - 减少输入长度或max_tokens设置

## 故障排除

如果遇到问题（如404错误、认证失败等），请参考详细的 [故障排除指南](TROUBLESHOOTING.md)。

常见问题：
- **404错误**：通常是因为使用了错误的模型ID，建议使用Endpoint ID
- **认证错误**：检查API密钥是否正确设置
- **模型不支持**：确保使用正确的模型类型（文本/视觉）

## 开发和贡献

欢迎提交Issue和Pull Request！

### 开发环境设置
```bash
git clone https://github.com/your-username/comfyui-doubao-llm.git
cd comfyui-doubao-llm
pip install -r requirements.txt
```

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。


---

**注意**: 使用本节点需要有效的火山引擎豆包API密钥。请确保遵守相关的使用条款和隐私政策。