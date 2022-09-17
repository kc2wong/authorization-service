# AUTHORIZATION SERVICE

A simple application written in python for user permission management and authorization token generation.  Reset APIs are provided to create permission profile and user, and generate JWT based which payload contains user permission

This application is originally written in Java with RBD as backend storage


### HIghlights
- RestApi development with contract first approach - prepare the api spec and generate stub code using openapi generator
- Separate code generation from actual logic implementation
- Written in python and using NoSQL as storage to facilitate deployment as serverless application on cloud 
- Use liquibase to manage database change


### Prerequisites
- Python 3.9.x
- Java 11+
- MongoDB 5.x
    - Sign up a free mongodb cluster at https://www.mongodb.com/atlas/database
    - Create a user with ***Password*** as authentication method and ***Atlas admin*** as role
    - Create a new database ***authorization-db***


### Setup
1. Configuration update
    1. Open the file resources/dbchangelog/liquibase.properties in editor
    2. Fill the value for url, username, password
    3. The value of url is in format of mongodb+srv://[cluster-name]/authorization-db?authSource=admin, the cluster-name can be found in mongodb atlas admin page
    4. Open the file src/.env
    5. Fill the value for ***MONGODB_URI***, ***MONGODB_USER***, ***MONGODB_PASSWORD***

2. Initialize database
    1. Run the command `./gradlew update` (Mac) or `gradlew update` (Windows)

3. Generate source from api-spec
    1. Run the command `./gradlew clean openApiGenerate`
    2. Run the command `pip install -r src/requirements.txt -r src/openapi_server/requirements.txt` to install required modules


### Startup
- `cd src`
- `python -m openapi_server`


### Testing
- Swagger UI
Open the URL http://localhost:8080/authorization-serv/ui/ in browser
- Unprotected API - The GET apis do not require any authorization check
    - eg `curl "http://localhost:8080/authorization-serv/end-points"`
- Protected API - The PUT and POST apis are protected.  It is required to pass a bearer token as `Authorization` header 
    1. `curl --location --request POST 'localhost:8080/authorization-serv/access-tokens/admin'` to generate an access token
    2. When calling POST /authorization-serv/profiles to create a profile, includes the token returned from above api in Authorization header

 
### Tweaks on code generation template
1. requirements.mustache
    - Flask >= 1.1.2 , in order to use Flask 2.0 in src/openapi_server/requirements.txt
2. controller.mustache
    - Implement api delegate pattern.  Instead of returning the default result ***do some magic!***, it looks for the class ***[controller]_impl*** in module openapi_server.controllers and call the same method