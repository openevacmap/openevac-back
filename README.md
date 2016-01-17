# OpenEvacMap

Crowdsourcing de plans d'évacuation via une webapp à utiliser sur smartphone.

Le site est consultable sur http://openevacmap.org/

# API

Les réponses sont au format JSON.

##GET /v0/maps-info?lat=xxxx&lon=xxxx

Retourne les plans disponibles à proximité, ainsi que les adresses proches sans plan.

En option:
- nb_maps = nombre maximum de plans à renvoyer
- nb_addr = nombre maximum d'adresses sans plan à renvoyer

##GET /v0/map?id=xxxx

Retourne l'image (JPEG) d'un plan.

En option:
- preview=1 -> pour obtenir une image de 600 pixels de côté maximum (quelques dizaines de Ko au lieu de quelques Mo)

##GET /v0/log

Retourne une collection geojson des derniers plans consultés.


# Notes pour l'install côté serveur...

    for d in 01 02 03 04 05 06 07 08 09 `seq 10 19` 2A 2B `seq 21 95` `seq 971 976`; do
      wget  http://bano.openstreetmap.fr/BAN_odbl/BAN_odbl_$d-csv.bz2
      grep -v '^id' BAN_odbl_$d-csv >> ban.csv 
      rm BAN_odbl_$d-csv
    done

    createdb evac -E utf8 -T template0

    create table ban (id text,nom_voie text,id_fantoir text,numero text,rep text,code_insee text,code_post text,alias text,nom_ld text,x float,y float,commune text,fant_voie text,fant_ld text,lat float,lon float);
    \copy ban from ban.csv with (format csv);
    alter table ban add geom geometry;
    update ban set geom = st_setsrid(st_makepoint(lon,lat),4326);
    create index ban_geom on ban using gist (geom);
    create index ban_id on ban (id);
