from .db import db

class PropertyImg(db.Model):
    __tablename__ = "property_imgs"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String(2000))

    property = db.relationship("Property", back_populates="images")
