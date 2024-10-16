from flask import Flask, request
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Welcome to My Flask app</title>
<style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                text-align: center;
                background-color: #fff;
                padding: 40px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 10px;
                color: #3498db;
            }
            p {
                font-size: 1.2em;
                margin-bottom: 20px;
            }
            a {
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            a:hover {
                background-color: #2980b9;
            }
</style>
</head>
<body>
<div class="container">
<h1>Welcome to My Flask app2</h1>
<p>This is a simple Flask web app2lication with beautiful HTML content!</p>
<a href="https://flask.palletsprojects.com/">Learn more about Flask</a>
</div>
</body>
</html>
    '''
@app.route('/describe')
def get_description():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Flask API Description</title>
<style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f8ff;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                max-width: 800px;
                background-color: #fff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #4CAF50;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            p {
                font-size: 1.2em;
                color: #555;
                margin-bottom: 20px;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background-color: #3498db;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
            }
            a {
                color: white;
                text-decoration: none;
                font-weight: bold;
                transition: color 0.3s ease;
            }
            a:hover {
                color: #ffeb3b;
            }
            code {
                background-color: #f4f4f4;
                padding: 4px 6px;
                border-radius: 4px;
                font-size: 1.1em;
            }
</style>
</head>
<body>
<div class="container">
<h1>Flask API</h1>
<p>
                This app2 supports the endpoint listed below. You can change the data being sent to the API by updating the URI.
</p>
<p>The four request methods we will use are <strong>GET, POST, PUT,</strong> and <strong>DELETE</strong>. GET requests can be used in a browser. The other methods can be used via CURL or another API platform, such as Postman or Thunder Client in VS Code.</p>
<ul>
<li><a href='
http://127.0.0.1:5000/describe'>GET
This Page</a></li>
<li><a href='
http://127.0.0.1:5000/username/1'>GET
a username from ID</a></li>
<li><a href='
http://127.0.0.1:5000/users/'>GET
all user info</a></li>
</ul>
<p>The endpoints below can be accessed over CURL using the correct request method:</p>
<ul>
<li><code>curl -X POST '
http://127.0.0.1:5000/new_user/Georgina/'</code>
# POST a new user</li>
<li><code>curl -X PUT '
http://127.0.0.1:5000/update_username/1/Hazel/'</code>
# PUT updates</li>
<li><code>curl -X DELETE '
http://127.0.0.1:5000/delete_user/1/'</code>
# DELETE a user by ID</li>
</ul>
</div>
</body>
</html>
    """

# In-memory contact storage with IDs
contact_list = {
    1: {"name": "Alice", "phone": 111},
    2: {"name": "Rachel", "phone": 222},
    3: {"name": "Joe", "phone": 333},
}

@app.route("/contacts/", methods=['GET'])
def get_contacts():
    """Get all contacts."""
    return contact_list

@app.route("/contacts/<int:id>/", methods=['GET'])
def get_contact(id):
    """Get a specific contact by ID."""
    if id in contact_list:
        return {id: contact_list[id]}
    else:
        return {"error": "Contact not found."}, 404

@app.route("/contacts/<string:name>/<int:phone>/", methods=['POST'])
def create_contact(name, phone):
    """Create a new contact."""
    name = name.capitalize()

    # Check if phone number already exists
    if any(contact['phone'] == phone for contact in contact_list.values()):
        return {"error": "Contact with this phone number already exists."}, 400

    # Generate a new ID for the contact
    new_id = max(contact_list.keys()) + 1 if contact_list else 1
    contact_list[new_id] = {"name": name, "phone": phone}

    return {"message": "Contact added successfully.", "contact": {new_id: contact_list[new_id]}}, 201

@app.route("/contacts/<int:id>/<string:new_name>/<int:new_phone>/", methods=['PUT'])
def update_contact(id, new_name, new_phone):
    """Update an existing contact."""
    if id not in contact_list:
        return {"error": "Contact not found."}, 404

    # Check for existing phone number
    if any(contact['phone'] == new_phone for contact in contact_list.values() if contact['phone'] != contact_list[id]['phone']):
        return {"error": "Phone number already exists. Update canceled."}, 400

    # Update the contact
    contact_list[id]["name"] = new_name.capitalize()
    contact_list[id]["phone"] = new_phone

    return {"message": "Contact updated successfully.", "contact": {id: contact_list[id]}}

@app.route("/contacts/<int:id>/", methods=['DELETE'])
def delete_contact(id):
    """Delete a contact."""
    if id in contact_list:
        deleted_contact = contact_list.pop(id)
        return {"message": "Contact deleted successfully.", "contact": {id: deleted_contact}}
    else:
        return {"error": "Contact not found."}, 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
