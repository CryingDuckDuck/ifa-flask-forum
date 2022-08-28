from app import app, db
from models import Role, User, Post


@app.cli.command("seed-db")
def seed_db():
    db.drop_all()
    db.create_all()

    db.session.bulk_save_objects([
        Role(name="admin"),
        Role(name="user")
    ])
    db.session.commit()

    # bulk_save_objects won't trigger events (user => before_insert)
    db.session.add(
        User(email="admin@admin.ch", password="password", username="admin", role_id=1)
    )
    db.session.add(
        User(email="user@user.ch", password="password", username="user", role_id=2)
    )
    db.session.commit()

    db.session.bulk_save_objects([
        Post(title="First post of the page",
             body="orem ipsum dolor sit amet, consectetur adipiscing elit. Aenean diam justo, accumsan vel pretium "
                  "ac, cursus quis arcu. Nulla cursus quam eu enim pharetra convallis. Nunc elementum ipsum ac "
                  "scelerisque molestie. Ut at augue ultrices, aliquet tellus quis, fermentum nunc. Maecenas sed "
                  "nulla non erat sodales vulputate. Etiam et neque tortor. Orci varius natoque penatibus et magnis "
                  "dis parturient montes, nascetur ridiculus mus. Pellentesque nec placerat purus, eu efficitur elit. "
                  "Curabitur vel faucibus lectus. Praesent venenatis nunc in ultrices mattis. Pellentesque dui nibh, "
                  "dignissim id viverra non, rutrum nec orci. Vestibulum a ex dui.",
             user_id=2),
        Post(title="Second one",
             body="orem ipsum dolor sit amet, consectetur adipiscing elit. Aenean diam justo, accumsan vel pretium "
                  "ac, cursus quis arcu. Nulla cursus quam eu enim pharetra convallis. Nunc elementum ipsum ac "
                  "scelerisque molestie. Ut at augue ultrices, aliquet tellus quis, fermentum nunc. Maecenas sed "
                  "nulla non erat sodales vulputate. Etiam et neque tortor. Orci varius natoque penatibus et magnis "
                  "dis parturient montes, nascetur ridiculus mus. Pellentesque nec placerat purus, eu efficitur elit. "
                  "Curabitur vel faucibus lectus. Praesent venenatis nunc in ultrices mattis. Pellentesque dui nibh, "
                  "dignissim id viverra non, rutrum nec orci. Vestibulum a ex dui.",
             user_id=1),
        Post(title="Last one",
             body="orem ipsum dolor sit amet, consectetur adipiscing elit. Aenean diam justo, accumsan vel pretium "
                  "ac, cursus quis arcu. Nulla cursus quam eu enim pharetra convallis. Nunc elementum ipsum ac "
                  "scelerisque molestie. Ut at augue ultrices, aliquet tellus quis, fermentum nunc. Maecenas sed "
                  "nulla non erat sodales vulputate. Etiam et neque tortor. Orci varius natoque penatibus et magnis "
                  "dis parturient montes, nascetur ridiculus mus. Pellentesque nec placerat purus, eu efficitur elit. "
                  "Curabitur vel faucibus lectus. Praesent venenatis nunc in ultrices mattis. Pellentesque dui nibh, "
                  "dignissim id viverra non, rutrum nec orci. Vestibulum a ex dui.",
             user_id=2),
    ])
    db.session.commit()
