from flask import Flask, render_template, request, redirect, session
import yaml
import os

app = Flask(__name__)
app.secret_key = "supersecret"

DATA_DIR = "/ctf/data"

def load_yaml(file):
    path = os.path.join(DATA_DIR, file)
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}

def save_yaml(file, data):
    with open(os.path.join(DATA_DIR, file), "w") as f:
        yaml.dump(data, f, sort_keys=False)

def current_user():
    return session.get("user")

def is_admin():
    user = current_user()
    users = load_yaml("users.yaml")
    return user and users["users"][user]["is_admin"]

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    user = current_user()
    if not user:
        return redirect("/login")
    users = load_yaml("users.yaml")
    if is_admin():  # Admin sees no points
        points = None
    else:
        points = users["users"][user]["points"]
    return render_template("home.html", user=user, points=points)

@app.route("/login", methods=["GET", "POST"])
def login():
    users = load_yaml("users.yaml")
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if u in users.get("users", {}) and users["users"][u]["password"] == p:
            session["user"] = u
            return redirect("/")
    return render_template("login.html", user=current_user(), mode="login")

@app.route("/register", methods=["POST"])
def register():
    users = load_yaml("users.yaml")
    u = request.form["username"]
    p = request.form["password"]
    if "users" not in users:
        users["users"] = {}
    if u not in users["users"]:
        users["users"][u] = {"password": p, "is_admin": False, "points": 0}
        save_yaml("users.yaml", users)
    return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/ctf", methods=["GET", "POST"])
def ctf():
    user = current_user()
    if is_admin():
        return redirect("/ctf_root")
    flags = load_yaml("flags.yaml")
    submissions = load_yaml("submissions.yaml")
    users = load_yaml("users.yaml")
    feedback = None
    if request.method == "POST" and user:
        block = request.form["block"]
        scenario = request.form["scenario"]
        task = request.form["task"]
        answer = request.form["flag"]
        correct_flag = flags[block][scenario][task]["flag"]
        task_points = flags[block][scenario][task].get("points", 0)
        already_solved = submissions.get("submissions", {}).get(user, {}).get(block, {}).get(scenario, {}).get(task)
        if already_solved:
            feedback = "Already solved ✅"
        elif answer == correct_flag:
            feedback = "Correct!"
            submissions.setdefault("submissions", {})
            submissions["submissions"].setdefault(user, {})
            submissions["submissions"][user].setdefault(block, {})
            submissions["submissions"][user][block].setdefault(scenario, {})
            submissions["submissions"][user][block][scenario][task] = True
            save_yaml("submissions.yaml", submissions)
            users["users"][user]["points"] += task_points
            save_yaml("users.yaml", users)
        else:
            feedback = "Incorrect!"
    return render_template("ctf.html", flags=flags, user=user, feedback=feedback, load_yaml=load_yaml)

@app.route("/ctf_root", methods=["GET", "POST"])
def ctf_root():
    if not is_admin():
        return redirect("/")
    flags = load_yaml("flags.yaml")
    if request.method == "POST":
        action = request.form.get("action")
        block = request.form.get("block")
        scenario = request.form.get("scenario")
        task = request.form.get("task")
        if action == "add_block":
            flags.setdefault(block, {})
        elif action == "add_scenario":
            flags.setdefault(block, {}).setdefault(scenario, {})
        elif action == "add_task":
            question = request.form.get("question")
            flag_val = request.form.get("flag")
            points = int(request.form.get("points"))
            flags.setdefault(block, {}).setdefault(scenario, {})
            flags[block][scenario][task] = {"question": question, "flag": flag_val, "points": points}
        elif action == "delete_block":
            flags.pop(block, None)
        elif action == "delete_scenario":
            flags.get(block, {}).pop(scenario, None)
        elif action == "delete_task":
            flags.get(block, {}).get(scenario, {}).pop(task, None)
        save_yaml("flags.yaml", flags)
        return redirect("/ctf_root")
    return render_template("ctf_root.html", flags=flags, user=current_user())

@app.route("/leaderboard")
def leaderboard():
    user = current_user()  # Get the current logged-in user

    import colorsys

    users = load_yaml("users.yaml").get("users", {})
    submissions = load_yaml("submissions.yaml")
    flags = load_yaml("flags.yaml")

    players = [(u, data["points"]) for u, data in users.items() if not data.get("is_admin")]
    players.sort(key=lambda x: x[1], reverse=True)
    block_labels = list(flags.keys())

    # Generate 40+ distinct colors using HSL
    num_colors = max(len(players), 40)
    colors = []
    for i in range(num_colors):
        h = i / num_colors
        r, g, b = colorsys.hsv_to_rgb(h, 0.7, 0.9)
        colors.append('#{:02X}{:02X}{:02X}'.format(int(r*255), int(g*255), int(b*255)))

    datasets = []
    for idx, (player, _) in enumerate(players):
        data = []
        for block in block_labels:
            block_points = 0
            # Check if player has submissions for the block
            if submissions.get("submissions", {}).get(player, {}).get(block):
                for scenario in flags.get(block, {}):
                    # Check if player has submissions for the scenario
                    if submissions["submissions"][player][block].get(scenario):
                        for task in flags.get(block, {}).get(scenario, {}):
                            # Check if the task is completed
                            if submissions["submissions"][player][block][scenario].get(task):
                                block_points += flags[block][scenario][task].get("points", 0)
            data.append(block_points)
        color = colors[idx % len(colors)]
        datasets.append({
            "label": player,
            "data": data,
            "backgroundColor": color + "55",
            "borderColor": color,
            "fill": True
        })

    return render_template("leaderboard.html",
                           datasets=datasets,
                           block_labels=block_labels,
                           players=players,
                           user=user)  # Pass the user to the template


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
