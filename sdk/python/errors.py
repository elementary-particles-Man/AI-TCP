class AICTPError(Exception):
    """Base exception for AI-TCP SDK errors."""
    def __init__(self, message, transaction_id=None):
        super().__init__(message)
        self.transaction_id = transaction_id

class AuthenticationError(AICTPError):
    """Raised when authentication fails."""
    pass

class TimeoutError(AICTPError):
    """Raised when a network operation times out."""
    pass

class ProtocolError(AICTPError):
    """Raised when there's an issue with the AI-TCP protocol."""
    pass

class KAIROError(AICTPError):
    """Raised when an error occurs within the KAIRO library."""
    pass
