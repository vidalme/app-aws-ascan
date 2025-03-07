import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todo-ascan-table')
counter_table = dynamodb.Table('TaskId')

def get_tasks():
    response = table.scan()
    print(get_next_user_id())
    return response.get('Items', [])


def get_next_user_id():
    return max( todo.TaskId for todo in get_tasks() ) + 1 


print(get_tasks()[1]['Task'])


def add_task(task_description):
    user_id = str(get_next_user_id())  # Use the auto-increment logic
    table.put_item(
        Item={
            'UserId': user_id,
            'task': task_description,
            'priority': 'low',
            'done': False
        }
    )
    return user_id

# def remove_task(user_id):
#     table.delete_item(Key={'UserId': user_id})

# def update_task(user_id, done):
#     table.update_item(
#         Key={'UserId': user_id},
#         UpdateExpression="SET done = :done",
#         ExpressionAttributeValues={":done": done}
#     )