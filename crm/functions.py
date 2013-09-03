__author__ = 'Zarin'

def get_choicename(obj, fieldname):
    """
    given an object and a field which has a choices argument,
    find the name of choice for that field instead of its stored
    database number svalue

    returns the tuple ( '$field$_choicename', field_choicename
    """
    field_key=int(getattr(obj, fieldname))
    field = obj._meta.get_field(fieldname) #*
    field_choicename=[val for key,val in field.choices if key==field_key][0]
    return '%s_choicename'%fieldname, field_choicename