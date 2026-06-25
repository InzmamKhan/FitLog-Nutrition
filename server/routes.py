from flask import Blueprint, render_template, redirect, request, session, url_for
import core.db_queries as queries
import core.calculations as calc

server_bp = Blueprint('server', __name__)

@server_bp.route('/')
def index():
    """Application gatekeeper: redirects to onboarding or profile selection screens."""
    if not queries.get_all_users():
        return redirect(url_for('server.wizard'))
    return redirect(url_for('server.selection'))

@server_bp.route('/wizard', methods=['GET', 'POST'])
def wizard():
    """Handles biometric collection onboarding logs for new system users."""
    if request.method == 'POST':
        user_id = queries.create_user(
            name=request.form['name'],
            weight=float(request.form['weight']),
            height=float(request.form['height']),
            age=int(request.form['age']),
            gender=request.form['gender'],
            activity_level=request.form['activity_level'],
            objective=request.form['objective']
        )
        session['user_id'] = user_id
        return redirect(url_for('server.dashboard'))
        
    return render_template('wizard.html')

@server_bp.route('/selection', methods=['GET', 'POST'])
def selection():
    """Handles rendering profile lists or binding a selected user token to the current session."""
    if request.method == 'POST':
        session['user_id'] = int(request.form['user_id'])
        return redirect(url_for('server.dashboard'))
        
    profiles = queries.get_all_users()
    return render_template('selection.html', profiles=profiles)

@server_bp.route('/dashboard')
def dashboard():
    """Assembles all data parameters required to render the primary tracking display interface."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('server.index'))

    profile = queries.get_user_profile(user_id)
    if not profile:
        session.clear()
        return redirect(url_for('server.index'))

    todays_record = queries.sync_daily_record(user_id)

    targets = calc.compute_fitness_targets(profile)

    raw_logs = queries.get_raw_history_logs(user_id, day_limit=7)
    historical_summary = calc.format_historical_summary(raw_logs)

    return render_template(
        'dashboard.html',
        profile=profile,
        today=todays_record,
        targets=targets,
        history=historical_summary
    )

@server_bp.route('/log_nutrient', methods=['POST'])
def log_nutrient():
    """Intercepts and applies incremental logging entries sent from individual KPI card fields."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('server.index'))

    column_target = request.form.get('nutrient_column')
    input_value = request.form.get('amount', 0)

    try:
        amount = int(input_value)
        if amount > 0:
            queries.update_daily_nutrient(user_id, column_target, amount)
    except ValueError:
        pass 

    return redirect(url_for('server.dashboard'))

@server_bp.route('/logout')
def logout():
    """Clears operational session bounds, routing users back to initialization frameworks."""
    session.clear()
    return redirect(url_for('server.index'))