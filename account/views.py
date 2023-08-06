from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# manual login user (fbv)
# def user_login(request):
#     if request.method == "POST":
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('home')
#                 else:
#                     return HttpResponse('user is not active')
#             else:
#                 return HttpResponse('user not found')
#
#     else:
#         form = forms.LoginForm()
#     return render(request, 'forms/../templates/registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))
