"""
interrupts.py
Copyright 2018-2020 Adam Greig
Licensed under the MIT and Apache 2.0 licenses. See LICENSE files for details.
"""

import xml.etree.ElementTree as ET


def parse_device(svd_file):
    interrupts = {}
    tree = ET.parse(svd_file)
    dname = tree.find("name").text
    for ptag in tree.iter("peripheral"):
        pname = ptag.find("name").text
        for itag in ptag.iter("interrupt"):
            name = itag.find("name").text
            value = itag.find("value").text
            desc = itag.find("description").text.replace("\n", " ")
            interrupts[int(value)] = {"name": name, "desc": desc, "pname": pname}
    return dname, interrupts


def main(svd_file, gaps=True):
    name, interrupts = parse_device(svd_file)
    missing = set()
    lastint = -1
    for val in sorted(interrupts.keys()):
        for v in range(lastint + 1, val):
            missing.add(v)
        lastint = val
        i = interrupts[val]
        print(f"{val} {i['name']}: {i['desc']} (in {i['pname']})")
    if gaps:
        print("Gaps:", ", ".join(str(x) for x in sorted(missing)))
