# -*- coding: UTF-8 -*-
"""MongoDB module to read/write data NoSQL database."""
import inspect
import sys
import pathlib
from pymongo import MongoClient, errors, version
from bson import ObjectId
import gridfs

"""
Sources:   default: 27017  test: 27018
pymongo version: 4.2.0
https://api.mongodb.com/python/current/tutorial.html
https://docs.mongodb.com/manual/reference/method/js-collection/
https://docs.mongodb.com/manual/core/gridfs/
https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html
https://api.mongodb.com/python/current/api/gridfs/index.html#gridfs.GridFS.put
https://github.com/realpython/list-of-python-api-wrappers
ObjectID = 12-byte string: (4-bytes timestamp, 5-byte random, 3-byte counter)
BSON is a binary serialization format
"""


class MongoMedia:
    """Class to connect to MongoDB instance on host and add/remove media."""

    @classmethod
    def __init__(cls, server: str = 'localhost',
                 port_num: int = 27017,
                 database: str = 'media_db',
                 username: str = 'run_admin_run',
                 password: str = 'run_pass_run'):
        cls.__auth_db = 'admin'
        cls.__media_db = database
        cls.__tags_collection = 'media_tags'
        cls.__files_collection = 'bin_media'
        cls.conn = MongoClient(server, port_num,
                               serverSelectionTimeoutMS=500,
                               username=username,
                               password=password,
                               authSource=cls.__auth_db, )
        cls.conn_status = cls.is_connected()
        cls.auth_conn = cls.conn[cls.__auth_db]
        cls.media_conn = cls.conn[cls.__media_db]
        cls.tags_coll = cls.media_conn[cls.__tags_collection]
        cls.files_coll = cls.media_conn[cls.__files_collection]
        cls.grid_fs = gridfs.GridFS(cls.media_conn,
                                    collection=cls.__files_collection)

    @classmethod
    def is_connected(cls) -> bool:
        """Checks if MongoDB has valid connection."""
        try:
            cls.conn.server_info()
            return True
        except (errors.ServerSelectionTimeoutError,
                errors.OperationFailure,
                errors.ConnectionFailure) as err:
            print("ERROR: pymongo", err)
            return False

    @classmethod
    def get_connection(cls) -> MongoClient:
        """Return client connection to 'admin' authorization database."""
        return cls.conn

    @classmethod
    def is_admin_setup(cls, username: str) -> bool:
        """Checks if username exists in the 'admin' database."""
        # 'users': [{'user': 'run_admin_run', 'db': 'admin'}]
        user_dict = cls.auth_conn.command('usersInfo')
        if user_dict:
            user_list = user_dict['users']
            if len(user_list) > 0:
                for db_entry in user_list:
                    if username == db_entry['user']:
                        return True
        return False

    @classmethod
    def add_admin(cls, username: str, password: str):
        """Adds admin user if missing from 'admin' database."""
        try:
            cls.auth_conn.command("createUser", username,
                                  pwd=password,
                                  roles=[{'role': "dbAdminAnyDatabase",
                                          'db': cls.__auth_db}])
        except errors.OperationFailure as err:
            print("ERROR: pymongo", err)

    @classmethod
    def show_database_status(cls) -> None:
        """Displays current list of MongoDB databases on host system."""
        def_name = inspect.currentframe().f_code.co_name
        print(f"{def_name}()\n   pymongo version: {version}")
        print(f"   server_info: {cls.conn.server_info()}")
        print(f"   {cls.__media_db}.collections: "
              f"{cls.media_conn.list_collection_names()}")
        print(f"   users: {cls.conn[cls.__auth_db].command('usersInfo')}")

    @classmethod
    def show_collections(cls) -> None:
        """Displays current list of MongoDB collections on host system."""
        collections = cls.media_conn.list_collection_names()
        if collections:
            print(f"{collections}")
        else:
            print(f"database: '{cls.__media_db}.{cls.__tags_collection}' "
                  f"does not exist")

    @classmethod
    def show_object_ids(cls) -> None:
        """Displays all MongoDB objectIDs for media database."""
        cursor = cls.tags_coll.find()
        for i, doc in enumerate(cursor):
            print(f"  id_{i:02}: {doc['_id']}")

    @classmethod
    def show_tags(cls, document_id: str, limited: bool = True) -> None:
        """Displays media tags in media database."""
        if isinstance(document_id, str) or document_id:
            if ObjectId.is_valid(document_id):
                obj_dict = cls.get_media(document_id)
                print()
                if limited:
                    for key in ['_id', 'artist_name',
                                'album_title', 'track_title']:
                        print(f"  {key:16}{obj_dict[key]}")
                else:
                    for key, val in obj_dict.items():
                        if 'file_name' not in key:
                            print(f"  {key:16}{val}")

    @classmethod
    def get_object_by_key(cls, tag: str = '_id',
                          unique_set: bool = False) -> list:
        """Retrieve document by key name from media database."""
        if isinstance(tag, str) or tag:
            if unique_set:
                result_set = cls.tags_coll.distinct(tag)
            else:
                # order = pymongo.DESCENDING
                cursor_set = cls.tags_coll.find({}, {tag: 1})
                result_set = []
                for doc in cursor_set:
                    result_set.append(doc[tag])
            return result_set
        return None

    @classmethod
    def get_collection_key_names(cls) -> list:
        """Map reduce of key names in media database."""
        docs = cls.media_conn[cls.__tags_collection].find_one()
        result_set = []
        if docs:
            for key in docs:
                result_set.append(key)
        print(f"\nkey_names: \n{result_set}")
        return result_set

    @classmethod
    def upsert_single_id(cls, document_id: ObjectId, data: dict) -> ObjectId:
        """Update document by '_id' in media database, with upsert option."""
        if isinstance(data, dict) or data:
            if ObjectId.is_valid(document_id):
                result = cls.tags_coll.update_one(
                    {'_id': ObjectId(document_id)},
                    {"$set": data}, upsert=True)
                upsert_id = result.upserted_id
                if not upsert_id:  # returns None if data already in db
                    upsert_id = document_id
                return upsert_id
        return None

    @classmethod
    def upsert_single_tags(cls, tag: str, data: dict) -> ObjectId:
        """Update single document by tag keyword, with upsert option."""
        if isinstance(data, dict) or data:
            if tag in data:
                result = cls.tags_coll.update_one(
                    {tag: data[tag]},
                    {"$set": data}, upsert=True)
                upsert_id = result.upserted_id
                if not upsert_id:  # returns None if data already in db
                    media_data = cls.tags_coll.find_one({tag: data[tag]})
                    upsert_id = media_data['_id']
                return upsert_id
        return None

    @classmethod
    def get_media(cls, document_id: ObjectId):
        """Retrieve single document in media database, from objectID."""
        media_data = None
        if isinstance(document_id, ObjectId) or document_id:
            if ObjectId.is_valid(document_id):
                media_data = cls.tags_coll.find_one(
                    {'_id': ObjectId(document_id)})
        return media_data

    @classmethod
    def get_media_by_filename(cls, file_path: pathlib.Path):
        """Retrieve single id in media database, from filename."""
        media_data = None
        if isinstance(file_path, pathlib.Path) or file_path:
            media_data = cls.tags_coll.find_one({'file_name': file_path.name})
        return media_data

    @classmethod
    def update_existing(cls, document_id: ObjectId, data: dict) -> bool:
        """Update document in media database, from objectID and new data."""
        status = False
        if isinstance(document_id, ObjectId) or document_id:
            if ObjectId.is_valid(document_id):
                result = cls.tags_coll.update_one(
                    {'_id': ObjectId(document_id)},
                    {"$set": data})
                status = result.acknowledged
        return status

    @classmethod
    def get_gridfs_id(cls, file_path: pathlib.Path) -> ObjectId:
        """Retrieves gridfs id of document from filename."""
        if cls.grid_fs.exists({"filename": str(file_path.name)}):
            bin_media = cls.grid_fs.find_one(
                {"filename": str(file_path.name)})
            return bin_media.__getattr__('_id')
        return None

    @classmethod
    def get_bin_file(cls, document_id: ObjectId) -> bytes:
        """Retrieves binary data of document from gridfs."""
        data = None
        if isinstance(document_id, str) or document_id:
            if ObjectId.is_valid(document_id):
                data = cls.grid_fs.get(document_id).read()
        return data

    @classmethod
    def store_bin_file(cls, file_path: pathlib.Path) -> ObjectId:
        """Inserts binary data of document into gridfs."""
        try:
            if file_path.exists():
                if not cls.grid_fs.exists({"filename": str(file_path.name)}):
                    with open(f"{str(file_path)}", 'rb') as file_ptr:
                        bin_media = file_ptr.read()
                        if bin_media:
                            bin_id = cls.grid_fs.put(bin_media, filename=file_path.name)
                        file_ptr.close()
                        return bin_id
                else:
                    bin_media = cls.grid_fs.find_one(
                        {"filename": str(file_path.name)})
                    return bin_media.__getattr__('_id')
            else:
                print(f"input path not found... {file_path}")
            return None
        except (gridfs.errors.GridFSError, gridfs.errors.FileExists) as exc:
            print(f"  {sys.exc_info()[0]}\n {exc}")

    @classmethod
    def remove_data(cls, document_id: ObjectId) -> bool:
        """Drops single document from media database."""
        status = False
        if isinstance(document_id, str) or document_id:
            if ObjectId.is_valid(document_id):
                doc = cls.tags_coll.delete_one({'_id': ObjectId(document_id)})
                status = doc.acknowledged
        return status

    @classmethod
    def drop_database(cls) -> None:
        """Removes tag and gridfs collections from media_db."""
        cls.conn.drop_database(cls.__media_db)
        print(f"   databases: {cls.conn.list_database_names()}")
