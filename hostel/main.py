from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection parameters
db_config = {
    "host": "127.0.0.1",
    "user": "your_username",
    "password": "your_password",
    "database": "hostel",
}

# Function to execute SQL queries
def execute_query(query, values=None, fetchall=False):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    
    if fetchall:
        result = cursor.fetchall()
    else:
        result = None

    connection.commit()
    cursor.close()
    connection.close()
    
    return result


# Route for a page displaying details of a specific user
@app.route('/user_details/<int:user_id>')
def user_details(user_id):
    # Example: Use a correlated subquery to get user details along with related information
    query = f"""
        SELECT
            userregistration.*,
            userlog.userEmail,
            userlog.city
        FROM
            userregistration
        LEFT JOIN
            userlog ON userregistration.id = userlog.userId
        WHERE
            userregistration.id = {user_id}
    """
    user_details = execute_query(query, fetchall=False)

    return render_template('user_details.html', user_details=user_details)

# Route for a page displaying details of a specific course
@app.route('/course_details/<int:course_id>')
def course_details(course_id):
    # Example: Use a nested query to get course details along with related information from registration
    query = f"""
        SELECT
            courses.*,
            registration.firstName,
            registration.lastName
        FROM
            courses
        LEFT JOIN
            registration ON courses.id = registration.course
        WHERE
            courses.id = {course_id}
    """
    course_details = execute_query(query, fetchall=False)

    return render_template('course_details.html', course_details=course_details)

@app.route('/update/<int:registration_id>', methods=['GET', 'POST'])
def update(registration_id):
    if request.method == 'POST':
        # Handle form submission
        # Example: Update data in the 'registration' table
        query = """
            UPDATE registration
            SET roomno=%s, seater=%s, feespm=%s, foodstatus=%s, stayfrom=%s, duration=%s,
                course=%s, regno=%s, firstName=%s, middleName=%s, lastName=%s, gender=%s,
                contactno=%s, emailid=%s, egycontactno=%s, guardianName=%s, guardianRelation=%s,
                guardianContactno=%s, corresAddress=%s, corresCIty=%s, corresState=%s, corresPincode=%s,
                pmntAddress=%s, pmntCity=%s, pmnatetState=%s, pmntPincode=%s, postingDate=%s, updationDate=%s
            WHERE id=%s
        """
        values = (
            request.form['roomno'], request.form['seater'], request.form['feespm'], request.form['foodstatus'],
            request.form['stayfrom'], request.form['duration'], request.form['course'], request.form['regno'],
            request.form['firstName'], request.form['middleName'], request.form['lastName'], request.form['gender'],
            request.form['contactno'], request.form['emailid'], request.form['egycontactno'], request.form['guardianName'],
            request.form['guardianRelation'], request.form['guardianContactno'], request.form['corresAddress'],
            request.form['corresCIty'], request.form['corresState'], request.form['corresPincode'], request.form['pmntAddress'],
            request.form['pmntCity'], request.form['pmnatetState'], request.form['pmntPincode'], request.form['postingDate'],
            request.form['updationDate'], registration_id
        )
        execute_query(query, values)

        return redirect(url_for('login'))

    # Fetch existing data for the registration_id
    query = "SELECT * FROM registration WHERE id=%s"
    registration = execute_query(query, (registration_id,), fetchall=False)

    return render_template('update.html', registration=registration)
