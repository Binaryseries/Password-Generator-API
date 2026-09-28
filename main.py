import secrets
import string
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Password Generator API",
    description="Generates cryptographically secure passwords for user signup flows.",
    version="1.0.0"
)

# Enable CORS so web apps can invoke this directly from frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input parameters schema
class PasswordParams(BaseModel):
    length: int = Field(default=16, ge=8, le=128, description="Password length (8-128)")
    use_uppercase: bool = Field(default=True, description="Include A-Z")
    use_lowercase: bool = Field(default=True, description="Include a-z")
    use_digits: bool = Field(default=True, description="Include 0-9")
    use_symbols: bool = Field(default=True, description="Include special characters (!@#$%...)")
    custom_symbols: str | None = Field(
        default="!@#$%^&*()_+-=[]{}|;:,.<>?",
        description="Override allowed special characters"
    )

# Response schema
class PasswordResponse(BaseModel):
    password: str
    length: int
    entropy_bits: float

def calculate_entropy(length: int, pool_size: int) -> float:
    """Calculates password strength entropy in bits."""
    import math
    if pool_size <= 0 or length <= 0:
        return 0.0
    return round(length * math.log2(pool_size), 2)

def generate_secure_password(params: PasswordParams) -> tuple[str, float]:
    pools = []
    guaranteed_chars = []

    if params.use_uppercase:
        pools.append(string.ascii_uppercase)
        guaranteed_chars.append(secrets.choice(string.ascii_uppercase))

    if params.use_lowercase:
        pools.append(string.ascii_lowercase)
        guaranteed_chars.append(secrets.choice(string.ascii_lowercase))

    if params.use_digits:
        pools.append(string.digits)
        guaranteed_chars.append(secrets.choice(string.digits))

    if params.use_symbols and params.custom_symbols:
        pools.append(params.custom_symbols)
        guaranteed_chars.append(secrets.choice(params.custom_symbols))

    if not pools:
        raise HTTPException(
            status_code=400, 
            detail="At least one character set (uppercase, lowercase, digits, symbols) must be enabled."
        )

    full_pool = "".join(pools)
    
    if len(guaranteed_chars) > params.length:
        raise HTTPException(
            status_code=400,
            detail=f"Requested length ({params.length}) is too short for selected character types."
        )

    # Fill remaining slots with cryptographically secure random choices
    remaining_length = params.length - len(guaranteed_chars)
    random_chars = [secrets.choice(full_pool) for _ in range(remaining_length)]
    
    # Combine guaranteed characters + remaining characters and shuffle securely
    password_list = guaranteed_chars + random_chars
    
    # Cryptographic shuffle using Fisher-Yates with secrets.randbelow
    for i in range(len(password_list) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_list[i], password_list[j] = password_list[j], password_list[i]

    password = "".join(password_list)
    entropy = calculate_entropy(params.length, len(set(full_pool)))
    
    return password, entropy


@app.get("/api/v1/generate", response_model=PasswordResponse)
async def generate_password_get(
    length: int = Query(16, ge=8, le=128),
    use_uppercase: bool = Query(True),
    use_lowercase: bool = Query(True),
    use_digits: bool = Query(True),
    use_symbols: bool = Query(True)
):
    """GET endpoint for easy integration via standard API queries."""
    params = PasswordParams(
        length=length,
        use_uppercase=use_uppercase,
        use_lowercase=use_lowercase,
        use_digits=use_digits,
        use_symbols=use_symbols
    )
    password, entropy = generate_secure_password(params)
    return PasswordResponse(password=password, length=len(password), entropy_bits=entropy)


@app.post("/api/v1/generate", response_model=PasswordResponse)
async def generate_password_post(params: PasswordParams):
    """POST endpoint allowing customization of custom symbol sets in body payload."""
    password, entropy = generate_secure_password(params)
    return PasswordResponse(password=password, length=len(password), entropy_bits=entropy)