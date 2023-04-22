1.Start mongodb server
---
2.Connect mongodb server with "mongodb://localhost/27017"
---
3.Create database "local"
---
4.Create following collections:
    1.user
    2.org
    3.permissions
---
5.For windows install following command:
pip install -r requirements.txt

OR

pip install fastapi pymongo uvicorn
---
6.Start server 
---
uvicorn index:app --reload
---
7.Hit this url:   http://127.0.0.1:8000/docs
---
8.All api endpoints are displayed on swagger ui


***Database Models***

user={
    "_id": ObjectId,
    "name": str,
    "email": str
}

org={
    "_id": ObjectId,
    "name": str
}

permissions=
{
    "_id": ObjectId,
    "user_id": str,
    "org_id": str,
    "access_level": str  #can be "READ", "WRITE", or "ADMIN"
}



