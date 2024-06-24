# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user

def getAllImages(input=None): #Agregado por facu 20/06
    json_collection = transport.getAllImages(input)  # Trae el codigo ya hecho de imágenes desde transport(el input es para ingresar que foto queres en views[supuestamente])
    images = [] #Acá guarda las fotos despues cuando convierte lis archivos JSON en NASACards

    for obj in json_collection: #lee cada objeto en json_collection :v
        if 'data' in obj and 'links' in obj and 'description' in obj['data'][0]: #esto verifica si el objeto anterior tiene datos y links necesarios para crear una NASACard
            nasa_card = mapper.fromRequestIntoNASACard(obj)  # Convierte con magia los JSON a NASACard usando mapper
            images.append(nasa_card) #guarda las fotos(NASACards) en images

    return images


def getImagesBySearchInputLike(input):
    return getAllImages(input)


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = mapper.fromTemplateIntoNASACard(request)  # Transformar request del template en NASACard
    fav.user = get_user(request)  # Asignar usuario correspondiente
    fav.comment = request.POST.get("comment", "")
    return repositories.saveFavourite(fav)  # lo guardamos en la base.


# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    user = get_user(request)
    favourites = repositories.getAllFavouritesByUser(user)
    return [mapper.fromRepositoryIntoNASACard(fav) for fav in favourites]


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.


def markImageAsUninteresting(request):
    image = mapper.fromTemplateIntoNASACard(request)
    image.user = get_user(request)
    return repositories.saveUninterestingImage(image)


def getUninterestingImagesByUser(user):
    uninteresting_images = repositories.getUninterestingImagesByUser(user)
    return [mapper.fromRepositoryIntoNASACard(img) for img in uninteresting_images]