import streamlit as st
import requests
import pandas as pd
import os
from time import monotonic
from json import loads as json_loads
from typing import Optional

# Utility functions
def interpolate_string(input_object, username):
    if isinstance(input_object, str):
        return input_object.replace("{}", username)
    elif isinstance(input_object, dict):
        return {k: interpolate_string(v, username) for k, v in input_object.items()}
    elif isinstance(input_object, list):
        return [interpolate_string(i, username) for i in input_object]
    return input_object

def get_response(url, headers, timeout):
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response, None
    except requests.exceptions.RequestException as e:
        return None, str(e)

def check_username(username, site_data, timeout=60):
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    }

    for site, info in site_data.items():
        url = interpolate_string(info['url'], username)

        response, error = get_response(url, headers, timeout)

        if response:
            if response.status_code == 200:
                results.append((site, url, "Found"))
            else:
                results.append((site, url, "Not Found"))
        else:
            results.append((site, url, f"Error: {error}"))

    return results

# Streamlit application
st.title("Usernames Across Social Networks")

# Input for username
username = st.text_input("Enter the username to search for:")

# Predefined site data
site_data = {
    "GitHub": {"url": "https://github.com/{}"},
    "Twitter": {"url": "https://twitter.com/{}"},
    "Instagram": {"url": "https://www.instagram.com/{}/"},
    "Facebook": {"url": "https://www.facebook.com/{}/"},
    "8tracks":{"url": "https://8tracks.com/{}/"},
    "Academia":{"url": "https://independent.academia.edu/{}/"},
    "Allmylinks":{"url": "https://allmylinks.com/{}/"},
    "Behance":{"url": "https://www.behance.net/{}/"},
    "Blogspot":{"url": "https://blogspot.com/{}/"},
    "Discord":{"url": "https://discord.com/{}/"},
    "Disqus":{"url": "https://disqus.com/{}/"},
    "Duolingo":{"url": "https://www.duolingo.com/{}/"},
    "fiverr":{"url": "https://www.fiverr.com/{}/"},
    "flipboard":{"url": "https://flipboard.com/{}/"},
    "Github":{"url": "https://www.github.com/{}/"},
    "flipboard":{"url": "https://flipboard.com/{}/"},
    "Hackenproof":{"url": "https://hackenproof.com/{}/"},
    "Cavalier hudsonrock":{"url": "https://cavalier.hudsonrock.com/{}/"},
    "Issuu":{"url": "https://issuu.com/{}/"},
    "Nitrotype":{"url": "https://www.nitrotype.com/{}/"},
    "Producthunt":{"url": "https://www.producthunt.com/{}/"},
    "Pypi":{"url": "https://pypi.org/{}/"},
    "Reddit":{"url": "https://www.reddit.com/{}/"},
    "Roblox":{"url": "https://www.roblox.com/{}/"},
    "Slideshare":{"url": "https://slideshare.net/{}/"},
    "Smule":{"url": "https://www.smule.com/{}/"},
    "Snapchat":{"url": "https://www.snapchat.com/{}/"},
    "Strava":{"url": "https://www.strava.com/{}/"},
    "Tetr":{"url": "https://ch.tetr.io/{}/"},
    "tldrlegal":{"url": "https://tldrlegal.com/{}/"},
    "t.me":{"url": "https://t.me/{}/"},
    "x.com":{"url": "https://x.com/{}/"},
    "ultimate-guitar":{"url": "https://ultimate-guitar.com/{}/"},
    "Wattpad":{"url": "https://www.wattpad.com/{}/"},
    "Xboxgamertag":{"url": "https://xboxgamertag.com/{}/"},
    "Youtube":{"url": "https://www.youtube.com/{}/"},
}

# Search button
if st.button("Search"):
    if not username:
        st.error("Please enter a username to search for.")
    else:
        try:
            # Perform username check
            with st.spinner("Searching for usernames..."):
                results = check_username(username, site_data)

            # Display results
            if results:
                st.success("Search completed!")

                # Convert results to DataFrame
                df = pd.DataFrame(results, columns=["Site", "URL", "Status"])

                # Display table
                st.dataframe(df)

                # Provide download options
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", data=csv, file_name=f"{username}_results.csv", mime="text/csv")

                excel_path = f"{username}_results.xlsx"
                df.to_excel(excel_path, index=False)
                with open(excel_path, "rb") as excel_file:
                    st.download_button("Download Excel", data=excel_file, file_name=f"{username}_results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                os.remove(excel_path)

            else:
                st.warning("No results found.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
st.caption("Powered by Eclogic ")