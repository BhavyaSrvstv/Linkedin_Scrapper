import requests
from bs4 import BeautifulSoup
from linkedin import linkedin

# Function to scrape a LinkedIn profile given a profile URL


def scrape_profile(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None
# this function tracks the new connections in the competitor's profile


def new_connections(competitor_url):
    # Retrieve HTML content of competitor's LinkedIn profile
    response = requests.get(competitor_url)
    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve profile HTML content")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content

    # Find the section containing the competitor's connections
    connections_section = soup.find('section', {'id': 'ember28'})

    if connections_section:
        connection_elements = connections_section.find_all(
            'li', {'class': 'reusable-search__result-container'})  # Find all the connection elements

        new_connections = []
        for connection_element in connection_elements:
            connection_name = connection_element.find(
                'span', {'class': 'actor-name'}).get_text(strip=True)
            connection_title = connection_element.find(
                'span', {'class': 'actor-title'}).get_text(strip=True)
            connection_profile_url = connection_element.find(
                'a', {'class': 'app-aware-link'}).get('href')

            new_connections.append({
                'name': connection_name,
                'title': connection_title,
                'profile_url': connection_profile_url
            })

        return new_connections
    else:
        print("Connections section not found")
        return []

# Function to extract relevant information from the profile HTML


def profile_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extract 'About Us' section
    about_section = soup.find('section', {'class': 'pv-about-section'})
    about_text = about_section.get_text(strip=True) if about_section else ''

    # Extract job description
    experience_section = soup.find(
        'section', {'id': 'experience-section'})  # Extract job description
    job_title = ''
    company = ''
    if experience_section:
        first_job = experience_section.find(
            'li', {'class': 'pv-entity__position-group-pager'})
        if first_job:
            job_title_element = first_job.find('h3', {'class': 't-16'})
            if job_title_element:
                job_title = job_title_element.get_text(strip=True)
            company_element = first_job.find(
                'p', {'class': 'pv-entity__secondary-title'})
            if company_element:
                company = company_element.get_text(strip=True)

    # Extract recent posts
    posts_section = soup.find(
        'section', {'class': 'pv-recent-activity-detail-section-v2'})
    recent_posts = []
    if posts_section:
        post_elements = posts_section.find_all(
            'li', {'class': 'pv-recent-activity-detail-v2'})
        for post_element in post_elements:
            post_text_element = post_element.find(
                'span', {'class': 'ember-view'})
            if post_text_element:
                post_text = post_text_element.get_text(strip=True)
                recent_posts.append(post_text)

    return about_text, job_title, company, recent_posts

# Function to generate connection request message


def connection_request_message(about, job_title, company, recent_posts):
    connection_request = f"Hi, {about}! I noticed you are a {job_title} at {company}. I enjoyed reading your recent posts: {', '.join(recent_posts)}"
    return connection_request

# Function to send connection request using LinkedIn API


def send_connection_request(api, profile_id, message):
    api.send_invitation(
        profile_id=profile_id,
        message=message
    )

# Main function


def main():
    api = linkedin.LinkedInApplication(token="ACCESS_TOKEN")

    competitor_profile_url = 'https://www.linkedin.com/company/competitor-profile'
    new_connections = new_connections(competitor_profile_url)

    for connection in new_connections:
        profile_url = connection['profile_url']
        profile_html = scrape_profile(profile_url)
        if profile_html:
            about, job_title, company, recent_posts = profile_info(
                profile_html)
            connection_request = connection_request_message(
                about, job_title, company, recent_posts)
            # Extract the profile ID from the URL
            profile_id = profile_url.split('/in/')[1]
            send_connection_request(api, profile_id, connection_request)
        else:
            print(f"Failed to scrape profile: {profile_url}")


if __name__ == '__main__':
    main()
