from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from requests import session
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.shortcuts import redirect
from face_detection import views as face_views
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
from django.db import connection
import json
from collections import OrderedDict
from proctoring import run
import threading as th
import cv2
import os
import base64

from backendapp.models import student
from backendapp.models import teacher
from backendapp.models import question
from backendapp.models import result
from backendapp.models import marks
from backendapp.serializers import userSerializer
import sys
import threading as th
stop_event = th.Event()
cheat_event = th.Event()

# run_thread = th.Thread(target=run.main)
# run_thread = th.Thread(target=run.main, args=(stop_event, cheat_event, user_name, quiz_id), name="Thread")
@csrf_exempt
# def register(request):
#     if request.method=='GET':
#         ud=user_data.objects.all()
#         ud_serializer=userSerializer(ud, many=True)
#         return JsonResponse(ud_serializer.data, safe=False)
#     elif request.method=='POST':
#         ud_data=JSONParser().parse(request)
#         ud_serializer=userSerializer(data=ud_data)
#         if ud_serializer.is_valid():
#             ud_serializer.save()
#             return JsonResponse("Added successfully", safe=False)
#         return JsonResponse("Failed to add", safe=True)
#     elif request.method=='PUT':
#         ud_data=JSONParser().parse(request)
#         ud=user_data.objects.get(email=ud_data['email'])
#         ud_serializer=userSerializer(ud, data=ud_data)
#         if ud_serializer.is_valid():
#             ud_serializer.save()
#             return JsonResponse('Update successful', safe=False)
#     elif request.method=='DELETE':
#         ud=user_data.objects.get()
#         ud.delete()
#         return JsonResponse('Delete successful', safe=False)
    
def index(request):
    return render(request, 'index.html')
@csrf_exempt
def landingpage2(request):
    # text=request.GET.get('text')
    # print('The text received in landingpage2 method is: ',text)
    if 'session_key' in request.session:
        return render(request, 'index.html')
    else:
        return redirect('/app/login_page/')
@csrf_exempt 
def landingpage1(request):
    # text=request.GET.get('text')
    # print('The text received in landingpage2 method is: ',text)
    if 'session_key' in request.session:
        return render(request, 'index.html')
    else:
        return redirect('/app/login_page/')

@csrf_exempt
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        branch=request.POST.get('branch')
        phone=request.POST.get('phone')
        year=request.POST.get('year')
        
        data=student(name=name, username=username, email=email, password=password, branch=branch, phone=phone, year=year)
        data.save()
        face_views.addFace(username)
        # return redirect('/app/login/')
        print("Successfully registered")
        return redirect('/app/login_page/')
    else:
        # return redirect('/app/register/')
        return render(request, 'index.html')
    
@csrf_exempt
def login(request):
    global user_name
    username=request.POST.get('username')
    password=request.POST.get('password')
    
    print('post request part executed')
    user = student.objects.filter(username=username, password=password).exists()
    face_id=face_views.login()
    username=int(username)
    if user and (face_id==username):
        user_name=username
        print("Successful part executed")
        request.session['session_key']=username
        request.session['user_name'] = username
        return redirect('/app/landingpage2/')
        # text= 'hello this is some text'
        # return redirect('/app/landingpage2/?text={}'.format(text))
        # return redirect('/app/login_page/')
    else:
        print("Unsuccessful part executed")
        return redirect('/app/login_page/')
        # return HttpResponseRedirect('/app/login_page/')
        # return redirect('backendapp:login_page')
   
@csrf_exempt     
def teacher_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    
    print('post request part executed')
    user = teacher.objects.filter(username=username, password=password).exists()
    if user:
        print("Successful part executed")
        request.session['session_key']=username
        return redirect('/app/landingpage1/')
        # return redirect('/app/login_page/')
    else:
        print("Unsuccessful part executed")
        return redirect('/app/login_page/')
        # return HttpResponseRedirect('/app/login_page/')
        # return redirect('backendapp:login_page')
@csrf_exempt   
def logout(request):
    if 'session_key' in request.session:
        stop_event.set()
        cheat_event.set()
        del request.session['session_key']
        request.session.save()
        print("i am logout function")
        return redirect('/')
    else:
        return redirect('/')

@csrf_exempt
def login_page(request):
    return render(request, 'index.html')

@csrf_exempt
def questions(request):
    if request.method=='POST':
        data=request.POST
        n=len(data.getlist('QuestionNumber'))
        # <QueryDict: {'quizid': ['100'], 'QuestionNumber': ['1', '2', '0'], 'Question': ['q1', 'q2', 'q0'], 'option1': ['o11', 'o21', 'q01'], 'option2': ['o12', 'o22', 'q02'], 'option3': ['o13', 'o23', 'q03'], 'option4': ['o14', 'o24', 'q04'], 'answer': ['0', '4', '3']}>
        print(data, n)
        for i in range(0,n):
            quiz_id=data.getlist('quizid')[0]
            quiz_desc=data['quiz_desc']
            QuestionNumber=data.getlist('QuestionNumber')[i]
            Question=data.getlist('Question')[i]
            option1=data.getlist('option1')[i]
            option2=data.getlist('option2')[i]
            option3=data.getlist('option3')[i]
            option4=data.getlist('option4')[i]
            answer=data.getlist('answer')[i]
            que=question(quizid=quiz_id, quiz_desc=quiz_desc, question_no=QuestionNumber, question=Question, option1=option1, option2=option2, option3=option3, option4=option4, answer=answer)
            que.save()
        return redirect('/app/landingpage1/')
    else:
        return render(request, 'index.html')

def exam_t(request):
    print("I am exam function")
    # data = list(question.objects.all().values())
    username=request.session['session_key']
    data = list(question.objects.values_list('quizid', 'quiz_desc').distinct())
    print("data from exam function is: ",data)
    # n=len(data.getlist('QuestionNumber'))
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT DISTINCT quizid FROM backendapp_question")
    #     results = cursor.fetchall()
    #     normal_list = [tup[0] for tup in results]
    # data={
    #     "data": [
    #         {"id": 1, "name": "John"},
    #         {"id": 2, "name": "Jane"},
    #         {"id": 3, "name": "Bob"}
    #     ]
    # }

    # print(data)
    # data='This is quiz'
    return JsonResponse(data, safe=False)

def exam(request):
    print("I am exam function")
    # data = list(question.objects.all().values())
    username=request.session['session_key']
    data = list(question.objects.values_list('quizid', 'quiz_desc').distinct())
    res=list(marks.objects.filter(username=username).values_list('quizid', flat=True).distinct())
    questions_not_in_marks = question.objects.exclude(quizid__in=res)
    data_not_in_marks = list(questions_not_in_marks.values_list('quizid', 'quiz_desc').distinct())
    print("data from exam function is: ",data_not_in_marks)
    # n=len(data.getlist('QuestionNumber'))
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT DISTINCT quizid FROM backendapp_question")
    #     results = cursor.fetchall()
    #     normal_list = [tup[0] for tup in results]
    # data={
    #     "data": [
    #         {"id": 1, "name": "John"},
    #         {"id": 2, "name": "Jane"},
    #         {"id": 3, "name": "Bob"}
    #     ]
    # }

    # print(data)
    # data='This is quiz'
    return JsonResponse(data_not_in_marks, safe=False)

def exam_created(request):
    print("I am exam function")
    data = list(question.objects.values_list('quizid', 'quiz_desc').distinct())
    return JsonResponse(data, safe=False)

@csrf_exempt
def attemp_quiz(request):
    quiz_id = request.POST.get("quiz_id")
    request.session['quiz_id']=quiz_id
    return redirect('/app/test_portal/')

@csrf_exempt
def view_quiz(request):
    quiz_id = request.POST.get("quiz_id")
    request.session['quiz_id']=quiz_id
    return redirect('/app/test_que/')

@csrf_exempt
def view_selected_responses(request):
    if request.method=='POST':
        user_name = request.POST.get("user_name")
        request.session['user_name']=user_name
    return redirect('/app/selected_responses/')

@csrf_exempt
def view_my_responses(request):
    if request.method=='POST':
        quiz_id = request.POST.get("quiz_id")
        request.session['quiz_id']=quiz_id
    return redirect('/app/selected_responses_stu/')

@csrf_exempt
def view_selected_responses_stu(request):
    if request.method=='POST':
        user_name = request.POST.get("user_name")
        request.session['user_name']=user_name
    return redirect('/app/selected_responses_stu/')

@csrf_exempt
def view_selected_responses_r(request):
    # quiz_id = request.POST.get("quiz_id")
    # user_name=request.session['session_key']
    # data = list(result.objects.filter(quizid=quiz_id, username=user_name).values('question_no', 'selected', 'actual', 'result'))
    # return JsonResponse(data, safe=False)
    quiz_id = request.session['quiz_id']
    user_name = request.session['user_name']
    score = list(marks.objects.filter(quizid=quiz_id, username=user_name).values_list('marks', flat=True))
    quiz_status = list(marks.objects.filter(quizid=quiz_id, username=user_name).values_list('quiz_status', flat=True))
    myList = list(
        result.objects.filter(username=user_name, quizid=quiz_id).values_list('question_no', 'selected', 'actual', 'result'))
    for s in score:
        print("The value of score is:",s)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(BASE_DIR,'../proctoring/Cheating')
    images = []
    x=1
    for filename in os.listdir(folder_path):
        image_name = 'User.' + str(user_name) + '.' + str(quiz_id) + '.' + str(x) + '.jpg'
        file_path = os.path.join(folder_path, image_name)
        if os.path.isfile(file_path):
            image = cv2.imread(file_path)
            if image is not None:
                with open(file_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                images.append(encoded_string)
                x=x+1
    print('length of images', len(images))
    data = {
        'myList': myList,
        'score': score,
        'quiz_status': quiz_status,
        'images': images,
    }
    # print("view_selected_responses_r func= ", data)
    return JsonResponse(data, safe=False)

def test(request):
    global run_thread
    global stop_event
    global cheat_event
    quiz_id=request.session['quiz_id']
    user_name = request.session['user_name']
    questions = list(question.objects.filter(quizid=quiz_id).values('quizid', 'quiz_desc', 'question_no', 'question', 'option1', 'option2', 'option3', 'option4' ))
    print("questions is test func= ",questions)
    # main_thread()
    stop_event = th.Event()
    cheat_event = th.Event()
    run_thread = th.Thread(target=run.main, args=(stop_event, cheat_event, user_name, quiz_id), name="Thread")
    run_thread.start()
    return JsonResponse(questions, safe=False)

def view_test(request):
    global run_thread
    quiz_id=request.session['quiz_id']
    request.session['user_name'] = request.session['session_key']
    questions = list(question.objects.filter(quizid=quiz_id).values('quizid', 'quiz_desc', 'question_no', 'question', 'option1', 'option2', 'option3', 'option4', 'answer'))
    print("questions is test func= ",questions)
    return JsonResponse(questions, safe=False)

# def main_thread():
#     while True:
#         run_thread.start()
#
#         if stop_event.is_set():
#             break


@csrf_exempt
def answers(request):
    a=0
    stop_event.set()
    quiz_id=request.session['quiz_id']
    username=request.session['session_key']
    option1_selected = request.POST.getlist('option1')
    option2_selected = request.POST.getlist('option2')
    option3_selected = request.POST.getlist('option3')
    option4_selected = request.POST.getlist('option4')
    
    option1_actual = question.objects.filter(quizid=quiz_id, answer=1).values_list('question_no', flat=True)
    option2_actual = question.objects.filter(quizid=quiz_id, answer=2).values_list('question_no', flat=True)
    option3_actual = question.objects.filter(quizid=quiz_id, answer=3).values_list('question_no', flat=True)
    option4_actual = question.objects.filter(quizid=quiz_id, answer=4).values_list('question_no', flat=True)
    
    # print(option1_selected," option1_selected")
    # print(option2_selected," option2_selected")
    # print(option3_selected," option3_selected")
    # print(option4_selected," option4_selected")
    # print(option1_actual," option1_actual")
    # print(option2_actual," option2_actual")
    # print(option3_actual," option3_actual")
    # print(option4_actual," option4_actual")
    
    # print("opt1 sel= ",option1_selected[0])
    # print("opt1 act= ", option1_actual[0])
    
    n=len(option1_selected)+len(option2_selected)+len(option3_selected)+len(option4_selected)
    for i in option1_selected:
        i=int(i)
        if i in option1_actual:
            data=result(username=username, quizid=quiz_id, question_no=i, selected=1, actual=1, result=1)
            data.save()
        else:
            if i in option2_actual:
                a=2
            elif i in option3_actual:
                a=3
            elif i in option4_actual:
                a=4
            data=result(username=username, quizid=quiz_id, question_no=i, selected=1, actual=a, result=0)
            data.save()
                
    for i in option2_selected:
        i=int(i)
        if i in option2_actual:
            data=result(username=username, quizid=quiz_id, question_no=i, selected=2, actual=2, result=1)
            data.save()
        else:
            if i in option1_actual:
                a=1
            elif i in option3_actual:
                a=3
            elif i in option4_actual:
                a=4
            data=result(username=username, quizid=quiz_id, question_no=i, selected=2, actual=a, result=0)
            data.save()
    
    for i in option3_selected:
        i=int(i)
        if i in option3_actual:
            data=result(username=username, quizid=quiz_id, question_no=i, selected=3, actual=3, result=1)
            data.save()
        else:
            if i in option1_actual:
                a=1
            elif i in option2_actual:
                a=2
            elif i in option4_actual:
                a=4
            data=result(username=username, quizid=quiz_id, question_no=i, selected=3, actual=a, result=0)
            data.save()
    for i in option4_selected:
        i=int(i)
        if i in option4_actual:
            data=result(username=username, quizid=quiz_id, question_no=i, selected=4, actual=4, result=1)
            data.save()
        else:
            if i in option1_actual:
                a=1
            elif i in option2_actual:
                a=2
            elif i in option3_actual:
                a=3
            data=result(username=username, quizid=quiz_id, question_no=i, selected=4, actual=a, result=0)
            data.save()
    data = result.objects.filter(username=username, quizid=quiz_id)
    mark=0
    for i in data:
        if i.result==1:
            mark+=1
    if stop_event.is_set() and cheat_event.is_set():
        return redirect('/app/landingpage2/')
    else:
        quiz_desc = question.objects.filter(quizid=quiz_id).values('quiz_desc')
        data = marks(username=username, quizid=quiz_id, quiz_desc=quiz_desc, quiz_status='Successful', marks=mark)
        data.save()
        return redirect('/app/view_selected_responses_stu/')

@csrf_exempt
def responses(request):
    data = request.POST
    request.session['quiz_id']=data['quiz_id']
    return redirect('/app/stu_resp/')

@csrf_exempt
def stu_responses(request):
    quiz_id=request.session['quiz_id']
    username = request.session['session_key']
    data=list(marks.objects.filter(quizid=quiz_id).values_list('username', 'marks', 'quiz_status'))
    print("stu_responses func= ", data)
    return JsonResponse(data, safe=False)


# def marks(request):
#     quiz_id=request.session['quiz_id']
#     username=request.session['session_key']
#     data = result.objects.filter(username=username, quizid=quiz_id)
#     mark=0
#     for i in data:
#         if i.result==1:
#             mark+=1
#     return mark

def value_checker(request):
    if cheat_event.is_set() and stop_event.is_set():
        quiz_id = request.session['quiz_id']
        username = request.session['session_key']
        quiz_desc = question.objects.filter(quizid=quiz_id).values('quiz_desc')
        data = marks(username=username, quizid=quiz_id, quiz_desc=quiz_desc, quiz_status='Aborted', marks=0)
        data.save()
        data = {'value': True}
        return JsonResponse(data)
    else:
        data = {'value': False}
        return JsonResponse(data)

def my_quizzes(request):
    user_name = request.session['session_key']
    data = list(marks.objects.filter(username=user_name).values_list('quizid', 'marks', 'quiz_status'))
    print("data from my_quizzes : ",data)
    return JsonResponse(data, safe=False)