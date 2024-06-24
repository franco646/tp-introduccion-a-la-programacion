# capa DAO de acceso/persistencia de datos.

from nasa_image_gallery.models import Favourite, UninterestingImage

def saveFavourite(image):
    try:
        fav = Favourite.objects.create(title=image.title, description=image.description, image_url=image.image_url, date=image.date, user=image.user, comment=image.comment)
        return fav
    except Exception as e:
        print(f"Error al guardar el favorito: {e}")
        return None

def getAllFavouritesByUser(user):
    favouriteList = Favourite.objects.filter(user=user).values('id', 'title', 'description', 'image_url', 'date', 'comment')
    return list(favouriteList)

def deleteFavourite(id):
    try:
        favourite = Favourite.objects.get(id=id)
        favourite.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {id} no existe.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False
    

def saveUninterestingImage(image):
    try:
        uninteresting_image = UninterestingImage.objects.create(title=image.title, description=image.description, image_url=image.image_url, date=image.date, user=image.user)
        return uninteresting_image
    except Exception as e:
        print(f"Error al guardar la imagen no interesante: {e}")
        return None

def getUninterestingImagesByUser(user):
    uninteresting_images = UninterestingImage.objects.filter(user=user).values('id', 'title', 'description', 'image_url', 'date')
    return list(uninteresting_images)