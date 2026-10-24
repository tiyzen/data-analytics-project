import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

st.set_page_config(
    page_title="Web Scraping Tool",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Web Scraping Tool")
st.write(
    "Extract page titles, headings, paragraphs, and links "
    "from publicly accessible webpages."
)

url = st.text_input(
    "Enter webpage URL",
    placeholder="https://example.com"
)

if st.button("Scrape Website"):
    if not url.strip():
        st.warning("Please enter a URL.")
    else:
        try:
            parsed = urlparse(url.strip())

            if (
                parsed.scheme not in ("http", "https")
                or not parsed.hostname
                or parsed.username
                or parsed.password
            ):
                st.error("Enter a valid public HTTP or HTTPS URL.")
                st.stop()

            # Avoid requesting local or private network addresses.
            host = parsed.hostname.lower()
            if (
                host == "localhost"
                or host.endswith(".localhost")
                or host.endswith(".local")
                or host == "0.0.0.0"
                or host == "::1"
                or host.startswith("127.")
                or host.startswith("10.")
                or host.startswith("192.168.")
                or host.startswith("169.254.")
                or (
                    host.startswith("172.")
                    and len(host.split(".")) == 4
                    and host.split(".")[1].isdigit()
                    and 16 <= int(host.split(".")[1]) <= 31
                )
            ):
                st.error("Local and private network addresses are not allowed.")
                st.stop()

            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; SimpleWebScraper/1.0)"
            }

            with st.spinner("Fetching webpage..."):
                response = requests.get(
                    url.strip(),
                    headers=headers,
                    timeout=15,
                    allow_redirects=False
                )
                response.raise_for_status()

                content_type = response.headers.get(
                    "Content-Type", ""
                ).lower()

                if "text/html" not in content_type:
                    st.error("The URL did not return an HTML webpage.")
                    st.stop()

                if len(response.content) > 2_000_000:
                    st.error("The webpage is too large to process (over 2 MB).")
                    st.stop()

                soup = BeautifulSoup(response.text, "html.parser")

                for element in soup(
                    ["script", "style", "noscript", "svg"]
                ):
                    element.decompose()

                title = (
                    soup.title.get_text(" ", strip=True)
                    if soup.title else "No title found"
                )

                headings = [
                    h.get_text(" ", strip=True)
                    for h in soup.find_all(
                        ["h1", "h2", "h3", "h4", "h5", "h6"]
                    )
                    if h.get_text(" ", strip=True)
                ]

                paragraphs = [
                    p.get_text(" ", strip=True)
                    for p in soup.find_all("p")
                    if p.get_text(" ", strip=True)
                ]

                links = []
                for a in soup.find_all("a", href=True):
                    links.append({
                        "Text": a.get_text(" ", strip=True),
                        "URL": requests.compat.urljoin(
                            response.url, a["href"]
                        )
                    })

            st.success("Webpage scraped successfully!")

            st.subheader("Page Title")
            st.write(title)

            tab1, tab2, tab3 = st.tabs(
                ["Headings", "Paragraphs", "Links"]
            )

            with tab1:
                if headings:
                    for heading in headings:
                        st.write(f"- {heading}")
                else:
                    st.info("No headings found.")

            with tab2:
                if paragraphs:
                    for paragraph in paragraphs:
                        st.write(paragraph)
                        st.divider()
                else:
                    st.info("No paragraphs found.")

            with tab3:
                if links:
                    links_df = pd.DataFrame(links)
                    st.dataframe(
                        links_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.download_button(
                        "Download Links CSV",
                        data=links_df.to_csv(index=False).encode("utf-8"),
                        file_name="scraped_links.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No links found.")

            report = (
                f"Page Title: {title}\n\n"
                + "HEADINGS\n"
                + "\n".join(headings)
                + "\n\nPARAGRAPHS\n"
                + "\n\n".join(paragraphs)
            )

            st.download_button(
                "Download Scraped Text",
                data=report,
                file_name="scraped_page.txt",
                mime="text/plain"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Could not fetch the webpage: {e}")
        except Exception as e:
            st.error(f"Scraping failed: {e}")
