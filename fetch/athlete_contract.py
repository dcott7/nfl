# import requests
# from bs4 import BeautifulSoup

# BASE_URL = 'https://www.spotrac.com/nfl/{team_name}/cap/_/year/2024'

# def get_team_page(team_name: str):
#     team_name = team_name.lower().replace(' ','-')
#     return BeautifulSoup(requests.get(BASE_URL.format(team_name=team_name)).content,"html.parser")


# soup = get_team_page('Carolina Panthers')

# table = soup.find("table", {"id": "table"})  # Use ID to find the specific table

# # Step 3: Extract rows with cap information
# cap_data = {}
# for row in table.find("tbody").find_all("tr", {"class": "totals"}):
#     # Find the description in the first <td>
#     description_cell = row.find("td", {"class": "text-left sticky"})
#     # Find the salary or cap number in the highlighted contract <td>
#     amount_cell = row.find("td", {"class": "text-center contract highlight"})
    
#     # Ensure both cells exist to avoid errors
#     if description_cell and amount_cell:
#         description = description_cell.get_text(strip=True)
#         amount = amount_cell.get_text(strip=True)
        
#         # Store the data in the dictionary
#         cap_data[description] = amount

# # Step 4: Display the extracted data
# for category, amount in cap_data.items():
#     print(f"{category}: {amount}")
