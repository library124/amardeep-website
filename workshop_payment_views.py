
# Workshop Payment Views
class WorkshopOrderView(APIView):
    """Create order for workshop payment"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            from ..models import Workshop, WorkshopApplication
            
            workshop_id = request.data.get('workshop_id')
            user_name = request.data.get('user_name', 'Guest User')
            user_email = request.data.get('email', 'guest@example.com')
            user_phone = request.data.get('user_phone', '')
            
            # Application data
            experience_level = request.data.get('experience_level', 'beginner')
            motivation = request.data.get('motivation', '')

            if not workshop_id:
                return Response({'error': 'Workshop ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                workshop = Workshop.objects.get(id=workshop_id, is_active=True)
            except Workshop.DoesNotExist:
                return Response({'error': 'Workshop not found'}, status=status.HTTP_404_NOT_FOUND)

            if workshop.is_full:
                return Response({'error': 'Workshop is full'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user already applied
            existing_application = WorkshopApplication.objects.filter(
                workshop=workshop,
                email=user_email
            ).first()
            
            if existing_application:
                return Response({'error': 'You have already applied for this workshop'}, status=status.HTTP_400_BAD_REQUEST)

            # Create workshop application
            application = WorkshopApplication.objects.create(
                workshop=workshop,
                name=user_name,
                email=user_email,
                phone=user_phone,
                experience_level=experience_level,
                motivation=motivation
            )

            if workshop.is_paid:
                # Create order for paid workshop
                order_payload = {
                    "amount": int(workshop.price * 100),
                    "currency": workshop.currency,
                    "receipt": f"workshop_{workshop.id}_{uuid.uuid4().hex[:8]}",
                    "notes": {
                        "workshop_id": str(workshop.id),
                        "workshop_title": workshop.title,
                        "user_name": user_name,
                        "user_email": user_email,
                        "application_id": str(application.id)
                    }
                }

                beeceptor_url = "https://razorpay-mock-api.proxy.beeceptor.com/orders"
                
                try:
                    response = requests.post(beeceptor_url, json=order_payload, timeout=10)
                    response.raise_for_status()
                    order_data = response.json()
                except requests.RequestException as e:
                    logger.error(f"Beeceptor request failed: {e}")
                    order_data = None

                # Create payment record
                payment = Payment.objects.create(
                    payment_id=f"PAY_{uuid.uuid4().hex[:12].upper()}",
                    razorpay_order_id=order_data.get('id') if order_data else f"order_mock_{uuid.uuid4().hex[:12]}",
                    amount=workshop.price,
                    currency=workshop.currency,
                    payment_type='workshop',
                    customer_name=user_name,
                    customer_email=user_email,
                    customer_phone=user_phone,
                    workshop_application=application,
                    gateway_response=order_data or {'mock': True}
                )

                return Response({
                    'order_id': order_data.get('id') if order_data else payment.razorpay_order_id,
                    'amount': order_data.get('amount') if order_data else int(workshop.price * 100),
                    'currency': workshop.currency,
                    'payment_id': payment.payment_id,
                    'item_title': workshop.title,
                    'item_price': workshop.price_display,
                    'item_type': 'workshop',
                    'application_id': application.id,
                    'mock': not bool(order_data)
                })
            else:
                # Free workshop - auto approve
                application.status = 'approved'
                application.save()
                workshop.registered_count += 1
                workshop.save()

                return Response({
                    'message': 'Successfully registered for free workshop',
                    'application_id': application.id,
                    'requires_payment': False
                })

        except Exception as e:
            logger.error(f"Error creating workshop order: {e}")
            return Response({'error': 'Failed to create workshop order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Service Payment Views  
class ServiceOrderView(APIView):
    """Create order for service payment"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            from ..models import TradingService, ServiceBooking
            
            service_id = request.data.get('service_id')
            user_name = request.data.get('user_name', 'Guest User')
            user_email = request.data.get('email', 'guest@example.com')
            user_phone = request.data.get('user_phone', '')
            message = request.data.get('message', '')
            preferred_contact_method = request.data.get('preferred_contact_method', 'whatsapp')
            preferred_time = request.data.get('preferred_time', '')

            if not service_id:
                return Response({'error': 'Service ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                service = TradingService.objects.get(id=service_id, is_active=True)
            except TradingService.DoesNotExist:
                return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

            # Create service booking
            booking = ServiceBooking.objects.create(
                service=service,
                name=user_name,
                email=user_email,
                phone=user_phone,
                message=message,
                preferred_contact_method=preferred_contact_method,
                preferred_time=preferred_time
            )

            # Create order for service payment
            order_payload = {
                "amount": int(service.price * 100),
                "currency": service.currency,
                "receipt": f"service_{service.id}_{uuid.uuid4().hex[:8]}",
                "notes": {
                    "service_id": str(service.id),
                    "service_name": service.name,
                    "user_name": user_name,
                    "user_email": user_email,
                    "booking_id": str(booking.id)
                }
            }

            beeceptor_url = "https://razorpay-mock-api.proxy.beeceptor.com/orders"
            
            try:
                response = requests.post(beeceptor_url, json=order_payload, timeout=10)
                response.raise_for_status()
                order_data = response.json()
            except requests.RequestException as e:
                logger.error(f"Beeceptor request failed: {e}")
                order_data = None

            # Create payment record
            payment = Payment.objects.create(
                payment_id=f"PAY_{uuid.uuid4().hex[:12].upper()}",
                razorpay_order_id=order_data.get('id') if order_data else f"order_mock_{uuid.uuid4().hex[:12]}",
                amount=service.price,
                currency=service.currency,
                payment_type='service',
                customer_name=user_name,
                customer_email=user_email,
                customer_phone=user_phone,
                trading_service=service,
                gateway_response=order_data or {'mock': True}
            )

            return Response({
                'order_id': order_data.get('id') if order_data else payment.razorpay_order_id,
                'amount': order_data.get('amount') if order_data else int(service.price * 100),
                'currency': service.currency,
                'payment_id': payment.payment_id,
                'item_title': service.name,
                'item_price': service.price_display,
                'item_type': 'service',
                'booking_id': booking.id,
                'mock': not bool(order_data)
            })

        except Exception as e:
            logger.error(f"Error creating service order: {e}")
            return Response({'error': 'Failed to create service order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)