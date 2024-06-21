# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py
import math

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request) if request.user.is_authenticated else []
    return images, favourite_list

# función principal de la galería.
def home(request, images_filtered=None):
    Q_IMAGES_PER_PAGE = 10 # define la cantidad de imagagenes que va a haber por cada pagina
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    if not images_filtered:
        images, favourite_list = getAllImagesAndFavouriteList(request)  #acá me esta dando las imagenes para mostrar en el inicio
    else:
        images = images_filtered
        favourite_list = []
    
    page = int(request.GET.get('page', '') or 1) # obtiene la pagina actual que es pasada a traves de un query, en caso de que no esté definido toma 1
    q_pages = math.ceil(len(images) / Q_IMAGES_PER_PAGE) # define la cantidad de paginas, dividiendo la cantidad de images por la cantidad de imagenes que deben mostrarse en cada pagina y rendondea para arriba

    filtered_images = []
    for i in range(Q_IMAGES_PER_PAGE * (page - 1), Q_IMAGES_PER_PAGE * (page - 1) + Q_IMAGES_PER_PAGE): 
        if i < len(images) and not i > len(images): # Si "i" está dentro del len(images) agrega la imagen[i] a la lista vacia
            filtered_images.append(images[i])
        else: # si está fuera del rango termina el ciclo
            break

    return render(request, 'home.html', {'images': filtered_images, 'favourite_list': favourite_list, 'q_pages': range(1, q_pages + 1)})


# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get("query", "")

    if search_msg != "":
        images_filtered = services_nasa_image_gallery.getImagesBySearchInputLike(search_msg)
        return home(request, images_filtered)
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
            return render(request, "registration/login.html", { "error": "El usuario no existe" })
    else:
        return render(request, "registration/login.html")
        
def logout_view(request):
    logout(request)
    return render(request, "registration/login.html")


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})



@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services_nasa_image_gallery.saveFavourite(request)
    return redirect('home')


@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services_nasa_image_gallery.deleteFavourite(request)
    return redirect('favoritos')


@login_required
def exit(request):
    logout(request)
    return redirect('login')