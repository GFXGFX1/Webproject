from flask import render_template, redirect, url_for, flash, request, jsonify

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Здесь стоит использовать хеширование паролей в реальном проекте
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    news = News.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', news=news)

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(news)
        db.session.commit()
        flash('News created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_news.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/api/news', methods=['GET'])
def api_news():
    news = News.query.all()
    output = [{'id': n.id, 'title': n.title, 'content': n.content} for n in news]
    return jsonify(output)

@app.route('/api/news/<int:news_id>', methods=['GET'])
def api_single_news(news_id):
    news = News.query.get_or_404(news_id)
    output = {'id': news.id, 'title': news.title, 'content': news.content}
    return jsonify(output)
