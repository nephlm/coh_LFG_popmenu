import json
import re

source_file = "reference/BadgeSetList.mnu"
out_file = "data/all_badges.json"


class Badges:
    def __init__(self) -> None:
        self.by_name: dict = {}

    def add(self, badge: "Badge"):
        self.by_name[badge.name] = badge

    def __len__(self):
        return len(self.by_name)

    def write(self):
        print(f"Writing badges to {out_file}")
        badge_list = [badge.dict for badge in self.by_name.values()]
        with open(out_file, "w") as out:
            json.dump(badge_list, out, indent=4)


class Badge:
    def __init__(self, name, setTitleId, key):
        self.name = name
        self.setTitleId = setTitleId
        self.badge_key = key

    @property
    def dict(self):
        return {
            "name": self.name,
            "setTitleId": self.setTitleId,
            "badge_key": self.badge_key,
        }

    @classmethod
    def make_badge_from_blob(self, blob: str):
        try:
            name = re.findall('DisplayName\s*"(.*)"', blob)[0]
            try:
                setTitleId = re.findall('settitle\s*(.*)"', blob)[0]
            except IndexError:
                if re.findall('Command\s""', blob):
                    setTitleId = None
                else:
                    raise
            key = re.findall("Badge\s*(.*)", blob)[0]
            return Badge(name, setTitleId, key)
        except IndexError:
            print("BAD BLOB")
            print(blob)
            raise
            return None

    def __str__(self) -> str:
        return str((self.name, self.setTitleId, self.badge_key))


def main():
    badges = Badges()
    locked_option_regex = re.compile(
        "LockedOption(.*?)}", re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    with open(source_file, "r") as fp:
        data = fp.read()
        match_list = locked_option_regex.findall(data)
        if match_list:
            for match in match_list:
                badge = Badge.make_badge_from_blob(match)
                if badge:
                    badges.add(badge)
                    print(f"Badge found: {badge}")
        else:
            print("no match list")
    badges.write()


if __name__ == "__main__":
    main()