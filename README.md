# Forms Service

The Forms Service is a microservice built with FastAPI for managing customer contact forms. It handles the submission, retrieval, and archiving of cancellation and feedback forms.

## Features

- **Cancellation Forms**: Submit, list, and archive cancellation requests.
- **Feedback Forms**: Submit, list, and archive customer feedback.
- **Authentication**: Integrates with an external authentication service for token management and admin access control.

## Endpoints

### Cancellation
- `GET /forms/cancellation`: Retrieve all cancellation forms (Admin only).
- `POST /forms/cancellation`: Submit a new cancellation form.
- `PUT /forms/cancellation/{cancellation_id}/archive`: Archive a cancellation form (Admin only).

### Feedback
- `GET /forms/feedback`: Retrieve all feedback forms (Admin only).
- `POST /forms/feedback`: Submit a new feedback form.
- `PUT /forms/feedback/{feedback_id}/archive`: Archive a feedback form (Admin only).

### Token
- `POST /token`: Obtain an access token using credentials.

## Configuration

The service is configured using environment variables. You can set these in a `.env` file or in your shell environment.

### General Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `CURRENT_ENV` | Runtime environment. Set to `development` for hot reload and API docs. | `production` (implied) |
| `HOST` | The host to bind the server to. | `0.0.0.0` |
| `PORT` | The port to bind the server to. | `8008` |

### Database Configuration (PostgreSQL)

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_HOST` | Hostname of the PostgreSQL database. | `localhost` |
| `POSTGRES_PORT` | Port of the PostgreSQL database. | `5432` |
| `POSTGRES_USER` | Username for the database connection. | `root` |
| `POSTGRES_PASSWORD` | Password for the database connection. | `""` (empty) |
| `POSTGRES_DB_NAME` | Name of the database to use. | `forms` |

### Authentication Service Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `AUTH_SVC_HOST` | Hostname of the authentication service. | **Required** |
| `AUTH_SVC_PORT` | Port of the authentication service. | **Required** |
| `AUTH_SVC_USER_ENDPOINT` | Endpoint to retrieve user details. | `/user/me` |
| `AUTH_SVC_TOKEN_ENDPOINT` | Endpoint to obtain authentication tokens. | `/token` |

## Running the Service

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up environment variables**:
    Create a `.env` file based on the configuration above.

3.  **Run the application**:
    ```bash
    python main.py
    ```
    Or use the provided Dockerfile to build and run the container.