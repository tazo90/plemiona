# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------

"""
Creates the default Objects, after created tables (syncdb) 
"""

from django.db.models import signals
from django.db import connections
from django.db import router
from .models import Obiekt, Kategoria as Kat
import models as site_app
from django.core.management.color import no_style

def create_default_navigation(app, created_models, verbosity, db, **kwargs):
    # Only create the default navigation in databases where Django created the table
    if Kat in created_models and router.allow_syncdb(db, Kat) and \
        Obiekt in created_models and router.allow_syncdb(db, Obiekt):
        if verbosity >= 2:
            print("Creating obiects")

        # We set an explicit pk instead of relying on auto-incrementation,
        # so we need to reset the database sequence. See #17415. 

        # Navigations 
        # -- Group = Page Main --        
        kat1 = Kat(pk=1, nazwa='Armia', url='armia')
        kat2 = Kat(pk=2, nazwa='Budynki', url='budynki')
        kat3 = Kat(pk=3, nazwa='Mieszkancy', url='mieszkancy')
        kat4 = Kat(pk=4, nazwa='Zasoby', url='zasoby')
        kat1.save(using=db)
        kat2.save(using=db)
        kat3.save(using=db)
        kat4.save(using=db)
               
        # Armia
        Obiekt(pk=1, nazwa='rycerz brazowy', kategoria=kat1, cena=300, poczatkowa_ilosc=4, max_ilosc=1000).save(using=db)        
        Obiekt(pk=2, nazwa='rycerz srebrny', kategoria=kat1, cena=500, poczatkowa_ilosc=1, max_ilosc=1000).save(using=db)        
        Obiekt(pk=3, nazwa='rycerz złoty', kategoria=kat1, cena=900, max_ilosc=1000).save(using=db)        

        # Budynki
        Obiekt(pk=4, nazwa='młyn', kategoria=kat2, cena=350, max_ilosc=5).save(using=db)
        Obiekt(pk=5, nazwa='piekarnia', kategoria=kat2, cena=400, max_ilosc=10).save(using=db)
        Obiekt(pk=6, nazwa='magazyn', kategoria=kat2, cena=200, poczatkowa_ilosc=1, max_ilosc=4).save(using=db)
        Obiekt(pk=7, nazwa='zbrojownia', kategoria=kat2, cena=600, max_ilosc=4).save(using=db)
        Obiekt(pk=8, nazwa='huta', kategoria=kat2, cena=450, max_ilosc=3).save(using=db)
        Obiekt(pk=9, nazwa='farma', kategoria=kat2, cena=500, max_ilosc=10).save(using=db)
        Obiekt(pk=10, nazwa='kopalnia złota', kategoria=kat2, cena=900, max_ilosc=10).save(using=db)
        Obiekt(pk=11, nazwa='kopalnia węgla', kategoria=kat2, cena=600, max_ilosc=10).save(using=db)

        # Mieszkancy
        Obiekt(pk=12, nazwa='pomocnik', kategoria=kat3, cena=10, poczatkowa_ilosc=10, max_ilosc=1000).save(using=db)
        Obiekt(pk=13, nazwa='budowniczy', kategoria=kat3, cena=15, poczatkowa_ilosc=5, max_ilosc=100).save(using=db)
        Obiekt(pk=14, nazwa='rolink', kategoria=kat3, cena=15, max_ilosc=100).save(using=db)
        Obiekt(pk=15, nazwa='młynarz', kategoria=kat3, cena=12, max_ilosc=100).save(using=db)
        Obiekt(pk=16, nazwa='piekarz', kategoria=kat3, cena=15, max_ilosc=100).save(using=db)
        Obiekt(pk=17, nazwa='górnik', kategoria=kat3, cena=17, max_ilosc=100).save(using=db)        

        # Zasoby
        Obiekt(pk=18, nazwa='jedzenie', kategoria=kat4, cena=30, poczatkowa_ilosc=10, max_ilosc=100000).save(using=db)        
        Obiekt(pk=19, nazwa='węgiel', kategoria=kat4, cena=80, max_ilosc=100000).save(using=db)        
        Obiekt(pk=20, nazwa='złoto', kategoria=kat4, cena=120, max_ilosc=100000).save(using=db)        
        Obiekt(pk=21, nazwa='woda', kategoria=kat4, cena=5, poczatkowa_ilosc=10, max_ilosc=100000).save(using=db)        
        Obiekt(pk=22, nazwa='drewno', kategoria=kat4, cena=10, poczatkowa_ilosc=5, max_ilosc=100000).save(using=db)        
        Obiekt(pk=23, nazwa='mąka', kategoria=kat4, cena=3, max_ilosc=100000).save(using=db)        
        Obiekt(pk=24, nazwa='mięso', kategoria=kat4, cena=8, poczatkowa_ilosc=5, max_ilosc=100000).save(using=db)        



        # for Nav
        sequence_sql = connections[db].ops.sequence_reset_sql(no_style(), [Kat])        
        if sequence_sql:
            if verbosity >= 2:
                print("Resetting sequence")
            cursor = connections[db].cursor()
            for command in sequence_sql:
                cursor.execute(command)

    #Nav.objects.clear_cache()

signals.post_syncdb.connect(create_default_navigation, sender=site_app)




