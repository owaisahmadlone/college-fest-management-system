"""imports"""
import hashlib

from flask import Flask, render_template, redirect, request, url_for, session, abort

import psycopg2


key = 23


def sha256_hash(input_string):
    """Hash the input string using SHA-256 algorithm and return the first 19 characters of the hash value."""
    sha256_hash_object = hashlib.sha256()
    sha256_hash_object.update(input_string.encode())
    return sha256_hash_object.hexdigest()[0:19]


def rsa_hash_encrypt(message, key):
    """Encrypt the message using RSA algorithm"""
    # Hash the message using SHA-256
    hashed_message = hashlib.sha256(message.encode()).hexdigest()

    # Convert the hash value to an integer
    hashed_int = int(hashed_message, 16)

    # Perform modular exponentiation
    encrypted_value = pow(hashed_int, key, 1024)

    return encrypted_value


# conn = psycopg2.connect(
#     dbname="21CS30032", user="21CS30032", password="21CS30032", host="10.5.18.70"
# )

conn = psycopg2.connect(
    dbname="21CS10014",
    user="21CS10014",
    password="21CS10014",
    host="10.5.18.68"
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page"""

    cursor = conn.cursor()

    try:
        cursor.execute(
            "select event_id,event_name,event_venue,event_description,event_date,event_time,event_type from event order by random() limit 3;"
        )
        events = cursor.fetchall()

    except psycopg2.Error as e:
        print(e)
        events = []
        conn.rollback()

    return render_template("home.html", events=events)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    flag = 0

    # flags to know if the user is a student or an organiser or a participant
    organise = 1
    student = 1

    if request.method == "POST":
        cursor = conn.cursor()
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute(
            f"SELECT * from admin where username = '{username}' and pass = '{password}'"
        )
        admin = cursor.fetchone()

        if admin is not None:
            print(admin)
            session["admin"] = sha256_hash(str(rsa_hash_encrypt(username, key)))
            return redirect(url_for("admin", url_encrypt=session["admin"]))

        username = username[6:]

        try:
            username = int(username)
        except(ValueError, TypeError):
            flag = 1
            return render_template("login.html", flag=flag)

        password = request.form["password"]

        fest_id = 0

        if username > 1000:
            organise = 0
            student = 0
            try:
                cursor.execute(
                    f"SELECT fest_id from ext_participant where fest_id = '{username}' and pass = '{password}'"
                )
                fest_id = cursor.fetchone()
            except psycopg2.Error as e:
                print(e)
                fest_id = 0
                conn.rollback()
        else:
            try:
                cursor.execute(
                    f"SELECT fest_id from student where fest_id = '{username}' and pass = '{password}'"
                )
                fest_id = cursor.fetchone()
            except psycopg2.Error as e:
                print(e)
                fest_id = 0
                conn.rollback()

            try:
                cursor.execute(
                    f"SELECT fest_id from organising where fest_id = '{username}'"
                )
                fest_id_organise = cursor.fetchone()
            except psycopg2.Error as e:
                print(e)
                fest_id_organise = None
                conn.rollback()

            if fest_id_organise is not None:
                organise = 1
            else:
                organise = 0

        cursor.close()
        if fest_id is not None:
            fest_id = fest_id[0]
            session["url_encrypt_global"] = sha256_hash(
                str(rsa_hash_encrypt(str(fest_id), key))
            )
            session["organise"] = organise
            session["student"] = student
            return redirect(
                url_for(
                    "index",
                    fest_id=fest_id,
                    organise=organise,
                    student=student,
                    x=0,
                    url_encrypt=session["url_encrypt_global"],
                )
            )
        else:
            flag = 1
            return render_template("login.html", flag=flag)

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout page"""
    if session.get("admin") is not None:
        session["admin"] = None
    if session.get("url_encrypt_global") is not None:
        session["url_encrypt_global"] = None
    if session.get("organise") is not None:
        session["organise"] = None
    if session.get("student") is not None:
        session["student"] = None

    return redirect(url_for("home"))


@app.route("/admin/<url_encrypt>")
def admin(url_encrypt):
    """Admin page"""

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT event_id,event_name, event_venue, event_date, event_time from event"
        )
        events = cursor.fetchall()
        organisers = []
        events2 = []
        for event in events:
            event_id = event[0]
            cursor.execute(
                f"SELECT roll from organising NATURAL JOIN student where event_id = {event_id}"
            )
            organisers = cursor.fetchall()

            events2.append((event, organisers))

    except psycopg2.Error as e:
        print(e)
        events2 = []
        conn.rollback()
    if url_encrypt == session["admin"]:
        return render_template("admin.html", events=events2, url_encrypt=url_encrypt)
    else:
        return render_template("error.html")


@app.route("/add_event/<url_encrypt>", methods=["GET", "POST"])
def add_event(url_encrypt):
    """Add event page"""
    cursor = conn.cursor()
    if request.method == "POST":
        event_name = request.form["event_name"]
        event_venue = request.form["event_venue"]
        event_date = request.form["event_date"]
        event_time = request.form["event_time"]
        event_type = request.form["event_type"]
        event_description = request.form["event_description"]
        cursor.execute("SELECT event_id from event order by event_id desc limit 1")
        event_id = cursor.fetchone()
        event_id = event_id[0] + 1
        try:
            cursor.execute(
                f"INSERT into event (event_id,event_name, event_venue, event_date, event_time, event_type, event_description) VALUES ('{event_id}','{event_name}','{event_venue}','{event_date}','{event_time}','{event_type}','{event_description}')"
            )
            conn.commit()
        except psycopg2.Error as e:
            print(e)
            conn.rollback()
    else:
        if url_encrypt == session["admin"]:
            return render_template("add_event.html", url_encrypt=url_encrypt)
        return render_template("error.html")
    if url_encrypt == session["admin"]:
        return redirect(url_for("admin", url_encrypt=url_encrypt))
    return render_template("error.html")


@app.route("/remove_participant/<url_encrypt>")
def remove_participant(url_encrypt):
    """Remove participant page"""

    cursor = conn.cursor()

    cursor.execute("SELECT fest_id, name from ext_participant")
    participants = cursor.fetchall()
    cursor.close()
    if url_encrypt == session["admin"]:
        return render_template(
            "remove_participant.html",
            participants=participants,
            url_encrypt=url_encrypt,
        )
    else:
        return render_template("error.html")


@app.route("/remove_participant2/<int:fest_id>/<url_encrypt>", methods=["GET", "POST"])
def remove_participant2(fest_id, url_encrypt):
    """Remove participant page"""
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT acc_id from ext_participant where fest_id = {fest_id}")
        acc_id = cursor.fetchone()
        cursor.execute(
            f"UPDATE accomodation SET capacity = capacity + 1 WHERE acc_id = {acc_id[0]}"
        )
        cursor.execute(f"DELETE from ext_participant where fest_id = {fest_id}")
        conn.commit()
    except psycopg2.Error as e:
        print(e)
        conn.rollback()
    if url_encrypt == session["admin"]:
        return redirect(url_for("remove_participant", url_encrypt=url_encrypt))
    else:
        return render_template("error.html")


@app.route("/add_organiser/<int:event_id>/<url_encrypt>", methods=["GET", "POST"])
def add_organiser(event_id, url_encrypt):
    """Add organiser page"""
    cursor = conn.cursor()
    flag = 0

    if request.method == "POST":
        roll = request.form["roll"]
        cursor.execute(f"SELECT fest_id from student where roll = '{roll}'")
        fest_id = cursor.fetchone()
        cursor.execute(
            f"SELECT * from participating_int where fest_id = {fest_id[0]} and event_id = {event_id}"
        )
        fest_id2 = cursor.fetchone()
        if fest_id2 is not None:
            flag = 1
            return render_template(
                "add_organiser.html",
                event_id=event_id,
                url_encrypt=url_encrypt,
                flag=flag,
            )
        else:
            try:
                cursor.execute(
                    f"INSERT into organising VALUES ({fest_id[0]},{event_id})"
                )
                conn.commit()
            except psycopg2.Error as e:
                print(e)
                conn.rollback()
    else:
        if url_encrypt == session["admin"]:
            return render_template(
                "add_organiser.html", event_id=event_id, url_encrypt=url_encrypt
            )
        else:
            return render_template("error.html")
    if url_encrypt == session["admin"]:
        return redirect(url_for("admin", url_encrypt=url_encrypt))
    else:
        return render_template("error.html")


@app.route("/remove_organiser/<int:event_id>/<url_encrypt>", methods=["GET", "POST"])
def remove_organiser(event_id, url_encrypt):
    """Remove organiser page"""
    cursor = conn.cursor()
    if request.method == "POST":
        roll = request.form["roll"]
        cursor.execute(f"SELECT fest_id from student where roll = '{roll}'")
        fest_id = cursor.fetchone()
        try:
            cursor.execute(
                f"DELETE from organising where fest_id = {fest_id[0]} and event_id = {event_id}"
            )
            conn.commit()
        except psycopg2.Error as e:
            print(e)
            conn.rollback()
    else:
        if url_encrypt == session["admin"]:
            return render_template(
                "remove_organiser.html", event_id=event_id, url_encrypt=url_encrypt
            )
        else:
            return render_template("error.html")
    if url_encrypt == session["admin"]:
        return redirect(url_for("admin", url_encrypt=url_encrypt))
    else:
        return render_template("error.html")


@app.route(
    "/index/<int:fest_id>/<int:organise>/<int:student>/<int:x>/<url_encrypt>",
    methods=["GET", "POST"],
)
def index(fest_id, organise, student, x, url_encrypt):
    """INDEX page"""

    cursor = conn.cursor()

    details = []
    participating_event = []
    non_participating_event = []
    volunteering_event = []
    non_volunteering_event = []
    other_events = []
    events_won = []
    participating_event_2 = []
    events_organised = []
    event_org_details = {}
    volunteering_event_2 = []
    
    # url_encrypt = sha256_hash(str(rsa_hash_encrypt(str(fest_id),key)))

    if student != session["student"] or organise != session["organise"]:
        return render_template("error.html")
    if fest_id > 1000:
        # show details of user
        try:
            cursor.execute(
                f"SELECT fest_id, ext_participant.name, college, accomodation.name from ext_participant, accomodation where fest_id = {fest_id} and accomodation.acc_id = ext_participant.acc_id"
            )
            details = cursor.fetchone()

        except psycopg2.Error as e:
            print(e)
            details = []
            conn.rollback()

        try:
            cursor.execute(
                f"SELECT event_id,event_name,event_date,event_time,event_venue,event_winner from event NATURAL JOIN participating_ext where fest_id = {fest_id}"
            )
            participating_event = cursor.fetchall()
            for event in participating_event:
                event_id = event[0]
                cursor.execute(
                    f"SELECT roll, name from organising NATURAL JOIN student where event_id = {event_id}"
                )
                participating_event_2.append((event, cursor.fetchall()))

        except psycopg2.Error as e:
            print(e)
            participating_event = []
            conn.rollback()

        try:
            cursor.execute(
                f"SELECT event_id,event_name,event_date,event_time,event_venue from event where event_id not in (select event_id from participating_ext where fest_id = {fest_id})"
            )
            non_participating_event = cursor.fetchall()

        except psycopg2.Error as e:
            print(e)
            non_participating_event = []
            conn.rollback()
            
        # get the events won by the participant
        try:
            cursor.execute(
                f"SELECT event_id,event_name,event_date,event_time,event_venue from event where event_id in (select event_id from participating_ext where fest_id = {fest_id} and event_winner = {fest_id})"
            )
            events_won = cursor.fetchall()

        except psycopg2.Error as e:
            print(e)
            events_won = []
            conn.rollback()

    else:
        # events won by the student
        try:
            cursor.execute(f"SELECT event_id,event_name,event_date,event_time,event_venue from event where event_id in (select event_id from participating_int where fest_id = {fest_id} and event_winner = {fest_id})")
            events_won = cursor.fetchall()
            
        except psycopg2.Error as e:
            print(e)
            events_won = []
            conn.rollback()
        
        # show details of user
        try:
            cursor.execute(
                f"SELECT fest_id, name, roll, dept from student where fest_id = {fest_id}"
            )
            details = cursor.fetchone()

        except psycopg2.Error as e:
            print(e)
            details = []
            conn.rollback()

        try:
            cursor.execute(
                f"SELECT event_id,event_name,event_date,event_time,event_venue,event_winner from event NATURAL JOIN participating_int where fest_id = {fest_id}"
            )
            participating_event = cursor.fetchall()
            for event in participating_event:
                event_id = event[0]
                cursor.execute(
                    f"SELECT roll, name from organising NATURAL JOIN student where event_id = {event_id}"
                )
                participating_event_2.append((event, cursor.fetchall()))
            print(participating_event_2)
        except psycopg2.Error as e:
            print(e)
            participating_event = []
            conn.rollback()

        try:
            cursor.execute(
                f"SELECT event_id,event_name,event_date,event_time,event_venue,event_winner from event where event_id in (select event_id from volunteering where fest_id = {fest_id})"
            )
            volunteering_event = cursor.fetchall()
            for event in volunteering_event:
                event_id = event[0]
                cursor.execute(
                    f"SELECT roll, name from organising NATURAL JOIN student where event_id = {event_id}"
                )
                volunteering_event_2.append((event, cursor.fetchall()))

        except psycopg2.Error as e:
            print(e)
            volunteering_event = []
            conn.rollback()

        # merge the tables of participating, volunteering and organising events and return all the events not in these tables such that the student can participate in them
        try:
            cursor.execute(
                f"SELECT event_id,event_name,event_date,event_time,event_venue from event where event_id not in (select event_id from participating_int where fest_id = {fest_id}) and event_id not in (select event_id from volunteering where fest_id = {fest_id}) and event_id not in (select event_id from organising where fest_id = {fest_id})"
            )
            other_events = cursor.fetchall()

        except psycopg2.Error as e:
            print(e)
            other_events = []
            conn.rollback()

        # Organising events

        if organise == 1:
            try:
                # list of events organised
                cursor.execute(
                    f"SELECT * FROM event WHERE event_id in (select event_id from organising where fest_id = {fest_id})"
                )
                events_organised = cursor.fetchall()

                for event in events_organised:
                    event_id = event[0]
                    
                    temp = dict()
                    
                    # participants of event_id
                    cursor.execute(
                        f"SELECT fest_id, name from participating_ext natural join ext_participant where event_id = {event_id} UNION SELECT fest_id, name from participating_int natural join student where event_id = {event_id}"
                    )
                    temp["participants"] = cursor.fetchall()

                    # volunteers of event_id
                    cursor.execute(f"SELECT roll, name from volunteering natural join student where event_id = {event_id}")
                    temp["volunteers"] = cursor.fetchall()

                    event_org_details[event_id] = temp

            except psycopg2.Error as e:
                print(e)
                participant_grouped_by_event_id = []
                conn.rollback()

    cursor.close()

    if url_encrypt == session["url_encrypt_global"]:
        return render_template(
            "index.html",
            fest_id=fest_id,
            organise=organise,
            student=student,
            state=x,
            participating_event=participating_event_2,
            non_participating_event=non_participating_event,
            volunteering_event=volunteering_event_2,
            non_volunteering_event=non_volunteering_event,
            events_organised=events_organised,
            event_org_details=event_org_details,
            other_events=other_events,
            events_won = events_won,
            details=details,
            url_encrypt=url_encrypt,

        )
    else:
        return render_template("error.html")


@app.route(
    "/winner/<int:fest_id>/<int:event_id>/<int:organise>/<int:student>/<winner_name>/<url_encrypt>",
    methods=["GET", "POST"],
)
def winner(fest_id, event_id, organise, student, winner_name, url_encrypt):
    """Winner page"""
    cursor = conn.cursor()
    
    # extract 24FEST from the winner_name

    try:
        cursor.execute(
            f"UPDATE event SET event_winner = '{winner_name}' WHERE event_id = {event_id}"
        )
        conn.commit()

    except psycopg2.Error as e:
        print(e)
        conn.rollback()

    cursor.close()
    return redirect(
        url_for(
            "index",
            fest_id=fest_id,
            organise=organise,
            student=student,
            x=1,
            url_encrypt=url_encrypt,
        )
    )


@app.route(
    "/participate/<int:fest_id>/<int:event_id>/<int:organise>/<int:student>/<url_encrypt>",
    methods=["GET", "POST"],
)
def participate(fest_id, event_id, organise, student, url_encrypt):
    """Participate page"""
    cursor = conn.cursor()
    if fest_id > 1000:
        try:
            cursor.execute(
                f"INSERT INTO participating_ext VALUES ({fest_id},{event_id})"
            )
            conn.commit()

        except psycopg2.Error as e:
            print(e)
            conn.rollback()
    else:
        try:
            cursor.execute(
                f"INSERT INTO participating_int VALUES ({fest_id},{event_id})"
            )
            conn.commit()

        except psycopg2.Error as e:
            print(e)
            conn.rollback()

    cursor.close()
    return redirect(
        url_for(
            "index",
            fest_id=fest_id,
            organise=organise,
            student=student,
            x=0,
            url_encrypt=url_encrypt,
        )
    )


@app.route(
    "/volunteer/<int:fest_id>/<int:event_id>/<int:organise>/<int:student>/<url_encrypt>",
    methods=["GET", "POST"],
)
def volunteer(fest_id, event_id, organise, student, url_encrypt):
    """Volunteer page"""
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO volunteering VALUES ({fest_id},{event_id})")
        conn.commit()

    except psycopg2.Error as e:
        print(e)
        conn.rollback()

    cursor.close()
    return redirect(
        url_for(
            "index",
            fest_id=fest_id,
            organise=organise,
            student=student,
            x=0,
            url_encrypt=url_encrypt,
        )
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page"""
    flag = 0
    if request.method == "POST":
        cursor = conn.cursor()

        # get the largest fest_id from ext_participant table
        try:
            cursor.execute(
                "SELECT fest_id from ext_participant order by fest_id desc limit 1"
            )
            fest_id = 0
            fest_id = cursor.fetchone()
            fest_id = fest_id[0]

        except psycopg2.Error as e:
            print(e)
            fest_id = None
            conn.rollback()

        # if fest_id is None, then set fest_id to 1001
        if fest_id is None:
            fest_id = 1000

        username = request.form["name"]
        password = request.form["password"]
        confirm_password = request.form["repassword"]
        college = request.form["college"]

        if password == confirm_password:
            try:
                cursor.execute(
                    "SELECT acc_id from accomodation order by capacity desc limit 1"
                )
                acc_id = cursor.fetchone()
                acc_id = int(acc_id[0])
                fest_id = fest_id + 1
                cursor.execute(
                    f"INSERT into ext_participant VALUES ({fest_id},'{username}','{college}',{acc_id},'{password}')"
                )
                conn.commit()
                cursor.execute(
                    f"UPDATE accomodation SET capacity = capacity - 1 WHERE acc_id = {acc_id}"
                )
                conn.commit()

            except psycopg2.Error as e:
                print(e)
                conn.rollback()

            cursor.close()

            flag = 1

            return render_template("register.html", flag=flag, fest_id=fest_id)
        else:
            # add the part where user is asked to enter again
            flag = -1
            return render_template("register.html", flag=flag)

    else:
        return render_template("register.html")

if __name__ == "__main__":
    # connect to the database

    app.secret_key = "secret"

    app.run(debug=True)

