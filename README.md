# Linkedin_Scrapper
This script allows you to monitor new connections of your competitors' decision-makers on LinkedIn. It tracks new connections, analyzes their profiles, and sends hyper-personalized connection requests based on the extracted information.

## Libraries Used

- `requests`: Used for making HTTP requests to retrieve the HTML content of LinkedIn profiles.

- `beautifulsoup4`: Used for parsing and extracting information from HTML content.

- `linkedin`: A custom library for interacting with the LinkedIn API.

## Code Explanation

The script consists of the following main components:

- `scrape_profile(url)`: This function retrieves the HTML content of a LinkedIn profile given a profile URL using the `requests` library.

- `new_connections(competitor_profile_url)`: This function tracks new connections in the competitor's LinkedIn profile by scraping the HTML content using `requests` and `beautifulsoup4` libraries. It extracts information about the new connections such as name, title, and profile URL.

- `profile_info(html)`: This function extracts relevant information from the profile HTML using `beautifulsoup4`. It retrieves the 'About Us' section, job description, and recent posts from the profile.

- `connection_request_message(about, job_title, company, recent_posts)`: This function generates a hyper-personalized connection request message based on the extracted information from the profile.

- `send_connection_request(api, profile_id, message)`: This function sends a connection request using the LinkedIn API. Please make sure you have provided a valid LinkedIn API access token.

- `main()`: The main function that initializes the LinkedIn API client, tracks new connections, scrapes their profiles, generates connection requests, and sends them.

## Disclaimer

Ensure that you use this script responsibly and in compliance with LinkedIn's Terms of Service and privacy rules. LinkedIn may have restrictions and rate limits in place for automated activities, so please adjust the script accordingly to avoid violating those terms.



