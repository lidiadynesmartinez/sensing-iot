import datetime
import io
import os
import secrets
import flask_bcrypt as bcrypt

from PIL import Image
from flask import Flask

from webapp.backend.data_analytics import save_figure, save_double_figure, save_fft_plot, save_tsr_plot, \
    calculate_correlation
from webapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, SearchForm, NewSearchForm, SearchActionForm
from flask import render_template, url_for, flash, redirect, request
from webapp.backend.data_storage import UserStorage
from webapp.backend.state_manager import StateManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c6767fse280ba245'

user_storage = UserStorage()
state_manager = StateManager()

MAPPING = {
    "London": "GB",
    "Madrid": "ES"
}



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if state_manager.is_authenticated():
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = user_storage.get_user_data(form.username.data)
        try:
            if user != {} and bcrypt.check_password_hash(user['password'], form.password.data):
                state_manager.authenticate_user(user['username'])
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        except ValueError:
            print("Wrong password/user")
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if state_manager.is_authenticated():
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if user_storage.insert_new_user(username=form.username.data,
                                        email=form.email.data,
                                        password=hashed_password):
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already in use- please use different details', 'danger')
    else:
        flash('Could not register, please check your information is correct', 'danger')
    return render_template('register.html', title='Register', form=form)


def perform_search(username, term, loc):
    geo = MAPPING[loc]
    state_manager.set_search({"geo": loc, "term": term})
    state_manager.execute_search(term, geo, loc)
    user_storage.add_search(username, term, loc)

    data = state_manager.get_current_search_data()

    weather_1y, trends_1y = data['1y']['weather'], data['1y']['trends']
    weather_5y, trends_5y = data['5y']['weather'], data['5y']['trends']

    # BELOW: RAW DATA GRAPHS
    size_1y = min(len(weather_1y), len(trends_1y))
    xs_1y = range(size_1y)

    size_5y = min(len(weather_5y), len(trends_5y))
    xs_5y = range(size_5y)

    ys_weather_1y = [w['temp'] for w in weather_1y][:size_1y]
    ys_trends_1y = [w['interest'] for w in trends_1y][:size_1y]
    ys_weather_5y = [w['temp'] for w in weather_5y][:size_5y]
    ys_trends_5y = [w['interest'] for w in trends_5y][:size_5y]

    save_double_figure(xs_1y, ys_weather_1y, ys_trends_1y, "raw_overlaid_1y",
                       x_label="Week", y_label1="Average Temperature (C)", y_label2=f"Interest in {term}",
                       title=f"Interest in {term} and average temperature in {loc} (1y)")

    save_double_figure(xs_5y, ys_weather_5y, ys_trends_5y, "raw_overlaid_5y",
                       x_label="Week", y_label1="Average Temperature (C)", y_label2=f"Interest in {term}",
                       title=f"Interest in {term} and average temperature in {loc} (5y)")

    save_fft_plot(ys_weather_5y, "weather_fft", title="Average Temperature Fourier Transform")
    save_fft_plot(ys_trends_5y, "trends_fft", title=f"Interest in {term} Fourier Transform")

    save_tsr_plot(ys_weather_5y, "weather_tsr", "Average Temperature TSR Breakdown")
    save_tsr_plot(ys_trends_5y, "trends_tsr", f"Interest in {term} TSR Breakdown")

    return calculate_correlation(ys_weather_5y, ys_trends_5y)

    # 1 year data: raw, trend, seasonal, residual
    # 5 years data: raw, trend, seasonal, residual
    # Correlation bar chart 1y5y
    # Noise
    # AR, MA, ARMA, ARIMA, VAR forecasting
    # FFT


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if not state_manager.is_authenticated():
        return redirect(url_for("login"))
    username = state_manager.get_user()
    user_searches = user_storage.get_searches(username)

    search_form = SearchForm()
    new_form = NewSearchForm()
    search_action_forms = [SearchActionForm(term, loc) for term, loc in reversed(user_searches)]

    corr = 0

    if state_manager.get_search() is None:
        if search_form.validate_on_submit():
            corr = perform_search(username, search_form.term.data, search_form.geo.data)
        else:
            for f in search_action_forms:
                if f.remove.data:
                    user_storage.remove_search(username, f.term, f.loc)
                    user_searches = user_storage.get_searches(username)
                    break
                if f.search.data:
                    corr = perform_search(username, f.term, f.loc)
                    break
    elif state_manager.get_search() is not None and new_form.is_submitted():
        state_manager.reset_search()

    return render_template('dashboard.html', title='Dashboard',
                           form=search_form, new_form=new_form, storage=user_storage, state=state_manager,
                           user_searches=user_searches,
                           enumerate=enumerate, reversed=reversed,
                           search_action_forms=search_action_forms, corr=corr)


@app.route("/account")
def account():
    if not state_manager.is_authenticated():
        return redirect(url_for("login"))
    form = UpdateAccountForm()
    user = user_storage.get_user_data(state_manager.get_user())
    if form.validate_on_submit():
        user_storage.update_user(form.username.data, email=form.email.data, password=None)

        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = user['username']
        form.email.data = user['email']
    return render_template('account.html', title='Account', form=form)


@app.route("/logout")
def logout():
    state_manager.deauthenticate_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


if __name__ == '__main__':
    app.run(debug=True)
