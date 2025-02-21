import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
TRAVEL_DB_ID = os.getenv("TRAVEL_DB_ID")

client = Client(auth=NOTION_API_KEY)


async def write_activity(destination, local_timezone,language, currency, landscape_types, best_months_to_visit, budget, visa_requirements, health_requirements, food, activities, cover_image):

    properties = {}
    budget_mapping = {'€€€': {'name': '€€€', 'id': 'iBKY'}, '€€': {'name': '€€', 'id': 'uKer'}, '€': {'name': '€', 'id': 'WqyF'}}

    
    try:
        
        # Add optional properties if provided
        if destination:
            properties["Destination"] = {
                "title": [{"text": {"content": destination}}]  # Correct title format
            }

        if local_timezone:
            properties["Local Timezone"] = {
                "rich_text": [{"text": {"content": local_timezone}}]  # Currency as text field
            }
        
        if language:
            # Split the language string by comma and strip spaces
            language_list = [lang.strip() for lang in language.split(",")]

            # Create the multi_select format for Notion
            properties["Language"] = {
                "multi_select": [{"name": lang} for lang in language_list]
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

        if visa_requirements:
            properties["Visa Requirements"] = {
                "rich_text": [{"text": {"content": visa_requirements}}]  # Correct rich_text format
            }

        if health_requirements:
            properties["Health Requirements"] = {
                "rich_text": [{"text": {"content": health_requirements}}]  # Correct rich_text format
            }
        
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
                "type": "heading_3",  # Same for this block
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "🛂 Visa Requirements"
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
                                "content": visa_requirements
                            }
                        }
                    ]
                }
            },{
                "object": "block",
                "type": "heading_3",  # Same for this block
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "💉 Health Requirements"
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
                                "content": health_requirements
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_3",  # Ensure you are using the correct block type
                "heading_3": {"rich_text": [{"type": "text","text": {"content": "🏞️ Activities"}}
                    ]
                }
            },
               {
                "object": "block",
                "type": "paragraph",  # And here as well
                "paragraph": {"rich_text": [{ "type": "text", "text": {"content": activities}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",  # Ensure you are using the correct block type
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "🥘 Food"}}]
                }
            },
               {
                "object": "block",
                "type": "paragraph",  # And here as well
                "paragraph": {
                    "rich_text": [{"type": "text","text": {"content": food}}]
                }
            }
        ]    
        
        # 📤 Create the activity in Notion
        new_page = client.pages.create(
            parent={"database_id": TRAVEL_DB_ID},
            properties=properties,
            children=children
        )

        # 🌟 Add the cover image (if provided)
        if cover_image:
            page_id = new_page["id"]
            client.pages.update(
                page_id=page_id,
                cover={"type": "external", "external": {"url": cover_image}}
            )
        
        print(f"✅ Successfully created activity: {destination}")
        return new_page
        
    except Exception as e:
        print(f"❌ Error creating activity in Notion: {str(e)}")
        return None