import sys

from file_handling import *



class DataAnalyze:
    def __init__(self):
        self.file_datas = {}

    # Adds files to DataAnalyze
    def set_files(self, *file_names):
        for name in file_names:
            self.file_datas[name] = read_data_file(name)


    # Prints all domains and amount of domains
    def get_domains(self):
        counter = 0
        for file in self.file_datas:
            for domain in self.file_datas[file]:
                print(domain)
                counter += 1
        print("Found", counter, "domains")

    # Removes all domains that doesn't have any valid data
    def remove_invalid(self):
        counter = 0
        for file in self.file_datas:
            changed = False
            domains = self.file_datas[file]
            remove = []
            for domain in domains:
                if domains[domain]["externalRequests"]["amount"] == 0 and \
                        domains[domain]["knownTrackers"]["amount"] == 0 and \
                        domains[domain]["knownTrackersAdBlocker"]["amount"] == 0 and \
                        domains[domain]["externalRequestsAdBlocker"]["amount"] == 0:
                    remove.append(domain)
                    changed = True
                    counter += 1
            if changed:
                print("CHANGED")
                for domain in remove:
                    print("Removing",domain)
                    domains.pop(domain)
                print(file)
                write_data_file(file, domains)
        print("Removed", counter, "files")


    def get_average_known_trackers(self):
        return self.get_average_amount("knownTrackers")

    def get_average_potential_trackers(self):
        return self.get_average_amount("externalRequests")

    def get_average_known_trackers_adblock(self):
        return self.get_average_amount("knownTrackersAdBlocker")

    def get_average_potential_trackers_adblock(self):
        return self.get_average_amount("externalRequestsAdBlocker")

    # Returns average amount of entries at given key and also amount of each entrie
    def get_average_amount(self, key):
        counter = 0
        total = 0
        domains_amount = {}

        for file in self.file_datas:
            domains = self.file_datas[file]
            for domain in domains:
                amount = domains[domain][key]["amount"]
                domains_amount[domain] = amount
                total += amount
                counter += 1

        return total / counter


    def get_domain_counts(self):
        counter = 0
        domains_amount = {}

        for file in self.file_datas:
            domains = self.file_datas[file]
            for domain in domains:
                for tracker in domains[domain]["externalRequests"]["data"]:
                    if domains_amount.get(tracker):
                        domains_amount[tracker] += 1
                    else:
                        domains_amount[tracker] = 1
                counter += 1

        print(counter)

        return sorted(domains_amount.items(), key=lambda item: item[1], reverse=True)[:11]


    def amount_sent_to_google(self):
        with open('disconnect_list.json', 'r') as file:
            disconnect_list = json.loads(file.read())
            google_resources = ["abc.xyz",
                                "google",
                                "ingress",
                                "admeld",
                                "blogger",
                                "google-melange",
                                "google.co.zw",
                                "google",
                                "panoramio",
                                "youtube"
                                "google",
                                "2mdn",
                                "admeld",
                                "admob",
                                "cc-dt",
                                "destinationurl",
                                "doubleclick",
                                "gmail",
                                "google-analytics",
                                "googleadservices",
                                "googlemail",
                                "googlesyndication",
                                "googlevideo",
                                "googletagservices",
                                "invitemedia",
                                "postrank",
                                "smtad",
                                "apture",
                                "blogger",
                                "ggpht",
                                "gmodules",
                                "googleapis",
                                "googleusercontent",
                                "gstatic",
                                "recaptcha",
                                "youtube",
                                "googletagmanager"
                                ]

            facebook_resources = [
                "facebook",
                "fb",
                "fb",
                "friendfeed",
                "instagram",
                "fbcdn",
                "messenger",
                "atlassolutions"
                "facebook",
                "facebook",
                "facebook",
                "facebook",
                "fb",
                "fb",
                "friendfeed",
                "instagram",
                "fbcdn",
                "messenger",
                "atlassolutions"
            ]

            amazon_resource = [
      "amazon",
      "alexa",
      "amazonaws"
      "amazon",
      "amazon-adsystem",
      "amazon",
      "alexametrics",
      "cloudfront",
      "amazonaws"
    ]

            counter = 0
            amount = 0

            list = []

            for file in self.file_datas:
                domains = self.file_datas[file]
                for domain in domains:
                    b = False
                    for tracker in domains[domain]["externalRequests"]["data"]:
                        for resource in amazon_resource:
                            if tracker in resource:
                                amount += 1
                                if tracker not in list:
                                    list.append(tracker)
                                b = True
                                break
                        if b:
                            break
                    counter += 1

        print(list)

        return amount/counter


    def get_average_blocked_requests(self):

        Blocked = 0
        Sent = 0

        for file in self.file_datas:
            domains = self.file_datas[file]
            for domain in domains:
                blocked_sent = domains[domain]["externalRequestsAdBlocker"]["data"]
                for blocked in blocked_sent:
                    Blocked += int(blocked_sent[blocked])

                not_blocked_sent = domains[domain]["externalRequests"]["data"]
                for not_blocked in not_blocked_sent:
                    Sent += int(not_blocked_sent[not_blocked])
        print("Blocked:", Blocked)
        print("Sent:", Sent)
        return 1 - (Blocked / Sent)





def getKnownTrackersFile(filename):
    analyse = DataAnalyze()
    analyse.set_files(filename)
    analyse.get_average_known_trackers()


def main(file_names):

    return


if __name__ == '__main__':
    main(sys.argv[1:])
