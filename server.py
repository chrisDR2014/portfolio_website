from flask import Flask
from flask_bootstrap import Bootstrap5
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
bootstrap = Bootstrap5(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Project(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    link: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    github_link: Mapped[str] = db.Column(db.String(300), unique=True, nullable=False)
    image_path: Mapped[str] = db.Column(db.String(300), unique=True, nullable=False)

with app.app_context():
    db.create_all()

"""new_project = Project(name="My Story",
                      description="This is a short story that I've created for the public to be able to enjoy for their entertainment.", 
                      link="hello.html", 
                      github_link="https://github.com/chrisDR2014/Story", 
                      image_path="https://images.pexels.com/photos/874242/pexels-photo-874242.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
    db.session.add(new_project)
    db.session.commit() """

@app.route('/')
def home():

    result = db.session.execute(db.select(Project))
    projects = result.scalars().all()
    for project in projects:
        print(project.image_path)
    return render_template('index.html', projects=projects)


if __name__ == '__main__':

    app.run(host="0.0.0.0", debug=True)