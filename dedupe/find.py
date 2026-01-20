from dedupe import registry

def run_find_duplicates(path:str):
    with registry.HashRegistry() as db:
        db.registerDir(path)
        all_dupes = db.allDupeEntries()

    dupe_groups = {}
    for p,h in all_dupes:
        if h not in dupe_groups:
            dupe_groups[h] = []
        dupe_groups[h].append(p)

    for h, pathlist in dupe_groups.items():
        print(f"=== {h} ===")
        print("- " + "\n- ".join(pathlist))

