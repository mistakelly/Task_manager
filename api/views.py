
# Views
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate

# Time
from django.utils.timezone import now

# Excempt csrf token
from django.views.decorators.csrf import csrf_exempt


# database
from .models import Task, Token
from django.contrib.auth.models import User
import json
from typing import Dict


# Custom imports
from .validators import validate_user_inputs
from .decorators import token_required


@csrf_exempt
def register(request: HttpRequest) -> JsonResponse:
    """
        register view function.
        accepts only post method
    """

    if request.method != 'POST':
        return JsonResponse({
            'error': 'Invalid request method',
            'message': 'Only POST method is allowed for register view.'
        }, status=405)

    # check the return type of the validate_user_inputs function, if its a JSONRESPONSE object, that means an error was returned, simply return the error.
    if isinstance(validate_user_inputs(request), JsonResponse):
        return validate_user_inputs(request)

    # if no error unpack the result
    username, password = validate_user_inputs(request)
    
    # check if user already exists
    if not User.objects.filter(username=username).first(): 

        user = User(username=username)
        user.set_password(password)  #hash user password
        user.save()

        # create token for user
        token = Token.objects.create(user=user)

        return JsonResponse({
            'token': token.key,
            'expires_at': token.expires_at.now().strftime('%Y-%m-%d T%H:%M:%SZ')
        }, status=201)
    

    return JsonResponse({'Error:': 'user already exists, kindly login with user auth token'}, status=400)



# LOGIN USER FUNCTION
def login(request: HttpRequest) -> JsonResponse:
    pass

@csrf_exempt
def refresh_token(request: HttpRequest) -> JsonResponse:

    if request.method != 'POST':
        return JsonResponse({
            'error': 'Invalid request method',
            'message': 'Only POST method is allowed for token refresh.'
        }, status=405)
            
    
    # check the return type of the validate_user_inputs function, if its a JSONRESPONSE object, that means an error was returned, simply return the error.
    if isinstance(validate_user_inputs(request), JsonResponse):
        return validate_user_inputs(request)

    # if no error unpack the result
    username, password = validate_user_inputs(request)

    # authenticate user
    user = authenticate(username=username, password=password)

    # return json response if user is none
    if not user:
        return JsonResponse({
            'error': 'Invalid credentials',
            'message': 'Username or password is incorrect.'
        }, status=401)
    
      
    # get old token
    old_token = user.auth_token

    # revoke user previous token.
    old_token.revoke_token(delete=True)

    # create new token
    new_token = Token.objects.create(user=user)


    return JsonResponse({
            'token': new_token.key,
            'expires_at': new_token.expires_at.now().strftime('%Y-%m-%d T%H:%M:%SZ')
        }, status=201)


@token_required
@csrf_exempt
def task_manager(request: HttpRequest) -> JsonResponse:
    print('inside task manager')
    method = request.method

    if request.method == 'GET':
        return JsonResponse({'GET': 'GET REQUEST'})
    elif method == 'POST':
        data = request.body
        try:
            data:Dict = json.loads(request.body.decode('utf-8')) #decode raw http body using utf-8 format then use json to parse decoded data.
            
            # extract data
            task_title      = data.get('title')
            task_content    = data.get('content')
            task_status     = data.setdefault('status', 'draft')

            print('title', task_title)
            print('content', task_content)
            print('status', task_status)
            print('data', data)

            # save task to database
            Task.objects.create(title=task_title, content=task_content, status=task_status)

            return JsonResponse(
                {
                    'title':    task_title, 
                    'content':  task_content,
                    'status':   task_status 
                }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid json format'}, status=400)
    
    elif method == 'PUT':
        return JsonResponse({'PUT': 'PUT REQUEST'})
    elif method == 'DELETE':
        return JsonResponse({'DELETE': 'DELETE REQUEST'})
    
    
    return JsonResponse({'welcome': 'Welcome to first api endpoint'})