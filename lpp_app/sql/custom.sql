
-- pilnuje aby uzytkownicy stali sie przyjaciolmi, 
-- gdy A wysle zapro do B, B wysle zapro do A
CREATE OR REPLACE FUNCTION make_friend_invite_trigger()
    RETURNS "trigger" AS $$
    DECLARE
        back_invite_id INTEGER;
    BEGIN
        SELECT id INTO back_invite_id FROM lpp_app_invites
            WHERE user_from_id=NEW.user_to_id and user_to_id=NEW.user_from_id;

        IF (back_invite_id IS NOT NULL) THEN
            INSERT INTO lpp_app_friends(user1_id, user2_id) values(NEW.user_to_id, NEW.user_from_id);
            
            DELETE FROM lpp_app_invites WHERE user_from_id=NEW.user_from_id and user_to_id=NEW.user_to_id;
            DELETE FROM lpp_app_invites WHERE user_from_id=NEW.user_to_id and user_to_id=NEW.user_from_id;

            RETURN NULL;        
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE 'plpgsql' VOLATILE;

CREATE TRIGGER make_friend_invite_trigger BEFORE INSERT OR UPDATE
    ON lpp_app_invites FOR EACH ROW
    EXECUTE PROCEDURE make_friend_invite_trigger();

----------------------------------------------------------

-- pilnuje czy uzytkownik chcacy dodac nowa oferta ma wystarczajaca ilosc surowca1
CREATE OR REPLACE FUNCTION czy_posiada_surowiec1()
    RETURNS "trigger" AS $$
    DECLARE
        surowiec INTEGER;
    BEGIN
        IF ( NEW.surowiec1 = 'drewno' ) THEN
            SELECT drewno INTO surowiec FROM lpp_app_osada where lpp_app_osada.id = NEW.osada_id;
            IF (surowiec >= NEW.ilosc1) THEN                
                UPDATE lpp_app_osada SET drewno = (drewno - NEW.ilosc1) WHERE lpp_app_osada.id = NEW.osada_id;
                RETURN NEW;
            END IF;
        END IF;

        IF ( NEW.surowiec1 = 'zloto' ) THEN
            SELECT zloto INTO surowiec FROM lpp_app_osada where lpp_app_osada.id = NEW.osada_id;
            IF (surowiec >= NEW.ilosc1) THEN                
                UPDATE lpp_app_osada SET zloto = (zloto - NEW.ilosc1) WHERE lpp_app_osada.id = NEW.osada_id;
                RETURN NEW;
            END IF;
        END IF;

        IF ( NEW.surowiec1 = 'kamien' ) THEN
            SELECT kamien INTO surowiec FROM lpp_app_osada where lpp_app_osada.id = NEW.osada_id;
            IF (surowiec >= NEW.ilosc1) THEN                
                UPDATE lpp_app_osada SET kamien = (kamien - NEW.ilosc1) WHERE lpp_app_osada.id = NEW.osada_id;
                RETURN NEW;
            END IF;
        END IF;

        IF ( NEW.surowiec1 = 'zelazo' ) THEN
            SELECT zelazo INTO surowiec FROM lpp_app_osada where lpp_app_osada.id = NEW.osada_id;
            IF (surowiec >= NEW.ilosc1) THEN                
                UPDATE lpp_app_osada SET zelazo = (zelazo - NEW.ilosc1) WHERE lpp_app_osada.id = NEW.osada_id;
                RETURN NEW;
            END IF;
        END IF;

        RETURN NULL;
    END;
$$ LANGUAGE 'plpgsql' VOLATILE;


CREATE TRIGGER czy_posiada_surowiec1 BEFORE INSERT OR UPDATE
    ON lpp_app_handel FOR EACH ROW
    EXECUTE PROCEDURE czy_posiada_surowiec1();



INSERT INTO lpp_app_budynki(nazwa,jednostka_prod,max_pojemnosc,produktywnosc,max_level,koszt,drewno,kamien,zelazo,zloto) VALUES ('Koszary'         ,'wojownikow', 30  , 60,  5, 2, 100, 100,  50, 150);
INSERT INTO lpp_app_budynki(nazwa,jednostka_prod,max_pojemnosc,produktywnosc,max_level,koszt,drewno,kamien,zelazo,zloto) VALUES ('Stajnie'         ,'rycerzy', 10  , 90,  5, 5, 300, 150, 100, 250);
INSERT INTO lpp_app_budynki(nazwa,jednostka_prod,max_pojemnosc,produktywnosc,max_level,koszt,drewno,kamien,zelazo,zloto) VALUES ('Tartak'          ,'desek', 1000, 30, 10, 3, 100,  10,  10, 150);
INSERT INTO lpp_app_budynki(nazwa,jednostka_prod,max_pojemnosc,produktywnosc,max_level,koszt,drewno,kamien,zelazo,zloto) VALUES ('Kopalnia żelaza' ,'rud', 1000, 40, 10, 3, 250,  10,   0, 150);
INSERT INTO lpp_app_budynki(nazwa,jednostka_prod,max_pojemnosc,produktywnosc,max_level,koszt,drewno,kamien,zelazo,zloto) VALUES ('Kopalnia złota'  ,'sztabek', 1000, 60, 10, 3, 200, 100,  20,  50);
INSERT INTO lpp_app_budynki(nazwa,jednostka_prod,max_pojemnosc,produktywnosc,max_level,koszt,drewno,kamien,zelazo,zloto) VALUES ('Kamieniołom'     ,'blokow', 1000, 30, 10, 3, 150, 100,  50, 200);
INSERT INTO lpp_app_budynki(nazwa,jednostka_prod,max_pojemnosc,produktywnosc,max_level,koszt,drewno,kamien,zelazo,zloto) VALUES ('Farma'           ,'swin', 10  , 90,  5, 5, 300, 150, 100, 250);
INSERT INTO lpp_app_budynki(nazwa,max_pojemnosc,produktywnosc,max_level,koszt,drewno,kamien,zelazo,zloto)                VALUES ('Market'          , 0,  0,  1, 1, 400, 100,  50, 400);

INSERT INTO lpp_app_armia(budynek_id,nazwa,atak,obrona,zbroja,drewno,kamien,zelazo,zloto) VALUES (1,'Pikinier',   4, 1, 2, 10, 0, 20, 15);
INSERT INTO lpp_app_armia(budynek_id,nazwa,atak,obrona,zbroja,drewno,kamien,zelazo,zloto) VALUES (1,'Miecznik',   5, 4, 2,  0, 0, 30, 20);
INSERT INTO lpp_app_armia(budynek_id,nazwa,atak,obrona,zbroja,drewno,kamien,zelazo,zloto) VALUES (1,'Krzyżowiec', 6, 4, 3,  0, 0, 40, 20);
INSERT INTO lpp_app_armia(budynek_id,nazwa,atak,obrona,zbroja,drewno,kamien,zelazo,zloto) VALUES (1,'Centurion',  8, 6, 5,  0, 0, 50, 40);

INSERT INTO lpp_app_armia(budynek_id,nazwa,atak,obrona,zbroja,drewno,kamien,zelazo,zloto) VALUES (2,'Lekki kawalerzysta',   5, 1, 2, 15, 0, 40, 25);
INSERT INTO lpp_app_armia(budynek_id,nazwa,atak,obrona,zbroja,drewno,kamien,zelazo,zloto) VALUES (2,'Rycerz',               7, 2, 2, 20, 0, 45, 30);
INSERT INTO lpp_app_armia(budynek_id,nazwa,atak,obrona,zbroja,drewno,kamien,zelazo,zloto) VALUES (2,'Ciężki kawalerzysta',  9, 2, 4, 20, 0, 60, 45);
INSERT INTO lpp_app_armia(budynek_id,nazwa,atak,obrona,zbroja,drewno,kamien,zelazo,zloto) VALUES (2,'Husar',               15, 3, 7, 25, 0, 80, 65);


