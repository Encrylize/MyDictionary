def get_or_create(model, **kwargs):
    """ Returns an instance of model and whether or not it already existed in a tuple. """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        return instance, True