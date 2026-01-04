
# B. Security and Validation Proof

## Security

**Authentication**: The system is built on a robust authentication model using **JSON Web Tokens (JWT)**. Users must register and log in to access protected administrative parts of the application. The frontend securely manages these tokens to maintain user sessions.

**Password Hashing**: User passwords are **never stored in plain text**. They are securely hashed on the backend using the **PBKDF2-SHA256** algorithm via the `passlib` library before being stored in the database. This ensures that even if the database is compromised, user credentials remain secure.

**Authorization & API Security**: The core security principle involves strict separation of concerns. Agents authenticate via **API Keys** (`X-API-Key` header), while administrative actions require a valid **JWT**. Every protected API endpoint uses a FastAPI dependency (`Depends`) to verify credentials before processing the request.

**Code Evidence (Protected Endpoint):**
The following code snippet from `backend/app/api/endpoints.py` demonstrates how the `delete_system` endpoint is protected. It forces the `get_current_user` dependency, ensuring only authenticated users can delete system records.

```python
# backend/app/api/endpoints.py

@router.delete("/systems/{system_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def delete_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    
    # Cascade deletes metrics and alerts automatically
    db.delete(system)
    db.commit()
    return None
```

**Database Proof (Hashed Credentials):**
The screenshot/table below verifies that sensitive user data is stored securely. Note the `hashed_password` column contains unreadable hash strings, not plain text.

| ID | Username / Email | Hashed Password | Is Active |
|----|------------------|-----------------|-----------|
| 1 | nthy2355@gmail.com | `$pbkdf2-sha256$29000$WKv1nhOCMOa...` | True |

*(Note: The full hash is truncated for display purposes)*

## Validation

**Frontend Validation**: The React dashboard implements client-side validation, ensuring forms (like Login or Settings) are filled out correctly before sending requests.

**Backend Validation**: The FastAPI backend uses **Pydantic** for powerful, automatic data validation. Every incoming request is strictly validated against a defined schema. If a client sends data of the wrong type (e.g., sending text for a CPU usage percentage which expects a float), the request is automatically rejected with a `422 Unprocessable Entity` error. This ensures that **no invalid data can ever reach the database**.

**Code Evidence (Schema Validation):**
The following snippet from `backend/app/schemas/schemas.py` shows the strict typing enforced on System data.

```python
# backend/app/schemas/schemas.py

class SystemBase(BaseModel):
    hostname: str
    ip_address: Optional[str] = None
    cpu_cores: Optional[int] = None      # Must be an Integer
    total_memory_gb: Optional[float] = None # Must be a Float
    
    # If a user attempts to send "ten" for cpu_cores, 
    # the server rejects it before it executes any code.
```
