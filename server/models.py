from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy


metadata=MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    
    }
)

db=SQLAlchemy(metadata=metadata)

class Episode(db.Model,SerializerMixin):
    __tablename__='episodes'
    serialize_rules=('-appearances.episode', )

    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.DateTime)
    number=db.Column(db.Integer)

    appearances=db.relationship( 'Appearance' ,back_populates="episode" ,cascade='all, delete-orphan')
    
    

    def __repr__(self):

        return f"<Episode {self.id}, date:{self.date} ,number:{self.number}>" 


class Guest(db.Model,SerializerMixin):
    __tablename__='guests'
    serialize_rules=('-appearances.guest', )
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    occupation=db.Column(db.String,nullable=False)
    

    appearances=db.relationship( 'Appearance' ,back_populates="guest" ,cascade='all, delete-orphan')
    def __repr__(self):

        return f"<Guest {self.id},name:{self.name} ,occupation:{self.occupation}>" 
    
class Appearance(db.Model,SerializerMixin):
    __tablename__="appearances"
    serialize_rules=("-episode.appearances", "-guest.appearances")

    id=db.Column(db.Integer,primary_key=True)
    rating=db.Column(db.Integer)
    


    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        allowed_values = [1,2,3,4,5]
        if value not in allowed_values:
            raise ValueError(f"Rating must be one of {allowed_values}")
        self._rating = value
        
    episode_id=db.Column(db.Integer,db.ForeignKey("episodes.id"))
    guest_id=db.Column(db.Integer,db.ForeignKey("guests.id"))    
    

    episode=db.relationship("Episode" , back_populates="appearances")
    guest=db.relationship("Guest" , back_populates="appearances")
    
    def __repr__(self):
        return f"<Appearance {self.id} has a rating of {self.rating} for episode {self.episode_id} and guest {self.guest_id}>"