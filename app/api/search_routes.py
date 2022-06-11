from sqlalchemy import or_, and_
from flask import Blueprint, jsonify, request
from app.models import Property, State

search_routes = Blueprint('search', __name__)



@search_routes.route("/<term>")
def search_by_term(term):

    # search by street
    split = term.split("-")
    st_num = split[0]
    st_name = " ".join(split[1:])
    streets = Property.query.filter(Property.st_num.ilike(f"%{st_num}%"), Property.st_name.ilike(f"%{st_name}%")).all()

    if streets:
        return {"properties": [street.to_dict() for street in streets]}


    parsedTerm = " ".join(term.split("-"))

    # search by zip
    zips = Property.query.filter(Property.zip.ilike(f"%{parsedTerm}%")).all()

    if zips:
        return {"properties": [property.to_dict() for property in zips]}

    results = []

    # search by city
    properties = Property.query.filter(Property.city.ilike(f"%{parsedTerm}%")).all()

    if properties:
        results.extend([property.to_dict() for property in properties])
        return {"properties": results}




    # search by street name
    street = Property.query.filter(Property.st_name.ilike(f"%{parsedTerm}%")).all()

    if street:
        results.extend([property.to_dict() for property in street])
        return {"properties": results}

    # search by street or
    streets_or = Property.query.filter(or_(Property.st_num.ilike(f"%{st_num}%"), Property.st_name.ilike(f"%{st_name}%"))).all()

    if streets_or:
        results.extend([property.to_dict() for property in streets_or])

    return {"properties": results}


@search_routes.route("/terms", methods=["GET"])
def search_terms():
    properties = Property.query.all()
    allStates = State.query.all()
    addresses = [property.st_num+" "+property.st_name.strip() for property in properties]
    cities = [property.city for property in properties]
    zip = [property.zip for property in properties]
    terms = set(cities + zip + addresses)
    sort = sorted(list(terms), key=str.casefold)

    return {"terms": sort}
