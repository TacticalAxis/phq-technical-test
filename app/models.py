from google.cloud import ndb

# Define a simple NDB model
class GhostUser(ndb.Model):
    """The GhostUser model
    
    user_id: The id of the user
    ghost_name: The ghost_name of the user
    created_at: The creation time of the user
    
    Args:
        ndb (_type_): extends the ndb Model
    """
    user_id = ndb.StringProperty()
    ghost_name = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
