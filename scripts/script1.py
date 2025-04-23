from utils.google_sheets import get_unsent_leads, update_status
from utils.message_sender import setup_driver, send_message
import random

messages = [
    "Hi {name}, I build premium websites. Interested in boosting your business online?",
    "Hey {name}, need a clean, fast website for your brand?",
    "Hello {name}, want a professional site that brings clients? Let's talk!"
]

driver = setup_driver()
leads = get_unsent_leads()

if not leads:
    print("🟡 No leads found to message.")
else:
    for row_num, lead in leads:
        try:
            name = lead.get('Brand Name', 'there')
            number = str(lead['Number']).replace("+", "").replace(" ", "").replace("-", "")
            message = random.choice(messages).format(name=name)

            if send_message(driver, number, message):
                update_status(row_num, "Sent")
            else:
                update_status(row_num, "Failed")
        except Exception as e:
            print(f"🔥 Error on row {row_num}: {e}")
            update_status(row_num, "Error")

input("✅ Done! Press Enter to close browser...")
driver.quit()
