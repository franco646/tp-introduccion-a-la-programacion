# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user

def getAllImages(input=None): #Agregado por facu 20/06
    json_collection = transport.getAllImages(input)  # Trae el codigo ya hecho de imágenes desde transport(el input es para ingresar que foto queres en views[supuestamente])
    images = [] #Acá guarda las fotos despues cuando convierte lis archivos JSON en NASACards

    for obj in json_collection: #lee cada objeto en json_collection :v
        if 'data' in obj and 'links' in obj: #esto verifica si el objeto anterior tiene datos y links necesarios para crear una NASACard
            nasa_card = mapper.fromRequestIntoNASACard(obj)  # Convierte con magia los JSON a NASACard usando mapper
            images.append(nasa_card) #guarda las fotos(NASACards) en images

    return images


def getImagesBySearchInputLike(input):
    return getAllImages(input)


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = mapper.map_to_nasa_card(request)  # Transformar request del template en NASACard
    fav.user = get_user(request)  # Asignar usuario correspondiente
    
    return repositories.saveFavourite(fav) # lo guardamos en la base.


# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated:  #chequea si el usuario inició sesión
        return []  #si no hay usuario no hay favoritos xd
    else:
        user = get_user(request)  #si inició sesión manda la solicitud para mostrar favoritos

        favourite_list = []  # Tenemos una lista vacía para guardar los favoritos del usuario
        mapped_favourites = [] # Y acá una lista vacía donde se meten las NASACards mapeadas

        for favourite in favourite_list:
            nasa_card = '' # transformamos cada favorito en una NASACard, y lo almacenamos en nasa_card.
            mapped_favourites.append(nasa_card)

        return mapped_favourites


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.