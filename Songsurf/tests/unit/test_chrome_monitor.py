"""
Tests pour le ChromeMonitor
"""
import pytest
from core.services.chrome_monitor import ChromeMonitor

class TestChromeMonitor:
    @pytest.fixture
    def monitor(self):
        return ChromeMonitor(port=0)  # Port 0 pour les tests

    def test_initialization(self, monitor):
        assert monitor.port == 0
        assert monitor._running is False

    def test_start_service(self, monitor):
        assert monitor.start() is True
        assert monitor._running is True

    def test_callbacks_registration(self, monitor):
        def dummy_callback(data):
            pass
            
        monitor.register_callback('on_detection', dummy_callback)
        assert monitor._callbacks['on_detection'] == dummy_callback
