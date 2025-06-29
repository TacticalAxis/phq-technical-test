from google.cloud import ndb
from dataclasses import dataclass

# Define a simple NDB model
class GhostUser(ndb.Model):
    """The GhostUser model
    
    ghost_name: The ghost_name of the user
    email: The email of the user
    first_name: The email of the user
    last_name: The email of the user    
    created_at: The creation time of the user
    
    Args:
        ndb (_type_): extends the ndb Model
    """
    ghost_name = ndb.StringProperty()
    email = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)

@dataclass
class PhantomData:
    ghost_name: str
    ghost_description: str
