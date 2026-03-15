<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>

<h1>Coderr – Developer Platform Backend</h1>

<p>
<strong>Coderr</strong> is a backend system for a developer platform that connects
clients and developers. The backend is built using
<em>Django</em> and <em>Django REST Framework</em>.
</p>

<p>
The project provides the server-side logic for managing users, developer
profiles, offers, and orders. It ensures that all data handling,
authentication, and permissions work reliably together with a frontend
application.
</p>

<p>
Coderr focuses on providing a structured API that allows clients to browse
developer services while enabling developers to manage their profiles and
offers.
</p>

<hr>

<h2>🚀 Features</h2>
<ul>
<li>User registration and authentication</li>
<li>Developer profile management</li>
<li>Service and offer creation</li>
<li>Order management between clients and developers</li>
<li>Permission-based access control</li>
<li>RESTful API endpoints for frontend integration</li>
</ul>

<hr>

<h2>🛠 Tech Stack</h2>
<ul>
<li>Python 3</li>
<li>Django</li>
<li>Django REST Framework</li>
<li>Token Authentication</li>
<li>SQLite (development)</li>
</ul>

<hr>

<h2>📦 Installation</h2>

<h3>1. Clone the repository</h3>

<pre>
git clone https://github.com/alexschoefer/Coderr.git
cd Coderr
</pre>

<h3>2. Create and activate a virtual environment</h3>

<pre>
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
</pre>

<h3>3. Install dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<h3>4. Apply migrations</h3>

<pre>
python manage.py migrate
</pre>

<h3>5. Run the development server</h3>

<pre>
python manage.py runserver
</pre>

<hr>

<h2>🔐 Authentication</h2>

<p>
Coderr uses <strong>token-based authentication</strong> to secure API access.
After successful registration or login, the API returns an authentication token.
</p>

<p>Include the token in the request headers:</p>

<pre>
Authorization: Token your_token_here
</pre>

<hr>

<h2>📚 API Overview</h2>

<h3>Authentication</h3>

<table>
<tr>
<th>Method</th>
<th>Endpoint</th>
<th>Description</th>
</tr>

<tr>
<td>POST</td>
<td>/api/register/</td>
<td>Register a new user</td>
</tr>

<tr>
<td>POST</td>
<td>/api/login/</td>
<td>Login and receive authentication token</td>
</tr>

</table>

<h3>Developer Profiles</h3>

<table>

<tr>
<th>Method</th>
<th>Endpoint</th>
<th>Description</th>
</tr>

<tr>
<td>GET</td>
<td>/api/developers/</td>
<td>List available developer profiles</td>
</tr>

<tr>
<td>GET</td>
<td>/api/developers/&lt;id&gt;/</td>
<td>Retrieve developer profile details</td>
</tr>

<tr>
<td>PATCH</td>
<td>/api/developers/&lt;id&gt;/</td>
<td>Update developer profile</td>
</tr>

</table>

<h3>Offers</h3>

<table>

<tr>
<th>Method</th>
<th>Endpoint</th>
<th>Description</th>
</tr>

<tr>
<td>POST</td>
<td>/api/offers/</td>
<td>Create a new service offer</td>
</tr>

<tr>
<td>GET</td>
<td>/api/offers/</td>
<td>List available offers</td>
</tr>

<tr>
<td>GET</td>
<td>/api/offers/&lt;id&gt;/</td>
<td>Retrieve offer details</td>
</tr>

<tr>
<td>PATCH</td>
<td>/api/offers/&lt;id&gt;/</td>
<td>Update an offer</td>
</tr>

<tr>
<td>DELETE</td>
<td>/api/offers/&lt;id&gt;/</td>
<td>Delete an offer</td>
</tr>

</table>

<hr>

<h2>🔐 Permission Concept</h2>

<ul>
<li>Only authenticated users can access protected endpoints</li>
<li>Developers can only manage their own profiles and offers</li>
<li>Clients can browse developers and available offers</li>
<li>Only offer owners can update or delete their offers</li>
<li>Orders can only be accessed by the involved users</li>
</ul>

<hr>

<h2>📄 License</h2>

<p>
This project was created for educational purposes and as a demonstration
of backend development using Django REST Framework.
</p>

</body>
</html>