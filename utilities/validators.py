from django.http import JsonResponse
import json

# VALIDATE USER INPUTS FUNCTION
def validate_user_inputs(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Json Format'}, status=400)

     # Using Python's walrus operator (:=) to check and assign values in a single expression
    if not (username := data.get('username')):
        return JsonResponse({'error': 'username cannot be null'}, status=400)

    if not (password := data.get('password')):
        return JsonResponse({'error': 'password cannot be null'}, status=400)
    

    
    return username, password


# VALIDATE TASK INPUTS
def validate_task_inputs(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Json Format'}, status=400)
    
     # validate and Extract data using python warlus operator.
    if not (title := data.get('title')):
        return JsonResponse({'error': 'Title cannot be null or empty.'}, status=400)

    if not (description := data.get('description')):
        return JsonResponse({'error': 'Description cannot be null or empty.'}, status=400)

    status = data.get('status')

    if status not in ['in-progress', 'completed', 'pending']:
        return JsonResponse({'error': 'Invalid status. Must be one of: in-progress, completed, pending.'}, status=400)

    if not (owner_id := data.get('owner')):
        return JsonResponse({'error': 'Owner ID cannot be null or empty.'}, status=400)
    

    return title, description, status, owner_id