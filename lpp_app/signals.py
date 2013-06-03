from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from .models import Osada, Kategoria, Obiekt, OsadaObiekt

"""
@receiver(pre_save, sender=Osada, dispatch_uid="osada_pre_save")
def update_product_count_on_save(sender, instance, **kwargs):
    # Update product count in category after product was saved 

    # if product is being updated (it has an "id"), removing it from previous category first
    if instance.id:
        # instance is new, not saved object. Let's get the old, unmodified one        
        #old_product = Product.objects.get(pk=instance.id)
        #old_product.category.product_count -= 1
        #old_product.category.save()

        # previous -1 won't affect instance
        #if old_product.category == instance.category:
        #    instance.category.product_count -= 1

    # now adding to the new category
    #instance.category.product_count += 1
    #instance.category.save()
"""

@receiver(post_save, sender=Osada, dispatch_uid="osada_post_save")
def update_objects_osada_on_save(sender, instance, **kwargs):
    """ Update product count in category if product was deleted """
    
    new_osada = Osada.objects.get(pk=instance.id)
    obiekty = Obiekt.objects.all()
    for ob in obiekty:
        OsadaObiekt.objects.create(osada=new_osada, obiekt=ob, ilosc=ob.poczatkowa_ilosc)


    #instance.category.product_count -= 1
    #instance.category.save()


from django.contrib.auth.signals import user_logged_in

def on_logged_in(sender, user, request, **kwargs):
    print 'User logged in as: \'{0}\''.format(user)

user_logged_in.connect(on_logged_in)
