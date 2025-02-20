import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
TRAVEL_DB_ID = os.getenv("TRAVEL_DB_ID")

client = Client(auth=NOTION_API_KEY)


async def write_activity(location, language, currency, landscape_types, best_months_to_visit, budget, food, activities):

    properties = {}
    budget_mapping = {'€€€': {'name': '€€€', 'id': 'iBKY'}, '€€': {'name': '€€', 'id': 'uKer'}, '€': {'name': '€', 'id': 'WqyF'}}

    
    try:
        
        # Add optional properties if provided
        if location:
            properties["Location"] = {
                "title": [{"text": {"content": location}}]  # Correct title format
            }
        
        if language:
            existing_languages = ["French", "Korean", "English", "Spanish", "Portuguese", "Italian", "Japanese", "Russian", "Arabic", "Turkish"]  # Predefined languages (can be fetched manually from your Notion database)
            language_list = language.split(",")  # Assume you get a comma-separated list from your web search

            selected_languages = [
                {"name": lang.strip()} if lang.strip() in existing_languages else {"name": "Other"}
                for lang in language_list
            ]
    
            properties["Language"] = {
                "multi_select": selected_languages
            }
        
        if currency:
            properties["Currency"] = {
                "rich_text": [{"text": {"content": currency}}]  # Currency as text field
            }
        
        if landscape_types:
            properties["Landscape Types"] = {
                "multi_select": [{"name": landscape_type} for landscape_type in landscape_types]  # Correct multi_select format
            }
        
        if best_months_to_visit:
            properties["Best Months to Visit"] = {
                "multi_select": [{"name": month} for month in best_months_to_visit]  # Correct multi_select format
            }
        
        if budget:
            if isinstance(budget, list):  # Handle case where budget is a list
                budget = budget[0]

            properties["Budget"] = {"select": budget_mapping.get(budget, {"name": budget})}

        
        if food:
            properties["Food"] = {
                "rich_text": [{"text": {"content": food}}]  # Correct rich_text format
            }
        
        if activities:
            properties["Activities"] = {
                "rich_text": [{"text": {"content": activities}}]  # Correct rich_text format
            }

        children = [
            {
                "object": "block",
                "type": "heading_3",  # Ensure you are using the correct block type
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Activities"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",  # Make sure it's a paragraph block
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": activities
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_3",  # Same for this block
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Food"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",  # And here as well
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": food
                            }
                        }
                    ]
                }
            }
        ]    
        
        # 📤 Create the activity in Notion
        new_page = client.pages.create(
            parent={"database_id": TRAVEL_DB_ID},
            properties=properties,
            children=children
        )
        
        print(f"✅ Successfully created activity: {location}")
        return new_page
        
    except Exception as e:
        print(f"❌ Error creating activity in Notion: {str(e)}")
        return None