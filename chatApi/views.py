from django.dispatch import receiver
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerilaizer, UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.decorators import api_view
from django.db.models import Q



# view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

# Views for get all the users
class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    def user_list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# views for getting a personal details
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)

  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# view for sending messsage
@api_view(["POST"])
def send_message(request):
    data = request.data
    username = data['username']
    
    try:
        recipient = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({ 
            "message":"User does not exist"
        })
    
    chat = Message.objects.create(
        sender=request.user, 
        receiver=recipient, 
        body=request.data["body"],  
    )
    serializer = MessageSerilaizer(instance=chat)
    return Response(serializer.data)


# view for getting a message
@api_view(["GET"])
def get_message(request, id):

    message = Message.objects.get(id=id)
    sender = Message.objects.filter(sender=request.user)
    receiver = Message.objects.filter(receiver=request.user)

    if sender :
        serializer = MessageSerilaizer(instance=message)
        return Response(({
            "LoggedIn user":request.user.username,
            "Messages":serializer.data   
        }))
    elif receiver:
        message.is_read_receipt = True
        serializer = MessageSerilaizer(instance=message)
        return Response(({
            "LoggedIn user":request.user.username,
            "Message":serializer.data   
        }))
    elif not sender or receiver:
        serializer = MessageSerilaizer(instance=message)
        return Response({
            "LoggedIn user":request.user.username,
            "data":"access denied, You can not view others message"
        })


# view for getting all message
@api_view(["GET"])
def get_messages(request):

    messages= Message.objects.filter(
        Q(sender = request.user) |
        Q(receiver = request.user)
    )
    
    if messages:
        serializer = MessageSerilaizer(instance=messages, many=True)
        return Response({
            "LoggedIn user":request.user.username,
            "All Messages":serializer.data   
        })

    else:
        return Response({
        "Message":"You haven't send nor received any messages"
        })

