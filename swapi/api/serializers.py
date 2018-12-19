

def serialize_people_as_json(people):
    return {
        'name': people.name,
        'height': people.height,
        'mass': people.mass,
        'hair_color': people.hair_color,
        'created': people.created.isoformat(),
    }
