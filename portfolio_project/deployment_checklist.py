#!/usr/bin/env python3
"""
Deployment Checklist and Verification Script
Verifies deployment readiness following SOLID principles

Author: Amardeep Asode
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class DeploymentChecker:
    """Single Responsibility: Checks deployment readiness"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_path = project_root / "backend"
        self.frontend_path = project_root / "frontend"
    
    def check_file_structure(self) -> Tuple[bool, List[str]]:
        """Check if required files exist"""
        required_files = [
            self.backend_path / "requirements.txt",
            self.backend_path / "manage.py",
            self.backend_path / "build.sh",
            self.backend_path / "render.yaml",
            self.backend_path / "backend" / "settings.py",
            self.backend_path / "backend" / "settings_production.py",
            self.frontend_path / "package.json",
            self.frontend_path / "next.config.ts",
            self.frontend_path / "vercel.json"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path.relative_to(self.project_root)))
        
        return len(missing_files) == 0, missing_files
    
    def check_environment_files(self) -> Tuple[bool, List[str]]:
        """Check environment file templates"""
        env_files = [
            self.backend_path / ".env.example",
            self.backend_path / ".env.production",
            self.frontend_path / ".env.example",
            self.frontend_path / ".env.production"
        ]
        
        missing_files = []
        for file_path in env_files:
            if not file_path.exists():
                missing_files.append(str(file_path.relative_to(self.project_root)))
        
        return len(missing_files) == 0, missing_files
    
    def check_dependencies(self) -> Tuple[bool, List[str]]:
        """Check if dependencies are properly defined"""
        issues = []
        
        # Check backend requirements.txt
        requirements_file = self.backend_path / "requirements.txt"
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                requirements = f.read()
                
            required_packages = [
                'Django', 'djangorestframework', 'django-cors-headers',
                'gunicorn', 'psycopg2-binary', 'dj-database-url', 'whitenoise'
            ]
            
            for package in required_packages:
                if package.lower() not in requirements.lower():
                    issues.append(f"Missing backend dependency: {package}")
        else:
            issues.append("requirements.txt not found")
        
        # Check frontend package.json
        package_file = self.frontend_path / "package.json"
        if package_file.exists():
            try:
                with open(package_file, 'r') as f:
                    package_data = json.load(f)
                
                required_scripts = ['build', 'start', 'dev']
                scripts = package_data.get('scripts', {})
                
                for script in required_scripts:
                    if script not in scripts:
                        issues.append(f"Missing frontend script: {script}")
                        
            except json.JSONDecodeError:
                issues.append("Invalid package.json format")
        else:
            issues.append("package.json not found")
        
        return len(issues) == 0, issues
    
    def check_configuration_files(self) -> Tuple[bool, List[str]]:
        """Check configuration files"""
        issues = []
        
        # Check render.yaml
        render_config = self.backend_path / "render.yaml"
        if render_config.exists():
            try:
                import yaml
                with open(render_config, 'r') as f:
                    config = yaml.safe_load(f)
                
                # Check required sections
                if 'services' not in config:
                    issues.append("render.yaml missing 'services' section")
                elif not config['services']:
                    issues.append("render.yaml 'services' section is empty")
                
                if 'databases' not in config:
                    issues.append("render.yaml missing 'databases' section")
                    
            except Exception as e:
                issues.append(f"Invalid render.yaml: {str(e)}")
        else:
            issues.append("render.yaml not found")
        
        # Check vercel.json
        vercel_config = self.frontend_path / "vercel.json"
        if vercel_config.exists():
            try:
                with open(vercel_config, 'r') as f:
                    config = json.load(f)
                
                # Check required sections
                if 'builds' not in config:
                    issues.append("vercel.json missing 'builds' section")
                    
            except json.JSONDecodeError:
                issues.append("Invalid vercel.json format")
        else:
            issues.append("vercel.json not found")
        
        return len(issues) == 0, issues

class EnvironmentValidator:
    """Single Responsibility: Validates environment configuration"""
    
    def __init__(self):
        self.required_backend_vars = [
            'DJANGO_SETTINGS_MODULE',
            'SECRET_KEY',
            'DATABASE_URL',
            'RAZORPAY_KEY_ID',
            'RAZORPAY_KEY_SECRET',
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD',
            'BREVO_API_KEY'
        ]
        
        self.required_frontend_vars = [
            'NEXT_PUBLIC_DJANGO_API_URL',
            'NEXT_PUBLIC_API_URL',
            'NEXT_PUBLIC_RAZORPAY_KEY_ID'
        ]
    
    def validate_backend_env_template(self, env_file: Path) -> Tuple[bool, List[str]]:
        """Validate backend environment template"""
        if not env_file.exists():
            return False, [f"Environment file not found: {env_file}"]
        
        missing_vars = []
        try:
            with open(env_file, 'r') as f:
                content = f.read()
            
            for var in self.required_backend_vars:
                if var not in content:
                    missing_vars.append(var)
                    
        except Exception as e:
            return False, [f"Error reading environment file: {str(e)}"]
        
        return len(missing_vars) == 0, missing_vars
    
    def validate_frontend_env_template(self, env_file: Path) -> Tuple[bool, List[str]]:
        """Validate frontend environment template"""
        if not env_file.exists():
            return False, [f"Environment file not found: {env_file}"]
        
        missing_vars = []
        try:
            with open(env_file, 'r') as f:
                content = f.read()
            
            for var in self.required_frontend_vars:
                if var not in content:
                    missing_vars.append(var)
                    
        except Exception as e:
            return False, [f"Error reading environment file: {str(e)}"]
        
        return len(missing_vars) == 0, missing_vars

class DeploymentValidator:
    """Single Responsibility: Orchestrates deployment validation"""
    
    def __init__(self, project_root: Optional[Path] = None):
        if project_root is None:
            project_root = Path(__file__).parent
        
        self.checker = DeploymentChecker(project_root)
        self.env_validator = EnvironmentValidator()
        self.project_root = project_root
    
    def run_all_checks(self) -> Dict[str, any]:
        """Run all deployment checks"""
        results = {
            "overall_status": "ready",
            "checks": {},
            "summary": {
                "total_checks": 0,
                "passed_checks": 0,
                "failed_checks": 0
            }
        }
        
        # File structure check
        passed, issues = self.checker.check_file_structure()
        results["checks"]["file_structure"] = {
            "status": "pass" if passed else "fail",
            "issues": issues
        }
        results["summary"]["total_checks"] += 1
        if passed:
            results["summary"]["passed_checks"] += 1
        else:
            results["summary"]["failed_checks"] += 1
            results["overall_status"] = "not_ready"
        
        # Environment files check
        passed, issues = self.checker.check_environment_files()
        results["checks"]["environment_files"] = {
            "status": "pass" if passed else "fail",
            "issues": issues
        }
        results["summary"]["total_checks"] += 1
        if passed:
            results["summary"]["passed_checks"] += 1
        else:
            results["summary"]["failed_checks"] += 1
            results["overall_status"] = "not_ready"
        
        # Dependencies check
        passed, issues = self.checker.check_dependencies()
        results["checks"]["dependencies"] = {
            "status": "pass" if passed else "fail",
            "issues": issues
        }
        results["summary"]["total_checks"] += 1
        if passed:
            results["summary"]["passed_checks"] += 1
        else:
            results["summary"]["failed_checks"] += 1
            results["overall_status"] = "not_ready"
        
        # Configuration files check
        passed, issues = self.checker.check_configuration_files()
        results["checks"]["configuration"] = {
            "status": "pass" if passed else "fail",
            "issues": issues
        }
        results["summary"]["total_checks"] += 1
        if passed:
            results["summary"]["passed_checks"] += 1
        else:
            results["summary"]["failed_checks"] += 1
            results["overall_status"] = "not_ready"
        
        # Environment validation
        backend_env = self.project_root / "backend" / ".env.production"
        passed, issues = self.env_validator.validate_backend_env_template(backend_env)
        results["checks"]["backend_environment"] = {
            "status": "pass" if passed else "fail",
            "issues": issues
        }
        results["summary"]["total_checks"] += 1
        if passed:
            results["summary"]["passed_checks"] += 1
        else:
            results["summary"]["failed_checks"] += 1
            results["overall_status"] = "not_ready"
        
        frontend_env = self.project_root / "frontend" / ".env.production"
        passed, issues = self.env_validator.validate_frontend_env_template(frontend_env)
        results["checks"]["frontend_environment"] = {
            "status": "pass" if passed else "fail",
            "issues": issues
        }
        results["summary"]["total_checks"] += 1
        if passed:
            results["summary"]["passed_checks"] += 1
        else:
            results["summary"]["failed_checks"] += 1
            results["overall_status"] = "not_ready"
        
        return results
    
    def generate_report(self) -> str:
        """Generate deployment readiness report"""
        results = self.run_all_checks()
        
        report = f"""
# Deployment Readiness Report

## Overall Status: {results['overall_status'].upper()}

## Summary
- Total Checks: {results['summary']['total_checks']}
- Passed: {results['summary']['passed_checks']}
- Failed: {results['summary']['failed_checks']}
- Success Rate: {(results['summary']['passed_checks'] / results['summary']['total_checks'] * 100):.1f}%

## Detailed Results

"""
        
        for check_name, check_result in results['checks'].items():
            status_emoji = "✅" if check_result['status'] == 'pass' else "❌"
            report += f"### {status_emoji} {check_name.replace('_', ' ').title()}\n"
            report += f"Status: {check_result['status'].upper()}\n"
            
            if check_result['issues']:
                report += "Issues:\n"
                for issue in check_result['issues']:
                    report += f"- {issue}\n"
            else:
                report += "No issues found.\n"
            
            report += "\n"
        
        if results['overall_status'] == 'ready':
            report += """
## Next Steps

Your project is ready for deployment! Follow these steps:

1. **Backend Deployment (Render.com)**
   - Create PostgreSQL database
   - Create web service
   - Set environment variables
   - Deploy

2. **Frontend Deployment (Vercel)**
   - Import project from GitHub
   - Set environment variables
   - Deploy

3. **Post-Deployment**
   - Update CORS settings
   - Test integration
   - Monitor health endpoints

Refer to SIMPLE_DEPLOYMENT_GUIDE.md for detailed instructions.
"""
        else:
            report += """
## Action Required

Your project is not ready for deployment. Please address the issues listed above before proceeding.

Common fixes:
- Create missing files
- Install missing dependencies
- Update configuration files
- Set up environment variables

Run this script again after making changes.
"""
        
        return report

def main():
    """Main function"""
    try:
        validator = DeploymentValidator()
        
        print("🔍 Running deployment readiness checks...")
        print("=" * 60)
        
        results = validator.run_all_checks()
        
        # Print summary
        print(f"\nOverall Status: {results['overall_status'].upper()}")
        print(f"Checks Passed: {results['summary']['passed_checks']}/{results['summary']['total_checks']}")
        
        # Print detailed results
        print("\nDetailed Results:")
        for check_name, check_result in results['checks'].items():
            status_emoji = "✅" if check_result['status'] == 'pass' else "❌"
            print(f"  {status_emoji} {check_name.replace('_', ' ').title()}: {check_result['status'].upper()}")
            
            if check_result['issues']:
                for issue in check_result['issues']:
                    print(f"    - {issue}")
        
        # Generate and save report
        report = validator.generate_report()
        report_file = Path("deployment_readiness_report.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📋 Detailed report saved to: {report_file}")
        
        if results['overall_status'] == 'ready':
            print("\n🎉 Your project is ready for deployment!")
            print("📖 Follow the SIMPLE_DEPLOYMENT_GUIDE.md for next steps.")
        else:
            print("\n⚠️  Please address the issues above before deployment.")
        
    except Exception as e:
        print(f"❌ Error running deployment checks: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()