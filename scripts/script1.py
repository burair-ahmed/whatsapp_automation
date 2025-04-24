from utils.google_sheets import get_unsent_leads, update_status, get_sheet
from utils.message_sender import setup_driver, send_message
import random

messages = [
    "Hi {name}, I am Testing my Whatsapp Automation. I build premium websites. Interested in boosting your business online?",
    "Hey {name}, I am Testing my Whatsapp Automation. Need a clean, fast website for your brand?",
    "Hello {name}, I am Testing my Whatsapp Automation. Want a professional site that brings clients? Let's talk!"
]

driver = setup_driver()
leads = get_unsent_leads()

if not leads:
    print("🟡 No leads found to message.")
else:
    sheet = get_sheet()

    for row_num, lead in leads:
        try:
            name = lead.get('Name', 'there')
            business_type = lead.get('Niche', 'business')
            city = lead.get('City', 'your city')
            number = str(lead['Number']).replace("+", "").replace(" ", "").replace("-", "")

            msg_index = random.randint(0, len(messages) - 1)
            message_template = messages[msg_index]
            message = message_template.format(
                name=name,
                business_type=business_type,
                city=city
            )



            if send_message(driver, number, message):
                update_status(row_num, "Sent")
            else:
                update_status(row_num, "Failed")
                
            sheet.update_cell(row_num, 6, msg_index + 1)
                
        except Exception as e:
            print(f"🔥 Error on row {row_num}: {e}")
            update_status(row_num, "Error")

input("✅ Done! Press Enter to close browser...")
driver.quit()
