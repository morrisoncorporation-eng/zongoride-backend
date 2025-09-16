# ZongoRide Mobile App Integration Guide

This document provides all the necessary details for developing a mobile application that uses the ZongoRide Fleet Management API as its backend.

## 1. Base URL

All API endpoints are relative to the base URL.

*   **Production/Staging:** `https://8000-firebase-zongoridebackend-1757577652061.cluster-2ywkqesibzdhuvybgxpusl4nj2.cloudworkstations.dev/`
*   **Local Development:** `http://localhost:8000/`

All endpoints listed below should be appended to this base URL. For example: `http://localhost:8000/api/token/`.

---

## 2. Authentication

The API uses JSON Web Tokens (JWT) for authentication. All requests to protected endpoints must include an `Authorization` header containing a valid access token.

`Authorization: Bearer <your_access_token>`

### Acquiring Tokens (Login)

To log a user in and get their initial tokens, send a `POST` request with their credentials.

*   **Endpoint:** `/api/token/`
*   **Method:** `POST`
*   **Body:**
    ```json
    {
        "username": "testuser",
        "password": "somepassword"
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
The mobile application must securely store both the `access` and `refresh` tokens.

### Refreshing Access Tokens

The access token has a short lifespan. When it expires, you must use the refresh token to get a new one without requiring the user to log in again.

*   **Endpoint:** `/api/token/refresh/`
*   **Method:** `POST`
*   **Body:**
    ```json
    {
        "refresh": "<the_long_lived_refresh_token>"
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

---

## 3. Core API Endpoints

These are the primary endpoints the mobile application will use.

### A. Finding Scooters

#### List All Scooters

Returns a list of all scooters in the fleet. The mobile app should filter this list on the client-side to show scooters with `status: "available"`.

*   **Endpoint:** `/api/scooters/`
*   **Method:** `GET`
*   **Permissions:** Authenticated User

#### Find Nearby Scooters

Returns a list of available scooters, sorted by distance from the user's current location.

*   **Endpoint:** `/api/scooters/nearby/`
*   **Method:** `GET`
*   **Permissions:** Authenticated User
*   **Query Parameters:**
    *   `latitude`: (Required) The user's current latitude.
    *   `longitude`: (Required) The user's current longitude.
*   **Example Request:** `GET /api/scooters/nearby/?latitude=40.748&longitude=-73.985`

### B. Managing Rides

#### Unlock a Scooter (Start a Ride)

Changes a scooter's status to "in_use" and creates a new ride history record for the user.

*   **Endpoint:** `/api/scooters/<scooter_id>/unlock/`
*   **Method:** `POST`
*   **Permissions:** Authenticated User
*   **Success Response (200 OK):** The updated `Scooter` object.

#### Lock a Scooter (End a Ride)

Changes a scooter's status to "available" and completes the user's active ride record, calculating the duration.

*   **Endpoint:** `/api/scooters/<scooter_id>/lock/`
*   **Method:** `POST`
*   **Permissions:** Authenticated User
*   **Success Response (200 OK):** The updated `Scooter` object.

### C. User Ride History

#### Get User's Ride History

Returns a list of all past rides for the currently authenticated user, sorted from most recent to oldest.

*   **Endpoint:** `/api/ride-history/`
*   **Method:** `GET`
*   **Permissions:** Authenticated User

---

## 4. Data Models (JSON Structure)

### Scooter Model

```json
{
    "id": 1,
    "model": "Zongo X1",
    "status": "available", // Can be "available", "in_use", "maintenance", "low_battery"
    "location": {
        "type": "Point",
        "coordinates": [
            -73.985, // Longitude
            40.748   // Latitude
        ]
    },
    "last_updated": "2024-08-15T18:30:00Z"
}
```

### Ride History Model

```json
{
    "id": 1,
    "scooter": 1, // ID of the scooter
    "rider": 5,   // ID of the user
    "start_time": "2024-08-15T14:00:00Z",
    "end_time": "2024-08-15T14:15:22Z",
    "duration": "0:15:22",
    "start_location": { // Note: start/end locations are not yet implemented in the API
        "type": "Point",
        "coordinates": [-73.985, 40.748]
    },
    "end_location": {
        "type": "Point",
        "coordinates": [-73.990, 40.750]
    }
}
```
