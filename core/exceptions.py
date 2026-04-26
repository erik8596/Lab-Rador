"""Custom exceptions for Lab-Rador."""


class LabRadorError(Exception):
    """Base exception for Lab-Rador."""

    pass


class ConfigurationError(LabRadorError):
    """Configuration-related errors."""

    pass


class ValidationError(LabRadorError):
    """Protocol validation errors."""

    pass


class ProtocolGenerationError(LabRadorError):
    """Errors during protocol generation."""

    pass


class APIError(LabRadorError):
    """External API errors."""

    def __init__(
        self, message: str, status_code: int = None, response_data: dict = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AnthropicAPIError(APIError):
    """Anthropic Claude API errors."""

    pass


class GeminiAPIError(APIError):
    """Google Gemini API errors."""

    pass


class AnthropicAPIError(APIError):
    """Anthropic/Claude API specific errors."""

    pass


class ProtocolsIOError(APIError):
    """protocols.io API specific errors."""

    pass


class ParsingError(LabRadorError):
    """Data parsing and serialization errors."""

    pass


class FileIOError(LabRadorError):
    """File input/output errors."""

    pass


class GeneratorError(LabRadorError):
    """Code generation errors."""

    pass


class OpentronsGeneratorError(GeneratorError):
    """Opentrons script generation errors."""

    pass


class MarkdownGeneratorError(GeneratorError):
    """Markdown generation errors."""

    pass


class AgentError(LabRadorError):
    """AI agent errors."""

    pass


class ProtocolAgentError(AgentError):
    """Protocol generation agent errors."""

    pass


class RefinementError(AgentError):
    """Protocol refinement errors."""

    pass
