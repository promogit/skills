# Create a session

Send a `POST` request to `/v1/sessions`.

The response contains the session identifier and its expiration time.

If the server returns `409`, reuse the active session identifier from the response body.

