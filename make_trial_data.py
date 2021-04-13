import json

trial_file = "data/trials.json"
trial_badge_file = "data/trial_badges.json"
all_badges = "data/all_badges.json"

out_file = "data/trail_data.json"


def read_json_file(infile):
    with open(infile, "r") as fp:
        data = json.load(fp)
    return data


def make_badge_db(infile):
    badge_db = {}
    for badge in read_json_file(infile):
        name = badge["name"].lower()
        name_key = name.split("/")[0].strip()
        badge_db[name_key] = badge
    return badge_db


def make_trial_db(infile):
    trial_db = {}
    for trial in read_json_file(infile):
        trial_db[trial["Trial Key"].lower()] = trial
    return trial_db


def make_trial_badges_db(badge_db, trial_db, infile):
    trial_badges_db = []
    last_trial = None
    for trial_badge in read_json_file(infile):
        key = trial_badge["Trial Key"].lower()
        name = trial_badge["Name"].lower().split("/")[0].strip()

        trial = trial_db[key]
        if last_trial and trial != last_trial:
            trial_badges_db.append(last_trial)
        trial_badge_list = trial.get("Badges", [])

        # If there is a key error her it means a mismatch on the badge name between
        # the two sources of data.   Correct the trial_badges.json file.
        badge = badge_db[name]

        trial_badge["setTitleId"] = badge["setTitleId"]
        trial_badge["badge_key"] = badge["badge_key"]
        trial_badge_list.append(trial_badge)
        trial["Badges"] = trial_badge_list
        last_trial = trial

    trial_badges_db.append(trial)
    return trial_badges_db


def main():
    badge_db = make_badge_db(all_badges)
    trial_db = make_trial_db(trial_file)
    trial_data = make_trial_badges_db(badge_db, trial_db, trial_badge_file)
    print(json.dumps(trial_data, indent=4))

    with open(out_file, "w") as out:
        json.dump(trial_data, out, indent=4)


if __name__ == "__main__":
    main()
