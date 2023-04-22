from fastapi import APIRouter
from models.user import User ,Organisation, Permissions
from config.db import conn 
from schemas.user import serializeDict, serializeList
from bson import ObjectId
from fastapi import HTTPException
import pydantic
from bson import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

user = APIRouter() 

#user apis
#create a user
@user.post('/user')
async def create_user(user: User):
    conn.local.user.insert_one(dict(user))
    return serializeList(conn.local.user.find())

#list all users
@user.get("/user/")
async def list_users(name: str = None, limit: int = 10, offset: int = 0):
    if name:
        query = serializeList(conn.local.user.find({"name":name}).skip(offset).limit(limit))
    else:
        query = serializeList(conn.local.user.find())
    
    total_count=len(query)
    return{
        "count":total_count,
        "All users": query
    }

#to fetch a single user using unique id
@user.get('/user/{id}')
async def fetch_user(id):
    return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))

#to update a user
@user.put('/user/{id}')
async def update_user(id,user: User):
    conn.local.user.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(user)
    })
    return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))

#to delete a user
@user.delete('/user/{id}')
async def delete_user(id,user: User):
    return serializeDict(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))


#Organisation apis
#create an organisation
#condition: No two organisations can have same name
@user.post('/organisation')
async def create_organisation(orga :Organisation):
    if conn.local.org.find_one({"name": orga.name}):
        raise HTTPException(status_code=400, detail="Organization name already taken")
    
    conn.local.org.insert_one(dict(orga))
    return serializeList(conn.local.org.find())

#list all organisations
@user.get('/organisation/{id}')
async def list_organisations(name: str = None, limit: int = 10, offset: int = 0):
    if name:
        query = serializeList(conn.local.org.find({"name":str(name)}).skip(offset).limit(limit))
    else:
        query = serializeList(conn.local.org.find())
    
    total_count=len(query)
    return{
        "count":total_count,
        "All users": query
    }


#permissions
#create a permission
@user.post("/permissions")
def create_permission(permissions : Permissions,access_level:str="READ"):
   conn.local.permissions.insert_one(dict(permissions))
   return serializeList(conn.local.permissions.find())

#list all permissions by organisation id
@user.get('/permissions/org/{org_id}')
async def get_org_permissions(org_id):
    return serializeList(conn.local.permissions.find({"org_id":str(org_id)}))

#list all permissions by user id
@user.get('/permissions/user/{user_id}')
async def get_org_permissions(user_id):
    return serializeList(conn.local.permissions.find({"user_id":str(user_id)}))

#update a permission
@user.put('/permissions/{id}')
async def update_user(id,permissions: Permissions):
    conn.local.permissions.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(permissions)
    })
    return serializeDict(conn.local.permissions.find_one({"_id":ObjectId(id)}))

#delete a permission
@user.delete('/permissions/delete/{id}')
async def delete_user(id,permissions: Permissions):
    return serializeDict(conn.local.permissions.find_one_and_delete({"_id":ObjectId(id)}))

