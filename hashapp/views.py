import json
from django.shortcuts import render
from django.http import JsonResponse
from .serializers import user_serializer
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from .models import Users
from .passwords import password_hash
import jwt
import datetime
from django.conf import settings
SECRET_KEY = settings.SECRET_KEY
# Create your views here.

def home_page(request):
    # return JsonResponse({'status':200})
    # session
    # if request.session.get('location') == 'India':
    #     return JsonResponse({'status' : 200,'message':'show india'})
    
    # token
    try:
        auth_token = request.headers.get('Authorization') #'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImhhcnJ5cG90dGVyNiIsImxvY2F0aW9uIjoiSW5kaWEiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3NjM3NDIxODh9.O2kECmZW-PllG8dXp2nmtJq4zeZUy3e5RLTI68cTDJs',
        auth_token = auth_token.split(' ')[1] # get token
        
        user_info = jwt.decode(auth_token,SECRET_KEY,algorithms='HS256')
        print(user_info)
        
    except Exception as e:
          return JsonResponse({'error':"user failed"})
    
    loc = user_info['location']
      
    
    return JsonResponse({'status' : 200,'message':'show home page' + 'of' + loc})
    
    

@csrf_exempt
def register(request):
    serializer_data = json.loads(request.body)
    
    
    u1 = user_serializer(data=serializer_data)
    
    if u1.is_valid():
        print(u1.validated_data)
        # received_password =u1.validated_data['password'].encode('utf-8')
        # salt = bcrypt.gensalt(rounds=12)
        # hashed_passowrd = bcrypt.hashpw(received_password,salt)
        hashed_password = password_hash(u1.validated_data['password'])
        u1.validated_data['password'] = hashed_password.decode('utf-8')
        # u1.validated_data['password'] = 'abc'
        
        # s=serializer_data.get('password')
        # print(s)
        u1.save()
        return JsonResponse({'status':'user_created','data':u1.data})
    
    else:
        return JsonResponse(u1.errors)
    
@csrf_exempt    
def login(request):
    # cookies
    # if 'is_logged_in' in request.COOKIES:
    #     message ='you are already logged in' + request.COOKIES.get('username')
    #     return JsonResponse({'status':200,'message':message})
    
    # session id
    # if request.session.get('username'):
    #     username =request.session.get('username')
    #     return JsonResponse({
    #         "status":"you are logged in" + username
    #     })
    data = json.loads(request.body)
    try:
        u1=Users.objects.get(username=data['username'])
    except Exception as e:
        return JsonResponse({'error' : 'usernotfound'})
    
    entered_password = data['password']
    database_password = u1.password
    
    if bcrypt.checkpw(entered_password.encode('utf-8'),database_password.encode('utf-8')):# second argument expect as salt
        # return JsonResponse({'status':200})
        # set cookies
        # response = JsonResponse({'status':200})
        # response.set_cookie(
        #     key = 'username',
        #     value = data['username'],
        #     max_age = 3600
        # )
        # response.set_cookie(
        #     key = 'is_logged_in',
        #     value = 'true',
        #     max_age = 3600
        # )
        
        #token
        data = {
            'username' : u1.username,
            'location' : 'India',
            'role':'admin',
            #isuued at
            'iat':datetime.datetime.now(datetime.timezone.utc)
        }
        
        token = jwt.encode(data,SECRET_KEY,algorithm='HS256')
        
        response=JsonResponse({'status':200,'user_token':token})
        # request.session['username'] =u1.username
        # request.session['location']= 'india'
        return response
    return JsonResponse({'status':'login_failed'})

@csrf_exempt
def update(request):
    data = json.loads(request.body)
    
    try:
        u1=Users.objects.get(username = data.get('username'))
    except Exception as e:
        return JsonResponse({'error':'user not found'})
    
    sent_password = data.get('password').encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(sent_password,salt)
    data['password'] = hashed_password.decode() # hashpassword usually cames bytes so we convert into string
    
    u1 = user_serializer(u1,data=data,partial=True)
    if u1.is_valid():
        u1.save()
        return JsonResponse({'status':'password changed'})
    else:
        return JsonResponse(u1.errors)
        
    
    
        


    
        
    
    
    
    
    


    

