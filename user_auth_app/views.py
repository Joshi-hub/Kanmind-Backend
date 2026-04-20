from django.shortcuts import render

class ContactListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer 
