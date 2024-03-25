from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import CreateBlog, Comment
from .forms import BlogForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from TP_blog import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import force_bytes , force_text 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken

class List(ListView):
    template_name = 'blog/index.html'
    queryset = CreateBlog.objects.all()
    paginate_by = 2

@login_required

def detailView(request,slug):
    post=CreateBlog.objects.get(slug=slug)
    comments=post.comments.all()
    if request.method=='POST':
        form=BlogForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.post=post
            form.save()
            return redirect('detailView',slug=post.slug)
    else:
        form=BlogForm
    content={
        'article':post,
        'comments':comments,
        'form':form,
    }
    return render(request,'blog/update.html',content)

def maison(request):
    return render(request, 'blog/acceuil.html')


def register(request):   
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        
        if User.objects.filter(username=username):
            messages.error(request, "Ce nom d'utilisateur est déjà pris, veuillez en choisir un autre.")
            return redirect('register')
        
        if User.objects.filter(email=email):
            messages.error(request, "Cette adresse e-mail est déjà associée à un compte.")
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, "Revoyez les caractères que vous venez d'entrer pour le nom d'utilisateur.")
            return redirect('register')
        
        if password != password1:
            messages.error(request, "Vous n'avez pas bien confirmé votre mot de passe.")
            return redirect('register')
        
        mon_utilisateur = User.objects.create_user(username, email, password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.is_active = False
        mon_utilisateur.save()
        
        messages.success(request, "Votre compte est enregistré avec succès.")
        # Envoi d'email de bienvenue
        subject = "Bienvenue sur notre blog : le blog des vampires"
        message = f"Bienvenue {mon_utilisateur.first_name} {mon_utilisateur.last_name}\nNous sommes ravis de vous compter parmi nous.\n\n\nMerci\nL'équipe technique"
        from_email = settings.EMAIL_HOST_USER
        to_list = [mon_utilisateur.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        # Email de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmation de votre inscription sur : le blog des vampires"
        messageConfirm = render_to_string("emailcomfirm.html", {
            "name": mon_utilisateur.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
            "token": generatorToken.make_token(mon_utilisateur)
        })
        
        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [mon_utilisateur.email],   
        )
        email.fail_silently = False
        email.send()
        
        return redirect('login')
        
    return render(request, 'blog/register.html')


def logIn(request):    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirection vers la page des articles
            return redirect('home')
        else:
            messages.error(request, 'Mauvaise authentification')
            return redirect('login')  # Redirection vers la page de connexion en cas d'erreur
        
    return render(request, 'blog/login.html')


@login_required
def logOut(request):
    logout(request)
    messages.success(request, 'Vous avez été bien déconnecté !!')
    return redirect('maison')

def activate(request , uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError ,User.DoesNotExist):
        user = None
        
    if user is not None and generatorToken.check_token(user , token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte a bien été activé, félicitation, connectez-vous maintenant.")
        return redirect('login')
    
    else:
        messages.error(request, "L'activation a échoué, veuillez réessayer !!")
        return redirect('maison')
