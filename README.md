# ComfyUI Doubao LLM

A ComfyUI custom node for integrating Doubao (ByteDance) large language models, supporting both text and vision understanding capabilities.

## Features

- 🤖 **Text Chat**: Pure text conversation with Doubao models
- 👁️ **Vision Understanding**: Image analysis and description capabilities
- 🔧 **Flexible Configuration**: Support for both Model ID and Endpoint ID calls
- 🎯 **Latest Models**: Support for Doubao 1.6 series, Doubao 1.5 series, and DeepSeek models
- 🔗 **Easy Integration**: Seamless integration with ComfyUI workflow

## Supported Models

### Doubao 1.6 Series (Latest)
- `doubao-seed-1.6-250615` (Recommended, supports vision)
- `doubao-seed-1.6-250615-32k`
- `doubao-seed-1.6-250615-128k`
- `doubao-seed-1.6-250615-256k`

### Doubao 1.5 Series
- `doubao-seed-1.5-250615`
- `doubao-seed-1.5-250615-32k`
- `doubao-seed-1.5-250615-128k`
- `doubao-seed-1.5-250615-256k`

### DeepSeek Series
- `deepseek-chat`
- `deepseek-coder`

### Legacy Models (Compatibility)
- `doubao-pro-4k`, `doubao-pro-32k`, `doubao-pro-128k`, `doubao-pro-256k`
- `doubao-lite-4k`, `doubao-lite-32k`, `doubao-lite-128k`
- `doubao-character-4k`, `doubao-character-32k`

## Quick Start

### 1. Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/your-username/comfyui-doubao-llm.git
cd comfyui-doubao-llm
pip install -r requirements.txt
```

### 2. Get API Credentials

1. Visit [Volcano Engine Console](https://console.volcengine.com/ark/region:ark+cn-beijing/model)
2. Create an API Key
3. (Optional) Create an Endpoint if you want to use Endpoint ID

### 3. Basic Configuration

**Recommended: Using Model ID (Simpler)**
```
API Key: your_api_key_here
Endpoint: https://ark.cn-beijing.volces.com/api/v3/
Model: doubao-seed-1.6-250615
```

**Alternative: Using Endpoint ID**
```
API Key: your_api_key_here
Endpoint: https://ark.cn-beijing.volces.com/api/v3/
Model: ep-20241201-xxxxxx
```

## Node Reference

### DoubaoAPI
Configures API connection settings.

**Inputs:**
- `api_key` (string): Your Doubao API key
- `endpoint` (string): API endpoint URL

### DoubaoConfig
Configures model parameters.

**Inputs:**
- `model` (string): Model ID (e.g., `doubao-seed-1.6-250615`) or Endpoint ID (e.g., `ep-20241201-xxxxxx`)
- `max_tokens` (int): Maximum tokens in response (default: 1024)
- `temperature` (float): Response randomness, 0.0-1.0 (default: 0.7)
- `top_p` (float): Nucleus sampling parameter, 0.0-1.0 (default: 0.9)

### DoubaoTextChat
Text-only conversation node.

**Inputs:**
- `user_prompt` (string): User input text
- `system_prompt` (string, optional): System prompt defining AI behavior
- `ignore_errors` (boolean, optional): When enabled (default), API errors will be ignored and return empty string instead of throwing exceptions
- `doubao_api`: DoubaoAPI configuration
- `doubao_config`: DoubaoConfig settings

**Outputs:**
- `response` (string): AI response text

### DoubaoVisionChat
Vision understanding conversation node.

**Inputs:**
- `image` (IMAGE): Input image for analysis
- `user_prompt` (string): User prompt about the image
- `system_prompt` (string, optional): System prompt for image analysis
- `ignore_errors` (boolean, optional): When enabled (default), API errors will be ignored and return empty string instead of throwing exceptions
- `doubao_api`: DoubaoAPI configuration
- `doubao_config`: DoubaoConfig settings (recommend using vision-capable models like `doubao-seed-1.6-250615` or vision Endpoint ID)

**Outputs:**
- `response` (string): AI analysis of the image

## Detailed Setup Guide

For detailed setup instructions, please refer to [SETUP_GUIDE.md](SETUP_GUIDE.md).

## Model Calling Methods

This plugin supports two calling methods:

### Method 1: Model ID (Recommended)
- **Advantages**: Simple configuration, no need to create Endpoints
- **Usage**: Directly input model ID (e.g., `doubao-seed-1.6-250615`)
- **Requirement**: Ensure the corresponding model service is activated

### Method 2: Endpoint ID
- **Advantages**: More flexible configuration, supports custom parameters
- **Usage**: Input Endpoint ID (e.g., `ep-20241201-xxxxxx`)
- **Requirement**: Need to create inference Endpoint in advance

## Example Workflows

### Text Conversation
1. Add `DoubaoAPI` node and configure API key and endpoint
2. Add `DoubaoConfig` node and set model and parameters
3. Add `DoubaoTextChat` node and connect the above configurations
4. Input user prompt and run

### Image Analysis
1. Load an image using ComfyUI's image loading node
2. Configure `DoubaoAPI` and `DoubaoConfig` nodes (ensure using vision-capable model)
3. Add `DoubaoVisionChat` node and connect image and configurations
4. Input prompt about the image and run

## Troubleshooting

### Common Issues

**404 Error**
- Check if API key is correct
- Verify endpoint URL format
- Ensure model service is activated (for Model ID calls)
- Confirm Endpoint ID exists and is active (for Endpoint ID calls)
- Try using recommended Model ID: `doubao-seed-1.6-250615`

**Vision Model Error**
- Ensure using vision-capable models (e.g., `doubao-seed-1.6-250615`)
- Or use vision-capable Endpoint ID
- Check if image format is supported

**Rate Limiting**
- Check API quota and usage limits
- Consider reducing request frequency

## Requirements

- Python 3.8+
- ComfyUI
- requests
- torch
- Pillow

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Note**: This plugin requires a valid Doubao API key. Please ensure you comply with ByteDance's terms of service when using this plugin.
