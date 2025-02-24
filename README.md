Refer this for understanding this backend.

## **Project Structure**

The project is structured as follows:
-  **`backend`**

-  **`accounts_app`**: For handling user authentication, profile management, and user-related operations.

-  **`banking_app`**: Managing banking-related operations such as accounts, transactions, and transaction statistics.
---

## **API Endpoints**

### **Authentication & User Management**

#### **1. Signup**

-  **URL**: `/api/auth/signup/`
-  **Method**: `POST`
-  **Description**: Creates a new user.
-  **Request Body**:

```json
{
  "username": "string",
  "email": "string",
  "full_name": "string",
  "password": "string",
  "confirm_password": "string"
}
```

*I think that the confirm_password would be better to implement on the frontend, as user would get the notificaton as there is a mismatch between the password and confirm_password fields.*


-  **Response**:

```json
{
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "full_name": "string",
    "profile_image": "string (URL)"
  },

  "refresh": "string (JWT refresh token)",
  "access": "string (JWT access token)"
}
```

  

#### **2. Login**

-  **URL**: `/api/auth/login/`
-  **Method**: `POST`
-  **Description**: Authenticates a user and returns JWT tokens.
-  **Request Body**:

```json
{
  "email": "string",
  "password": "string"
}
```

-  **Response**:
```json
{
    "refresh": "string (JWT refresh token)",
    "access": "string (JWT access token)",
    "user": {
        "id": "integer",
        "email": "string",
        "username": "string",
        "full_name": "string",
        "profile_image": "string (URL)"
    },
    "accounts": [
        {
            "id": "integer",
            "name": "string",
            "account_number": "string",
            "balance": "decimal"
        },
        ... (Other Accounts)
    ]
}
```

#### **3. Profile Image Management**
-  **URL**: `/api/auth/profile-image/`
-  **Headers**: `Authorization: Bearer <access_token>`
  (replace <access_token> with the actual token)
-  **Method**: `PUT` (Updates photo of the user)  `PATCH` (Update from previous image), `DELETE` (Remove)
-  **Description**: Updates or deletes the user's profile image.
-  **Request Body (PATCH)**:
```json
{
    "profile_image": "file"
}
```
-  **Response (PATCH)**:
```json
{
    "profile_image": "string (URL)"
}
```
-  **Response (DELETE)**: `204 No Content`

---

### **Banking Operations**

For all the endpoints below you would have to use authrization
**Headers**: `Authorization: Bearer <access_token>`  (replace <access_token> with the actual token)

#### **1. Account Management**

-  **URL**: `/api/banking/accounts/`
-  **Method**: `GET` (List), `POST` (Create)
-  **Description**: Lists all accounts or creates a new account.
-  **Request Body (POST)**:

```json
{
    "name": "string",
    "account_number": "string",
    "balance": "decimal"
}
```
-  **Response (POST)**:
```json
{
    "id": "integer",
    "name": "string",
    "account_number": "string",
    "balance": "decimal"
}
```
-  **URL**: `/api/banking/accounts/<int:pk>/`
-  **Method**: `GET` (Retrieve), `PUT` (Update), `PATCH`(Update limited number of field), `DELETE` (Delete)
-  **Description**: Retrieves, updates, or deletes a specific account.

 
#### **2. Transaction Management**

-  **URL**: `/api/banking/transactions/`
-  **Method**: `GET` (List), `POST` (Create)
-  **Description**: Lists all transactions or creates a new transaction.
-  **Request Body (POST)**:
```json
{
    "account": "integer (account ID)",
    "name": "string",
    "amount": "decimal",
    "type": "string (credit/debit)",
    "category": "string",
    "date": "string (YYYY-MM-DD)",
    "description": "string"
}
```

-  **Response (POST)**:
```json
{
    "id": "integer",
    "account": "integer",
    "name": "string",
    "amount": "decimal",
    "type": "string",
    "category": "string",
    "date": "string (YYYY-MM-DD)",
    "description": "string"
}
```

-  **URL**: `/api/banking/transactions/<int:pk>/`
-  **Method**: `GET` (Retrieve), `PUT` (Update), `PATCH`,  `DELETE` (Delete)
-  **Description**: Retrieves, updates, or deletes a specific transaction.

#### **3. Transaction Statistics**

-  **URL**: `/api/banking/stats/`
-  **Method**: `GET`
-  **Description**: Returns filtered transactions based on query parameters.
-  **Query Parameters**:
    -  `start_date`: Start date for filtering (format: `YYYY-MM-DD`).
    -  `end_date`: End date for filtering (format: `YYYY-MM-DD`).
    *Put both to get the desired result of filtering the data between two dates*
    -  `category`: Filter by category.
    -  `type`: Filter by transaction type (`credit` or `debit`).
    -  `account`: Filter by account ID.

- Example requests:
    -  `http://127.0.0.1:8000/api/banking/stats/?account=2&category=Income`
    - `http://127.0.0.1:8000/api/banking/stats/?type=credit`
-  **Response**:
```json
{
    "transactions": [
        {
        "id": "integer",
        "account": "integer",
        "name": "string",
        "amount": "decimal",
        "type": "string",
        "category": "string",
        "date": "string (YYYY-MM-DD)",
        "description": "string"
        },
        ... (Other Transactions)
    ],
    "filters": {
        "start_date": "string (YYYY-MM-DD)",
        "end_date": "string (YYYY-MM-DD)",
        "category": "string",
        "type": "string",
        "account": "integer"
    }
}
```

---

## **Dependencies**

To set up the project, install the following dependencies:
```bash
pip  install  -r  requirements.txt
```

---

## **Setting Up the Project**

1.  **Clone the repository**:
```bash
git clone <repository-url>
cd <project-folder>
```
2.  **Install dependencies**:

<div align="center">OR</div>

```bash
pip install -r requirements.txt
```
Install all the necessary dependencies.

3.  **Run migrations**:
```bash
python manage.py migrate
```

4.  **Run the server**:
```bash
python manage.py runserver
```
5.  **Access the API**:
- The API will be available at `http://127.0.0.1:8000/`. Use the checkpoints to proceed and get going.
---

## **Authentication**

- Use the JWT tokens returned from the `/api/auth/login/` or `/api/auth/signup/` endpoints for authenticated requests.

- Include the token in the `Authorization` **header** wherever you are making the requests from any other endpoints than `api/auth/signup/`or `api/auth/login/`:

```plaintext
Authorization: Bearer <access_token>
```
Currently the access token lasts for 15 mins, after that you would have to login again, or else we can change this window as required.

---

## **Media Files**
- Profile images are stored in the `media/` directory.
- The URL for accessing media files is `/media/<file-path>`.
