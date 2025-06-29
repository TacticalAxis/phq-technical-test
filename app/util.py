import os
from dotenv import load_dotenv
from flask.sessions import SessionMixin
from google.cloud import secretmanager
from typing import List
import csv

from app.models import PhantomData

def load_environment_variables():
    """Loads the environment variables from file.
    """
    load_dotenv()


def get_secret_value(secret_id: str, version_id: str = "latest") -> str:
    """Returns a secret value stored in either the envvars or secrets manager.

    Args:
        secret_id (str): The secret identifier.
        version_id (str, optional): The version number. Defaults to "latest".

    Returns:
        str: Returns the value of the secret.
    """
    
    # check if the secret was in the environment variables
    env_secret = os.environ.get(secret_id)
    if env_secret:
        return env_secret
    
    # get secret value from secret manager
    project_id = os.environ.get("GCP_PROJECT_ID")
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    secret_client = secretmanager.SecretManagerServiceClient()
    
    response = secret_client.access_secret_version(request={"name": secret_name})
    secret_payload = response.payload.data.decode("UTF-8")
    
    return secret_payload


def session_active(session: SessionMixin) -> bool:
    """
    Check if the session is active.

    Args:
        session (SessionMixin): The Flask session object.

    Returns:
        bool: Returns true if the session exists.
    """
    return session.get("user") != None


def get_session_user(session: SessionMixin) -> dict:
    """
    Retrieve the user dict from the session.

    Args:
        session (SessionMixin): The Flask session object.

    Returns:
        dict: The user dict from the session, or an empty dict if not found or invalid.
    """
    user = session.get("user") if session else None
    return user if isinstance(user, dict) else {}

def load_ghost_names() -> List[PhantomData]:
    data:List[PhantomData] = []
    with open("./data/ghost_names.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ghost_name = row['Ghost name']
            ghost_description = row['Description']
            data.append(PhantomData(ghost_name=ghost_name, ghost_description=ghost_description))
    return data
    