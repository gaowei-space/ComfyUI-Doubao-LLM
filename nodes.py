import os
import json
import base64
import requests
from io import BytesIO
from PIL import Image
import torch
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from enum import Enum

# Doubao LLM supported model list (based on latest API documentation)
doubao_models = [
    # Latest Doubao 1.6 series models (recommended)
    "doubao-seed-1.6-250615",
    "doubao-seed-1.6-flash-250615",
    "doubao-seed-1.6-thinking-250615",
    # Doubao 1.5 series models
    "doubao-1.5-thinking-vision-pro-250428",
    "doubao-1.5-thinking-pro-250415",
    "doubao-1.5-thinking-pro-m-250428",
    "doubao-1.5-vision-pro-250328",
    "doubao-1.5-pro-32k",
    "doubao-1.5-pro-256k",
    "doubao-1.5-lite-32k",
    # DeepSeek models
    "deepseek-r1-250528",
    "deepseek-r1-250120",
    "deepseek-r1-distill-qwen-32b-250120",
    "deepseek-r1-distill-qwen-7b-250120",
]

# Models that support vision understanding
doubao_vision_models = [
    # Latest Doubao 1.6 series vision models (recommended)
    "doubao-seed-1.6-250615",
    "doubao-seed-1.6-flash-250615",
    "doubao-seed-1.6-thinking-250615",
    # Doubao 1.5 series vision models
    "doubao-1.5-thinking-vision-pro-250428",
    "doubao-1.5-thinking-pro-m-250428",
    "doubao-1.5-vision-pro-250328",
    "doubao-1.5-vision-pro-32k",
]


class DoubaoConfig(BaseModel):
    """Doubao LLM configuration"""

    model: str = (
        "doubao-seed-1.6-flash-250615"  # Default to latest Doubao 1.6 model, can also use Endpoint ID
    )
    max_tokens: int = 1000
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = False


class MessageRole(str, Enum):
    """Message role enumeration"""

    system = "system"
    user = "user"
    assistant = "assistant"


class DoubaoMessage(BaseModel):
    """Doubao message format"""

    role: MessageRole
    content: List[Dict[str, Any]]

    @classmethod
    def create_text_message(cls, role: MessageRole, text: str):
        """Create text-only message"""
        return cls(role=role, content=[{"type": "text", "text": text}])

    @classmethod
    def create_multimodal_message(cls, role: MessageRole, text: str, image_base64: str):
        """Create multimodal message (text + image)"""
        return cls(
            role=role,
            content=[
                {"type": "text", "text": text},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                },
            ],
        )


class DoubaoAPI:
    """Doubao LLM API client"""

    def __init__(
        self,
        api_key: str = None,
        endpoint: str = "https://ark.cn-beijing.volces.com/api/v3",
    ):
        # API key priority: parameter > environment variable
        self.api_key = api_key or os.getenv("DOUBAO_API_KEY")
        self.endpoint = endpoint
        self.timeout = 60

        if not self.api_key:
            raise ValueError(
                "API key not set. Please set DOUBAO_API_KEY environment variable or provide api_key parameter during initialization"
            )

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat_completions(
        self, messages: List[DoubaoMessage], config: DoubaoConfig
    ) -> str:
        """Call Doubao chat completion API"""
        # Validate model format: supports Endpoint ID or Model ID
        model = config.model.strip()
        if not model:
            raise ValueError("Model cannot be empty")

        url = f"{self.endpoint}/chat/completions"

        # Build request data
        data = {
            "model": config.model,
            "messages": [msg.dict() for msg in messages],
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "stream": config.stream,
        }

        try:
            response = requests.post(
                url, json=data, headers=self._get_headers(), timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()

            if "error" in result:
                raise Exception(f"API Error: {result['error']['message']}")

            if "choices" not in result or len(result["choices"]) == 0:
                raise Exception("No response generated")

            return result["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse response: {str(e)}")
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")


def tensor_to_base64(tensor: torch.Tensor) -> str:
    """Convert ComfyUI image tensor to base64 encoding"""
    # Ensure tensor is on CPU
    if tensor.device != torch.device("cpu"):
        tensor = tensor.cpu()

    # Convert to numpy array and adjust dimension order
    # ComfyUI tensor format: [batch, height, width, channels]
    # Take the first image
    if len(tensor.shape) == 4:
        tensor = tensor[0]

    # Convert to PIL Image
    # Ensure value range is 0-255
    if tensor.max() <= 1.0:
        tensor = tensor * 255

    tensor = tensor.clamp(0, 255).byte()

    # Convert to PIL Image
    pil_image = Image.fromarray(tensor.numpy(), mode="RGB")

    # Convert to base64
    buffer = BytesIO()
    pil_image.save(buffer, format="JPEG", quality=95)
    img_bytes = buffer.getvalue()

    return base64.b64encode(img_bytes).decode("utf-8")


class DoubaoAPINode:
    """Doubao API configuration node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "",
                        "tooltip": "Doubao LLM API key",
                    },
                ),
                "endpoint": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "https://ark.cn-beijing.volces.com/api/v3",
                        "tooltip": "API endpoint URL",
                    },
                ),
            },
        }

    RETURN_TYPES = ("DOUBAO_API",)
    RETURN_NAMES = ("doubao_api",)
    FUNCTION = "create_api"
    CATEGORY = "Doubao LLM"

    def create_api(self, api_key: str, endpoint: str):
        # If no API key is provided, try to get it from environment variable
        if not api_key or api_key.strip() == "":
            api_key = os.environ.get("DOUBAO_API_KEY")

        if not api_key:
            raise Exception(
                "Doubao API key is required. Please provide API key or set DOUBAO_API_KEY environment variable."
            )

        return (DoubaoAPI(api_key=api_key, endpoint=endpoint),)


class DoubaoConfigNode:
    """Doubao model configuration node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "doubao-seed-1.6-250615",
                        "tooltip": "Enter Model ID or inference endpoint's Endpoint ID. Recommended to use latest doubao-seed-1.6-250615 model, or create inference endpoint to use Endpoint ID (format: ep-xxxxxxxxxx-xxxxx)",
                    },
                ),
                "max_tokens": (
                    "INT",
                    {
                        "default": 1000,
                        "min": 1,
                        "max": 4000,
                        "step": 1,
                        "tooltip": "Maximum number of output tokens",
                    },
                ),
                "temperature": (
                    "FLOAT",
                    {
                        "default": 0.7,
                        "min": 0.0,
                        "max": 2.0,
                        "step": 0.01,
                        "tooltip": "Controls output randomness, higher values are more random",
                    },
                ),
                "top_p": (
                    "FLOAT",
                    {
                        "default": 0.9,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.01,
                        "tooltip": "Nucleus sampling parameter, controls output diversity",
                    },
                ),
            }
        }

    RETURN_TYPES = ("DOUBAO_CONFIG",)
    RETURN_NAMES = ("doubao_config",)
    FUNCTION = "create_config"
    CATEGORY = "Doubao LLM"

    def create_config(
        self, model: str, max_tokens: int, temperature: float, top_p: float
    ):
        return (
            DoubaoConfig(
                model=model, max_tokens=max_tokens, temperature=temperature, top_p=top_p
            ),
        )


class DoubaoTextChatNode:
    """Doubao text-only chat node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "user_prompt": (
                    "STRING",
                    {"multiline": True, "default": "", "tooltip": "User input prompt"},
                ),
                "doubao_api": ("DOUBAO_API",),
                "doubao_config": ("DOUBAO_CONFIG",),
            },
            "optional": {
                "system_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "You are a helpful AI assistant.",
                        "tooltip": "System prompt that defines AI's role and behavior",
                    },
                ),
                "ignore_errors": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "When enabled, API errors (timeout, network issues, etc.) will be ignored and return empty string instead of throwing exceptions",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "chat"
    CATEGORY = "Doubao LLM"

    def chat(
        self,
        user_prompt: str,
        doubao_api: DoubaoAPI,
        doubao_config: DoubaoConfig,
        system_prompt: str = "",
        ignore_errors: bool = True,
    ):
        messages = []

        # Add system prompt (if provided)
        if system_prompt and system_prompt.strip():
            messages.append(
                DoubaoMessage.create_text_message(
                    MessageRole.system, system_prompt.strip()
                )
            )

        # Add user prompt
        messages.append(
            DoubaoMessage.create_text_message(MessageRole.user, user_prompt)
        )

        # Call API with error handling
        try:
            response = doubao_api.chat_completions(messages, doubao_config)
            return (response,)
        except Exception as e:
            if ignore_errors:
                print(f"Doubao API error (ignored): {str(e)}")
                return ("",)
            else:
                raise e


class DoubaoVisionChatNode:
    """Doubao vision understanding chat node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "user_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "Please describe this image.",
                        "tooltip": "User input prompt",
                    },
                ),
                "doubao_api": ("DOUBAO_API",),
                "doubao_config": ("DOUBAO_CONFIG",),
            },
            "optional": {
                "system_prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "You are a professional image analysis AI assistant that can describe and analyze image content in detail.",
                        "tooltip": "System prompt that defines AI's role and behavior",
                    },
                ),
                "ignore_errors": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "When enabled, API errors (timeout, network issues, etc.) will be ignored and return empty string instead of throwing exceptions",
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "vision_chat"
    CATEGORY = "Doubao LLM"

    def vision_chat(
        self,
        image: torch.Tensor,
        user_prompt: str,
        doubao_api: DoubaoAPI,
        doubao_config: DoubaoConfig,
        system_prompt: str = "",
        ignore_errors: bool = True,
    ):
        try:
            messages = []

            # Add system prompt (if provided)
            if system_prompt and system_prompt.strip():
                messages.append(
                    DoubaoMessage.create_text_message(
                        MessageRole.system, system_prompt.strip()
                    )
                )

            # Convert image to base64
            image_base64 = tensor_to_base64(image)

            # Add user message (containing image and text)
            messages.append(
                DoubaoMessage.create_multimodal_message(
                    MessageRole.user, user_prompt, image_base64
                )
            )

            # Call API
            response = doubao_api.chat_completions(messages, doubao_config)
            return (response,)
        except Exception as e:
            if ignore_errors:
                print(f"Doubao Vision API error (ignored): {str(e)}")
                return ("",)
            else:
                raise e


# Node mappings
NODE_CLASS_MAPPINGS = {
    "DoubaoAPI": DoubaoAPINode,
    "DoubaoConfig": DoubaoConfigNode,
    "DoubaoTextChat": DoubaoTextChatNode,
    "DoubaoVisionChat": DoubaoVisionChatNode,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "DoubaoAPI": "Doubao API",
    "DoubaoConfig": "Doubao Config",
    "DoubaoTextChat": "Doubao Text Chat",
    "DoubaoVisionChat": "Doubao Vision Chat",
}
