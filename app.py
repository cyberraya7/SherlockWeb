import streamlit as st
import requests
import pandas as pd
import os
import io

# Utility functions
def interpolate_string(input_string, username):
    """Replaces placeholders in URLs with the given username."""
    return input_string.replace("{}", username)

def get_response(url, headers, timeout=10):
    """Performs a GET request and handles exceptions."""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.status_code, None
    except requests.exceptions.RequestException as e:
        return None, str(e)

def check_username(username, site_data):
    """Checks if the username exists on various platforms."""
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    }

    for site, info in site_data.items():
        url = interpolate_string(info['url'], username)
        status_code, error = get_response(url, headers)

        if status_code == 200:
            results.append((f'<a href="{url}" target="_blank">{site}</a>', "Found"))
        elif status_code == 404:
            results.append((f'<a href="{url}" target="_blank">{site}</a>', "Not Found"))
        else:
            results.append((f'<a href="{url}" target="_blank">{site}</a>', "Not Found"))

    return results

# Streamlit application
st.title("Username Availability Checker")

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
            with st.spinner("Searching for usernames..."):
                results = check_username(username, site_data)

            # Convert results to DataFrame (only Profile Link & Status)
            df = pd.DataFrame(results, columns=["Profile Link", "Status"])

            if not df.empty:
                st.success("Search completed!")

                # Create an HTML table with hyperlinks
                html_table = df.to_html(escape=False, index=False)
                st.markdown(html_table, unsafe_allow_html=True)

                # Provide CSV download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name=f"{username}_results.csv",
                    mime="text/csv"
                )

                # Provide Excel download (in-memory)
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                excel_data = excel_buffer.getvalue()

                st.download_button(
                    "Download Excel",
                    data=excel_data,
                    file_name=f"{username}_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            else:
                st.warning("No results found.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

st.caption("Powered by Eclogic")
