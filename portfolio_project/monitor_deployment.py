#!/usr/bin/env python3
"""
Deployment Monitoring Script for Amardeep Portfolio Project
Monitors both backend (Render.com) and frontend (Vercel) deployments
Following SOLID principles for robust monitoring

Author: Amardeep Asode
"""

import os
import sys
import time
import json
import requests
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deployment_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ServiceEndpoint:
    """Data class for service endpoint configuration"""
    name: str
    url: str
    health_path: str
    timeout: int = 30
    expected_status: int = 200

class MonitorInterface(ABC):
    """Interface for monitoring implementations (Interface Segregation Principle)"""
    
    @abstractmethod
    def check_health(self) -> Dict[str, any]:
        """Check service health"""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, any]:
        """Get service metrics"""
        pass

class ServiceMonitor(MonitorInterface):
    """Single Responsibility: Monitors individual service health"""
    
    def __init__(self, endpoint: ServiceEndpoint):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.session.timeout = endpoint.timeout
    
    def check_health(self) -> Dict[str, any]:
        """Check service health with detailed metrics"""
        try:
            start_time = time.time()
            
            # Make health check request
            response = self.session.get(
                f"{self.endpoint.url}{self.endpoint.health_path}",
                timeout=self.endpoint.timeout
            )
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Parse response if JSON
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:500]}
            
            return {
                "service": self.endpoint.name,
                "status": "healthy" if response.status_code == self.endpoint.expected_status else "unhealthy",
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.now().isoformat(),
                "url": f"{self.endpoint.url}{self.endpoint.health_path}",
                "response_data": response_data
            }
            
        except requests.exceptions.Timeout:
            return {
                "service": self.endpoint.name,
                "status": "timeout",
                "error": f"Request timed out after {self.endpoint.timeout}s",
                "timestamp": datetime.now().isoformat(),
                "url": f"{self.endpoint.url}{self.endpoint.health_path}"
            }
        except requests.exceptions.ConnectionError:
            return {
                "service": self.endpoint.name,
                "status": "unreachable",
                "error": "Connection failed",
                "timestamp": datetime.now().isoformat(),
                "url": f"{self.endpoint.url}{self.endpoint.health_path}"
            }
        except Exception as e:
            return {
                "service": self.endpoint.name,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "url": f"{self.endpoint.url}{self.endpoint.health_path}"
            }
    
    def get_metrics(self) -> Dict[str, any]:
        """Get detailed service metrics"""
        health_data = self.check_health()
        
        # Add additional metrics
        metrics = {
            **health_data,
            "availability": 1.0 if health_data["status"] == "healthy" else 0.0,
            "performance_score": self._calculate_performance_score(health_data)
        }
        
        return metrics
    
    def _calculate_performance_score(self, health_data: Dict) -> float:
        """Calculate performance score based on response time and status"""
        if health_data["status"] != "healthy":
            return 0.0
        
        response_time = health_data.get("response_time_ms", float('inf'))
        
        # Score based on response time thresholds
        if response_time < 100:
            return 1.0
        elif response_time < 500:
            return 0.8
        elif response_time < 1000:
            return 0.6
        elif response_time < 2000:
            return 0.4
        else:
            return 0.2

class DeploymentMonitor:
    """Single Responsibility: Orchestrates monitoring of all services"""
    
    def __init__(self):
        self.services = self._initialize_services()
        self.monitors = {
            service.name: ServiceMonitor(service) 
            for service in self.services
        }
    
    def _initialize_services(self) -> List[ServiceEndpoint]:
        """Initialize service endpoints for monitoring"""
        return [
            ServiceEndpoint(
                name="backend",
                url="https://amardeep-portfolio-backend.onrender.com",
                health_path="/api/health/",
                timeout=30
            ),
            ServiceEndpoint(
                name="backend_simple",
                url="https://amardeep-portfolio-backend.onrender.com",
                health_path="/api/health/simple/",
                timeout=15
            ),
            ServiceEndpoint(
                name="frontend",
                url="https://amardeep-portfolio-frontend.vercel.app",
                health_path="/",
                timeout=20
            ),
            ServiceEndpoint(
                name="api_status",
                url="https://amardeep-portfolio-backend.onrender.com",
                health_path="/api/status/",
                timeout=15
            )
        ]
    
    def run_health_checks(self) -> Dict[str, any]:
        """Run health checks for all services"""
        logger.info("Starting health checks for all services...")
        
        results = {}
        overall_status = "healthy"
        
        for service_name, monitor in self.monitors.items():
            try:
                result = monitor.check_health()
                results[service_name] = result
                
                logger.info(f"{service_name}: {result['status']} ({result.get('response_time_ms', 'N/A')}ms)")
                
                if result["status"] != "healthy":
                    overall_status = "degraded"
                    
            except Exception as e:
                logger.error(f"Failed to check {service_name}: {str(e)}")
                results[service_name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                overall_status = "degraded"
        
        summary = {
            "overall_status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "services": results,
            "summary": self._generate_summary(results)
        }
        
        return summary
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate summary statistics"""
        total_services = len(results)
        healthy_services = sum(1 for r in results.values() if r.get("status") == "healthy")
        
        avg_response_time = 0
        response_times = [
            r.get("response_time_ms", 0) 
            for r in results.values() 
            if r.get("response_time_ms") is not None
        ]
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
        
        return {
            "total_services": total_services,
            "healthy_services": healthy_services,
            "availability_percentage": (healthy_services / total_services) * 100,
            "average_response_time_ms": round(avg_response_time, 2)
        }
    
    def continuous_monitoring(self, interval_seconds: int = 300, duration_hours: int = 24):
        """Run continuous monitoring for specified duration"""
        logger.info(f"Starting continuous monitoring for {duration_hours} hours...")
        
        end_time = datetime.now() + timedelta(hours=duration_hours)
        check_count = 0
        
        while datetime.now() < end_time:
            check_count += 1
            logger.info(f"Health check #{check_count}")
            
            # Run health checks
            results = self.run_health_checks()
            
            # Log summary
            summary = results["summary"]
            logger.info(
                f"Summary: {summary['healthy_services']}/{summary['total_services']} healthy, "
                f"{summary['availability_percentage']:.1f}% availability, "
                f"{summary['average_response_time_ms']}ms avg response"
            )
            
            # Save results to file
            self._save_results(results, check_count)
            
            # Check for alerts
            self._check_alerts(results)
            
            # Wait for next check
            if datetime.now() < end_time:
                logger.info(f"Waiting {interval_seconds} seconds for next check...")
                time.sleep(interval_seconds)
        
        logger.info("Continuous monitoring completed")
    
    def _save_results(self, results: Dict, check_count: int):
        """Save monitoring results to file"""
        filename = f"monitoring_results_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Load existing results or create new
        try:
            with open(filename, 'r') as f:
                all_results = json.load(f)
        except FileNotFoundError:
            all_results = {"checks": []}
        
        # Add current results
        all_results["checks"].append({
            "check_number": check_count,
            **results
        })
        
        # Save updated results
        with open(filename, 'w') as f:
            json.dump(all_results, f, indent=2)
    
    def _check_alerts(self, results: Dict):
        """Check for alert conditions"""
        summary = results["summary"]
        
        # Alert if availability drops below 80%
        if summary["availability_percentage"] < 80:
            logger.warning(
                f"🚨 ALERT: Low availability - {summary['availability_percentage']:.1f}%"
            )
        
        # Alert if average response time is too high
        if summary["average_response_time_ms"] > 5000:
            logger.warning(
                f"🚨 ALERT: High response time - {summary['average_response_time_ms']}ms"
            )
        
        # Alert for specific service failures
        for service_name, service_result in results["services"].items():
            if service_result.get("status") != "healthy":
                logger.warning(
                    f"🚨 ALERT: {service_name} is {service_result.get('status')} - "
                    f"{service_result.get('error', 'Unknown error')}"
                )

class ReportGenerator:
    """Single Responsibility: Generates monitoring reports"""
    
    def __init__(self, monitor: DeploymentMonitor):
        self.monitor = monitor
    
    def generate_status_report(self) -> str:
        """Generate a comprehensive status report"""
        results = self.monitor.run_health_checks()
        
        report = f"""
# Deployment Status Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Status: {results['overall_status'].upper()}

## Summary
- Total Services: {results['summary']['total_services']}
- Healthy Services: {results['summary']['healthy_services']}
- Availability: {results['summary']['availability_percentage']:.1f}%
- Average Response Time: {results['summary']['average_response_time_ms']}ms

## Service Details
"""
        
        for service_name, service_data in results['services'].items():
            status_emoji = "✅" if service_data['status'] == 'healthy' else "❌"
            report += f"""
### {status_emoji} {service_name.title()}
- Status: {service_data['status']}
- Response Time: {service_data.get('response_time_ms', 'N/A')}ms
- URL: {service_data.get('url', 'N/A')}
"""
            if 'error' in service_data:
                report += f"- Error: {service_data['error']}\n"
        
        return report
    
    def save_report(self, filename: Optional[str] = None) -> str:
        """Save status report to file"""
        if not filename:
            filename = f"status_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report = self.generate_status_report()
        
        with open(filename, 'w') as f:
            f.write(report)
        
        logger.info(f"Status report saved to {filename}")
        return filename

def main():
    """Main monitoring function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor Amardeep Portfolio Deployment')
    parser.add_argument('--mode', choices=['check', 'monitor', 'report'], 
                       default='check', help='Monitoring mode')
    parser.add_argument('--interval', type=int, default=300, 
                       help='Monitoring interval in seconds (default: 300)')
    parser.add_argument('--duration', type=int, default=24, 
                       help='Monitoring duration in hours (default: 24)')
    
    args = parser.parse_args()
    
    try:
        monitor = DeploymentMonitor()
        
        if args.mode == 'check':
            # Single health check
            logger.info("Running single health check...")
            results = monitor.run_health_checks()
            
            print("\n" + "="*60)
            print("DEPLOYMENT HEALTH CHECK RESULTS")
            print("="*60)
            print(f"Overall Status: {results['overall_status'].upper()}")
            print(f"Timestamp: {results['timestamp']}")
            print(f"Availability: {results['summary']['availability_percentage']:.1f}%")
            print(f"Average Response Time: {results['summary']['average_response_time_ms']}ms")
            print("\nService Details:")
            
            for service_name, service_data in results['services'].items():
                status_emoji = "✅" if service_data['status'] == 'healthy' else "❌"
                print(f"  {status_emoji} {service_name}: {service_data['status']} "
                      f"({service_data.get('response_time_ms', 'N/A')}ms)")
        
        elif args.mode == 'monitor':
            # Continuous monitoring
            monitor.continuous_monitoring(args.interval, args.duration)
        
        elif args.mode == 'report':
            # Generate report
            report_generator = ReportGenerator(monitor)
            filename = report_generator.save_report()
            print(f"Status report generated: {filename}")
        
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Monitoring failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()