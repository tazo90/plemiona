from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from .models import Osada, Kategoria, Obiekt, OsadaObiekt
from .models import Armia, Armia_osada, Budynki, Budynki_osada

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
    # When created osada then create Armia and Budynki connected with created Osada
    new_osada = Osada.objects.get(pk=instance.id)

    armia = Armia.objects.all()
    budynki = Budynki.objects.all()

    for ar in armia:
        Armia_osada.objects.create(osada=new_osada, armia=ar, zloto=ar.zloto, drewno=ar.drewno, kamien=ar.kamien, zelazo=ar.zelazo)

    for bud in budynki:
        Budynki_osada.objects.create(osada=new_osada, budynek=bud, zloto=bud.zloto, drewno=bud.drewno, kamien=bud.kamien, zelazo=bud.zelazo, produktywnosc=bud.produktywnosc, max_pojemnosc=bud.max_pojemnosc)


"""@receiver(post_save, sender=Osada, dispatch_uid="osada_post_save")
def update_objects_osada_on_save(sender, instance, **kwargs):
    # Update product count in category if product was deleted 
    
    new_osada = Osada.objects.get(pk=instance.id)
    obiekty = Obiekt.objects.all()
    for ob in obiekty:
        OsadaObiekt.objects.create(osada=new_osada, obiekt=ob, ilosc=ob.poczatkowa_ilosc)


    #instance.category.product_count -= 1
    #instance.category.save()
"""

from django.contrib.auth.signals import user_logged_in

def on_logged_in(sender, user, request, **kwargs):
    print 'User logged in as: \'{0}\''.format(user)

user_logged_in.connect(on_logged_in)
