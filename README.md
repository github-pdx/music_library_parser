# *Music Library* Reporting

[![Build Status](https://travis-ci.com/averille-dev/music_library_parser.svg?branch=master)](https://travis-ci.com/averille-dev/music_library_parser)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Python v3.9 script to Extract FLAC/MP3/M4A Tags:
Runs media tag dump to extract specific information about each music file and exports desired metadata to Excel report '.xlsx'. 

## Example Output:
![Screenshot](https://github.com/github-pdx/music_library_parser/blob/master/img/report_output.png)
* [Excel Report](https://github.com/github-pdx/music_library_parser/blob/master/data/output/~media_report.xlsx)
* [Log](https://github.com/github-pdx/music_library_parser/blob/master/data/output/~media_report.txt)

## Filename Encoding:
![Screenshot](https://github.com/github-pdx/music_library_parser/blob/master/img/file_encoding.png)

## Media Tag Status:
![Screenshot](https://github.com/github-pdx/music_library_parser/blob/master/img/media_status.png)

## Tested On:
* Ubuntu 18.04 LTS (Bionic Beaver)
* Ubuntu 20.04 LTS (Focal Fossa)
* CentOS 8 (RHEL)
* Windows 10

## Custom Genres
```
def build_genre_dictionary() -> dict:
    genre_dict = OrderedDict()
    genre_dict['Arcade Fire']='Indie-Rock'
    genre_dict['Beethoven']='Classical'
    genre_dict['Interpol']='Post-Punk-Revival'
    genre_dict['M. Ward']='Indie-Rock'
    genre_dict['Massive Attack']='Trip-Hop'
    genre_dict['Mazzy Star']='Alternative'
    genre_dict['Patsy Cline']='Rockabilly'
    genre_dict['Ravel']='Classical'
    genre_dict['Rimsky-Korsakov']='Classical'
    genre_dict['The Fall']='Post-Punk'
    genre_dict['Sallie Ford & The Sound Outside'] = 'Rockabilly'
    ...
```

## *Music Tag* Resources:
* [mutagen](https://mutagen.readthedocs.io/en/latest/)
* [TagLib](https://taglib.org/api/index.html)
* [Discogs Music Database](https://www.discogs.com/)
* [MediaMonkey](https://www.mediamonkey.com/information/free/)
* [Foobar 2000](https://www.foobar2000.org/)
* [Spotify API](https://developer.spotify.com/documentation/web-api/quick-start/)
* [Spotipy](https://spotipy.readthedocs.io/en/2.12.0/#)
* [Picard Tag Mappings](https://picard.musicbrainz.org/docs/mappings/)

## Optional:
* [Install Docker](https://www.docker.com/products/docker-desktop)

* [Docker Commands](https://docs.docker.com/engine/reference/commandline/build/)
```
# start MongoDB in docker
docker-compose up --build
docker ps
docker-compose ps
docker exec -it {CONTAINER_ID} /bin/bash
docker-compose run media_parser sh -c "python /media_parser/show_installed_pkgs.py"
docker-compose run media_parser sh -c "python /media_parser/create_media_report.py"
# once docker is up, run scripts from PyCharm IDE on host
python ./media_parser/insert_media_mongodb.py -p=27017
python ./media_parser/db/postgres_etl.py -p=5432
# hit CTRL-C to exit MongoDB in docker
docker-compose down --remove-orphans
```

* [Install MongoDB](https://docs.mongodb.com/manual/administration/install-community/)

* [MongoDB Shell Commands](https://docs.mongodb.com/manual/reference/mongo-shell/)
```
sudo sed -i 's/port: 27017/port: 27018/g' /etc/mongod.conf
sudo service mongod restart
sudo lsof -iTCP -sTCP:LISTEN | grep mongod
systemctl status mongod
mongo admin --eval 'db.createUser({user:"run_admin_run",pwd:"run_pass_run",roles:["dbAdminAnyDatabase"]});'
```


## License:
[MIT License](LICENSE)
