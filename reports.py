import base64

def download_html(df,title):

    html=df.to_html(index=False)

    b64=base64.b64encode(html.encode()).decode()

    href=f'<a href="data:file/html;base64,{b64}" download="{title}.html">ڈاؤنلوڈ کریں</a>'

    return href
