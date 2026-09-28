🔐 Cryptographically Secure Password Generator APIAn enterprise-ready, lightweight Python REST API built with FastAPI that generates cryptographically secure passwords for signup flows, developer tools, and user management systems.Unlike standard pseudo-random generators, this API uses Python's secrets module to ensure cryptographically strong randomness. It guarantees that generated passwords contain chosen character sets and provides an entropy calculation (in bits) to quantify password strength.✨ FeaturesCryptographically Secure: Built using Python's secrets module (suitable for managing security primitives like passwords and tokens).Guaranteed Character Inclusion: Ensures at least one character from each selected category (uppercase, lowercase, digits, symbols) is included.Configurable Constraints: Customize length (8–128 characters) and toggle specific character sets or custom symbols.Entropy Calculation: Returns the exact mathematical strength of the password in entropy bits.Developer-Friendly: Provides both GET and POST endpoints with built-in CORS support for seamless browser integration.Self-Documenting: Auto-generates Swagger UI and ReDoc documentation out of the box.🚀 QuickstartPrerequisitesPython 3.10+pip (Python package installer)1. InstallationClone the repository and install the required dependencies:git clone https://github.com/your-username/password-generator-api.git
cd password-generator-api

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2. Run the ServerStart the API server locally using uvicorn:uvicorn main:app --reload --port 8000
The API will be available at http://localhost:8000.📚 API DocumentationOnce the server is running, interactive API docs are automatically accessible at:Swagger UI: http://localhost:8000/docsReDoc: http://localhost:8000/redoc🛠️ Usage & Examples with curl1. Simple GET Request (Default Options)Generates a default 16-character password with uppercase, lowercase, numbers, and standard symbols.curl -X 'GET' 'http://localhost:8000/api/v1/generate'
Example Response:{
  "password": "k9#P2$vX7!mL4@qA9z",
  "length": 16,
  "entropy_bits": 104.96
}
2. GET Request with Query ParametersCustomize length and select specific character sets using query parameters.Request: Generate a 20-character alphanumeric password (no symbols)curl -X 'GET' \
  'http://localhost:8000/api/v1/generate?length=20&use_symbols=false'
Example Response:{
  "password": "R8vM2kP9aQ1zX4yB7cN0",
  "length": 20,
  "entropy_bits": 119.09
}
Query Parameter ReferenceParameterTypeDefaultDescriptionlengthinteger16Length of the password (min: 8, max: 128)use_uppercasebooleantrueInclude uppercase characters (A-Z)use_lowercasebooleantrueInclude lowercase characters (a-z)use_digitsbooleantrueInclude numeric digits (0-9)use_symbolsbooleantrueInclude special symbols3. POST Request with Custom Body PayloadFor advanced requirements (such as restricting special characters to specific allowed sets), use the POST endpoint.Request: Custom symbol set and 24-character lengthcurl -X 'POST' \
  'http://localhost:8000/api/v1/generate' \
  -H 'Content-Type: application/json' \
  -d '{
    "length": 24,
    "use_uppercase": true,
    "use_lowercase": true,
    "use_digits": true,
    "use_symbols": true,
    "custom_symbols": "!@#$"
  }'
Example Response:{
  "password": "m9!P@2#vX$7!mL4@qA9z#k1!",
  "length": 24,
  "entropy_bits": 145.07
}
💻 Web Integration ExampleFrontend developers can easily invoke the API directly within signup forms to offer a "Generate Password" feature.JavaScript (Fetch API)async function fetchSecurePassword() {
  try {
    const response = await fetch('http://localhost:8000/api/v1/generate?length=16');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    
    // Inject into input element
    const passwordInput = document.getElementById('signup-password');
    passwordInput.value = data.password;
    passwordInput.type = 'text'; // Briefly display the generated password
    
    console.log(`Password strength: ${data.entropy_bits} bits of entropy`);
  } catch (error) {
    console.error('Failed to generate password:', error);
  }
}
🧪 Error ResponsesThe API validates inputs and returns standard HTTP status codes:400 Bad Request: Occurs if all character types are disabled or if length is insufficient to contain required character guarantees.Example Error Payload:{
  "detail": "At least one character set (uppercase, lowercase, digits, symbols) must be enabled."
}
📄 LicenseThis project is open source and available under the MIT License.
