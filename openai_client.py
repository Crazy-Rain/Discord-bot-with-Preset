"""OpenAI-compatible API client."""
from openai import OpenAI
from typing import Dict, Any, List, Optional

class OpenAIClient:
    def __init__(self, api_key: str, base_url: str, model: str = "gpt-3.5-turbo"):
        # Store the API key even if it's a placeholder
        # This allows the bot to start and be configured via web interface
        self.api_key = api_key or "none"
        self.model = model
        
        # Only create the client if we have a valid API key
        # Otherwise, defer client creation until a valid key is provided
        if self.api_key and self.api_key not in ["YOUR_API_KEY", "", "none"]:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        else:
            # Create a dummy client - will be replaced when config is updated
            self.client = OpenAI(
                api_key="none",  # Placeholder to prevent errors
                base_url=base_url
            )
    
    def update_config(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        """Update client configuration."""
        if api_key:
            # Validate API key is not a placeholder
            if api_key in ["YOUR_API_KEY", "", "none"]:
                raise ValueError(
                    "API key is not configured. Please set a valid API key in the configuration."
                )
            self.client.api_key = api_key
            self.api_key = api_key
        if base_url:
            self.client.base_url = base_url
        if model:
            self.model = model
    
    def list_models(self) -> List[str]:
        """
        Fetch available models from the OpenAI-compatible API.
        
        Returns:
            List of available model names
        """
        # Check if API key is configured
        if not self.api_key or self.api_key in ["YOUR_API_KEY", "", "none"]:
            raise ValueError(
                "API key is not configured. Please set a valid API key in the configuration."
            )
        
        try:
            models_response = self.client.models.list()
            return [model.id for model in models_response.data]
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg:
                raise Exception(
                    f"API authentication failed. Please verify your API key is correct. "
                    f"Original error: {error_msg}"
                )
            raise Exception(f"Error fetching models from API: {error_msg}")
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        frequency_penalty_enabled: bool = True,
        presence_penalty_enabled: bool = True
    ) -> str:
        """
        Generate chat completion using OpenAI-compatible API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
            frequency_penalty: Frequency penalty
            presence_penalty: Presence penalty
            frequency_penalty_enabled: Whether to include frequency penalty in request
            presence_penalty_enabled: Whether to include presence penalty in request
        
        Returns:
            Generated text response
        """
        # Check if API key is configured
        if not self.api_key or self.api_key in ["YOUR_API_KEY", "", "none"]:
            raise ValueError(
                "API key is not configured. Please set a valid API key in the configuration. "
                "You can configure it via the web interface at http://localhost:5000 or by editing config.json"
            )
        
        try:
            # Build request parameters
            request_params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
            
            # Only include penalties if they are enabled
            if frequency_penalty_enabled:
                request_params["frequency_penalty"] = frequency_penalty
            if presence_penalty_enabled:
                request_params["presence_penalty"] = presence_penalty
            
            response = self.client.chat.completions.create(**request_params)
            
            # Safely access response choices with validation
            if not hasattr(response, 'choices') or not response.choices:
                raise Exception(
                    "API returned an invalid response structure (missing 'choices'). "
                    "This may indicate a proxy or API configuration issue. "
                    "Please check your API endpoint and model settings."
                )
            
            if not hasattr(response.choices[0], 'message') or not hasattr(response.choices[0].message, 'content'):
                raise Exception(
                    "API returned an invalid response structure (missing message content). "
                    "This may indicate a proxy or API configuration issue. "
                    "Please check your API endpoint and model settings."
                )
            
            return response.choices[0].message.content
        except Exception as e:
            # Provide more helpful error message for API key issues
            error_msg = str(e)
            # Check for authentication/token errors with broader pattern matching
            if any(pattern in error_msg.lower() for pattern in [
                "401", "invalid_api_key", "incorrect api key", "invalid api key", "invalid token", 
                "invalid_request_error", "authentication", "unauthorized"
            ]):
                raise Exception(
                    f"API authentication failed. Please verify your API key/token is correct. "
                    f"You can update it via the web interface at http://localhost:5000. "
                    f"Note: If using a proxy (like anas-proxy.xyz), ensure:\n"
                    f"1. Your API key/token is valid for that specific proxy\n"
                    f"2. The proxy URL is correct (should end with /v1)\n"
                    f"3. The proxy service is currently accessible\n"
                    f"Original error: {error_msg}"
                )
            # Provide helpful message for context length/token limit errors
            elif any(pattern in error_msg.lower() for pattern in [
                "context_length_exceeded", "maximum context length", "context window",
                "too many tokens", "token limit", "reduce the length"
            ]):
                raise Exception(
                    f"Message too long - exceeded context window limit. "
                    f"The combined length of your message, conversation history, and system prompts exceeded the model's token limit. "
                    f"Please try:\n"
                    f"1. Sending a shorter message\n"
                    f"2. Using !clear to clear conversation history\n"
                    f"3. Reducing the auto context limit with !setcontext (current messages loaded from history)\n"
                    f"Original error: {error_msg}"
                )
            # Provide helpful message for Google AI proxy errors (specific pattern)
            elif "googleAIBlockingResponseHandler" in error_msg or "Cannot read properties of undefined" in error_msg:
                raise Exception(
                    f"Google AI proxy error - likely content filtering or response parsing issue. "
                    f"This often happens when:\n"
                    f"1. Your message contains content that triggers safety filters\n"
                    f"2. The message format (e.g., with newlines or special characters) causes parsing issues\n"
                    f"3. The proxy cannot parse the API response correctly\n"
                    f"Try:\n"
                    f"- Rewording your message\n"
                    f"- Removing extra line breaks or special formatting\n"
                    f"- Using a different API endpoint/proxy if available\n"
                    f"Original error: {error_msg}"
                )
            # Provide helpful message for server errors
            elif "500" in error_msg or "Internal server error" in error_msg:
                raise Exception(
                    f"API server error (500). This is typically a problem with the API provider or proxy. "
                    f"Possible causes:\n"
                    f"1. Your API endpoint is not accessible or incorrect\n"
                    f"2. The model name is invalid for your API provider\n"
                    f"3. Your proxy (if using one) has a configuration issue\n"
                    f"4. Your message may be too long (try a shorter message or use !clear to reset history)\n"
                    f"5. Content filtering - your message may contain blocked content (try rewording)\n"
                    f"Original error: {error_msg}"
                )
            raise Exception(f"Error calling OpenAI-compatible API: {error_msg}")
