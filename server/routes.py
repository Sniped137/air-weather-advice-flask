from flask import Flask, render_template, request, session, redirect, url_for, jsonify,  make_response
from database import client, get_post_contents_by_id, get_post_comments_by_id, generate_post_id, store_post_in_database, login_user, register_user
from datetime import timedelta
import random, time

app = Flask(__name__, template_folder='../templates',static_folder='../static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(days=7) 

@app.route('/')
@app.route('/weather')
def weather():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# @app.route('/advice')
def advice_overview():
    non_duplicate_posts = []
    load_posts_quantity = 19
    load_elements_quantity = 7
    response = dict(client.table('posts').select('*').execute())['data']
    advice_posts = list(response)
    number_of_posts = len((advice_posts))
    for i in range(number_of_posts):
        choice = random.choice(advice_posts)
        advice_posts.remove(choice)
        non_duplicate_posts.append(choice)
        # for i 
    
#     return render_template('advice_overview.html')

# posts = [{'title': 'title1', 'content': 'Content1'},
#          {'title': 'title2', 'content': 'Content2'},
#          {'title': 'title3', 'content': 'Content3'},
#          {'title': 'title4', 'content': 'Content4'},
#          {'title': 'title5', 'content': 'Content5'},
#          {'title': 'title6', 'content': 'Content6'},  
#          {'title': 'title7', 'content': 'Content7'},            
#          {'title': 'title8', 'content': 'Content8'},
#          {'title': 'title9', 'content': 'Content9'}]

# for post in advice_posts:
#     list_of_lists.append([dict1['post_id'], dict1['content']])
non_duplicate_posts = []
response = dict(client.table('posts').select('*').execute())['data']
advice_posts = list(response)
posts = []
while len(advice_posts) > 0:
    choice = random.choice(advice_posts)
    non_duplicate_posts.append(choice)
    advice_posts.remove(choice)


for post in non_duplicate_posts:
    title = post['title']
    content = post['content']
    posts.append([title, content]) 

quantity = 9

@app.route('/test')
def test():
    return render_template('advice_individual.html')

@app.route('/advice')
def advice_overview():
    return render_template('advice_overview.html')

@app.route("/load")
def load():
    time.sleep(0.2)

    if not request.args:
        return make_response(jsonify({'error': 'No query string parameters provided'}), 400)

    counter = int(request.args.get("c", 0))

    if counter >= len(posts):
        print("No more posts")
        return make_response(jsonify({}), 200)

    print(f"Returning posts {counter} to {counter + quantity}")
    res = make_response(jsonify(posts[counter: counter + quantity]), 200)

    return res


@app.route('/advice/post/<string:post_id>', methods=['GET'])
def view_advice_post(post_id):
    post, post_comments = get_post_contents_by_id(post_id), get_post_comments_by_id(post_id)
    return render_template('view_advice_post.html', post=post, post_comments=post_comments)

@app.route('/advice/create')
def create_advice_post():
    if request.method == 'POST':
        post_id = generate_post_id()
        post_data = {
        'post_id' : post_id,
        'title': request.form['title'],
        'description': request.form['description'],
        'upvotes' : 0,
        'content': request.form['content'],
        'author_name': session['username'],
        'author_user_id': session['user_id']
        }
        outputmessage = store_post_in_database(post_id, post_data)
        if outputmessage[1]: 
            return redirect(url_for('advice'))
        else:
            return render_template('create_article.html', outputmessage[0])
    return render_template('create_article.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    response = {}
    if session.get('loggedin'):
        return redirect(url_for('weather'))
    if request.method == 'POST':
        email, username, password, checkbox = request.form['email'], request.form['username'], request.form['password'], request.form.get("checkbox", "off")
        response = register_user(email, username, password, checkbox)
        if response['success']:
            return redirect(url_for('login'))
    return render_template('register.html', response=response)

@app.route('/login', methods=['GET', 'POST'])
def login():
    response = {}
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        checkbox = request.form.get("checkbox", "off")
        response = login_user(email, password)
        if response['success']:
            if checkbox == 'on':
                session.permanent = True
            else:
                session.permanent = False
            session['loggedin'] = True
            session['user_id'] = response['user_id']
            session['username'] = response['username']
            return redirect(url_for('weather'))
    return render_template('login.html', response=response)

@app.route('/reset-password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('_permanent', None)
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/terms-conditions', methods=['GET', 'POST'])
def termsandconditions():
    return render_template('termsandconditions.html')

if __name__ == '__main__':
    app.run(debug=True)

