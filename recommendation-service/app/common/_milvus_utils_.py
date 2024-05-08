from functools import lru_cache
from pymilvus import CollectionSchema, DataType, FieldSchema, connections as MilvusConnManager, db as MilvusDBManager, utility as MilvusUtility, Collection

from common import ConfigVars



def get_collection(name):
    return Collection(using=ConfigVars.MILVUS_CONN_ALIAS, name=name)

def configure_milvus(recreate_collections=False):
    # Create database, if not exists
    MilvusConnManager.connect("default", host=ConfigVars.MILVUS_HOST, port=ConfigVars.MILVUS_PORT)
    if ConfigVars.MILVUS_DATABASE not in MilvusDBManager.list_database():
        MilvusDBManager.create_database(db_name=ConfigVars.MILVUS_DATABASE)
    
    conn_config = {"user": "", "address": f"{ConfigVars.MILVUS_HOST}:{ConfigVars.MILVUS_PORT}"}
    MilvusConnManager.add_connection(**{ConfigVars.MILVUS_CONN_ALIAS: conn_config})
    MilvusConnManager.connect(alias=ConfigVars.MILVUS_CONN_ALIAS, host=ConfigVars.MILVUS_HOST, port=ConfigVars.MILVUS_PORT, db_name=ConfigVars.MILVUS_DATABASE)
    MilvusConnManager.connect(alias=ConfigVars.MILVUS_CONN_ALIAS)
    
    
    
    # Use database throughout the application
    MilvusDBManager.using_database(using=ConfigVars.MILVUS_CONN_ALIAS, db_name=ConfigVars.MILVUS_DATABASE)
    
    # Create collections, if required
    _collection_create_(ConfigVars.MILVUS_COL_USERS, "This collection holds user vector data", recreate_collection=recreate_collections)
    _collection_create_(ConfigVars.MILVUS_COL_PRODS, "This collection holds product vector data", recreate_collection=recreate_collections)



def _collection_users_get_fields(vec_dim:int = 384):
    return [
        FieldSchema(name="id",             dtype=DataType.INT64,                         is_primary=True,   auto_id=False),
        FieldSchema(name="title",          dtype=DataType.VARCHAR,      max_length=512),
        FieldSchema(name="vector_str",     dtype=DataType.VARCHAR,      max_length=8192),
        FieldSchema(name="vec_data",       dtype=DataType.FLOAT_VECTOR, dim=vec_dim)
    ]
def prepare_record_user_collection(customer_id:int, customer_title:str, vec_str:str, vec_data):
    return [
        [customer_id],
        [customer_title],
        [vec_str],
        [vec_data]
    ]



def _collection_prods_get_fields(vec_dim:int = 384):
    return [
        FieldSchema(name="product_id",     dtype=DataType.INT64,                         is_primary=True,   auto_id=False),
        FieldSchema(name="category_id",    dtype=DataType.INT64),
        FieldSchema(name="product_title",  dtype=DataType.VARCHAR,      max_length=500),
        FieldSchema(name="category_title", dtype=DataType.VARCHAR,      max_length=500),
        FieldSchema(name="vector_str",     dtype=DataType.VARCHAR,      max_length=8192),
        FieldSchema(name="vec_data",       dtype=DataType.FLOAT_VECTOR, dim=vec_dim)
    ]
def prepare_record_prod_collection(product_id:int, category_id:int, product_title:str, category_title:str, vec_str:str, vec_data):
    return [
        [product_id],
        [category_id],
        [product_title],
        [category_title],
        [vec_str],
        [vec_data]
    ]
def _collection_create_(
        name:str,
        description:str,
        recreate_collection:bool = False,
        vec_dim:int = 384
    ) -> Collection:
    
    collection = None
    create_collection_flag = True
    
    #region check if Collection exists or needs recreation
    if MilvusUtility.has_collection(using=ConfigVars.MILVUS_CONN_ALIAS, collection_name=name):
        create_collection_flag = False
        if recreate_collection:
            create_collection_flag = True
            MilvusUtility.drop_collection(using=ConfigVars.MILVUS_CONN_ALIAS, collection_name=name)
        else:
            collection = Collection(using=ConfigVars.MILVUS_CONN_ALIAS, name=name)
    #endregion
    
    #region create Collection, if needed
    if create_collection_flag:
        fields = None
        if name == ConfigVars.MILVUS_COL_USERS:
            fields = _collection_users_get_fields(vec_dim)
        elif name == ConfigVars.MILVUS_COL_PRODS:
            fields = _collection_prods_get_fields(vec_dim)
        
        schema = CollectionSchema(fields, description)
        collection = Collection(using=ConfigVars.MILVUS_CONN_ALIAS, name=name, schema=schema, consistency_level="Strong")
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "IP",
            "params": {"nlist": 128},
        }
        collection.create_index(field_name="vec_data", index_params=index_params)
    #endregion
    
    collection.load()
    return collection


