import pandas as pd

# القائمة الرسمية المعتمدة في الكود عندك
official_cities = [
    "Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", 
    "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", 
    "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", 
    "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", 
    "New Valley", "Matrouh", "North Sinai", "South Sinai"
]

# توزيع أوردرات تقريبي للمحافظات الجديدة
avg_orders = [
    150, 120, 140, 110, 100, 95, 90, 105, 95, 80, 75, 
    85, 80, 82, 70, 75, 78, 82, 76, 72, 65, 60, 55, 
    45, 50, 40, 35
]

df_updated = pd.DataFrame({
    'city': official_cities,
    'avg_daily_orders': avg_orders
})

# حفظ الملف الجديد
df_updated.to_csv('orders_data.csv', index=False)
print("✅ تم تحديث ملف orders_data.csv بالأسماء الرسمية المطابقة للكود!")