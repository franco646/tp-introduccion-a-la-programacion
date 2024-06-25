# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py
import math

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator

Q_IMAGES_PER_PAGE = 10  # Define la cantidad de imágenes por página

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request) if request.user.is_authenticated else []


    if request.user.is_authenticated:
        uninteresting_images = services_nasa_image_gallery.getUninterestingImagesByUser(request.user)
        images = [img for img in images if img not in uninteresting_images]

    return images, favourite_list

# función principal de la galería.
def home(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)

    page = int(request.GET.get('page', '1')) # obtiene el numeor de pagina actual
    
    paginator = Paginator(images, Q_IMAGES_PER_PAGE) # Utiliza el Paginator de Django para manejar la paginación
    
    filtered_images = paginator.page(page) # Obtiene las imágenes para la página actual
    
    return render(request, 'home.html', {
        'images': filtered_images,
        'favourite_list': favourite_list,
        'page': page,
        'q_pages': range(1, paginator.num_pages + 1),
    })

# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)

    search_msg = request.POST.get("search_msg", "") if request.method == 'POST' else request.GET.get("search_msg", "")
    
    if search_msg != "":
        searched_images = services_nasa_image_gallery.getImagesBySearchInputLike(search_msg)
        if request.user.is_authenticated:
            uninteresting_images = services_nasa_image_gallery.getUninterestingImagesByUser(request.user)
            searched_images = [img for img in searched_images if img not in uninteresting_images]

        page = int(request.GET.get('page', '1'))

        paginator = Paginator(searched_images, Q_IMAGES_PER_PAGE)

        filtered_images = paginator.page(page)

        return render(request, "home.html", {
            "images": filtered_images, 
            "favourite_list": favourite_list, 
            'q_pages': range(1, paginator.num_pages + 1), 
            'page': page,
            'search_msg': search_msg})
    else:
        return redirect("home")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return home(request)
        else:
            return render(request, "registration/login.html", { "error": "Usuario o contraseña incorrectos" })
    else:
        return render(request, "registration/login.html")
        
def logout_view(request):
    logout(request)
    return render(request, "registration/login.html")

def signup_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]  
        repeat_password = request.POST["repeat_password"]  

        if password != repeat_password:
            return render(request, "registration/signup.html", { 'error': 'Las contraseñas deben coincidir' }) 

        user_already_exists = User.objects.filter(username=username).exists()

        if user_already_exists:
            return render(request, "registration/signup.html", { 'error': 'El nombre de usuario ya existe' }) 

        user = User.objects.create_user(username, None, password)
        user.save()

        return redirect('login')
    else:
        return render(request, "registration/signup.html")


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})



@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services_nasa_image_gallery.saveFavourite(request)
    return redirect('favoritos')


@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services_nasa_image_gallery.deleteFavourite(request)
    return redirect('favoritos')


@login_required
def exit(request):
    logout(request)
    return redirect('login')


@login_required
def markUninteresting(request):
    if request.method == 'POST':
        services_nasa_image_gallery.markImageAsUninteresting(request)
    return redirect('home')