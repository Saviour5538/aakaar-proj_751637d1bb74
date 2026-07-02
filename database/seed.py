import uuid
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base, engine, SessionLocal, User, Todo

def seed_database():
    session = SessionLocal()
    try:
        # Clear existing data
        session.query(Todo).delete()
        session.query(User).delete()
        session.commit()

        # Insert sample users
        user1 = User(
            id=uuid.uuid4(),
            email="alice@example.com",
            password_hash="hashed_password_1",
            created_at="2023-01-01 00:00:00"
        )
        user2 = User(
            id=uuid.uuid4(),
            email="bob@example.com",
            password_hash="hashed_password_2",
            created_at="2023-01-02 00:00:00"
        )
        user3 = User(
            id=uuid.uuid4(),
            email="charlie@example.com",
            password_hash="hashed_password_3",
            created_at="2023-01-03 00:00:00"
        )

        session.add_all([user1, user2, user3])

        # Insert sample todos
        todo1 = Todo(
            id=uuid.uuid4(),
            user_id=user1.id,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=False,
            due_date="2023-01-10 00:00:00",
            created_at="2023-01-01 00:00:00",
            updated_at="2023-01-01 00:00:00"
        )
        todo2 = Todo(
            id=uuid.uuid4(),
            user_id=user2.id,
            title="Finish project",
            description="Complete the final report",
            completed=False,
            due_date="2023-01-15 00:00:00",
            created_at="2023-01-02 00:00:00",
            updated_at="2023-01-02 00:00:00"
        )
        todo3 = Todo(
            id=uuid.uuid4(),
            user_id=user3.id,
            title="Call mom",
            description="Weekly check-in",
            completed=True,
            due_date="2023-01-05 00:00:00",
            created_at="2023-01-03 00:00:00",
            updated_at="2023-01-03 00:00:00"
        )

        session.add_all([todo1, todo2, todo3])
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_database()