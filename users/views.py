from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.utils import translation
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm

# --- REGISTRATSIYA ---
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'users/register.html', {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'users/register.html', {'form': form})

# --- LOGIN ---
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'users/login.html', {'form': AuthenticationForm()})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Profilidagi tilni aniqlash va aktivlashtirish
            try:
                lang = user.profile.language
                translation.activate(lang)
                request.session[translation.LANGUAGE_SESSION_KEY] = lang
                
                response = redirect('dashboard')
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
                return response
            except:
                return redirect('dashboard')
        
        return render(request, 'users/login.html', {'form': form})

# --- TILNI TEZKOR O'ZGARTIRISH (Masalan, tepadagi menyudan) ---
class SetLanguageView(LoginRequiredMixin, View):
    def post(self, request):
        lang_code = request.POST.get('language')
        if lang_code in [lang[0] for lang in settings.LANGUAGES]:
            # Profilni yangilash
            profile = request.user.profile
            profile.language = lang_code
            profile.save()
            
            # Tilni aktivlashtirish
            translation.activate(lang_code)
            request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
            
            response = redirect(request.META.get('HTTP_REFERER', 'dashboard'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            return response
            
        return redirect('dashboard')

# --- PROFILNI KO'RISH ---
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile_view.html')

# --- PROFILNI TAHRIRLASH (Til muammosi hal qilingan variant) ---
class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'users/profile_update.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save()
            user_language = profile.language 
            
            # 1. Tilni aktivlashtirish
            translation.activate(user_language)
            
            # 2. Redirect javobini tayyorlash
            response = redirect('profile_update') 
            
            # 3. Sessiyani yangilash (Django standart kaliti orqali)
            request.session['_language'] = user_language            
            # 4. Kuki (Cookie) ni yangilash - Brauzer tilni eslab qolishi uchun
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
            
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return response
            
        return render(request, 'users/profile_update.html', {'form': form})

# --- PAROLNI O'ZGARTIRISH ---
class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'users/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Sessiya uzilib qolmasligi uchun
            messages.success(request, "Parolingiz o'zgartirildi!")
            return redirect('profile_view')
        return render(request, 'users/change_password.html', {'form': form})

# --- CHIQISH ---
class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')