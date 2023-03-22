from flask import redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import configparser
import uuid
import supabase
import re


config = configparser.ConfigParser()
config.read('config.ini')

supabase_url = config.get('Supabase', 'url')
supabase_key = config.get('Supabase', 'key')
client = supabase.create_client(supabase_url, supabase_key)

def is_valid_email(email):
    response = client.table('user_details').select("email").eq('email', email).execute()
    try:
        response.data[0]['email']
        return "Email address already exists"
    except:
        if len(email) == 0:
            return 'Email address field cannot be empty'
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return 'Email address is not valid'
        return None

def is_valid_username(username):
    response = client.table('user_details').select("username").eq('username', username).execute()
    try:
        response.data[0]['username']
        return "Username already exists"
    except:
        if len(username) == 0:
            return 'Username field cannot be empty'
        if not re.match('^[a-zA-Z0-9]+$', username):
            return 'Username must contain only letters and numbers'
        if len(username) < 4:
            return 'Username must be at least 4 characters long'
        return None

def is_valid_password(password):
    if len(password) == 0:
        return 'Password field cannot be empty'
    if not re.match('^(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$', password):
        return 'Password requirements below not met'
    return None

def is_checkbox_checked(checkbox):
    if checkbox == 'off':
        return 'You have to accept T&Cs to proceed'
    
def register_user(email, username, password, checkbox):
    email_error = is_valid_email(email)
    username_error = is_valid_username(username)
    password_error = is_valid_password(password)
    checkbox_error = is_checkbox_checked(checkbox)
    if email_error or username_error or password_error or checkbox:
        return {f'success': False, 'email_error': email_error, 'username_error' : username_error, 'password_error' : password_error, 'checkbox_error' : checkbox_error}
    res = client.auth.sign_up({"email": email,"password": password})
    user_id = res.user.id
    print(user_id)
    client.table('user_details').insert({'user_id' : user_id, 'email' : email, 'username' : username}).execute()
    return {'success': True}
    
def login_user(email, password):
    try:
        data = client.auth.sign_in_with_password({"email": email, "password": password})
        user_id = data.user.id
        response = client.table('user_details').select("username").eq('user_id', user_id).execute()
        username = response.data[0]['username']
        response = ({'success' : True, 'user_id': user_id, 'username' : username})
        return response
    except Exception as error:
        error = str(error)
        if error == 'Email not confirmed':
            response = ({'success' : False, 'email_error': 'Email not verified'})
            return response
        if error == 'Invalid login credentials' or 'You must provide either an email or phone number and a password':
            response = ({'success' : False, 'password_error': 'Invalid email or password'})
            return response


def get_post_contents_by_id(post_id):
    post = client.table('posts').select('*').eq('post_id', post_id).execute().get('data', [])
    return post

def get_post_comments_by_id(post_id):
    post_comments = client.table('comments').select('*').eq('post_id', post_id).execute().get('data', [])
    return post_comments

def generate_post_id():
    unique = False
    try:
        query = client.table('posts').select('post_id').execute()
        print(query)
        post_id_list = query.data
        while not unique:
            duplicate_found = False
            post_id = str(uuid.uuid4())[:8]
            for row in post_id_list:
                if row['post_id'] == post_id:
                    duplicate_found = True
                    print(duplicate_found)
            if not duplicate_found:
                unique = True
        return post_id
    except Exception as e:
        outputmessage = (f"Error generating the post id. Error: {e}", False)
        return outputmessage

def store_post_in_database(post_id, post_data):
    try:
        client.table('posts').insert({'post_id' : post_id}, post_data).execute()
        outputmessage = (f"Post Submitted with ID {post_id} successfully stored in database.", True)
        return outputmessage
    except Exception as e:
        outputmessage = (f"Error storing post with ID {post_id} in database: {str(e)}", False)
        return outputmessage
