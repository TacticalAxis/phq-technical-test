import os
from dotenv import load_dotenv
from google.cloud import secretmanager

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
