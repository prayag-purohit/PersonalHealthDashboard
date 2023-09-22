import myfitnesspal
from datetime import datetime, timedelta
import pandas as pd
import ctypes

client = myfitnesspal.Client()
today = datetime.now().date()

def show_popup_message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)

def get_dates(start_date, end_date):
    ndays = (end_date - start_date).days
    return [start_date + timedelta(i) for i in range(ndays + 1)]


if today.weekday() == 6:  # Sunday
    r_start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    r_end_date = today.strftime("%Y-%m-%d")
else:
    r_start_date = input("Please enter start date in YYYY-M-D format: ")
    r_end_date = input("Please enter end date in YYYY-M-D format: ")
    if r_end_date == '':
        r_end_date = r_start_date

        
start_date = datetime.strptime(r_start_date, "%Y-%m-%d").date()
end_date = datetime.strptime(r_end_date, "%Y-%m-%d").date()
dates = get_dates(start_date, end_date)

#try:
df = pd.DataFrame(data=None, columns=['date', 'mealname', 'calories', 'carbohydrates', 'fat', 'protein', 'sodium', 'sugar'])
data = []
for dt in dates:
    L_date = dt
    day = client.get_date(dt)
    for i in range(3):
        mealname, nutrient_values = str(day.meals[i]).split(' ', 1)
        nutrient_dict = eval(nutrient_values)
        
        meal_data = {
            'date': L_date.strftime("%d-%m-%Y"),
            'mealname': mealname,
            'calories': nutrient_dict.get('calories', None),
            'carbohydrates': nutrient_dict.get('carbohydrates', None),
            'fat': nutrient_dict.get('fat', None),
            'protein': nutrient_dict.get('protein', None),
            'sodium': nutrient_dict.get('sodium', None),
            'sugar': nutrient_dict.get('sugar', None),
            'date_extracted': datetime.now()}
        
        data.append(meal_data)
        df = pd.concat([df, pd.DataFrame(data)])
#except Exception as e: 
 #   error_message = "An error occured while running MFP script, try logging in through the browser"
 #   show_popup_message("Error", error_message)

directory_path = 'C:/Users/praya/OneDrive/Desktop/Personal Health Dashboard/mfpDATA python API/Data_exports/'
df.to_csv(directory_path + 'mega_nutrition_data.csv', mode="a",header=False ,index=False)
df.to_csv(directory_path + f"{start_date} - {end_date} nutrition data.csv", mode = 'w',index=False)
print("run complete")

