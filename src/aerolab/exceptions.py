class AeroLabError(Exception):
    """Base exception for expected AeroLab failures."""


class DataValidationError(AeroLabError):
    """Raised when input data violates the documented schema."""


class AnalysisError(AeroLabError):
    """Raised when an analysis cannot be computed from the supplied data."""
