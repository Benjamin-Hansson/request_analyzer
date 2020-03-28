import json
import tablib
from pathlib import Path

repo_path = Path("C:/Users/vicka/Dropbox/liu/adblocker-measurements")
files = ["Adult_50.json", "Kids_50.json", "Media_50.json", "Media_SE_50.json", "Shopping_50.json",
             "Shopping_SE_50.json", "top_1000.json", "top_SE_500.json"]
data_folder_path = repo_path / "collected_data"
new_data_folder_path = repo_path / "new_collected_data"


def create_excel_book():
    book = tablib.Databook()

    for filename in files:
        file = new_data_folder_path / filename

        a = json.loads(file.read_text())
        data = tablib.Dataset()

        data.headers = ("Domain", "External req", "Ext. Req w/ adblock", "known trackers", "known trackers w/ adblock")

        for elem in a:
            extReq = a[elem]["externalRequests"]["amount"]
            extReqABP = a[elem]["externalRequestsAdBlocker"]["amount"]
            knownTrackers = a[elem]["knownTrackers"]["amount"]
            knownTrackersABP = a[elem]["knownTrackersAdBlocker"]["amount"]

            data.append([elem, extReq, extReqABP, knownTrackers, knownTrackersABP])

        book.add_sheet(data)

    output_file = new_data_folder_path / "results.xls"
    output_file.touch()
    output_file.write_bytes(book.export("xls"))

    return


def stuff ():
    for filename in files:
        file = data_folder_path / filename
        disconnect_file = repo_path / "disconnect_list.json"
        disc_list = json.loads(disconnect_file.read_text())

        data = json.loads(file.read_text())

        for domain in data:
            extReq = data[domain]["externalRequests"]["data"]
            extReqABP = data[domain]["externalRequestsAdBlocker"]["data"]
            known_trackers = requests_in_know_trackers(extReq, disc_list)
            known_trackers_ABP = requests_in_know_trackers(extReqABP, disc_list)

            data[domain]["knownTrackers"] = {"amount" : len(known_trackers), "data" : known_trackers}
            data[domain]["knownTrackersAdBlocker"] = {"amount" : len(known_trackers_ABP), "data" : known_trackers_ABP}

        new_data_file = new_data_folder_path / filename
        new_data_file.write_text(json.dumps(data, indent=6))
    return


#data i json fil = externalReq i param
def requests_in_know_trackers(externalReq, disconnect_list):
    known_trackers = {}

    for external_domain in externalReq:
        for known_tracker_domain in disconnect_list:
            li = disconnect_list[known_tracker_domain]["properties"] + disconnect_list[known_tracker_domain]["resources"]
            for property in li:
                if (str(external_domain)).lower() in (str(property)).lower():
                    known_trackers[external_domain] = externalReq[external_domain]
                    break

    return known_trackers

create_excel_book()