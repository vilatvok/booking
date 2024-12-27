
def format_offer(data, owner=None) -> dict:
    offer_entity = data.to_entity()

    prices = data.prices
    price_entity = prices.to_entity()

    images = []
    for image in data.images:
        image_entity = image.to_entity()
        images.append(image_entity.to_dict())

    response_data = offer_entity.to_dict()
    if owner:
        response_data['owner'] = owner
    else:
        response_data['owner'] = data.owner.username
    response_data['prices'] = price_entity.to_dict()
    response_data['images'] = images
    return response_data
