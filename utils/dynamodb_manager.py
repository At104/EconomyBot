import boto3
import json
from botocore.exceptions import ClientError
from decimal import Decimal
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DynamoDBManager:
    def __init__(self):
        """Initialize DynamoDB connection"""
        # Load AWS configuration from environment variables
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_DEFAULT_REGION')
        aws_endpoint = os.getenv('AWS_ENDPOINT_URL')  # For LocalStack
        
        self.table_name = os.getenv('DYNAMODB_TABLE_NAME')
        
        # Initialize DynamoDB resource
        if aws_endpoint:
            # Use LocalStack or custom endpoint
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=aws_endpoint,
                region_name=aws_region,
                aws_access_key_id=aws_access_key or 'test',
                aws_secret_access_key=aws_secret_key or 'test'
            )
        else:
            # Use AWS with credentials
            if aws_access_key and aws_secret_key:
                self.dynamodb = boto3.resource(
                    'dynamodb',
                    region_name=aws_region,
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                )
            else:
                # Use default AWS credentials (IAM role, ~/.aws/credentials, etc.)
                self.dynamodb = boto3.resource('dynamodb', region_name=aws_region)
        
        self.table = None
        
    def create_table(self):
        """Create the DynamoDB table for user economy data"""
        try:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'user_id',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'user_id',
                        'AttributeType': 'S'  # String
                    }
                ],
                BillingMode='PAY_PER_REQUEST'  # On-demand billing
            )
            
            # Wait for table to be created
            table.wait_until_exists()
            print(f"Table {self.table_name} created successfully!")
            self.table = table
            return table
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print(f"Table {self.table_name} already exists")
                self.table = self.dynamodb.Table(self.table_name)
                return self.table
            else:
                print(f"Error creating table: {e}")
                return None
    
    def get_table(self):
        """Get reference to the table"""
        if self.table is None:
            try:
                self.table = self.dynamodb.Table(self.table_name)
                # Check if table exists
                self.table.load()
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    print(f"Table {self.table_name} does not exist. Creating...")
                    return self.create_table()
                else:
                    raise e
        return self.table
    
    def put_user_data(self, user_id, amount, workers, income, gold):
        """Insert or update user economy data"""
        table = self.get_table()
        
        try:
            response = table.put_item(
                Item={
                    'user_id': str(user_id),
                    'amount': Decimal(str(amount)),
                    'workers': Decimal(str(workers)),
                    'income': Decimal(str(income)),
                    'gold': Decimal(str(gold))
                }
            )
            return True
        except ClientError as e:
            print(f"Error putting user data: {e}")
            return False
    
    def get_user_data(self, user_id):
        """Get user economy data"""
        table = self.get_table()
        
        try:
            response = table.get_item(
                Key={'user_id': str(user_id)}
            )
            
            if 'Item' in response:
                item = response['Item']
                # Convert Decimal back to int for your bot
                return {
                    'id': int(item['user_id']),
                    'amount': int(item['amount']),
                    'workers': int(item['workers']),
                    'income': int(item['income']),
                    'gold': int(item['gold'])
                }
            else:
                return None
                
        except ClientError as e:
            print(f"Error getting user data: {e}")
            return None
    
    def update_user_data(self, user_id, **kwargs):
        """Update specific fields for a user"""
        table = self.get_table()
        
        # Build update expression
        update_expression = "SET "
        expression_values = {}
        
        for key, value in kwargs.items():
            if key in ['amount', 'workers', 'income', 'gold']:
                update_expression += f"{key} = :{key}, "
                expression_values[f":{key}"] = Decimal(str(value))
        
        # Remove trailing comma and space
        update_expression = update_expression.rstrip(', ')
        
        try:
            response = table.update_item(
                Key={'user_id': str(user_id)},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="UPDATED_NEW"
            )
            return True
        except ClientError as e:
            print(f"Error updating user data: {e}")
            return False
    
    def delete_user_data(self, user_id):
        """Delete user data"""
        table = self.get_table()
        
        try:
            response = table.delete_item(
                Key={'user_id': str(user_id)}
            )
            return True
        except ClientError as e:
            print(f"Error deleting user data: {e}")
            return False
    
    def get_all_users(self):
        """Get all users (for rankings, etc.)"""
        table = self.get_table()
        
        try:
            response = table.scan()
            items = response['Items']
            
            # Convert to your expected format
            users = []
            for item in items:
                users.append({
                    'id': int(item['user_id']),
                    'amount': int(item['amount']),
                    'workers': int(item['workers']),
                    'income': int(item['income']),
                    'gold': int(item['gold'])
                })
            
            return users
            
        except ClientError as e:
            print(f"Error scanning users: {e}")
            return []

# Convenience functions to maintain compatibility with existing code
def load_data():
    """Load all user data - DynamoDB version"""
    db = DynamoDBManager()
    users = db.get_all_users()
    
    # Convert to your current format
    data = {}
    for user in users:
        user_id = str(user['id'])
        data[user_id] = [user]  # Keep the list format for compatibility
    
    return data

def save_data(data):
    """Save data - DynamoDB version"""
    db = DynamoDBManager()
    
    for user_id, user_list in data.items():
        if user_list:  # If user has data
            user_data = user_list[0]  # Get the first (and only) entry
            db.put_user_data(
                user_data['id'],
                user_data['amount'],
                user_data['workers'],
                user_data['income'],
                user_data['gold']
            )
    
    return True
