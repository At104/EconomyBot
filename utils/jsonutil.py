import json
from .dynamodb_manager import DynamoDBManager

# -- Functions dealing with data storage -- #
# Updated to use DynamoDB instead of JSON files

def read_json_file(filename: str) -> dict:
    """ 
    Load all user data from DynamoDB 
    Maintains compatibility with existing code that expects JSON format
    """
    try:
        # If it's the DataHolding.json file, use DynamoDB
        if 'DataHolding' in filename:
            db = DynamoDBManager()
            users = db.get_all_users()
            
            # Convert to your current format for compatibility
            data = {}
            for user in users:
                user_id = str(user['id'])
                data[user_id] = [user]  # Keep the list format for compatibility
            
            return data
        else:
            # For other files, still use JSON
            with open(filename, 'r') as json_file:
                json_decoded = json.load(json_file)
                json_file.close()
            return json_decoded
            
    except Exception as e:
        print(f"ERROR: Could not read data. {e}")
        return {}

def write_json_file(filename: str, data: dict) -> None:
    """ 
    Save data to DynamoDB 
    Maintains compatibility with existing code 
    """
    try:
        # If it's the DataHolding.json file, use DynamoDB
        if 'DataHolding' in filename:
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
        else:
            # For other files, still use JSON
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
                json_file.close()
                
    except Exception as e:
        print(f"ERROR: Could not save data. {e}")


