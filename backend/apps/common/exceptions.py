import logging

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

logger = logging.getLogger('gocart')


class ServiceError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A service error occurred.'
    default_code = 'service_error'


class PaymentError(APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'Payment processing failed.'
    default_code = 'payment_error'


class InsufficientStockError(ServiceError):
    default_detail = 'Insufficient stock for one or more items.'
    default_code = 'insufficient_stock'


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'success': False,
            'error': response.data,
        }
    else:
        logger.exception('Unhandled exception', exc_info=exc)
    return response
