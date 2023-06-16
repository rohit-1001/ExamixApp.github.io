from django.shortcuts import render,redirect
from face_detection.detection import FaceRecognition
from .forms import *
from django.contrib import messages
from backendapp.models import student

faceRecognition = FaceRecognition()

# def home(request):
#     return render(request,'faceDetection/home.html')


# def register(request):
#     if request.method == "POST":
#         form = ResgistrationForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             print("IN HERE")
#             messages.success(request,"SuceessFully registered")
#             print(request.POST['face_id'])
#             addFace(request.POST['face_id'])
#             # face_id = request.POST.get('face_id', [])
#             redirect('/face/')
#         else:
#             messages.error(request,"Account registered failed")
#     else:
#         form = ResgistrationForm()

#     return render(request, 'faceDetection/register.html', {'form':form})

def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('/face/')

def login():
    face_id = int(faceRecognition.recognizeFace())
    print("face_id in login function: ",face_id)
    # return redirect('/face/greeting/' ,str(face_id))
    return face_id

# def Greeting(request,face_id):
#     face_id = int(face_id)
#     context ={
#         'user' : student.objects.get(username = face_id)
#     }
#     return render(request,'faceDetection/greeting.html',context=context)

