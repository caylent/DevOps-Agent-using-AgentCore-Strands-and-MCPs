"""
AWS Account Management for Multi-Account DevOps Operations
Handles account detection, validation, and switching
"""

import boto3
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import sys


@dataclass
class AWSAccountInfo:
    """Information about an AWS account"""
    account_id: str
    account_name: Optional[str] = None
    region: str = "us-east-1"
    profile: Optional[str] = None
    role_arn: Optional[str] = None
    is_current: bool = False
    last_accessed: Optional[datetime] = None
    permissions: List[str] = field(default_factory=list)
    status: str = "unknown"  # active, inactive, error


class AWSAccountManager:
    """Manages AWS account detection, validation, and switching"""
    
    def __init__(self, region: str = "us-east-1", profile: str = "default"):
        self.region = region
        self.profile = profile
        self.accounts: Dict[str, AWSAccountInfo] = {}
        self.current_account: Optional[AWSAccountInfo] = None
        self.session_cache: Dict[str, boto3.Session] = {}
        
    def detect_current_account(self) -> Optional[AWSAccountInfo]:
        """Detect the current AWS account from credentials"""
        try:
            # Try to get caller identity
            session = boto3.Session(region_name=self.region, profile_name=self.profile)
            sts = session.client('sts')
            response = sts.get_caller_identity()
            
            account_id = response['Account']
            user_id = response.get('UserId', 'unknown')
            arn = response.get('Arn', 'unknown')
            
            # Extract account name if possible
            account_name = self._extract_account_name_from_arn(arn)
            
            account_info = AWSAccountInfo(
                account_id=account_id,
                account_name=account_name,
                region=self.region,
                profile=self.profile,
                is_current=True,
                last_accessed=datetime.now(),
                status="active"
            )
            
            # Validate permissions
            account_info.permissions = self._validate_permissions(session)
            
            self.current_account = account_info
            self.accounts[account_id] = account_info
            
            return account_info
            
        except Exception as e:
            print(f"⚠️  Could not detect current AWS account: {e}")
            return None
    
    def _extract_account_name_from_arn(self, arn: str) -> Optional[str]:
        """Extract account name from ARN if possible"""
        try:
            # ARN format: arn:aws:sts::123456789012:assumed-role/RoleName/SessionName
            # or arn:aws:iam::123456789012:user/UserName
            parts = arn.split(':')
            if len(parts) >= 6:
                resource_part = parts[5]
                if '/' in resource_part:
                    return resource_part.split('/')[-1]
            return None
        except:
            return None
    
    def _validate_permissions(self, session: boto3.Session) -> List[str]:
        """Validate what permissions are available in the current account"""
        permissions = []
        
        # Test common services
        services_to_test = [
            ('ce', 'Cost Explorer'),
            ('cloudwatch', 'CloudWatch'),
            ('ec2', 'EC2'),
            ('s3', 'S3'),
            ('iam', 'IAM'),
            ('organizations', 'Organizations'),
            ('securityhub', 'Security Hub'),
            ('config', 'Config'),
            ('inspector2', 'Inspector'),
            ('pricing', 'Pricing')
        ]
        
        for service_name, display_name in services_to_test:
            try:
                client = session.client(service_name, region_name=self.region)
                # Try a simple operation to test permissions
                if service_name == 'ce':
                    client.describe_cost_category_definition(CostCategoryArn='test')
                elif service_name == 'cloudwatch':
                    client.list_metrics(MaxRecords=1)
                elif service_name == 'ec2':
                    client.describe_regions(MaxResults=1)
                elif service_name == 's3':
                    client.list_buckets()
                elif service_name == 'iam':
                    client.get_user()
                elif service_name == 'organizations':
                    client.describe_organization()
                elif service_name == 'securityhub':
                    client.describe_hub()
                elif service_name == 'config':
                    client.describe_configuration_recorders()
                elif service_name == 'inspector2':
                    client.list_coverage()
                elif service_name == 'pricing':
                    client.describe_services()
                
                permissions.append(display_name)
            except Exception:
                # Service not available or no permissions
                pass
        
        return permissions
    
    def add_account(self, account_id: str, account_name: str = None, 
                   role_arn: str = None, region: str = None) -> AWSAccountInfo:
        """Add a new account to the manager"""
        account_info = AWSAccountInfo(
            account_id=account_id,
            account_name=account_name,
            region=region or self.region,
            role_arn=role_arn,
            last_accessed=datetime.now(),
            status="added"
        )
        
        self.accounts[account_id] = account_info
        return account_info
    
    def validate_account_access(self, account_id: str) -> Tuple[bool, str]:
        """Validate if we can access a specific account"""
        if account_id not in self.accounts:
            return False, "Account not found in manager"
        
        account = self.accounts[account_id]
        
        try:
            if account.role_arn:
                # Try to assume role
                session = boto3.Session(region_name=account.region, profile_name=self.profile)
                sts = session.client('sts')
                response = sts.assume_role(
                    RoleArn=account.role_arn,
                    RoleSessionName='aws-devops-agent'
                )
                
                # Create new session with assumed role credentials
                assumed_session = boto3.Session(
                    aws_access_key_id=response['Credentials']['AccessKeyId'],
                    aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                    aws_session_token=response['Credentials']['SessionToken'],
                    region_name=account.region
                )
                
                # Test access
                sts_assumed = assumed_session.client('sts')
                caller_identity = sts_assumed.get_caller_identity()
                
                if caller_identity['Account'] == account_id:
                    account.status = "active"
                    account.last_accessed = datetime.now()
                    account.permissions = self._validate_permissions(assumed_session)
                    return True, "Access validated successfully"
                else:
                    return False, f"Role assumption failed - got account {caller_identity['Account']}, expected {account_id}"
            
            else:
                # Use current credentials
                session = boto3.Session(region_name=account.region, profile_name=self.profile)
                sts = session.client('sts')
                caller_identity = sts.get_caller_identity()
                
                if caller_identity['Account'] == account_id:
                    account.status = "active"
                    account.last_accessed = datetime.now()
                    account.permissions = self._validate_permissions(session)
                    return True, "Access validated successfully"
                else:
                    return False, f"Current credentials are for account {caller_identity['Account']}, not {account_id}"
        
        except Exception as e:
            account.status = "error"
            return False, f"Access validation failed: {str(e)}"
    
    def get_session_for_account(self, account_id: str) -> Optional[boto3.Session]:
        """Get a boto3 session for a specific account"""
        if account_id not in self.accounts:
            return None
        
        account = self.accounts[account_id]
        
        # Check cache first
        if account_id in self.session_cache:
            return self.session_cache[account_id]
        
        try:
            if account.role_arn:
                # Assume role
                session = boto3.Session(region_name=account.region, profile_name=self.profile)
                sts = session.client('sts')
                response = sts.assume_role(
                    RoleArn=account.role_arn,
                    RoleSessionName='aws-devops-agent'
                )
                
                assumed_session = boto3.Session(
                    aws_access_key_id=response['Credentials']['AccessKeyId'],
                    aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                    aws_session_token=response['Credentials']['SessionToken'],
                    region_name=account.region
                )
                
                self.session_cache[account_id] = assumed_session
                return assumed_session
            
            else:
                # Use current credentials
                session = boto3.Session(region_name=account.region, profile_name=self.profile)
                self.session_cache[account_id] = session
                return session
        
        except Exception as e:
            print(f"⚠️  Could not create session for account {account_id}: {e}")
            return None
    
    def list_accounts(self) -> List[AWSAccountInfo]:
        """List all managed accounts"""
        return list(self.accounts.values())
    
    def get_account_summary(self) -> Dict[str, Any]:
        """Get a summary of all accounts"""
        summary = {
            "total_accounts": len(self.accounts),
            "current_account": self.current_account.account_id if self.current_account else None,
            "accounts": []
        }
        
        for account in self.accounts.values():
            summary["accounts"].append({
                "account_id": account.account_id,
                "account_name": account.account_name,
                "region": account.region,
                "status": account.status,
                "is_current": account.is_current,
                "permissions": account.permissions,
                "last_accessed": account.last_accessed.isoformat() if account.last_accessed else None
            })
        
        return summary
    
    def interactive_account_selection(self) -> Optional[AWSAccountInfo]:
        """Interactive account selection on startup"""
        print("\n🔍 AWS Account Detection and Selection")
        print("=" * 50)
        
        # First, try to detect current account
        current_account = self.detect_current_account()
        
        if current_account:
            print(f"✅ Detected current AWS account: {current_account.account_id}")
            if current_account.account_name:
                print(f"   Account Name: {current_account.account_name}")
            print(f"   Region: {current_account.region}")
            print(f"   Permissions: {', '.join(current_account.permissions) if current_account.permissions else 'None detected'}")
            print()
        
        # Show options
        print("Account Selection Options:")
        print("1. Use current account (recommended)")
        print("2. Specify a different account ID")
        print("3. Add account with cross-account role")
        print("4. List all managed accounts")
        print("5. Skip account selection (use environment variables)")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == "1":
                    if current_account:
                        print(f"✅ Using current account: {current_account.account_id}")
                        return current_account
                    else:
                        print("❌ No current account detected. Please check your AWS credentials.")
                        continue
                
                elif choice == "2":
                    account_id = input("Enter account ID: ").strip()
                    if not account_id:
                        print("❌ Account ID cannot be empty")
                        continue
                    
                    account_name = input("Enter account name (optional): ").strip() or None
                    region = input(f"Enter region (default: {self.region}): ").strip() or self.region
                    
                    account = self.add_account(account_id, account_name, region=region)
                    success, message = self.validate_account_access(account_id)
                    
                    if success:
                        print(f"✅ Account {account_id} validated successfully")
                        return account
                    else:
                        print(f"❌ Account validation failed: {message}")
                        continue
                
                elif choice == "3":
                    account_id = input("Enter account ID: ").strip()
                    if not account_id:
                        print("❌ Account ID cannot be empty")
                        continue
                    
                    role_arn = input("Enter role ARN (e.g., arn:aws:iam::123456789012:role/DevOpsRole): ").strip()
                    if not role_arn:
                        print("❌ Role ARN cannot be empty")
                        continue
                    
                    account_name = input("Enter account name (optional): ").strip() or None
                    region = input(f"Enter region (default: {self.region}): ").strip() or self.region
                    
                    account = self.add_account(account_id, account_name, role_arn, region)
                    success, message = self.validate_account_access(account_id)
                    
                    if success:
                        print(f"✅ Account {account_id} with role {role_arn} validated successfully")
                        return account
                    else:
                        print(f"❌ Account validation failed: {message}")
                        continue
                
                elif choice == "4":
                    accounts = self.list_accounts()
                    if not accounts:
                        print("No accounts managed yet")
                    else:
                        print("\nManaged Accounts:")
                        for i, account in enumerate(accounts, 1):
                            status_icon = "✅" if account.status == "active" else "❌"
                            print(f"{i}. {status_icon} {account.account_id} ({account.account_name or 'No name'}) - {account.status}")
                    continue
                
                elif choice == "5":
                    print("⚠️  Skipping account selection - using environment variables only")
                    return None
                
                else:
                    print("❌ Invalid choice. Please enter 1-5.")
                    continue
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")
                continue


def get_aws_account_manager(region: str = "us-east-1", profile: str = "default") -> AWSAccountManager:
    """Get an AWS account manager instance"""
    return AWSAccountManager(region=region, profile=profile)
