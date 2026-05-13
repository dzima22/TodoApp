from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from ..models import Todos,Users
import pytest 
from ..routers.auth import bcrypt_context


sql_alchemy_database_url='sqlite:///./testdb.db'
engine=create_engine(sql_alchemy_database_url,connect_args={"check_same_thread":False},poolclass=StaticPool)

testingsessiolocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=testingsessiolocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return{"username":"sani","id":1,"user_role":"admin"}

client=TestClient(app)

@pytest.fixture
def test_todo():
    todo=Todos(title="Learn to code!",
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1)
    db=testingsessiolocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user=Users(username="sani",
               email="sani@email.com",
               first_name="sani",
               last_name="alto",
               is_active=True,
               hashed_password=bcrypt_context.hash("testpassword"),
               role="admin",
               phone_number="(111)-111-1111")
    db=testingsessiolocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()