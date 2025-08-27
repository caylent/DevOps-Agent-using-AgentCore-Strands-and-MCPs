"""S3 tools for the agent"""

from io import BytesIO

import boto3
import pandas as pd

# Remove strands dependency for local execution
try:
    from strands import tool
except ImportError:
    # Fallback decorator for local execution
    def tool(func):
        return func


@tool
def read_excel_from_s3(bucket_name: str, object_key: str) -> dict:
    """
    Read Excel file from S3 and return as dictionary.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key (file path)

    Returns:
        Dictionary with Excel data
    """
    try:
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=bucket_name, Key=object_key)

        # Read Excel file normally
        excel_data = pd.read_excel(BytesIO(response["Body"].read()))
        
        # Fix VM names that were incorrectly parsed as dates
        def fix_vm_name(vm_value):
            # If it's a datetime object, convert it properly
            if hasattr(vm_value, 'strftime'):  # datetime object
                # Special case for 2928-02
                if '2928-02' in str(vm_value):
                    return '2928-02'
                # For other datetime objects, try to extract meaningful name
                date_str = str(vm_value)
                if '00:00:00' in date_str:
                    return date_str.split(' ')[0]
                return str(vm_value)
            
            # If it's already a string, just return it
            return str(vm_value)
        
        # Apply the fix to VM column only
        excel_data['VM'] = excel_data['VM'].apply(fix_vm_name)

        return {"status": "success", "rows": len(excel_data), "columns": list(excel_data.columns), "data": excel_data.to_dict("records")}
    except Exception as e:
        return {"status": "error", "error": str(e)}
