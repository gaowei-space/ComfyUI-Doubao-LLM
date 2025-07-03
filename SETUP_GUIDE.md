# 豆包大模型节点设置指南

本指南将帮助您正确设置豆包大模型节点，避免404错误等常见问题。

## 重要说明

🔄 **重要更新：现在同时支持Model ID和Endpoint ID调用** 🔄

豆包API现在支持两种调用方式：
1. **直接使用Model ID**（推荐）：如 `doubao-seed-1.6-250615`
2. **使用Endpoint ID**：如 `ep-xxxxxxxxxx-xxxxx`（提供更多高级功能）

推荐优先使用Model ID，更简单快捷。如需高级功能或专属资源，可选择创建Endpoint ID。

## 第一步：获取API密钥

1. 访问 [火山方舟控制台](https://console.volcengine.com/ark)
2. 注册并登录您的火山引擎账号
3. 在左侧导航栏找到「API Key管理」
4. 点击「创建API Key」
5. 复制生成的API Key并妥善保存

## 第二步：开通模型服务

1. 在火山方舟控制台，点击左侧导航栏的「开通管理」
2. 找到您需要的豆包模型，例如：
   - **文本模型**：`doubao-1.5-pro-32k`、`doubao-1.5-lite-32k`
   - **视觉模型**：`doubao-1.5-vision-pro`、`doubao-1.5-vision-lite`
3. 点击对应模型的「开通服务」按钮
4. 根据提示完成开通流程

## 第三步：创建推理接入点（可选，如需使用Endpoint ID）

### 3.1 进入推理接入点管理

1. 在火山方舟控制台，点击左侧导航栏的「在线推理」
2. 选择「自定义推理接入点」页签
3. 点击「创建推理接入点」按钮

### 3.2 配置推理接入点

1. **基本信息**
   - 接入点名称：自定义名称（如：我的豆包文本模型）
   - 描述：可选

2. **模型选择**
   - 接入来源：选择「火山方舟」
   - 选择模型：从「模型广场」中选择已开通的模型
   - 模型版本：选择最新版本

3. **购买方式**
   - 推荐选择「按Token付费」（按使用量计费）
   - 如有高流量需求，可考虑「TPM保障包」

4. **其他配置**
   - 接入点限流：根据需要设置（可使用默认值）
   - 数据投递：可选配置

5. **确认创建**
   - 阅读并勾选相关协议
   - 点击「确认接入」

### 3.3 获取Endpoint ID

1. 创建成功后，在「在线推理」页面可以看到新创建的接入点
2. 找到您的接入点，复制其「Endpoint ID」
3. Endpoint ID格式类似：`ep-20241201123456-abcde`

## 第四步：配置ComfyUI节点

### 4.1 设置环境变量（推荐）

**macOS/Linux:**
```bash
export DOUBAO_API_KEY="your-api-key-here"
```

**Windows (CMD):**
```cmd
set DOUBAO_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:DOUBAO_API_KEY = "your-api-key-here"
```

### 4.2 在ComfyUI中使用

1. 重启ComfyUI
2. 在节点菜单中找到「Doubao LLM」分类
3. 添加以下节点到工作流：
   - `DoubaoAPI`：配置API密钥
   - `DoubaoConfig`：配置模型参数
   - `DoubaoTextChat` 或 `DoubaoVisionChat`：执行对话

4. **重要：在DoubaoConfig节点中**
   - **方式一（推荐）**：在「model」字段中输入Model ID
     - 例如：`doubao-seed-1.6-250615`
   - **方式二**：在「model」字段中输入您的Endpoint ID
     - 例如：`ep-20241201123456-abcde`

## 第五步：测试配置

1. 连接节点：DoubaoAPI → DoubaoConfig → DoubaoTextChat
2. 在DoubaoTextChat节点中输入测试文本："你好"
3. 执行工作流
4. 如果配置正确，应该能收到模型的回复

## 常见问题解决

### Q1: 仍然出现404错误

**可能原因：**
- 使用了无效的模型ID或Endpoint ID
- Endpoint ID格式错误或状态异常
- 模型服务未开通

**解决方案：**
1. **使用Model ID时**：确认模型ID正确（如 `doubao-seed-1.6-250615`）
2. **使用Endpoint ID时**：确认格式正确（以`ep-`开头）并检查接入点状态
3. 确认已开通对应的模型服务
4. 尝试使用推荐的最新模型ID

### Q2: 认证错误

**可能原因：**
- API密钥错误或过期
- 环境变量未正确设置

**解决方案：**
1. 重新生成API密钥
2. 确认环境变量设置正确
3. 重启ComfyUI

### Q3: 模型不支持视觉理解

**解决方案：**
- 确保为视觉任务创建了视觉模型的推理接入点
- 使用`DoubaoVisionChat`节点而不是`DoubaoTextChat`