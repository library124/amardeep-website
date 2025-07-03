"""
Tests for SOLID-compliant payment services
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal

from .interfaces import PaymentRequest, PaymentCompletionRequest, PaymentType, PaymentStatus
from .gateways import BeeceptorPaymentGateway, PaymentGatewayFactory
from .repositories import PaymentRepository, ItemRepository
from .validators import PaymentValidationService
from .processors import PaymentProcessor
from .handlers import CoursePaymentHandler, WorkshopPaymentHandler, ServicePaymentHandler
from .service import PaymentService


class TestPaymentInterfaces(unittest.TestCase):
    """Test payment interfaces and data structures"""
    
    def test_payment_request_creation(self):
        """Test PaymentRequest data structure"""
        request = PaymentRequest(
            item_id="123",
            item_type=PaymentType.COURSE,
            amount=100.0,
            currency="INR",
            customer_email="test@example.com"
        )
        
        self.assertEqual(request.item_id, "123")
        self.assertEqual(request.item_type, PaymentType.COURSE)
        self.assertEqual(request.amount, 100.0)
        self.assertEqual(request.currency, "INR")
        self.assertEqual(request.customer_email, "test@example.com")
    
    def test_payment_completion_request(self):
        """Test PaymentCompletionRequest data structure"""
        request = PaymentCompletionRequest(
            payment_id="PAY_123",
            gateway_payment_id="pay_456",
            gateway_order_id="order_789",
            gateway_signature="signature_abc"
        )
        
        self.assertEqual(request.payment_id, "PAY_123")
        self.assertEqual(request.gateway_payment_id, "pay_456")


class TestPaymentGateways(unittest.TestCase):
    """Test payment gateway implementations"""
    
    def setUp(self):
        self.gateway = BeeceptorPaymentGateway()
        self.payment_request = PaymentRequest(
            item_id="123",
            item_type=PaymentType.COURSE,
            amount=100.0,
            currency="INR",
            customer_email="test@example.com"
        )
    
    @patch('requests.post')
    def test_beeceptor_gateway_success(self, mock_post):
        """Test successful order creation with Beeceptor"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "order_123", "amount": 10000}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        order_data, error = self.gateway.create_order(self.payment_request)
        
        self.assertIsNotNone(order_data)
        self.assertIsNone(error)
        self.assertEqual(order_data["id"], "order_123")
    
    @patch('requests.post')
    def test_beeceptor_gateway_failure(self, mock_post):
        """Test failed order creation with Beeceptor"""
        mock_post.side_effect = Exception("Network error")
        
        order_data, error = self.gateway.create_order(self.payment_request)
        
        self.assertIsNone(order_data)
        self.assertIsNotNone(error)
    
    def test_payment_gateway_factory(self):
        """Test payment gateway factory"""
        gateway = PaymentGatewayFactory.create_gateway("beeceptor")
        self.assertIsInstance(gateway, BeeceptorPaymentGateway)


class TestPaymentValidation(unittest.TestCase):
    """Test payment validation services"""
    
    def setUp(self):
        self.mock_item_repository = Mock()
        self.validator = PaymentValidationService(self.mock_item_repository)
    
    def test_valid_payment_request(self):
        """Test validation of valid payment request"""
        request = PaymentRequest(
            item_id="123",
            item_type=PaymentType.COURSE,
            amount=100.0,
            currency="INR",
            customer_email="test@example.com"
        )
        
        is_valid, error = self.validator.validate_payment_request(request)
        
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_invalid_email(self):
        """Test validation with invalid email"""
        request = PaymentRequest(
            item_id="123",
            item_type=PaymentType.COURSE,
            amount=100.0,
            currency="INR",
            customer_email="invalid-email"
        )
        
        is_valid, error = self.validator.validate_payment_request(request)
        
        self.assertFalse(is_valid)
        self.assertIn("Invalid email", error)
    
    def test_zero_amount(self):
        """Test validation with zero amount"""
        request = PaymentRequest(
            item_id="123",
            item_type=PaymentType.COURSE,
            amount=0.0,
            currency="INR",
            customer_email="test@example.com"
        )
        
        is_valid, error = self.validator.validate_payment_request(request)
        
        self.assertFalse(is_valid)
        self.assertIn("Amount must be greater than zero", error)


class TestPaymentProcessor(unittest.TestCase):
    """Test payment processor"""
    
    def setUp(self):
        self.mock_gateway = Mock()
        self.mock_payment_repo = Mock()
        self.mock_item_repo = Mock()
        self.mock_validator = Mock()
        
        self.processor = PaymentProcessor(
            self.mock_gateway,
            self.mock_payment_repo,
            self.mock_item_repo,
            self.mock_validator
        )
    
    def test_successful_payment_processing(self):
        """Test successful payment processing"""
        # Setup mocks
        self.mock_validator.validate_payment_request.return_value = (True, None)
        self.mock_validator.validate_item_availability.return_value = (True, None)
        
        mock_item = Mock()
        mock_item.title = "Test Course"
        mock_item.price_display = "INR 100"
        self.mock_item_repo.get_item_by_id.return_value = mock_item
        
        self.mock_gateway.create_order.return_value = ({"id": "order_123"}, None)
        
        mock_payment = Mock()
        mock_payment.payment_id = "PAY_123"
        mock_payment.razorpay_order_id = "order_123"
        self.mock_payment_repo.create_payment_record.return_value = mock_payment
        
        # Test
        request = PaymentRequest(
            item_id="123",
            item_type=PaymentType.COURSE,
            amount=100.0,
            currency="INR",
            customer_email="test@example.com"
        )
        
        response = self.processor.process_payment_request(request)
        
        self.assertTrue(response.success)
        self.assertEqual(response.payment_id, "PAY_123")


class TestPaymentHandlers(unittest.TestCase):
    """Test payment handlers"""
    
    def setUp(self):
        self.mock_notification_service = Mock()
    
    @patch('portfolio_app.services.payment.handlers.PurchasedCourse')
    def test_course_payment_handler(self, mock_purchased_course):
        """Test course payment handler"""
        handler = CoursePaymentHandler(self.mock_notification_service)
        
        mock_payment = Mock()
        mock_payment.payment_id = "PAY_123"
        mock_payment.customer_email = "test@example.com"
        mock_payment.amount = Decimal('100.00')
        mock_payment.currency = "INR"
        mock_payment.gateway_response = {"user_id": 1}
        
        mock_course = Mock()
        mock_course.title = "Test Course"
        mock_course.short_description = "Test Description"
        mock_course.enrolled_count = 0
        
        handler.handle_successful_payment(mock_payment, mock_course, PaymentType.COURSE)
        
        # Verify notifications were sent
        self.mock_notification_service.send_payment_confirmation.assert_called_once()
        self.mock_notification_service.send_enrollment_notification.assert_called_once()
        
        # Verify course enrollment count was incremented
        self.assertEqual(mock_course.enrolled_count, 1)


class TestPaymentService(unittest.TestCase):
    """Test main payment service facade"""
    
    @patch('portfolio_app.services.payment.service.PaymentProcessor')
    @patch('portfolio_app.services.payment.service.PaymentValidationService')
    @patch('portfolio_app.services.payment.service.ItemRepository')
    @patch('portfolio_app.services.payment.service.PaymentRepository')
    @patch('portfolio_app.services.payment.service.PaymentGatewayFactory')
    def test_payment_service_initialization(self, mock_gateway_factory, mock_payment_repo,
                                          mock_item_repo, mock_validator, mock_processor):
        """Test payment service initialization"""
        service = PaymentService()
        
        # Verify all dependencies were initialized
        mock_gateway_factory.create_gateway.assert_called_once_with("beeceptor")
        mock_payment_repo.assert_called_once()
        mock_item_repo.assert_called_once()
        mock_validator.assert_called_once()
        mock_processor.assert_called_once()
    
    def test_create_course_order_convenience_method(self):
        """Test convenience method for course orders"""
        with patch.object(PaymentService, '__init__', lambda x: None):
            service = PaymentService()
            service.item_repository = Mock()
            service.processor = Mock()
            
            mock_course = Mock()
            mock_course.price = Decimal('100.00')
            mock_course.currency = "INR"
            service.item_repository.get_item_by_id.return_value = mock_course
            
            mock_user = Mock()
            mock_user.get_full_name.return_value = "Test User"
            mock_user.email = "test@example.com"
            mock_user.id = 1
            
            service.processor.process_payment_request.return_value = Mock(success=True)
            
            response = service.create_course_order("123", mock_user)
            
            # Verify processor was called
            service.processor.process_payment_request.assert_called_once()


if __name__ == '__main__':
    unittest.main()