import csv
import json
import os

# input_path = "taskforce.csv"
# input_path = "giant_monsters.csv"
# input_path = "trials.csv"
# input_path = "trial_badges.csv"

# output_path = "taskforcex.json"
# output_path = "giant_monsters.json"
# output_path = "trials.json"
# output_path = "trial_badges.json"


def main():
    all_data = []
    with open(os.path.join("data", input_path), "r") as fp:
        dreader = csv.DictReader(fp)
        for row in dreader:
            # if row["Hero Badge"] == "" and row["Villain Badge"] == "":
            #     continue
            print(row)
            all_data.append(row)

    with open(os.path.join("data", output_path), "w") as out:
        json.dump(all_data, out, indent=4)


if __name__ == "__main__":
    main()