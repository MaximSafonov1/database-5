import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://postgres:password@localhost:5432/postgres')

connect = engine.connect()



performer_number = connect.execute("""select g.name, COUNT(performer_id) from performergenre p
inner join genre g on p.genre_id = g.id
group by g.id;
""").fetchall()
print('Количество исполнителей в каждом жанре:', performer_number)

track_number = connect.execute("""select a.name, COUNT(t.id) from album a
inner join track t on t.album_id = a.id
where a.year_of_issue between 2010 and 2020
group by a.id;
""").fetchall()
print('\nКоличество треков, вошедших в альбомы 2010-2020 годов:', track_number)

average_duration = connect.execute("""select a.name, round(AVG(t.duration), 2) from album a
inner join track t on t.album_id = a.id
group by a.id;
""").fetchall()
print('\nСредняя продолжительность треков по каждому альбому:', average_duration)

all_performers = connect.execute("""select per.name from performer per 
inner join performeralbum p on per.id = p.performer_id 
inner join album a on a.id = p.album_id 
where a.year_of_issue != 2020;
""").fetchall()
print('\nВсе исполнители, которые не выпустили альбомы в 2020 году:', all_performers)

name_of_collections = connect.execute("""select distinct c.name collection from performer p
inner join performeralbum pa on pa.performer_id = p.id
inner join album a on a.id = pa.album_id
inner join track t on t.album_id = a.id
inner join trackcollection tc on tc.track_id = t.id
inner join collection c on c.id = tc.collection_id
where p.name like '%%Eminem%%'
order by c.name;
""").fetchall()
print('\nНазвания сборников, в которых присутствует Eminem:', name_of_collections)

name_of_albums = connect.execute("""select distinct a.name from album a
inner join performeralbum pa on pa.album_id = a.id
where performer_id  in (SELECT performer_id from performergenre
group by performer_id
having count(genre_id)>1);
""").fetchall()
print('\nНазвание альбомов, в которых присутствуют исполнители более 1 жанра:', name_of_albums)

name_of_tracks = connect.execute("""select t.name from track t 
left join trackcollection tc on t.id = tc.track_id
where tc.collection_id is null;
""").fetchall()
print('\nНаименование треков, которые не входят в сборники:', name_of_tracks)

name_of_performers = connect.execute("""select p.name from track t
inner join performeralbum pa on pa.album_id = t.album_id
inner join performer p on p.id = pa.performer_id
where duration = (select MIN(duration) from track);
""").fetchall()
print('\nИсполнитель(-и), написавший(-ие) самый короткий по продолжительности трек:', name_of_performers)

al_with_min_num_tr = connect.execute("""select a.name, count(t.id) from album a
inner join track t ON t.album_id = a.id
group by a.id
having count(t.id) = (select MIN(count_track) from (select album_id, count(id) count_track from track 
group by album_id) AS min_track);
""").fetchall()
print('\nНазвание альбомов, содержащих наименьшее количество треков:', al_with_min_num_tr)
