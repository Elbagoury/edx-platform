"""Tests of commerce utilities."""
from django.test import TestCase
from mock import patch

from commerce.utils import audit_log, EcommerceService
from commerce.models import CommerceConfiguration


class AuditLogTests(TestCase):
    """Tests of the commerce audit logging helper."""
    @patch('commerce.utils.log')
    def test_log_message(self, mock_log):
        """Verify that log messages are constructed correctly."""
        audit_log('foo', qux='quux', bar='baz')

        # Verify that the logged message contains comma-separated
        # key-value pairs ordered alphabetically by key.
        message = 'foo: bar="baz", qux="quux"'
        self.assertTrue(mock_log.info.called_with(message))


class EcommerceServiceTests(TestCase):
    """Tests for the EcommerceService helper class."""

    def setUp(self):
        CommerceConfiguration.objects.create(
            checkout_on_ecommerce_service=True,
            single_course_checkout_page='/test_basket/'
        )
        super(EcommerceServiceTests, self).setUp()

    def test_is_enabled(self):
        """Verify that is_enabled() returns True."""
        is_enabled = EcommerceService().is_enabled()
        self.assertTrue(is_enabled)

    def test_is_enabled_for_microsites(self):
        """Verify that is_enabled() returns false in case of a microsite."""
        patcher = patch('microsite_configuration.microsite.is_request_in_microsite')
        patcher.start()
        is_enabled = EcommerceService().is_enabled()
        self.assertFalse(is_enabled)
        patcher.stop()

    @patch('django.conf.settings.ECOMMERCE_PUBLIC_URL_ROOT', 'http://ecommerce_url')
    def test_payment_page_url(self):
        """Verify that the proper url is returned."""
        url = EcommerceService().payment_page_url()
        self.assertEqual(url, 'http://ecommerce_url/test_basket/')
