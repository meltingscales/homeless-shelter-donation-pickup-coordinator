# Shelter Pickup Coordinator API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Password123!",
  "name": "John Doe",
  "phone": "555-1234",
  "role": "donor",
  "shelter_id": null
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Password123!"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer <token>
```

### Donations

#### Create Donation (requires auth)
```http
POST /api/donations
Authorization: Bearer <token>
Content-Type: application/json

{
  "donor_name": "Jane Doe",
  "donor_email": "jane@example.com",
  "donor_phone": "555-5678",
  "address": "123 Main St",
  "city": "Chicago",
  "state": "IL",
  "zip_code": "60601",
  "items_text": "blankets, coats",
  "items_structured": {"clothing": {"winter": {"coats": 5}}},
  "notes": "Pickup by Friday"
}
```

#### List Donations
```http
GET /api/donations?status=available&zip_code=60601
```

#### Get Nearby Donations
```http
GET /api/donations/nearby?lat=41.8781&lng=-87.6298&radius_miles=25&status=available
```

#### Get My Donations (requires auth)
```http
GET /api/donations/my-donations
Authorization: Bearer <token>
```

#### Get Donation
```http
GET /api/donations/{donation_id}
```

#### Claim Donation (requires shelter_staff)
```http
POST /api/donations/{donation_id}/claim
Authorization: Bearer <token>
```

### Shelters

#### Create Shelter
```http
POST /api/shelters
Content-Type: application/json

{
  "name": "Helping Hands Shelter",
  "contact_name": "John Smith",
  "email": "contact@shelter.org",
  "phone": "555-9999",
  "address": "456 Shelter Ave",
  "city": "Chicago",
  "state": "IL",
  "zip_code": "60602",
  "description": "Helping those in need",
  "website": "https://shelter.org",
  "needed_items_text": "blankets, coats, socks",
  "needed_items_structured": {"clothing": {"winter": {"coats": 10}}}
}
```

#### List Shelters
```http
GET /api/shelters
```

#### Get Nearby Shelters
```http
GET /api/shelters/nearby?lat=41.8781&lng=-87.6298&radius_miles=50
```

#### Get Shelter
```http
GET /api/shelters/{shelter_id}
```

### Routes

#### Create Route (requires shelter_staff)
```http
POST /api/routes
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Friday Pickup Route",
  "description": "North side pickups",
  "shelter_id": 1,
  "driver_user_id": 5,
  "scheduled_date": "2025-02-15T09:00:00Z"
}
```

#### List Routes
```http
GET /api/routes?shelter_id=1&status=planned
Authorization: Bearer <token>
```

#### Get Route
```http
GET /api/routes/{route_id}
Authorization: Bearer <token>
```

#### Update Route
```http
PUT /api/routes/{route_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "in_progress"
}
```

#### Add Donations to Route
```http
POST /api/routes/{route_id}/pickups
Authorization: Bearer <token>
Content-Type: application/json

{
  "donation_ids": [1, 2, 3]
}
```

#### Get Route Pickups with Details
```http
GET /api/routes/{route_id}/pickups
Authorization: Bearer <token>
```

#### Update Pickup Status
```http
PUT /api/routes/pickups/{pickup_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "completed",
  "notes": "Donor was very helpful"
}
```

#### Skip Pickup
```http
POST /api/routes/pickups/{pickup_id}/skip
Authorization: Bearer <token>
Content-Type: application/json

"Bad address - donor not home"
```

#### Get Optimized Route
```http
GET /api/routes/shelter/{shelter_id}/optimized
Authorization: Bearer <token>
```

#### Get Route Summary
```http
GET /api/routes/{route_id}/summary
Authorization: Bearer <token>
```

### Items

#### Get Item Categories
```http
GET /api/items/categories
```

Returns all available item categories for donations and shelter needs:
```json
{
  "categories": {
    "food": {
      "produce": ["lettuce", "apples", ...],
      "non-perishable": ["canned meat", ...],
      ...
    },
    "clothing": {
      "shoes": ["boots", ...],
      ...
    },
    ...
  }
}
```

#### Get Flat Item List
```http
GET /api/items/flat
```

## Status Codes

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Validation Error

## User Roles

- `donor` - Can create donations
- `shelter_staff` - Can claim donations, manage routes for their shelter
- `admin` - Full access

## Interactive API Docs

When the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
