import requests
from bs4 import BeautifulSoup

def wolfram_alpha_query(query):
    base_url = "http://api.wolframalpha.com/v2/query"
    app_id = 'YourAPI'  # Replace with your actual API key
    input_format = "plaintext"

    params = {
        'input': query,
        'format': input_format,
        'output': 'JSON',  # You can change the output format as needed
        'appid': app_id,
        'format': 'image',

    }

    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check for errors in the request
        result = response.json()
        print(result)
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def convert_to_html(result):
    html_output = "<html><body>"

    pods = result.get('queryresult', {}).get('pods', [])

    for pod in pods:
        title = pod.get('title', '')
        subpods = pod.get('subpods', [])

        for subpod in subpods:
            plaintext = subpod.get('plaintext', '')
            img_src = subpod.get('img', {}).get('src', '')

            # Display the title and plaintext content
            html_output += f"<h3>{title}</h3>"
            html_output += f"<p>{plaintext}</p>"

            # Display the image if available
            if img_src:
                html_output += f"<img src='{img_src}' alt='{title}' width='auto' height='auto'>"

    html_output += "</body></html>"
    return html_output

# Rest of your code remains unchanged


if __name__ == "__main__":
    query_text = "What is the integral of root of tan(x)"
    result = wolfram_alpha_query(query_text)

    if result:
        html_output = convert_to_html(result)
        with open("app/templates/output.html", "w", encoding="utf-8") as html_file:
            html_file.write(html_output)
        print("Output saved to output.html.")
    else:
        print("Error in processing the query.")
