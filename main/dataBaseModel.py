# This class encapsulates all communication with the DB
#from models import User
from django.contrib.auth.models import User
from models import Comment
from models import Product
from models import Category
from models import WishList
from models import FitList
from models import TempProduct
from models import Added
from models import User as CustomUser

from django.db.models import Q

class dataBaseModel (object):
    
    SUCCESS = 1
    ERR_BAD_PRODUCT = -1
    ERR_BAD_USER = -2
    ERR_UNABLE_TO_REMOVE_FROM_WISHLIST = -3
    ERR_UNABLE_TO_REMOVE_FROM_FITLIST = -4
    ERR_BAD_CATEGORY = -5
    ERR_WISHLIST_ALREADY_EXIST = -6
    ERR_FITLIST_ALREADY_EXIST = -7
    ERR_BAD_REQUEST = -8
    ERR_BAD_TOKEN = -9
    ERR_UNABLE_TO_PREVIEW_PRODUCT = -10
    ERR_UNABLE_TO_ADD_PRODUCT = -11
    ERR_UNABLE_TO_ADD_PROFILE_PIC = -12
    ERR_UNABLE_TO_GET_USER_INFO = -13
    ERR_UNABLE_TO_REMOVE_CUSTOM_PRODUCT = -14
    ERR_UNABLE_TO_EDIT_CUSTOM_PRODUCT = -15
    ERR_UNABLE_TO_SET_POSITIONAL_CONFIG = -16

    
    
    def __init__(self):
        # do nothing
        pass
            
    def addToWishList(self, userID, product, productID): 
        try:
            user = User.objects.get(pk = userID)
            p = Product.objects.get(Q(pk = productID), Q(name = product))
            if WishList.objects.filter(Q(owner = user), Q(product = p)).count() != 0: #check if item already exist
                return dataBaseModel.ERR_WISHLIST_ALREADY_EXIST
        
            newOne = WishList(owner = user, product = p) # create a new wishlist item
            newOne.save()
            return dataBaseModel.SUCCESS
        except:
            return dataBaseModel.ERR_BAD_PRODUCT


    def removeFromWishList(self, userID, product, productID):
        try:
            #try to get the wishlist item
            newOne = WishList.objects.get(Q(owner = User.objects.get(pk = userID)), Q(product = Product.objects.get(Q(pk = productID), Q(name=product))))
        except:
            return dataBaseModel.ERR_UNABLE_TO_REMOVE_FROM_WISHLIST
        newOne.delete() # delete the item
        return dataBaseModel.SUCCESS

    def getWishList(self, userID):
        try:
            User.objects.get(pk = userID)
        except:
            return ([], dataBaseModel.ERR_BAD_USER)
        
        queryset = WishList.objects.filter(owner = User.objects.get(pk = userID)) # query the wishlist of the user 
        items = []
        for item in queryset:
            items.append(item)

        return (items, dataBaseModel.SUCCESS)
    
    """ fitlist operation is very similar to wishlist...may consider refactor? """
    
    def addToFitList(self, userID, product, productID): 
        try:
            user = User.objects.get(pk = userID)
            p = Product.objects.get(Q(pk = productID), Q(name = product))
            if FitList.objects.filter(Q(owner = user), Q(product = p)).count() != 0: #check if item already exist
                return dataBaseModel.ERR_FITLIST_ALREADY_EXIST
        
            newOne = FitList(owner = user, product = p) # create a new fitlist item
            newOne.save()
            return dataBaseModel.SUCCESS
        except:
            return dataBaseModel.ERR_BAD_PRODUCT


    def removeFromFitList(self, userID, product, productID):
        try:
            #try to get the fitlist item
            newOne = FitList.objects.get(Q(owner = User.objects.get(pk = userID)), Q(product = Product.objects.get(Q(pk = productID), Q(name=product))))
        except:
            return dataBaseModel.ERR_UNABLE_TO_REMOVE_FROM_FITLIST
        newOne.delete() # delete the item
        return dataBaseModel.SUCCESS

    def getFitList(self, userID):
        try:
            User.objects.get(pk = userID)
        except:
            return ([], dataBaseModel.ERR_BAD_USER)
        
        queryset = FitList.objects.filter(owner = User.objects.get(pk = userID)) # query the fitlist of the user 
        items = []
        for item in queryset:
            items.append(item)

        return (items, dataBaseModel.SUCCESS)


    def addComment(self, userID, product, pid, content, time):
        try:
            user = User.objects.get(pk=userID)
            p = Product.objects.get(Q(pk=pid), Q(name=product))
            newOne = Comment(owner = user, product = p, content = content, time=time)
            newOne.save()
            return dataBaseModel.SUCCESS
        except:
            return dataBaseModel.ERR_BAD_PRODUCT


    def getComments(self, product, pid):
        try :
            p = Product.objects.get(Q(pk = pid), Q(name=product))
                
            
            items = []
            for item in Comment.objects.filter(product = p).order_by('time'):
                items.append(item)
            
            return (items, dataBaseModel.SUCCESS)
        except:
            return ([], dataBaseModel.ERR_BAD_PRODUCT) 


    def getProducts(self, category):
        queryset = Product.objects.filter(category = Category.objects.filter(name = category))
        if queryset.count() == 0:
            return ([], dataBaseModel.ERR_BAD_CATEGORY)

        items = []
        for item in queryset:
            items.append(item)
            
        return (items, dataBaseModel.SUCCESS)
    
    def getDetail(self, product, productID):
        try:
            return (Product.objects.get(Q(pk=productID), Q(name=product)), dataBaseModel.SUCCESS)
        except:
            return (None,dataBaseModel.ERR_BAD_PRODUCT)
        
    def getTempProduct(self, userID, ttoken):
        try:
            temp = TempProduct.objects.get(Q(owner = User.objects.get(pk = userID)), Q(token = ttoken))
            return (temp, dataBaseModel.SUCCESS)
        except:
            return (None,  dataBaseModel.ERR_BAD_TOKEN)
        
    """ if can't remove, do nothing
        return image path """
    def removeTempProduct(self, userID):
        try:
            temps = TempProduct.objects.filter(owner = User.objects.get(pk = userID))
            data = []
            for temp in temps:
                data.append(temp.overlay)
                
            temps.delete()
            return data
        except:
            return []
    
    def addTempProduct(self, puserID, ptoken, poverlay, pcategory):
        user = User.objects.get(pk = puserID)
        cat = Category.objects.get(name=pcategory)
        pyoffset = 0.0
        if pcategory == "hats":
            pyoffset = -0.58
        elif pcategory == "headphones":
            pyoffset = -0.15
        newTemp = TempProduct(owner = user, overlay = poverlay, token = ptoken, category = cat, xoffset = 0.0, yoffset = pyoffset, scale = 1.0, rotation = 0.0)
        newTemp.save()
    
    def addProduct(self, puserID, pimage, poverlay, pcategory, pbrand, pname, purl, pprice, pdescription, pxoffset = 0.0, pyoffset = 0.0, pscale = 1.0, protation = 0.0, default = True):
        try:
            # add the product
            if default == True:
                if pcategory == "hats":
                    pyoffset = -0.58
                elif pcategory == "headphones":
                    pyoffset = -0.15
            
            cat = Category.objects.get(name=pcategory)
            newProduct = Product(category = cat, name = pname, brand = pbrand, url = purl, price = pprice, description = pdescription, photo = pimage, overlay = poverlay, xoffset = pxoffset, yoffset = pyoffset, scale = pscale, rotation = protation)
            newProduct.save()
            # add the added relationship
            user = User.objects.get(pk = puserID)
            newAdd = Added(owner = user, product = newProduct)
            newAdd.save()
            
            return dataBaseModel.SUCCESS
        except Exception:
            return dataBaseModel.ERR_UNABLE_TO_ADD_PRODUCT
        
    def editProduct(self, puserID, pimage, poverlay, pcategory, pbrand, pname, purl, pprice, pdescription, pproductID, pxoffset = 0.0, pyoffset = 0.0, pscale = 1.0, protation = 0.0, needChange = False):
        try:
            user = User.objects.get(pk = puserID)
            pproduct = Product.objects.get(pk = pproductID)
            added = Added.objects.get(Q(owner = user), Q(product = pproduct)) # check if it really exists
            # if can't get should jump to catch block
            if pimage != "":
                pproduct.photo = pimage
            if poverlay != "":
                pproduct.overlay = poverlay
            pproduct.category = Category.objects.get(name=pcategory)
            pproduct.brand = pbrand
            pproduct.name = pname
            pproduct.url = purl
            pproduct.price = pprice
            pproduct.description = pdescription
            if needChange == True:
                pproduct.xoffest = pxoffset
                pproduct.yoffset = pyoffset
                pproduct.scale = pscale
                pproduct.rotation = protation
            pproduct.save()
            return dataBaseModel.SUCCESS
        except:
            return dataBaseModel.ERR_UNABLE_TO_EDIT_CUSTOM_PRODUCT

    def searchProducts(self, searchName):
        list = Product.objects.filter(Q(name__icontains = searchName))
        # = Product.objects.get(Q(name.lower().find(searchName.lower())), dataBaseModel.SUCCESS)
        items = []
        for item in list:
            items.append(item)

        brand = Product.objects.filter(Q(brand__icontains = searchName))
        print "brand is :",brand
        items = []
        for item in brand:
            items.append(item)

        return (items, dataBaseModel.SUCCESS)

    def addProfilePic(self, userID, file):
        try:
            user = CustomUser.objects.get(pk=userID)
            user.update(user_image = file)
            user.save()            
        except:
            newUser = CustomUser(id=userID, user_id = userID, count = 0, user_image = file)
            newUser.save()
            
    def getProfilePic(self, userID):
        try:
            user = CustomUser.objects.get(pk=userID)
            return user.user_image
        except:
            return ""
        
    def getUserInfo(self, userID):
        try:
            user = User.objects.get(pk=userID)
            return user
        except:
            return ""
        
    def getNumAdded(self, userID):
        try:
            user = User.objects.get(pk=userID)
            added = Added.objects.filter(owner = user)
            return added.count()
        except:
            return 0
        
    def getCustomProduct(self, userID):
        try:
            user = User.objects.get(pk=userID)
            added = Added.objects.filter(owner = user)
            item = []
            for p in added:
                item.append(p.product)
            return item
        except:
            return []
        
    def removeCustomProduct(self, userID, productID):
        try:
            user = User.objects.get(pk=userID)
            tproduct = Product.objects.get(pk = productID)
            
            added = Added.objects.get(Q(owner = user), Q(product = tproduct))
            added.delete() # remove association with user
            tproduct.delete() # remove the actual product
            return dataBaseModel.SUCCESS
        except:
            return dataBaseModel.ERR_UNABLE_TO_REMOVE_CUSTOM_PRODUCT
    
    # this method makes edit product faster by checking if it exists before processing the image
    # code restructuring should use this method for removing custom item
    def checkIfOwnCustomProduct(self, userID, productID):
        try:
            user = User.objects.get(pk=userID)
            tproduct = Product.objects.get(pk = productID)         
            added = Added.objects.get(Q(owner = user), Q(product = tproduct))
            return True;
        except:
            return False;
        
    def findPositionalConfig(self, ptoken):
        try:
            item = TempProduct.objects.get(token = ptoken)
            return (item.xoffset, item.yoffset, item.scale, item.rotation)
        except:
            return None
        
    def setPositionalConfig(self, ptoken, pxoffset, pyoffset, pscale, protation):
        item = TempProduct.objects.get(token = ptoken)
        item.xoffset = pxoffset
        item.yoffset = pyoffset
        item.scale = pscale
        item.rotation = protation
        item.save()