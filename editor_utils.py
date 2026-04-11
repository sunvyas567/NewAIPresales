from bs4 import BeautifulSoup

# -------------------------
# JSON → HTML (for editor)
# -------------------------

def payload_to_html(payload):

    #print("inside pqyl;oad_to_html Converting payload to HTML:", payload)
    if not payload or "sections" not in payload:
        return ""

    html = ""

    for sec in payload["sections"]:
        html += f"<h3>{sec.get('title','')}</h3>"
        html += f"<p>{sec.get('content','')}</p>"

    return html


# -------------------------
# HTML → JSON (for DB)
# -------------------------

def html_to_payload(html):

    soup = BeautifulSoup(html, "html.parser")

    sections = []
    current_title = None
    buffer = []

    for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):

        if tag.name in ["h1", "h2", "h3"]:
            if current_title:
                sections.append({
                    "title": current_title,
                    "content": "\n".join(buffer).strip()
                })
                buffer = []

            current_title = tag.get_text()

        else:
            buffer.append(tag.get_text())

    if current_title:
        sections.append({
            "title": current_title,
            "content": "\n".join(buffer).strip()
        })

    #print("Extracted Sections:", sections)

    return {"sections": sections}