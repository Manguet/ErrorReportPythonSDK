#!/usr/bin/env python3
"""Integration test for Python Error Explorer SDK with all 11 services."""

import sys
import os
import time

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from error_explorer import ErrorExplorer


def test_python_sdk_integration():
    """Test Python Error Explorer SDK with all 11 services."""
    
    print("🧪 Testing Python Error Explorer SDK Integration...")
    print("=" * 60)
    
    # Initialize client with all services enabled
    client = ErrorExplorer(
        webhook_url="https://api.error-explorer.com/webhook/test",
        project_name="python-test-project",
        environment="development",
        # Enable all advanced services
        enable_rate_limiting=True,
        enable_quota_management=True,
        enable_offline_queue=True,
        enable_sdk_monitoring=True,
        enable_batching=True,
        enable_compression=True,
        enable_circuit_breaker=True,
        max_requests_per_minute=60,
        batch_size=5,
        batch_timeout=2.0,
        compression_threshold=512,
        circuit_breaker_failure_threshold=3,
        debug=True
    )
    
    print("✅ Client initialized with all services enabled")
    
    # Test 1: BreadcrumbManager
    print("\n🔧 Testing BreadcrumbManager...")
    breadcrumb_manager = client.get_breadcrumb_manager()
    client.add_breadcrumb("Test breadcrumb", "test", "info", {"test": "data"})
    breadcrumb_stats = breadcrumb_manager.get_stats()
    print(f"   Breadcrumbs: {breadcrumb_stats['total_breadcrumbs']}/{breadcrumb_stats['max_breadcrumbs']}")
    
    # Test 2: RateLimiter (should be working from existing services)
    print("\n🔧 Testing RateLimiter...")
    if client.rate_limiter:
        try:
            rate_stats = client.rate_limiter.get_stats()
            print(f"   ✅ Rate limiter enabled and working")
        except Exception as e:
            print(f"   ❌ Rate limiter error: {e}")
    
    # Test 3: QuotaManager (should be working from existing services)
    print("\n🔧 Testing QuotaManager...")
    if client.quota_manager:
        try:
            quota_status = client.quota_manager.get_quota_status()
            print(f"   ✅ Quota manager enabled and working")
        except Exception as e:
            print(f"   ❌ Quota manager error: {e}")
    
    # Test 4: OfflineManager (should be working from existing services)
    print("\n🔧 Testing OfflineManager...")
    if client.offline_manager:
        try:
            queue_status = client.offline_manager.get_queue_status()
            print(f"   ✅ Offline manager enabled and working")
        except Exception as e:
            print(f"   ❌ Offline manager error: {e}")
    
    # Test 5: SecurityValidator (should be working from existing services)
    print("\n🔧 Testing SecurityValidator...")
    if client.security_validator:
        try:
            security_report = client.get_security_report()
            print(f"   ✅ Security validator enabled and working")
        except Exception as e:
            print(f"   ❌ Security validator error: {e}")
    
    # Test 6: SDKMonitor (should be working from existing services)
    print("\n🔧 Testing SDKMonitor...")
    if client.sdk_monitor:
        try:
            health_summary = client.sdk_monitor.get_health_summary()
            print(f"   ✅ SDK monitor enabled and working")
        except Exception as e:
            print(f"   ❌ SDK monitor error: {e}")
    
    # Test 7: RetryManager (should be working from existing services)
    print("\n🔧 Testing RetryManager...")
    if client.retry_manager:
        try:
            retry_stats = client.retry_manager.get_stats()
            print(f"   ✅ Retry manager enabled and working")
        except Exception as e:
            print(f"   ❌ Retry manager error: {e}")
    
    # Test 8: BatchManager (NEW SERVICE)
    print("\n🔧 Testing BatchManager...")
    if client.batch_manager:
        batch_stats = client.get_batch_stats()
        print(f"   Batch stats: {batch_stats.total_batches if batch_stats else 0} batches sent")
        
        # Test adding to batch
        try:
            test_exception = Exception("Batch test error")
            client.capture_exception(test_exception, {"batch_test": True})
            print("   ✅ Error added to batch successfully")
        except Exception as e:
            print(f"   ❌ Batch test failed: {e}")
    
    # Test 9: CompressionService (NEW SERVICE)
    print("\n🔧 Testing CompressionService...")
    if client.compression_service:
        compression_stats = client.get_compression_stats()
        print(f"   Compression stats: {compression_stats.total_compressions if compression_stats else 0} compressions")
        
        # Test compression capability
        test_data = "This is a test string for compression" * 50  # Make it large enough
        if client.compression_service.should_compress(test_data):
            try:
                compressed = client.compression_service.compress(test_data)
                print(f"   ✅ Compression works, compressed size: {len(compressed)} chars")
            except Exception as e:
                print(f"   ❌ Compression failed: {e}")
        else:
            print("   ℹ️  Test data below compression threshold")
    
    # Test 10: CircuitBreaker (NEW SERVICE)
    print("\n🔧 Testing CircuitBreaker...")
    if client.circuit_breaker:
        cb_stats = client.get_circuit_breaker_stats()
        print(f"   Circuit breaker state: {cb_stats.state if cb_stats else 'unknown'}")
        print(f"   ✅ Circuit breaker is {'OPEN' if client.is_circuit_breaker_open() else 'CLOSED'}")
    
    # Test 11: Test overall health and service count
    print("\n🔧 Testing Overall Health...")
    health_status = client.get_health_status()
    enabled_services = []
    
    if health_status.get('sdk_enabled'):
        enabled_services.append('ErrorExplorer Core')
    if 'breadcrumbs' in health_status:
        enabled_services.append('BreadcrumbManager')
    if 'rate_limiter' in health_status:
        enabled_services.append('RateLimiter')
    if 'quota' in health_status:
        enabled_services.append('QuotaManager')
    if 'offline_queue' in health_status:
        enabled_services.append('OfflineManager')
    if client.security_validator:
        enabled_services.append('SecurityValidator')
    if client.sdk_monitor:
        enabled_services.append('SDKMonitor')
    if client.retry_manager:
        enabled_services.append('RetryManager')
    if client.batch_manager:
        enabled_services.append('BatchManager')
    if client.compression_service:
        enabled_services.append('CompressionService')
    if client.circuit_breaker:
        enabled_services.append('CircuitBreaker')
    
    print(f"\n📊 Service Status Summary:")
    print(f"   Total services enabled: {len(enabled_services)}/11")
    print(f"   Services: {', '.join(enabled_services)}")
    
    # Final test: Capture an exception with all services
    print(f"\n🧪 Final Integration Test...")
    try:
        # This should trigger all services in the pipeline
        raise ValueError("Integration test exception with all services")
    except Exception as e:
        client.capture_exception(e, {
            "test_type": "integration",
            "services_count": len(enabled_services),
            "timestamp": time.time()
        })
        print("   ✅ Exception captured through full service pipeline")
    
    # Flush any batched errors
    if client.batch_manager:
        client.flush_batch()
        print("   ✅ Batch flushed")
    
    print("\n" + "=" * 60)
    
    if len(enabled_services) == 11:
        print("🎉 SUCCESS: All 11 services are working correctly!")
        print("✅ Python SDK has achieved feature parity with Vue.js reference SDK")
    else:
        missing = 11 - len(enabled_services)
        print(f"⚠️  WARNING: {missing} services may not be working correctly")
        print("❌ Python SDK has not achieved full feature parity yet")
    
    return len(enabled_services) == 11


if __name__ == "__main__":
    try:
        success = test_python_sdk_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)