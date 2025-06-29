set -o errexit -o nounset

export PROJECT="phq-ghost-name-picker"
export FLASK_ENV="development"
export FLASK_APP="main:app"
export FLASK_DEBUG=1
export PYTHONDONTWRITEBYTECODE=1

# Set --host-port to work around bug with NDB unable to connect to ::1.
# gcloud beta emulators datastore start \
#     --project "$PROJECT" \
#     --host-port localhost \
#     &

# sleep 5
# $(gcloud beta emulators datastore env-init)

# Start your local development server.
export FLASK_SETTINGS_FILENAME="settings.py"
export GCP_PROJECT_ID="phq-ghost-name-picker"
FLASK_ENV="$FLASK_ENV" FLASK_APP="$FLASK_APP" flask run

# Clean up the datastore emulator.
# curl --silent -X POST "$DATASTORE_HOST/shutdown"