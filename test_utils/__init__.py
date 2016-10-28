from itertools import chain


# https://docs.djangoproject.com/en/1.10/ref/models/meta/
def get_all_field_names(model_class):
    field_names = list(set(chain.from_iterable(
        (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
        for field in model_class._meta.get_fields()
        # For complete backwards compatibility, you may want to exclude
        # GenericForeignKey from the results.
        if not (field.many_to_one and field.related_model is None)
    )))
    return field_names
