"""
Payment service exceptions following SOLID principles
"""


class PaymentException(Exception):
    """Base payment exception"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class PaymentValidationError(PaymentException):
    """Payment validation error"""
    pass


class PaymentGatewayError(PaymentException):
    """Payment gateway error"""
    pass


class PaymentNotFoundError(PaymentException):
    """Payment not found error"""
    pass


class PaymentAlreadyProcessedError(PaymentException):
    """Payment already processed error"""
    pass


class ItemNotFoundError(PaymentException):
    """Item not found error"""
    pass


class ItemNotAvailableError(PaymentException):
    """Item not available error"""
    pass


class PaymentVerificationError(PaymentException):
    """Payment verification error"""
    pass


class PaymentProcessingError(PaymentException):
    """General payment processing error"""
    pass