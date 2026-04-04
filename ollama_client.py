import requests
from typing import Optional


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api"

    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "options": {"num_predict": max_tokens},
        }
        if system:
            payload["system"] = system

        response = requests.post(f"{self.api_url}/generate", json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["response"]

    def is_connected(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self):
        response = requests.get(f"{self.base_url}/api/tags", timeout=5)
        response.raise_for_status()
        return [m["name"] for m in response.json().get("models", [])]


if __name__ == "__main__":
    client = OllamaClient()
    if client.is_connected():
        print("Connected to Ollama!")
        print("Available models:", client.list_models())
    else:
        print("Could not connect to Ollama. Is it running?")
