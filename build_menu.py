import operator
import json
from typing import Sequence, Tuple, Union, Optional, Dict


INDENT = "    "

outfile = "build/BadgeSetListNeph.mnu"


class MenuComponent:
    pass


class Menu(MenuComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self.items: dict = {}
        self.sort_key = self.name
        self.title: Optional[str] = None
        self.first_item = True

    def sorted_items(self):
        if isinstance(list(self.items.values())[0], Sequence):
            item_list = []
            for items in list(self.items.values()):
                item_list += items
            # item_list = [x[0] for x in list(self.items.values())]
        else:
            item_list = self.items.values()

        return sorted(item_list, key=operator.attrgetter("sort_key"))
        # return self.items.items()

    def build(self, indent=0):
        ret = ""
        # if not content_only:
        #     ret += self.build_header(indent)

        # ret += self.build_title(indent)

        last_key = None
        for value in self.sorted_items():
            if value.name != last_key:
                if last_key is not None:
                    ret += value.build_footer(indent + 1)
                ret += value.build_header(indent + 1)
            ret += value.build(indent + 1)
            last_key = value.name
        ret += value.build_footer(indent + 1)

        # if not content_only:
        #     ret += self.build_footer(indent)

        return ret

    def build_header(self, indent):
        return f'{self.build_title(indent)}{INDENT*indent}Menu "{self.name}"\n{INDENT*indent}{{\n'

    def build_footer(self, indent):
        return f"{INDENT*indent}}}\n"

    def build_title(self, indent):
        if self.title and False:
            return f'{INDENT*indent}Title "{self.title}"\n'
        else:
            return ""


class TopMenu(Menu):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.items["trials"] = TrialCategoryMenu("Trials")
        self.items["monsters"] = MonsterListMenu("Giant Monsters")
        self.items["taskforces"] = LevelMenu("TaskForces")
        self.title = "Categories"

    @property
    def taskforces(self):
        return self.items["taskforces"]

    @property
    def monsters(self):
        return self.items["monsters"]

    @property
    def trials(self):
        return self.items["trials"]


class MonsterListMenu(Menu):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def add_monster(self, monster: dict):
        monster_menu = MonsterMenu(monster["Name"])
        monster_menu.add_monster(monster)
        self.items[monster["Name"]] = monster_menu


class MonsterMenu(Menu):
    def add_monster(self, monster_dict: dict):
        self.items[monster_dict["Name"]] = MonsterOption(monster_dict)
        self.name = f'{self.name} [{monster_dict["Zone"]}]'


class TrialCategoryMenu(Menu):
    NORMAL = "Normal"
    RESPEC = "Respec"
    INCARNATE = "Incarnate"

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.items = {
            self.NORMAL: TrialsMenu(self.NORMAL),
            self.RESPEC: TrialsMenu(self.RESPEC),
            self.INCARNATE: TrialsMenu(self.INCARNATE),
        }
        self.name = "Trials"

    def get_category_key(self, trial_dict):
        if trial_dict["Type"].lower() in ("respec"):
            return self.RESPEC
        elif trial_dict["Type"].lower() in ("incarnate"):
            return self.INCARNATE
        return self.NORMAL

    def add_trial(self, trial_dict: dict):
        category_key = self.get_category_key(trial_dict)
        self.items[category_key].add_trial(trial_dict)


class TrialsMenu(Menu):
    def add_trial(self, trial_dict):
        merit_string = ""
        if trial_dict["Merits"]:
            merit_string = f"; M: {trial_dict['Merits']}"
        trial_name_menu = TrialNameMenu(
            f'{trial_dict["Trial"]} [L: {trial_dict["Min Level"]}+; P: {trial_dict["Max Players"]}{merit_string}]'
        )
        trial_name_menu.add_trial(trial_dict)
        self.items[trial_dict["Trial"] + "TM"] = trial_name_menu


class TrialNameMenu(Menu):
    def add_trial(self, trial_dict):
        for badge_dict in trial_dict["Badges"]:
            self.items[badge_dict["Name"] + "TNM"] = TrialOption(badge_dict)


class LevelMenu(Menu):
    LOW = (1, 24)
    MID = (25, 39)
    HIGH = (40, 50)

    TIERS = (LOW, MID, HIGH)

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.title = "Categories"
        for tier in self.TIERS:
            self.items[tier] = LevelTierMenu(tier)

    def _get_tier(self, min_level):
        for tier in self.TIERS:
            if tier[0] <= min_level <= tier[1]:
                return tier

    def add_TF(self, tf):
        min_level = int(tf["Min Level"])
        tier = self._get_tier(min_level)
        self.items[tier].add_TF(tf)


class LevelTierMenu(Menu):
    def __init__(self, tier: Tuple[int, int]) -> None:
        name = f"{tier[0]}-{tier[1]}"
        super().__init__(name)
        self.tier = tier
        self.title = "Levels"

    def add_TF(self, tf):
        contact = tf["Contact"]
        contact_menu = ContactMenu(contact)
        contact_menu.add_TF(tf)

        tf_list = self.items.get(contact, [])
        tf_list.append(contact_menu)
        self.items[contact] = tf_list


class ContactMenu(Menu):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.title = "Contacts"

    def add_TF(self, tf):
        option = TFOption(tf)
        self.items[option.key] = option
        self.sort_key = int(tf["Min Level"])


class Title(MenuComponent):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.key = name
        self.name = name

    def build_header(self, indent):
        return f""

    def build_footer(self, indent):
        return f""

    def build(self, indent):
        return f"{INDENT*indent}Title {self.get_display_name()}\n"

    def get_display_name(self):
        return self.name

    def get_command(self):
        return ""


class Option(Title):
    def __init__(self, name: str, command: str) -> None:
        super().__init__(name)
        self.key = name
        self.name = name
        self.command = command

    def build(self, indent):
        return f"{INDENT*indent}Option {self.get_display_name()} {self.get_command()}\n"

    def get_command(self):
        return self.command


class LockedOption(Option):
    def __init__(self, name, command, badge) -> None:
        super().__init__(name, command)
        self.badge = badge

    def build_header(self, indent):
        return f"{INDENT*indent}LockedOption\n{INDENT*indent}{{\n"

    def build_footer(self, indent):
        return f"{INDENT*indent}}}\n"

    def build(self, indent):
        indent += 1
        display_name = f'{INDENT*indent}DisplayName "{self.get_display_name()}"'
        command = f'{INDENT*indent}Command "{self.get_command()}"'
        badge = f"{INDENT*indent}Badge {self.get_badge_ident()}"
        return f"{display_name}\n{command}\n{badge}\n"

    def get_display_name(self):
        return self.get_badge_name()

    def get_command(self):
        return self.command
        return f"settitle {self.get_setTitleId()}"

    def get_badge_name(self):
        return self.badge

    def get_badge_ident(self):
        return ""

    def get_setTitleId(self):
        return ""


class SetTitleLockedOption(LockedOption):
    def __init__(self, badge: dict) -> None:
        self.badge_dict = badge
        command = f"settitle {self.get_setTitleId()}"
        badge = self.get_badge_name()
        name = self.get_display_name()
        super().__init__(name, command, badge)
        self.key = self.get_key()
        self.sort_key = self.key
        self.name = self.key

    def get_display_name(self):
        return f"{self.get_badge_name()}"

    def get_key(self):
        return self.get_badge_name()

    def get_badge_name(self):
        return self.badge_dict["Badge"]

    def get_badge_ident(self):
        return self.badge_dict["Badge Key"]

    def get_setTitleId(self):
        return self.badge_dict["setTitleId"]


class MonsterOption(SetTitleLockedOption):
    pass


class TrialOption(SetTitleLockedOption):
    def get_badge_name(self):
        return self.badge_dict["Name"]

    def get_badge_ident(self):
        return self.badge_dict["badge_key"]


class TFOption(SetTitleLockedOption):
    def get_badge_name(self):
        if self.badge_dict["Hero Badge"]:
            return self.badge_dict["Hero Badge"]
        else:
            return self.badge_dict["Villain Badge"]

    def get_display_name(self):
        return f'{self.get_badge_name()} [L:{self.badge_dict["Min Level"]}-{self.badge_dict["Max Level"]}; M:{self.badge_dict["Merits"]}]'


def load_json_file(infile):
    with open(infile, "r") as infile:
        data = json.load(infile)
        return data


def build_TFs(data_file, top_menu):

    tf_menu = top_menu.taskforces

    data = load_json_file(data_file)
    for tf in data:
        tf_menu.add_TF(tf)
    return top_menu


def build_monsters(data_file, top_menu):

    monster_menu = top_menu.monsters

    data = load_json_file(data_file)
    for monster in data:
        monster_menu.add_monster(monster)
    return top_menu


def build_trials(data_file, top_menu):

    trial_menu = top_menu.trials

    data = load_json_file(data_file)
    for trial in data:
        trial_menu.add_trial(trial)
    return top_menu


def main():
    top_menu = TopMenu("LFG")
    with open(outfile, "w") as out:
        with open("data/LFGPopmenu_header.txt", "r") as header:
            out.write(header.read() + "\n")

        top_menu = build_TFs("data/taskforces.json", top_menu)
        top_menu = build_monsters("data/giant_monsters.json", top_menu)
        top_menu = build_trials("data/trial_data.json", top_menu)
        out.write(top_menu.build(indent=1))

        with open("data/LFGPopmenu_footer.txt", "r") as footer:
            out.write("\n" + footer.read())


if __name__ == "__main__":
    main()