Notes pour l'install côté serveur...

for d in 01 02 03 04 05 06 07 08 09 `seq 10 19` 2A 2B `seq 21 95` `seq 971 976`; do
  wget  http://bano.openstreetmap.fr/BAN_odbl/BAN_odbl_$d-csv.bz2
  grep -v '^id' BAN_odbl_$d-csv >> ban.csv 
  rm BAN_odbl_$d-csv
done


create table ban (id text,nom_voie text,id_fantoir text,numero text,rep text,code_insee text,code_post text,alias text,nom_ld text,x float,y float,commune text,fant_voie text,fant_ld text,lat float,lon float);
\copy ban from ban.csv with (format csv);
update ban set geom = st_setsrid(st_makepoint(lon,lat),4326);
create index ban_geom on ban using gist (geom);
create index ban_id on ban (id);

create table maps (id uuid, path text, adress text, level text, building text);
