from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    flash,
    make_response
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, Category, Item, LatestItem, User

from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

# Connect to the database
engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# For login functionality
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Item App"


@app.route('/')
@app.route('/main')
def mainPage():
    """This method shows the main page and lists the categories and items.

    RETURNS the main page if there's a logged-in user
            the public main page if there's no logged-in user
    """
    categories = session.query(Category).all()
    latest_items = session.query(LatestItem).order_by(
        LatestItem.id.desc()).limit(8)

    if 'username' not in login_session:
        # Login session state token
        state = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for x in range(32))
        login_session['state'] = state
        print login_session['state']
        return render_template('publicpage.html', p_categories=categories,
                               p_latest_items=latest_items, p_main_page=True,
                               p_session=login_session, STATE=state)
    else:
        return render_template('page.html', p_categories=categories,
                               p_latest_items=latest_items, p_main_page=True,
                               p_session=login_session)


# Log into the application
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """This method handles the log in procedure. The response from Google
    sign in is sent to this method as a request. All the validation is done
    here.

    RETURNS the output response or the error.
    """

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain the authorization code
    code = request.data

    try:
        # Convert the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, return
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the right user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the login session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Store the session data into login_session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if the current user has been recorded in database already
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome!</h1>'
    return output


# Log out from the application - Revoke a current user's token and
# reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    """This method disconnects the user from the session and deletes
    all the session information

    RETURNS the successful log out page or the error
    """
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For some reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    """This method creates a user and stores it in the database. """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """This method returns the information of the requested user."""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """This method returns the user id from the email."""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/catalog/<string:category_name>')
def showCategory(category_name):
    """This method displays the items of a category.

    RETURNS the editable page of the category if there's a logged-in user
            the public page of the category if there's no logged-in user
    """

    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    no_items = len(items)
    if 'username' not in login_session:
        return render_template('publicpage.html', p_categories=categories,
                               p_category=category, p_items=items,
                               p_no_items=no_items, p_main_page=False,
                               p_session=login_session)
    else:
        return render_template('page.html', p_categories=categories,
                               p_category=category, p_items=items,
                               p_no_items=no_items, p_main_page=False,
                               p_session=login_session)


@app.route('/catalog/<string:category_name>/<string:item_name>')
def showCategoryItem(category_name, item_name):
    """This method displays the description of an item.

    RETURNS the public description page if there's no logged user
            the editable description page if there's a logged user
    """

    item = session.query(Item).filter_by(name=item_name).one()
    if 'username' not in login_session:
        return render_template('publicshowItemDescription.html',
                               p_item_name=item_name,
                               p_description=item.description,
                               p_session=login_session)
    else:
        return render_template('showItemDescription.html',
                               p_item_name=item_name,
                               p_description=item.description,
                               p_session=login_session)


@app.route('/add', methods=['GET', 'POST'])
def addItem():
    """This method adds an item to the database.

    RETURNS on POST the add page
            on GET the main page
    """

    if 'username' in login_session:
        categories = session.query(Category).all()
        # If the request is POST, add the item into the db
        if request.method == 'POST':
            new_category = session.query(Category).filter_by(
                name=request.form['new_category']).one()
            newItem = Item(name=request.form['new_name'],
                           description=request.form['new_description'],
                           category_id=new_category.id,
                           user_id=login_session['user_id'])
            session.add(newItem)
            newLatestItem = LatestItem(item_name=request.form['new_name'],
                                       category_name=new_category.name)
            session.add(newLatestItem)
            session.commit()
            return redirect(url_for('mainPage'))
        else:
            return render_template('addItem.html', p_categories=categories,
                                   p_session=login_session)
    else:
        return redirect(url_for('mainPage'))


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    """This method edits an item of a cateogory.

    RETURNS on POST the edit item page
            on GET the main page
    """

    if 'username' in login_session:
        editedItem = session.query(Item).filter_by(name=item_name).one()

        # If the login user is authorized to edit, do it
        if login_session['user_id'] == editedItem.user_id:
            category = session.query(Category).filter_by(
                id=editedItem.category_id).one()
            categories = session.query(Category).all()
            if request.method == 'POST':
                if request.form['title']:
                    editedItem.name = request.form['title']
                if request.form['description']:
                    editedItem.description = request.form['description']
                if request.form['category']:
                    category = session.query(Category).filter_by(
                        name=(request.form['category'])).one()
                    editedItem.category_id = category.id
                session.add(editedItem)
                session.commit()
                return redirect(url_for('showCategory',
                                category_name=category.name))
            else:
                return render_template('editItem.html', p_item=editedItem,
                                       p_categories=categories,
                                       p_session=login_session)
        else:
            flash('You\'re not authorized to edit this item. You can ' +
                  'only edit the items you created. Back to the main page.')
            return redirect(url_for('mainPage'))
    else:
        return redirect(url_for('mainPage'))


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    """This method deletes an item from a database.

    RETURNS on POST the delete item page
            on GET the main page
    """

    if 'username' in login_session:
        itemToDelete = session.query(Item).filter_by(name=item_name).one()

        # If the login user is authorized to delete, do it
        if login_session['user_id'] == itemToDelete.user_id:
            isDeleteNecessary = True  # if latestItemDelete needs to be deleted
            try:
                latestItemToDelete = session.query(LatestItem).filter_by(
                    item_name=item_name).one()
            except:
                isDeleteNecessary = False  # no latestItemToDelete in database
            category = session.query(Category).filter_by(
                id=itemToDelete.category_id).one()
            if request.method == 'POST':
                session.delete(itemToDelete)
                if isDeleteNecessary:
                    session.delete(latestItemToDelete)
                session.commit()
                return redirect(url_for('showCategory',
                                category_name=category.name))
            else:
                return render_template('deleteItem.html', p_item=itemToDelete,
                                       p_session=login_session)
        else:
            flash('You\'re not authorized to delete this item. You can ' +
                  'only delete the items you created. Back to the main page.')
            return redirect(url_for('mainPage'))
    else:
        return redirect(url_for('mainPage'))


# Show the catalog info in JSON format
@app.route('/catalog.json')
def catalogJSON1():
    """This method displays the catalog information in JSON format.

    RETURNS the JSON formatted output
    """

    categories = session.query(Category).all()
    items = session.query(Item).all()
    output_list = []
    categories = [c.serialize for c in categories]
    items = [i.serialize for i in items]
    for c in categories:
        for i in items:
            if i["category_id"] == c["id"]:
                output_list.append({'id': c["id"],
                                   'name': c["name"], 'Item': i})
    return jsonify(output_list)


# Show the catalog item info in JSON format
@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def showCategoryItemJSON(category_name, item_name):
    """This method displays the catalog item information in JSON format.

    RETURNS the JSON formatted output
    """

    item = session.query(Item).filter_by(name=item_name).one()
    return jsonify(Item=item.serialize)

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
