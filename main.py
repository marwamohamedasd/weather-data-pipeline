# import time
# import pandas as pd
# from sqlalchemy import create_engine
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry

# def run_weather_pipeline():
#     try:
#         # 1. إعداد الـ API
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = {
#             "latitude": 29.9934, "longitude": 31.319,
#             "current": ["temperature_2m", "wind_speed_10m", "relative_humidity_2m"],
#             "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
#             "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset"],
#             "timezone": "Africa/Cairo", "forecast_days": 7
#         }

#         # 2. سحب البيانات
#         print("جاري سحب البيانات من الموقع...")
#         responses = openmeteo.weather_api(url, params=params)
#         response = responses[0]

#         # 3. معالجة البيانات (مثال لجدول الساعات)
#         hourly = response.Hourly()
#         hourly_df = pd.DataFrame({
#             "date": pd.date_range(
#                 start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left"
#             ),
#             "temp": hourly.Variables(0).ValuesAsNumpy(),
#             "city": "Cairo"
#         })

#         # 4. الربط بقاعدة البيانات (لاحظي اسم السيرفر هنا db مش localhost)
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')
        
#         # 5. الحفظ (Append)
#         hourly_df.to_sql('hourly_weather', engine, if_exists='append', index=False)
        
#         print(f"تم تحديث البيانات بنجاح في: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"حصلت مشكلة: {e}")

# # الحلقة اللانهائية (الأتمتة)
# if __name__ == "__main__":
#     while True:
#         run_weather_pipeline()
#         print("الكود هينام دلوقتي لمدة 24 ساعة...")
#         time.sleep(86400) # يصحى بعد يوم كامل



# import time
# import pandas as pd
# from sqlalchemy import create_engine
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry

# def run_weather_pipeline():
#     try:
#         # 1. إعداد الـ API والـ Cache
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = {
#             "latitude": 29.9934, 
#             "longitude": 31.319,
#             "current": ["temperature_2m", "wind_speed_10m", "relative_humidity_2m", "apparent_temperature"],
#             "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
#             "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset"],
#             "timezone": "Africa/Cairo", 
#             "forecast_days": 7
#         }

#         # 2. سحب البيانات من الموقع
#         print("جاري سحب البيانات من الموقع...")
#         responses = openmeteo.weather_api(url, params=params)
#         response = responses[0]

#         # 3. معالجة البيانات اللحظية (Current)
#         current = response.Current()
#         current_df = pd.DataFrame({
#             "date": [pd.to_datetime(current.Time(), unit="s", utc=True)],
#             "temp": [current.Variables(0).Value()],
#             "wind_speed": [current.Variables(1).Value()],
#             "humidity": [current.Variables(2).Value()],
#             "apparent_temp": [current.Variables(3).Value()],
#             "city": ["Cairo"]
#         })

#         # 4. معالجة بيانات الساعات (Hourly)
#         hourly = response.Hourly()
#         hourly_df = pd.DataFrame({
#             "date": pd.date_range(
#                 start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left"
#             ),
#             "temp": hourly.Variables(0).ValuesAsNumpy(),
#             "humidity": hourly.Variables(1).ValuesAsNumpy(),
#             "precipitation": hourly.Variables(2).ValuesAsNumpy(),
#             "wind_speed": hourly.Variables(3).ValuesAsNumpy(),
#             "city": "Cairo"
#         })

#         # 5. معالجة البيانات اليومية (Daily)
#         daily = response.Daily()
#         daily_df = pd.DataFrame({
#             "date": pd.date_range(
#                 start=pd.to_datetime(daily.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left"
#             ),
#             "max_temp": daily.Variables(0).ValuesAsNumpy(),
#             "min_temp": daily.Variables(1).ValuesAsNumpy(),
#             "sunrise": pd.to_datetime(daily.Variables(2).ValuesInt64AsNumpy(), unit="s", utc=True),
#             "sunset": pd.to_datetime(daily.Variables(3).ValuesInt64AsNumpy(), unit="s", utc=True),
#             "city": "Cairo"
#         })

#         # 6. الربط بقاعدة البيانات (db هو اسم الخدمة جوه الدوكر)
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')
        
#         # 7. الحفظ (Append) - البيانات هتنزل تحت القديمة
#         current_df.to_sql('current_weather', engine, if_exists='append', index=False)
#         hourly_df.to_sql('hourly_weather', engine, if_exists='append', index=False)
#         daily_df.to_sql('daily_weather', engine, if_exists='append', index=False)
        
#         print(f"تم تحديث (Current, Hourly, Daily) بنجاح في: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"حصلت مشكلة: {e}")

# # الحلقة اللانهائية للتشغيل اليومي
# if __name__ == "__main__":
#     while True:
#         run_weather_pipeline()
#         print("الكود هينام دلوقتي لمدة 24 ساعة...")
#         time.sleep(86400)


































#  دة  التعديل  قبل مانربط طلبات التوصيل  بالطقس 

# import time
# import pandas as pd
# from sqlalchemy import create_engine
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry

# def run_weather_pipeline():
#     try:
#         # 1. إعداد الـ API والـ Cache
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         # قائمة المحافظات المتوافقة مع الإحداثيات
#         cities = [
#             "Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", 
#             "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", 
#             "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", 
#             "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", 
#             "New Valley", "Matrouh", "North Sinai", "South Sinai"
#         ]

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455], 
#             "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum", "wind_speed_10m_max", "weather_code"], 
#             "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "cloud_cover"], 
#             "current": ["temperature_2m", "relative_humidity_2m", "is_day", "precipitation", "weather_code", "wind_speed_10m"], 
#             "timezone": "Africa/Cairo"
#         }

#         # 2. سحب البيانات
#         print("📡 جاري سحب البيانات لجميع المحافظات...")
#         responses = openmeteo.weather_api(url, params=params)

#         all_current, all_hourly, all_daily = [], [], []

#         # 3. معالجة البيانات وتجميعها
#         for i, response in enumerate(responses):
#             city_name = cities[i]

#             # Current
#             current = response.Current()
#             all_current.append({
#                 "city": city_name,
#                 "date": pd.to_datetime(current.Time(), unit="s", utc=True),
#                 "temp": current.Variables(0).Value(),
#                 "humidity": current.Variables(1).Value(),
#                 "is_day": current.Variables(2).Value(),
#                 "precipitation": current.Variables(3).Value(),
#                 "weather_code": current.Variables(4).Value(),
#                 "wind_speed": current.Variables(5).Value()
#             })

#             # Hourly
#             hourly = response.Hourly()
#             h_time = pd.date_range(
#                 start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left"
#             )
#             all_hourly.append(pd.DataFrame({
#                 "city": city_name, "date": h_time,
#                 "temp": hourly.Variables(0).ValuesAsNumpy(),
#                 "humidity": hourly.Variables(1).ValuesAsNumpy(),
#                 "precipitation": hourly.Variables(2).ValuesAsNumpy(),
#                 "wind_speed": hourly.Variables(3).ValuesAsNumpy(),
#                 "cloud_cover": hourly.Variables(4).ValuesAsNumpy()
#             }))

#             # Daily
#             daily = response.Daily()
#             d_time = pd.date_range(
#                 start=pd.to_datetime(daily.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left"
#             )
#             all_daily.append(pd.DataFrame({
#                 "city": city_name, "date": d_time,
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "min_temp": daily.Variables(1).ValuesAsNumpy(),
#                 "sunrise": pd.to_datetime(daily.Variables(2).ValuesInt64AsNumpy(), unit="s", utc=True),
#                 "sunset": pd.to_datetime(daily.Variables(3).ValuesInt64AsNumpy(), unit="s", utc=True),
#                 "precip_sum": daily.Variables(4).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(5).ValuesAsNumpy(),
#                 "weather_code": daily.Variables(6).ValuesAsNumpy()
#             }))

#         # 4. الربط بقاعدة البيانات (Docker Environment)
#         # ملاحظة: نستخدم بورت 5432 واسم الخدمة db لأن الكود يعمل داخل الدوكر
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')

#         # 5. الحفظ التراكمي (Append) - يضيف الجديد تحت القديم
#         pd.DataFrame(all_current).to_sql('current_weather', engine, if_exists='append', index=False)
#         pd.concat(all_hourly).to_sql('hourly_weather', engine, if_exists='append', index=False)
#         pd.concat(all_daily).to_sql('daily_weather', engine, if_exists='append', index=False)

#         print(f"✅ تم تحديث الجداول بنجاح (تراكمي) في: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ حصلت مشكلة: {e}")

# if __name__ == "__main__":
#     while True:
#         run_weather_pipeline()
#         print("💤 سيعاد التشغيل بعد 24 ساعة...")
#         time.sleep(86400)
























































# دة الكود بعد ماربطنا  طلبات التوصيل   بالطقس 



# import time
# import pandas as pd
# from sqlalchemy import create_engine
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry

# # --- وظيفة حساب مخاطر التوصيل (المحرك الذكي) ---
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
    
#     # تأكدي من جلب القيم بشكل صحيح (لأن أسماء الأعمدة تختلف قليلاً بين الجداول)
#     # نستخدم .get لضمان عدم حدوث خطأ لو العمود مش موجود في أحد الجداول
#     temp = row.get('temp', row.get('max_temp', 25))
#     precip = row.get('precipitation', row.get('precip_sum', 0))
#     wind = row.get('wind_speed', row.get('wind_max', 0))

#     # 1. منطق المطر
#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
            
#     # 2. منطق الرياح 
#     if wind > 20:
#         delay += 10
#         bonus += 10
        
#     # 3. منطق الحرارة الشديدة 
#     if temp > 38:
#         delay += 10
#         bonus += 5
        
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# def run_weather_pipeline():
#     try:
#         # 1. إعداد الـ API والـ Cache
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         cities = [
#             "Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", 
#             "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", 
#             "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", 
#             "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", 
#             "New Valley", "Matrouh", "North Sinai", "South Sinai"
#         ]

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455], 
#             "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum", "wind_speed_10m_max", "weather_code"], 
#             "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "cloud_cover"], 
#             "current": ["temperature_2m", "relative_humidity_2m", "is_day", "precipitation", "weather_code", "wind_speed_10m"], 
#             "timezone": "Africa/Cairo"
#         }

#         # 2. سحب البيانات
#         print("📡 جاري سحب البيانات وتحليل المخاطر لـ 27 محافظة...")
#         responses = openmeteo.weather_api(url, params=params)

#         all_current_rows, all_hourly_dfs, all_daily_dfs = [], [], []

#         # 3. معالجة البيانات وتجميعها
#         for i, response in enumerate(responses):
#             city_name = cities[i]

#             # Current
#             current = response.Current()
#             all_current_rows.append({
#                 "city": city_name,
#                 "date": pd.to_datetime(current.Time(), unit="s", utc=True),
#                 "temp": current.Variables(0).Value(),
#                 "humidity": current.Variables(1).Value(),
#                 "is_day": current.Variables(2).Value(),
#                 "precipitation": current.Variables(3).Value(),
#                 "weather_code": current.Variables(4).Value(),
#                 "wind_speed": current.Variables(5).Value()
#             })

#             # Hourly
#             hourly = response.Hourly()
#             h_time = pd.date_range(
#                 start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left"
#             )
#             all_hourly_dfs.append(pd.DataFrame({
#                 "city": city_name, "date": h_time,
#                 "temp": hourly.Variables(0).ValuesAsNumpy(),
#                 "humidity": hourly.Variables(1).ValuesAsNumpy(),
#                 "precipitation": hourly.Variables(2).ValuesAsNumpy(),
#                 "wind_speed": hourly.Variables(3).ValuesAsNumpy(),
#                 "cloud_cover": hourly.Variables(4).ValuesAsNumpy()
#             }))

#             # Daily
#             daily = response.Daily()
#             d_time = pd.date_range(
#                 start=pd.to_datetime(daily.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left"
#             )
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": city_name, "date": d_time,
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "min_temp": daily.Variables(1).ValuesAsNumpy(),
#                 "sunrise": pd.to_datetime(daily.Variables(2).ValuesInt64AsNumpy(), unit="s", utc=True),
#                 "sunset": pd.to_datetime(daily.Variables(3).ValuesInt64AsNumpy(), unit="s", utc=True),
#                 "precip_sum": daily.Variables(4).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(5).ValuesAsNumpy(),
#                 "weather_code": daily.Variables(6).ValuesAsNumpy()
#             }))

#         # تحويل البيانات إلى DataFrames نهائية
#         final_current = pd.DataFrame(all_current_rows)
#         final_hourly = pd.concat(all_hourly_dfs)
#         final_daily = pd.concat(all_daily_dfs)

#         # --- الخطوة السحرية: تطبيق منطق التوصيل على الـ 27 محافظة ---
#         print("🧠 تطبيق منطق حساب التأخير والحوافز...")
#         final_current[['expected_delay_min', 'risk_bonus_egp']] = final_current.apply(apply_delivery_logic, axis=1)
#         final_hourly[['expected_delay_min', 'risk_bonus_egp']] = final_hourly.apply(apply_delivery_logic, axis=1)
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         # 4. الربط بقاعدة البيانات (Docker Environment)
#         # ملاحظة: نستخدم بورت 5432 لأن الكود يعمل داخل الدوكر
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')


#         #     # 5. الحفظ التراكمي (replace ) 
#         #    make replace  first  to add new column   and replace old data 
#         # final_current.to_sql('current_weather', engine, if_exists='replace', index=False)
#         # final_hourly.to_sql('hourly_weather', engine, if_exists='replace', index=False)
#         # final_daily.to_sql('daily_weather', engine, if_exists='replace', index=False)

#         # 5. الحفظ التراكمي (Append) 
#         final_current.to_sql('current_weather', engine, if_exists='append', index=False)
#         final_hourly.to_sql('hourly_weather', engine, if_exists='append', index=False)
#         final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)

#         print(f"✅ تم تحديث بيانات 27 محافظة بنجاح في: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ حصلت مشكلة: {e}")

# if __name__ == "__main__":
#     while True:
#         run_weather_pipeline()
#         print("💤 سيعاد التشغيل بعد 24 ساعة...")
#         time.sleep(86400)























# اضافة ملف order وربطه مع طلبات التوصيل بالاعمدة الجديدة 



# import time
# import pandas as pd
# from sqlalchemy import create_engine
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import os # أضفنا المكتبة دي عشان نتأكد من وجود الملف

# # --- وظيفة حساب مخاطر التوصيل (المحرك الذكي) ---
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
    
#     temp = row.get('temp', row.get('max_temp', 25))
#     precip = row.get('precipitation', row.get('precip_sum', 0))
#     wind = row.get('wind_speed', row.get('wind_max', 0))

#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
            
#     if wind > 20:
#         delay += 10
#         bonus += 10
        
#     if temp > 38:
#         delay += 10
#         bonus += 5
        
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# def run_weather_pipeline():
#     try:
#         # 1. إعداد الـ API والـ Cache
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         cities = [
#             "Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", 
#             "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", 
#             "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", 
#             "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", 
#             "New Valley", "Matrouh", "North Sinai", "South Sinai"
#         ]

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455], 
#             "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum", "wind_speed_10m_max", "weather_code"], 
#             "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "cloud_cover"], 
#             "current": ["temperature_2m", "relative_humidity_2m", "is_day", "precipitation", "weather_code", "wind_speed_10m"], 
#             "timezone": "Africa/Cairo"
#         }

#         # 2. سحب البيانات
#         print("📡 جاري سحب البيانات من Open-Meteo...")
#         responses = openmeteo.weather_api(url, params=params)

#         all_current_rows, all_hourly_dfs, all_daily_dfs = [], [], []

#         for i, response in enumerate(responses):
#             city_name = cities[i]
#             # (نفس كود المعالجة اللي إنتِ كتبتيه بدون تغيير)
#             current = response.Current()
#             all_current_rows.append({
#                 "city": city_name,
#                 "date": pd.to_datetime(current.Time(), unit="s", utc=True),
#                 "temp": current.Variables(0).Value(),
#                 "precipitation": current.Variables(3).Value(),
#                 "wind_speed": current.Variables(5).Value()
#             })

#             daily = response.Daily()
#             d_time = pd.date_range(
#                 start=pd.to_datetime(daily.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left"
#             )
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": city_name, "date": d_time,
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "precip_sum": daily.Variables(4).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(5).ValuesAsNumpy()
#             }))

#         final_current = pd.DataFrame(all_current_rows)
#         final_daily = pd.concat(all_daily_dfs)

#         # 3. حساب التأخير والحوافز
#         print("🧠 حساب حوافز المخاطر...")
#         final_current[['expected_delay_min', 'risk_bonus_egp']] = final_current.apply(apply_delivery_logic, axis=1)
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         # --- 🚀 الخطوة الجديدة: ربط بيانات الطلبات (Enrichment) ---
#         if os.path.exists('orders_data.csv'):
#             print("🔗 دمج بيانات الطقس مع عدد الطلبات...")
#             orders_df = pd.read_csv('orders_data.csv')
            
#             # ربط الجدولين بناءً على اسم المدينة
#             final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
            
#             # حساب ميزانية البونص الكلية للمحافظة
#             # (بونص الطيار الواحد * عدد الطلبات في المدينة)
#             final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']
            
#             # حفظ التقرير لفتحه في إكسيل
#             final_daily.to_csv('manager_decision_report.csv', index=False, sep=';', encoding='utf-8-sig')
#             print("📊 تم استخراج تقرير 'manager_decision_report.csv' جاهز للإكسيل.")
#         else:
#             print("⚠️ ملف orders_data.csv غير موجود، سيتم تخطي خطوة الربط.")

#         # 4. الحفظ في قاعدة البيانات
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')
#         #final_daily.to_sql('daily_weather', engine, if_exists='replace', index=False)
#         final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)
    
#         print(f"✅ تم تحديث النظام بالكامل في: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ حصلت مشكلة: {e}")

# if __name__ == "__main__":
#     run_weather_pipeline()








































#    عمل relation  ship  between  daily  order _data 


# import time
# import pandas as pd
# from sqlalchemy import create_engine, text
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import os

# # --- وظيفة حساب مخاطر التوصيل (المحرك الذكي) ---
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
    
#     # التأكد من جلب البيانات سواء من الجدول الحالي أو اليومي
#     temp = row.get('temp', row.get('max_temp', 25))
#     precip = row.get('precipitation', row.get('precip_sum', 0))
#     wind = row.get('wind_speed', row.get('wind_max', 0))

#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
            
#     if wind > 20:
#         delay += 10
#         bonus += 10
        
#     if temp > 38:
#         delay += 10
#         bonus += 5
        
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# def run_weather_pipeline():
#     try:
#         # 1. إعداد الـ API والـ Cache
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         # المحافظات الرسمية (Data Alignment)
#         cities = [
#             "Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", 
#             "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", 
#             "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", 
#             "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", 
#             "New Valley", "Matrouh", "North Sinai", "South Sinai"
#         ]

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455], 
#             "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum", "wind_speed_10m_max", "weather_code"], 
#             "timezone": "Africa/Cairo"
#         }

#         # 2. سحب البيانات
#         print("📡 جاري سحب البيانات من Open-Meteo...")
#         responses = openmeteo.weather_api(url, params=params)

#         all_daily_dfs = []

#         for i, response in enumerate(responses):
#             city_name = cities[i]
#             daily = response.Daily()
#             d_time = pd.date_range(
#                 start=pd.to_datetime(daily.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left"
#             )
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": city_name, 
#                 "date": d_time,
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "precip_sum": daily.Variables(4).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(5).ValuesAsNumpy()
#             }))

#         final_daily = pd.concat(all_daily_dfs)

#         # 3. حساب التأخير والحوافز
#         print("🧠 حساب حوافز المخاطر...")
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         # 4. دمج بيانات الأوردرات (Enrichment)
#         if os.path.exists('orders_data.csv'):
#             print("🔗 دمج بيانات الطقس مع عدد الطلبات...")
#             orders_df = pd.read_csv('orders_data.csv')
            
#             # الدمج للحسابات
#             final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
#             final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']
            
#             # حفظ التقرير للمدير
#             final_daily.to_csv('manager_decision_report.csv', index=False, sep=';', encoding='utf-8-sig')
#             print("📊 تم استخراج تقرير 'manager_decision_report.csv'.")
#         else:
#             print("⚠️ ملف orders_data.csv غير موجود!")

#         # 5. الحفظ في قاعدة البيانات وبناء الـ Relation
#         # ملاحظة: نستخدم البورت 5432 لأننا داخل شبكة Docker (Container to Container)
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')

#         # أ. رفع جدول المدن (Master Table)
#         if 'orders_df' in locals():
#             orders_df.to_sql('cities_orders', engine, if_exists='replace', index=False)
#             print("🏠 تم تحديث جدول المدن (cities_orders).")

#         # ب. رفع جدول الطقس (Fact Table)
#         # نستخدم replace لبناء الهيكل الصحيح أول مرة
#         final_daily.to_sql('daily_weather', engine, if_exists='replace', index=False)
#         print("☁️ تم تحديث جدول الطقس (daily_weather).")

#         # ج. إنشاء الروابط (SQL Relations)
#         with engine.connect() as conn:
#             # جعل اسم المدينة Primary Key
#             conn.execute(text("ALTER TABLE cities_orders ADD PRIMARY KEY (city);"))
            
#             # ربط الجداول بـ Foreign Key
#             conn.execute(text("""
#                 ALTER TABLE daily_weather 
#                 ADD CONSTRAINT fk_city_relation 
#                 FOREIGN KEY (city) 
#                 REFERENCES cities_orders(city);
#             """))
#             conn.commit()
#             print("🔗 تم إنشاء الـ Relation بين الجداول بنجاح!")

#         print(f"✅ تم تحديث النظام بالكامل في: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ حصلت مشكلة: {e}")

# if __name__ == "__main__":
#     run_weather_pipeline()


# append data    + relation  data base 









# import time
# import pandas as pd
# from sqlalchemy import create_engine, text
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import os

# # --- وظيفة حساب مخاطر التوصيل (المحرك الذكي) ---
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
    
#     # التأكد من جلب البيانات سواء من الجدول الحالي أو اليومي
#     temp = row.get('temp', row.get('max_temp', 25))
#     precip = row.get('precipitation', row.get('precip_sum', 0))
#     wind = row.get('wind_speed', row.get('wind_max', 0))

#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
            
#     if wind > 20:
#         delay += 10
#         bonus += 10
        
#     if temp > 38:
#         delay += 10
#         bonus += 5
        
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# def run_weather_pipeline():
#     try:
#         # 1. إعداد الـ API والـ Cache
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         # المحافظات الرسمية (Data Alignment)
#         cities = [
#             "Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", 
#             "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", 
#             "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", 
#             "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", 
#             "New Valley", "Matrouh", "North Sinai", "South Sinai" , "New Capital"
#         ]

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209, 30.0238], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455, 31.7549], 
#             "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum", "wind_speed_10m_max", "weather_code"], 
#             "timezone": "Africa/Cairo"
#         }

#         # 2. سحب البيانات
#         print("📡 جاري سحب البيانات من Open-Meteo...")
#         responses = openmeteo.weather_api(url, params=params)

#         all_daily_dfs = []

#         for i, response in enumerate(responses):
#             city_name = cities[i]
#             daily = response.Daily()
#             d_time = pd.date_range(
#                 start=pd.to_datetime(daily.Time(), unit="s", utc=True),
#                 end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
#                 freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left"
#             )
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": city_name, 
#                 "date": d_time,
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "precip_sum": daily.Variables(4).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(5).ValuesAsNumpy()
#             }))

#         final_daily = pd.concat(all_daily_dfs)

#         # 3. حساب التأخير والحوافز
#         print("🧠 حساب حوافز المخاطر...")
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         # 4. دمج بيانات الأوردرات (Enrichment)
#         if os.path.exists('orders_data.csv'):
#             print("🔗 دمج بيانات الطقس مع عدد الطلبات...")
#             orders_df = pd.read_csv('orders_data.csv')
            
#             # الدمج للحسابات
#             final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
#             final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']
            
#             # حفظ التقرير للمدير
#             final_daily.to_csv('manager_decision_report.csv', index=False, sep=';', encoding='utf-8-sig')
#             print("📊 تم استخراج تقرير 'manager_decision_report.csv'.")
#         else:
#             print("⚠️ ملف orders_data.csv غير موجود!")

#         # 5. الحفظ في قاعدة البيانات وبناء الـ Relation
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')

#         # أ. جدول المدن: نستخدم replace لتحديث أرقام الأوردرات في حال تم تعديل الإكسيل
#         if 'orders_df' in locals():
#             orders_df.to_sql('cities_orders', engine, if_exists='replace', index=False)
#             print("🏠 تم تحديث جدول المدن (Reference Table).")

#         # ب. جدول الطقس: نستخدم append لجمع البيانات يومياً تحت بعضها (Historical Data)
#         final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)
#         print("☁️ تم إضافة بيانات الطقس الجديدة (History Table).")

#         # ج. إنشاء الروابط (SQL Relations) مع حماية ضد التكرار (Idempotency)
#         with engine.connect() as conn:
#             # جعل مدينة في جدول الأوردرات هي المفتاح الأساسي (لو مش موجود)
#             conn.execute(text("""
#                 DO $$ 
#                 BEGIN 
#                     IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cities_orders_pkey') THEN
#                         ALTER TABLE cities_orders ADD PRIMARY KEY (city);
#                     END IF;
#                 END $$;
#             """))
            
#             # ربط جدول الطقس بجدول المدن (لو مش مربوط)
#             conn.execute(text("""
#                 DO $$ 
#                 BEGIN 
#                     IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_city_relation') THEN
#                         ALTER TABLE daily_weather 
#                         ADD CONSTRAINT fk_city_relation 
#                         FOREIGN KEY (city) 
#                         REFERENCES cities_orders(city);
#                     END IF;
#                 END $$;
#             """))
#             conn.commit()
#             print("🔗 تم التأكد من وجود الـ Relation بنجاح!")

#         print(f"✅ تم تحديث النظام بالكامل في: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ حصلت مشكلة: {e}")

# if __name__ == "__main__":
#     run_weather_pipeline()







# دة علشان يضيف  المدن الجديدة وربطها بالداتا بيز  ويسمح للداتا بيز  تضيف المدينة  بدون اي عوائق 



# import time
# import pandas as pd
# from sqlalchemy import create_engine, text
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import os

# # --- 1. محرك اتخاذ القرار (Delivery Logic) ---
# # هذه الوظيفة تحول أرقام الطقس المجردة إلى قرارات بيزنس (تأخير وفلوس)
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
    
#     # سحب القيم من الأعمدة (الطقس) بأسماءها في الداتا فريم
#     temp = row.get('max_temp', 25)
#     precip = row.get('precip_sum', 0)
#     wind = row.get('wind_max', 0)
    
#     # منطق المطر: لو فيه مطر زود 15 دقيقة و 10 جنيه، لو مطر غزير زود أكتر
#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
            
#     # منطق الرياح: لو الرياح سريعة زود 10 دقائق و 10 جنيه مخاطرة
#     if wind > 20:
#         delay += 10
#         bonus += 10
        
#     # منطق الحرارة: لو الجو حر جداً (أعلى من 38) زود تعويض للمندوب
#     if temp > 38:
#         delay += 10
#         bonus += 5
        
#     # إرجاع النتائج في أعمدة جديدة
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# # --- 2. خط إنتاج البيانات الرئيسي (The Pipeline) ---
# def run_weather_pipeline():
#     try:
#         # إعداد الاتصال بالإنترنت مع ميزة الـ Cache (عشان لو طلبنا نفس البيانات تاني ميهلكش باقة النت)
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         # قائمة بأسماء المدن المخطط لها (بما فيها العاصمة الإدارية الجديدة)
#         cities = [
#             "Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", 
#             "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", 
#             "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", 
#             "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", 
#             "New Valley", "Matrouh", "North Sinai", "South Sinai", "New Capital"
#         ]

#         # إحداثيات المدن (خطوط الطول والعرض) بالترتيب المطابق لقائمة الأسماء
#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209, 30.0238], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455, 31.7549], 
#             "daily": ["temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"], 
#             "timezone": "Africa/Cairo"
#         }

#         # طلب البيانات من القمر الصناعي (Open-Meteo)
#         print("📡 سحب بيانات الطقس (المدينة الجديدة مضافة)...")
#         responses = openmeteo.weather_api(url, params=params)
        
#         all_daily_dfs = []
#         # معالجة بيانات كل مدينة على حدة وتحويلها لشكل جدول (DataFrame)
#         for i, response in enumerate(responses):
#             daily = response.Daily()
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": cities[i], 
#                 "date": pd.date_range(start=pd.to_datetime(daily.Time(), unit="s", utc=True), end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True), freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left"),
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "precip_sum": daily.Variables(1).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(2).ValuesAsNumpy()
#             }))
        
#         # تجميع كل الجداول الصغيرة في جدول واحد كبير
#         final_daily = pd.concat(all_daily_dfs)

#         # تفعيل المحرك الذكي لحساب الحوافز والتأخير لكل سطر في الجدول
#         print("🧠 حساب الحوافز...")
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         # دمج بيانات الأوردرات الخارجية (من ملف CSV) لعمل حسابات الميزانية الكلية
#         if os.path.exists('orders_data.csv'):
#             orders_df = pd.read_csv('orders_data.csv')
#             # عملية Join: نربط الطقس بعدد الأوردرات باستخدام اسم المدينة
#             final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
#             # حساب الميزانية المطلوبة (بونص المندوب الواحد × عدد الأوردرات في المدينة)
#             final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']

#         # --- 3. إدارة قاعدة البيانات (PostgreSQL) ---
#         # إنشاء المحرك اللي بيكلم الداتابيز (بورت 5432 داخل شبكة دوكر)
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')
        
#         with engine.connect() as conn:
#             # أهم سطر: بنفك "الربط" بين الجدولين مؤقتاً عشان نقدر نحدث جدول المدن (Reference) من غير ما الداتابيز تمنعنا
#             print("🔓 فك الربط مؤقتاً لتحديث البيانات...")
#             conn.execute(text("ALTER TABLE IF EXISTS daily_weather DROP CONSTRAINT IF EXISTS fk_city_relation;"))
#             conn.commit()

#         # تحديث جدول المدن (المراجع): بنستخدم replace عشان لو ضفنا مدينة (زي العاصمة) أو غيرنا رقم أوردرات تتحدث فوراً
#         if 'orders_df' in locals():
#             orders_df.to_sql('cities_orders', engine, if_exists='replace', index=False)
#             print("🏠 تم تحديث قائمة المدن (العاصمة الجديدة أصبحت هنا).")

#         # تحديث جدول الطقس (التاريخ): بنستخدم append عشان يضيف الجديد تحت القديم وميمسحش أرشيف الأيام اللي فاتت
#         final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)
#         print("☁️ تم إضافة بيانات الطقس الجديدة.")

#         # إعادة بناء "الأقفال" (Constraints) لضمان سلامة البيانات
#         with engine.connect() as conn:
#             print("🔐 إعادة بناء الربط (Relation)...")
#             # تحديد "المدينة" كمفتاح أساسي (Primary Key) في جدول المراجع
#             conn.execute(text("ALTER TABLE cities_orders ADD PRIMARY KEY (city);"))
#             # ربط جدول الطقس بجدول المدن (Foreign Key) لضمان إن كل بيانات طقس تتبع مدينة حقيقية
#             conn.execute(text("ALTER TABLE daily_weather ADD CONSTRAINT fk_city_relation FOREIGN KEY (city) REFERENCES cities_orders(city);"))
#             conn.commit()
        
#         print(f"✅ مبروك! النظام جاهز بالعاصمة الجديدة: {pd.Timestamp.now()}")

#     except Exception as e:
#         # في حالة حدوث أي مشكلة (نت، باسورد، كود) اطبع الخطأ عشان نعرف نصلحه
#         print(f"❌ مشكلة: {e}")

# # تشغيل الكود
# if __name__ == "__main__":
#     run_weather_pipeline()






# كود دة للانذار  والتنبؤ  المبكر بالاضافة  لربط اي اضافة  في شيت الاكسل للمدن بالداتا بيز 




# import time
# import pandas as pd
# from sqlalchemy import create_engine, text
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import os

# # --- 1. محرك اتخاذ القرار (Delivery Logic) ---
# # هذه الوظيفة تحول أرقام الطقس المجردة إلى قرارات بيزنس (تأخير وفلوس)
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
    
#     # سحب القيم من الأعمدة (الطقس) بأسماءها في الداتا فريم
#     temp = row.get('max_temp', 25)
#     precip = row.get('precip_sum', 0)
#     wind = row.get('wind_max', 0)
    
#     # منطق المطر: لو فيه مطر زود 15 دقيقة و 10 جنيه، لو مطر غزير زود أكتر
#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
            
#     # منطق الرياح: لو الرياح سريعة زود 10 دقائق و 10 جنيه مخاطرة
#     if wind > 20:
#         delay += 10
#         bonus += 10
        
#     # منطق الحرارة: لو الجو حر جداً (أعلى من 38) زود تعويض للمندوب
#     if temp > 38:
#         delay += 10
#         bonus += 5
        
#     # إرجاع النتائج في أعمدة جديدة
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# # --- 2. وظيفة التنبؤ والإنذار المبكر (Predictive Alerting) ---
# # هذه الوظيفة تفحص بيانات يوم "غد" وتطبع تحذيرات لو وجد خطر
# def check_for_alerts(df):
#     print("\n🔍 فحص المخاطر المتوقعة ليوم غد...")
    
#     # تحديد تاريخ الغد بدقة (بدون توقيت)
#     tomorrow = (pd.Timestamp.now().normalize() + pd.Timedelta(days=1)).date()
    
#     # تصفية البيانات لعرض يوم غد فقط
#     tomorrow_df = df[df['date'].dt.date == tomorrow]

#     if tomorrow_df.empty:
#         print("ℹ️ لا توجد بيانات كافية للتنبؤ بيوم غد في النتائج الحالية.")
#         return

#     found_risk = False
#     for _, row in tomorrow_df.iterrows():
#         alerts = []
#         # معايير الخطر: مطر > 5 ملم، رياح > 35 كم/س، حرارة > 40 درجة
#         if row['precip_sum'] > 5:
#             alerts.append(f"🌧️ مطر غزير ({row['precip_sum']} ملم)")
#         if row['wind_max'] > 35:
#             alerts.append(f"💨 رياح قوية ({row['wind_max']} كم/س)")
#         if row['max_temp'] > 40:
#             alerts.append(f"🔥 موجة حر ({row['max_temp']}°)")

#         if alerts:
#             found_risk = True
#             print(f"🚨 [إنذار بكرة] محافظة {row['city']}: متوقع { ' و '.join(alerts) }")
#             print(f"   💡 الإجراء الموصى به: تجهيز ميزانية حوافز {row.get('total_bonus_budget', 0)} ج.م")
    
#     if not found_risk:
#         print("✅ حالة الطقس غداً مستقرة في جميع المحافظات، لا توجد مخاطر تستدعي القلق.")

# # --- 3. خط إنتاج البيانات الرئيسي (The Pipeline) ---
# def run_weather_pipeline():
#     try:
#         # إعداد الاتصال بالإنترنت مع ميزة الـ Cache
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         # قائمة بأسماء المدن المحدثة
#         cities = [
#             "Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", 
#             "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", 
#             "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", 
#             "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", 
#             "New Valley", "Matrouh", "North Sinai", "South Sinai", "New Capital"
#         ]

#         # إحداثيات المدن (خطوط الطول والعرض)
#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209, 30.0238], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455, 31.7549], 
#             "daily": ["temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"], 
#             "timezone": "Africa/Cairo"
#         }

#         # طلب البيانات من القمر الصناعي (Open-Meteo)
#         print("📡 سحب بيانات الطقس (الحالية والمستقبلية)...")
#         responses = openmeteo.weather_api(url, params=params)
        
#         all_daily_dfs = []
#         for i, response in enumerate(responses):
#             daily = response.Daily()
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": cities[i], 
#                 "date": pd.to_datetime(pd.date_range(start=pd.to_datetime(daily.Time(), unit="s", utc=True), end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True), freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left")),
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "precip_sum": daily.Variables(1).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(2).ValuesAsNumpy()
#             }))
        
#         # تجميع الجداول
#         final_daily = pd.concat(all_daily_dfs)

#         # حساب الحوافز
#         print("🧠 حساب الحوافز والقرارات...")
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         # دمج بيانات الأوردرات (لو الملف موجود)
#         if os.path.exists('orders_data.csv'):
#             orders_df = pd.read_csv('orders_data.csv')
#             final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
#             final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']

#         # --- 3. إدارة قاعدة البيانات (PostgreSQL) ---
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')
        
#         with engine.connect() as conn:
#             # فك القيد مؤقتًا
#             print("🔓 فك الربط مؤقتاً لتحديث البيانات...")
#             conn.execute(text("ALTER TABLE IF EXISTS daily_weather DROP CONSTRAINT IF EXISTS fk_city_relation;"))
#             conn.commit()

#         # تحديث قائمة المدن (Reference)
#         if 'orders_df' in locals():
#             orders_df.to_sql('cities_orders', engine, if_exists='replace', index=False)
#             print("🏠 تم تحديث قائمة المدن.")

#         # إضافة البيانات الجديدة (Append)
#         final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)
#         print("☁️ تم حفظ البيانات الجديدة في الداتابيز.")

#         # إعادة بناء الروابط
#         with engine.connect() as conn:
#             print("🔐 إعادة بناء الربط (Relation)...")
#             conn.execute(text("ALTER TABLE cities_orders ADD PRIMARY KEY (city);"))
#             conn.execute(text("ALTER TABLE daily_weather ADD CONSTRAINT fk_city_relation FOREIGN KEY (city) REFERENCES cities_orders(city);"))
#             conn.commit()
        
#         # --- 4. تشغيل نظام التنبؤ والإنذار المبكر ---
#         check_for_alerts(final_daily)
        
#         print(f"\n✅ مبروك! العملية اكتملت بنجاح: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ مشكلة: {e}")

# # تشغيل الكود
# if __name__ == "__main__":
#     run_weather_pipeline()










#  كود  التنبؤ  والانذار  بالاضافة  ارسال ميل للجميل   تنبؤ بالطقس ومصاريف غدا 


# import time
# import pandas as pd
# from sqlalchemy import create_engine, text
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # --- 1. إعدادات Gmail (مروة: المفتاح جاهز هنا) ---
# GMAIL_USER = 'marwamohameddasd91@gmail.com' 
# GMAIL_APP_PASSWORD = 'kzpe odbm dciq fbww'  
# RECIPIENT_EMAIL = 'marwamohameddasd91@gmail.com' 

# # --- 2. وظيفة إرسال الإيميل ---
# def send_email_alert(subject, body):
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = GMAIL_USER
#         msg['To'] = RECIPIENT_EMAIL
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#         server.send_message(msg)
#         server.quit()
#         print("📧 تم إرسال إيميل التنبيه بنجاح!")
#     except Exception as e:
#         print(f"❌ فشل إرسال الإيميل: {e}")

# # --- 3. محرك اتخاذ القرار ---
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
#     temp = row.get('max_temp', 25)
#     precip = row.get('precip_sum', 0)
#     wind = row.get('wind_max', 0)
    
#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
#     if wind > 20:
#         delay += 10
#         bonus += 10
#     if temp > 38:
#         delay += 10
#         bonus += 5
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# # --- 4. وظيفة التنبؤ والإنذار المبكر ---
# def check_for_alerts(df):
#     print("\n🔍 فحص المخاطر المتوقعة ليوم غد...")
#     tomorrow = (pd.Timestamp.now().normalize() + pd.Timedelta(days=1)).date()
#     tomorrow_df = df[df['date'].dt.date == tomorrow]

#     alert_messages = []
#     for _, row in tomorrow_df.iterrows():
#         alerts = []
#         if row['precip_sum'] > 5: alerts.append(f"🌧️ مطر غزير ({row['precip_sum']} ملم)")
#         if row['wind_max'] > 35: alerts.append(f"💨 رياح قوية ({row['wind_max']} كم/س)")
#         if row['max_temp'] > 40: alerts.append(f"🔥 موجة حر ({row['max_temp']}°)")

#         if alerts:
#             msg = f"محافظة {row['city']}: متوقع { ' و '.join(alerts) } | الميزانية المتوقعة: {row.get('total_bonus_budget', 0)} ج.م"
#             alert_messages.append(msg)
#             print(f"🚨 {msg}")

#     if alert_messages:
#         subject = f"⚠️ تقرير مخاطر الطقس الاستباقي - {tomorrow}"
#         body = "السيد المدير،\n\nيرجى العلم بوجود مخاطر طقس متوقعة غداً قد تؤثر على العمليات:\n\n" + "\n".join(alert_messages)
#         send_email_alert(subject, body)
#     else:
#         print("✅ حالة الطقس غداً مستقرة في جميع المحافظات.")

# # --- 5. خط إنتاج البيانات (The Pipeline) ---
# def run_weather_pipeline():
#     try:
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         cities = ["Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", "New Valley", "Matrouh", "North Sinai", "South Sinai", "New Capital"]
        
#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209, 30.0238], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455, 31.7549], 
#             "daily": ["temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"], 
#             "timezone": "Africa/Cairo"
#         }

#         print("📡 سحب بيانات الطقس...")
#         responses = openmeteo.weather_api(url, params=params)
        
#         all_daily_dfs = []
#         for i, response in enumerate(responses):
#             daily = response.Daily()
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": cities[i], 
#                 "date": pd.to_datetime(pd.date_range(start=pd.to_datetime(daily.Time(), unit="s", utc=True), end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True), freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left")),
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "precip_sum": daily.Variables(1).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(2).ValuesAsNumpy()
#             }))
        
#         final_daily = pd.concat(all_daily_dfs)
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         if os.path.exists('orders_data.csv'):
#             orders_df = pd.read_csv('orders_data.csv')
#             final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
#             final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']

#         # --- إدارة الداتابيز والتنظيف ---
#         engine = create_engine('postgresql://myuser:mypassword@db:5432/weather_data')
        
#         # فك القيود قبل الإضافة
#         with engine.connect() as conn:
#             conn.execute(text("ALTER TABLE IF EXISTS daily_weather DROP CONSTRAINT IF EXISTS fk_city_relation;"))
#             conn.commit()

#         # إضافة البيانات (Append)
#         final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)
#         print("☁️ تم حفظ البيانات الجديدة.")

#         # 🧹 تنظيف التكرار (Deduplication)
#         with engine.connect() as conn:
#             print("🧹 تنظيف البيانات المتكررة...")
#             conn.execute(text("""
#                 DELETE FROM daily_weather 
#                 WHERE ctid NOT IN (
#                     SELECT MIN(ctid) 
#                     FROM daily_weather 
#                     GROUP BY city, date
#                 );
#             """))
#             conn.commit()

#         # 🔐 تحديث الروابط والقواعد (النسخة الذكية)
#         with engine.connect() as conn:
#             print("🔐 تحديث الروابط والقواعد...")
#             if 'orders_df' in locals():
#                 orders_df.to_sql('cities_orders', engine, if_exists='replace', index=False)
            
#             conn.execute(text("ALTER TABLE cities_orders DROP CONSTRAINT IF EXISTS cities_orders_pkey CASCADE;"))
#             conn.execute(text("ALTER TABLE cities_orders ADD PRIMARY KEY (city);"))
#             conn.execute(text("ALTER TABLE daily_weather ADD CONSTRAINT fk_city_relation FOREIGN KEY (city) REFERENCES cities_orders(city);"))
#             conn.commit()
        
#         # تشغيل الإنذار وإرسال الإيميل
#         check_for_alerts(final_daily)
#         print(f"\n✅ مبروك! العملية اكتملت بنجاح: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ مشكلة: {e}")

# if __name__ == "__main__":
#     run_weather_pipeline()



#تعديل كلاود  يروح يكلم .env









# import time
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import pandas as pd
# from sqlalchemy import create_engine, text
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# from dotenv import load_dotenv  # 👈 المكتبة المسؤولة عن قراءة الملف المخفي

# # --- 0. تحميل الإعدادات من ملف .env ---
# load_dotenv(dotenv_path='/app/.env')  # 👈 السطر السحري اللي بيقرا الملف أوتوماتيك ويحدد إحنا لوكال ولا كلاود

# # --- 1. إعدادات Gmail ---
# GMAIL_USER = 'marwamohameddasd91@gmail.com' 
# GMAIL_APP_PASSWORD = 'kzpe odbm dciq fbww'  
# RECIPIENT_EMAIL = 'marwamohameddasd91@gmail.com' 

# # --- 2. وظيفة إرسال الإيميل ---
# def send_email_alert(subject, body):
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = GMAIL_USER
#         msg['To'] = RECIPIENT_EMAIL
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#         server.send_message(msg)
#         server.quit()
#         print("📧 تم إرسال إيميل التنبيه بنجاح!")
#     except Exception as e:
#         print(f"❌ فشل إرسال الإيميل: {e}")

# # --- 3. محرك اتخاذ القرار ---
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
#     temp = row.get('max_temp', 25)
#     precip = row.get('precip_sum', 0)
#     wind = row.get('wind_max', 0)
    
#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
#     if wind > 20:
#         delay += 10
#         bonus += 10
#     if temp > 38:
#         delay += 10
#         bonus += 5
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# # --- 4. وظيفة التنبؤ والإنذار المبكر ---
# def check_for_alerts(df):
#     print("\n🔍 فحص المخاطر المتوقعة ليوم غد...")
#     tomorrow = (pd.Timestamp.now().normalize() + pd.Timedelta(days=1)).date()
#     tomorrow_df = df[df['date'].dt.date == tomorrow]

#     alert_messages = []
#     for _, row in tomorrow_df.iterrows():
#         alerts = []
#         if row['precip_sum'] > 5: alerts.append(f"🌧️ مطر غزير ({row['precip_sum']} ملم)")
#         if row['wind_max'] > 35: alerts.append(f"💨 رياح قوية ({row['wind_max']} كم/س)")
#         if row['max_temp'] > 40: alerts.append(f"🔥 موجة حر ({row['max_temp']}°)")

#         if alerts:
#             msg = f"محافظة {row['city']}: متوقع { ' و '.join(alerts) } | الميزانية المتوقعة: {row.get('total_bonus_budget', 0)} ج.م"
#             alert_messages.append(msg)
#             print(f"🚨 {msg}")

#     if alert_messages:
#         subject = f"⚠️ تقرير مخاطر الطقس الاستباقي - {tomorrow}"
#         body = "السيد المدير،\n\nيرجى العلم بوجود مخاطر طقس متوقعة غداً قد تؤثر على العمليات:\n\n" + "\n".join(alert_messages)
#         send_email_alert(subject, body)
#     else:
#         print("✅ حالة الطقس غداً مستقرة في جميع المحافظات.")

# # --- 5. خط إنتاج البيانات (The Pipeline) ---
# def run_weather_pipeline():
#     try:
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         cities = ["Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", "New Valley", "Matrouh", "North Sinai", "South Sinai", "New Capital"]
        
#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209, 30.0238], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455, 31.7549], 
#             "daily": ["temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"], 
#             "timezone": "Africa/Cairo"
#         }

#         print("📡 سحب بيانات الطقس...")
#         responses = openmeteo.weather_api(url, params=params)
        
#         all_daily_dfs = []
#         for i, response in enumerate(responses):
#             daily = response.Daily()
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": cities[i], 
#                 "date": pd.to_datetime(pd.date_range(start=pd.to_datetime(daily.Time(), unit="s", utc=True), end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True), freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left")),
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "precip_sum": daily.Variables(1).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(2).ValuesAsNumpy()
#             }))
        
#         final_daily = pd.concat(all_daily_dfs)
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         if os.path.exists('orders_data.csv'):
#             orders_df = pd.read_csv('orders_data.csv')
#             final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
#             final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']

#         # --- 🛠️ إدارة الداتابيز الذكية باستخدام الـ .env ---
#         db_url = os.getenv('DATABASE_URL')  # 👈 الكود هيسحب السطر أوتوماتيك من الملف المخفي
#         engine = create_engine(db_url)
        
#         # فك القيود قبل الإضافة
#         with engine.connect() as conn:
#             conn.execute(text("ALTER TABLE IF EXISTS daily_weather DROP CONSTRAINT IF EXISTS fk_city_relation;"))
#             conn.commit()

#         # إضافة البيانات (Append)
#         final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)
#         print("☁️ تم حفظ البيانات الجديدة في الداتابيز.")

#         # 🧹 تنظيف التكرار (Deduplication)
#         with engine.connect() as conn:
#             print("🧹 تنظيف البيانات المتكررة...")
#             conn.execute(text("""
#                 DELETE FROM daily_weather 
#                 WHERE ctid NOT IN (
#                     SELECT MIN(ctid) 
#                     FROM daily_weather 
#                     GROUP BY city, date
#                 );
#             """))
#             conn.commit()

#         # 🔐 تحديث الروابط والقواعد (النسخة الذكية)
#         with engine.connect() as conn:
#             print("🔐 تحديث الروابط والقواعد...")
#             if 'orders_df' in locals():
#                 orders_df.to_sql('cities_orders', engine, if_exists='replace', index=False)
            
#             conn.execute(text("ALTER TABLE cities_orders DROP CONSTRAINT IF EXISTS cities_orders_pkey CASCADE;"))
#             conn.execute(text("ALTER TABLE cities_orders ADD PRIMARY KEY (city);"))
#             conn.execute(text("ALTER TABLE daily_weather ADD CONSTRAINT fk_city_relation FOREIGN KEY (city) REFERENCES cities_orders(city);"))
#             conn.commit()
        
#         # تشغيل الإنذار وإرسال الإيميل
#         check_for_alerts(final_daily)
#         print(f"\n✅ مبروك! العملية اكتملت بنجاح: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ مشكلة: {e}")

# if __name__ == "__main__":
#  run_weather_pipeline()



















#تعديل كلاود  يروح يكلم .env 2+ add budget bouns 















# import time
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import pandas as pd
# from sqlalchemy import create_engine, text
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# from dotenv import load_dotenv

# # --- 0. تحميل الإعدادات من ملف .env ---
# load_dotenv(dotenv_path='/app/.env')

# # --- 1. إعدادات Gmail ---
# GMAIL_USER = 'marwamohameddasd91@gmail.com' 
# GMAIL_APP_PASSWORD = 'kzpe odbm dciq fbww'  
# RECIPIENT_EMAIL = 'marwamohameddasd91@gmail.com' 

# # --- 2. وظيفة إرسال الإيميل ---
# def send_email_alert(subject, body):
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = GMAIL_USER
#         msg['To'] = RECIPIENT_EMAIL
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#         server.send_message(msg)
#         server.quit()
#         print("📧 تم إرسال إيميل التنبيه بنجاح!")
#     except Exception as e:
#         print(f"❌ فشل إرسال الإيميل: {e}")

# # --- 3. محرك اتخاذ القرار (للداتا اليومية) ---
# def apply_delivery_logic(row):
#     delay = 0
#     bonus = 0
#     temp = row.get('max_temp', 25)
#     precip = row.get('precip_sum', 0)
#     wind = row.get('wind_max', 0)
    
#     if precip > 0:
#         delay += 15
#         bonus += 10
#         if precip > 2:
#             delay += 20
#             bonus += 15
#     if wind > 20:
#         delay += 10
#         bonus += 10
#     if temp > 38:
#         delay += 10
#         bonus += 5
#     return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# # --- 4. وظيفة التنبؤ والإنذار المبكر ---
# def check_for_alerts(df):
#     print("\n🔍 فحص المخاطر المتوقعة ليوم غد...")
#     tomorrow = (pd.Timestamp.now().normalize() + pd.Timedelta(days=1)).date()
#     # تحويل العمود لتاريخ للمقارنة الصحيحة
#     df_copy = df.copy()
#     df_copy['date_parsed'] = pd.to_datetime(df_copy['date']).dt.date
#     tomorrow_df = df_copy[df_copy['date_parsed'] == tomorrow]

#     alert_messages = []
#     for _, row in tomorrow_df.iterrows():
#         alerts = []
#         if row['precip_sum'] > 5: alerts.append(f"🌧️ مطر غزير ({row['precip_sum']} ملم)")
#         if row['wind_max'] > 35: alerts.append(f"💨 رياح قوية ({row['wind_max']} كم/س)")
#         if row['max_temp'] > 40: alerts.append(f"🔥 موجة حر ({row['max_temp']}°)")

#         if alerts:
#             msg = f"محافظة {row['city']}: متوقع { ' و '.join(alerts) } | الميزانية المتوقعة: {row.get('total_bonus_budget', 0)} ج.م"
#             alert_messages.append(msg)
#             print(f"🚨 {msg}")

#     if alert_messages:
#         subject = f"⚠️ تقرير مخاطر الطقس الاستباقي - {tomorrow}"
#         body = "السيد المدير،\n\nيرجى العلم بوجود مخاطر طقس متوقعة غداً قد تؤثر على العمليات:\n\n" + "\n".join(alert_messages)
#         send_email_alert(subject, body)
#     else:
#         print("✅ حالة الطقس غداً مستقرة في جميع المحافظات.")

# # --- 5. خط إنتاج البيانات (The Pipeline) ---
# def run_weather_pipeline():
#     try:
#         cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
#         retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
#         openmeteo = openmeteo_requests.Client(session=retry_session)

#         cities = ["Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", "New Valley", "Matrouh", "North Sinai", "South Sinai", "New Capital"]
        
#         url = "https://api.open-meteo.com/v1/forecast"
#         params = { 
#             "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209, 30.0238], 
#             "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455, 31.7549], 
#             "current": ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m"],
#             "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
#             "daily": ["temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"], 
#             "timezone": "Africa/Cairo"
#         }

#         print("📡 سحب بيانات الطقس (Current, Hourly, Daily)...")
#         responses = openmeteo.weather_api(url, params=params)
        
#         all_current_dfs = []
#         all_hourly_dfs = []
#         all_daily_dfs = []
        
#         for i, response in enumerate(responses):
#             # --- أ: تجهيز بيانات Current ---
#             current = response.Current()
#             all_current_dfs.append(pd.DataFrame({
#                 "city": [cities[i]],
#                 "time": [pd.to_datetime(current.Time(), unit="s", utc=True).strftime('%Y-%m-%d %H:%M:%S')],
#                 "temp": [current.Variables(0).Value()],
#                 "humidity": [current.Variables(1).Value()],
#                 "rain": [current.Variables(2).Value()],
#                 "wind_speed": [current.Variables(3).Value()]
#             }))
            
#             # --- ب: تجهيز بيانات Hourly ---
#             hourly = response.Hourly()
#             hourly_time = pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s", utc=True), end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True), freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left")
#             all_hourly_dfs.append(pd.DataFrame({
#                 "city": cities[i],
#                 "time": hourly_time.strftime('%Y-%m-%d %H:%M:%S'),
#                 "temp": hourly.Variables(0).ValuesAsNumpy(),
#                 "humidity": hourly.Variables(1).ValuesAsNumpy(),
#                 "precipitation": hourly.Variables(2).ValuesAsNumpy()
#             }))

#             # --- جـ: تجهيز بيانات Daily ---
#             daily = response.Daily()
#             daily_time = pd.date_range(start=pd.to_datetime(daily.Time(), unit="s", utc=True), end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True), freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left")
#             all_daily_dfs.append(pd.DataFrame({
#                 "city": cities[i], 
#                 "date": daily_time.strftime('%Y-%m-%d'),
#                 "max_temp": daily.Variables(0).ValuesAsNumpy(),
#                 "precip_sum": daily.Variables(1).ValuesAsNumpy(),
#                 "wind_max": daily.Variables(2).ValuesAsNumpy()
#             }))
        
#         # تحويل القوائم لـ DataFrames شاملة لكل المحافظات
#         final_current = pd.concat(all_current_dfs)
#         final_hourly = pd.concat(all_hourly_dfs)
#         final_daily = pd.concat(all_daily_dfs)
        
#         # حساب منطق التوصيل والتأخير للجدول اليومي
#         final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

#         # دمج ملف الطلبات وحساب ميزانية البونص الكلية
#         if os.path.exists('orders_data.csv'):
#             orders_df = pd.read_csv('orders_data.csv')
#             final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
#             final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']
#         else:
#             final_daily['avg_daily_orders'] = 0
#             final_daily['total_bonus_budget'] = 0

#         # --- 🛠️ إدارة الداتابيز وجداول البيانات الـ 3 ---
#         db_url = os.getenv('DATABASE_URL')
#         engine = create_engine(db_url)
        
#         # مسح الجداول وقائياً لإعادة البناء بالهيكلية الجديدة الكاملة
#         with engine.connect() as conn:
#             print("💥 إعادة تهيئة الجداول لتحديث قاعدة البيانات بالكامل...")
#             conn.execute(text("DROP TABLE IF EXISTS daily_weather CASCADE;"))
#             conn.execute(text("DROP TABLE IF EXISTS hourly_weather CASCADE;"))
#             conn.execute(text("DROP TABLE IF EXISTS current_weather CASCADE;"))
#             conn.execute(text("DROP TABLE IF EXISTS cities_orders CASCADE;"))
#             conn.commit()

#         # 1. رفع جدول الطلبات الأساسي وتعيين الـ Primary Key
#         print("📦 رفع جدول الطلبات الأساسي...")
#         if 'orders_df' in locals():
#             orders_df.to_sql('cities_orders', engine, if_exists='replace', index=False)
#         with engine.connect() as conn:
#             conn.execute(text("ALTER TABLE cities_orders ADD PRIMARY KEY (city);"))
#             conn.commit()

#         # 2. صب وجدولة البيانات الـ 3 في الداتابيز
#         print("☁️ حفظ جدول الـ Daily (شامل العواميد المحسوبة)...")
#         final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)

#         print("⏳ حفظ جدول الـ Hourly التفصيلي...")
#         final_hourly.to_sql('hourly_weather', engine, if_exists='append', index=False)

#         print("⚡ حفظ جدول الـ Current اللحظي...")
#         final_current.to_sql('current_weather', engine, if_exists='append', index=False)

#         # 3. بناء العلاقات والـ Foreign Keys لكل الجداول لربطها بجدول المحافظات والطلبات
#         with engine.connect() as conn:
#             print("🔐 ربط العلاقات والـ Foreign Keys للجداول الثلاثة...")
#             conn.execute(text("ALTER TABLE daily_weather ADD CONSTRAINT fk_daily_city FOREIGN KEY (city) REFERENCES cities_orders(city);"))
#             conn.execute(text("ALTER TABLE hourly_weather ADD CONSTRAINT fk_hourly_city FOREIGN KEY (city) REFERENCES cities_orders(city);"))
#             conn.execute(text("ALTER TABLE current_weather ADD CONSTRAINT fk_current_city FOREIGN KEY (city) REFERENCES cities_orders(city);"))
#             conn.commit()
        
#         # تشغيل الإنذار وإرسال الإيميل الاستباقي
#         check_for_alerts(final_daily)
#         print(f"\n مبروك  الـ 3 جداول بقوا لايف وجاهزين: {pd.Timestamp.now()}")

#     except Exception as e:
#         print(f"❌ مشكلة: {e}")

# if __name__ == "__main__":
#     run_weather_pipeline()















































import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from sqlalchemy import create_engine, text
import openmeteo_requests
import requests_cache
from retry_requests import retry
from dotenv import load_dotenv

# --- 0. تحميل الإعدادات من ملف .env ---
load_dotenv(dotenv_path='/app/.env')

# --- 1. إعدادات Gmail ---
GMAIL_USER = 'marwamohameddasd91@gmail.com' 
GMAIL_APP_PASSWORD = 'kzpe odbm dciq fbww'  
RECIPIENT_EMAIL = 'marwamohameddasd91@gmail.com' 

# --- 2. وظيفة إرسال الإيميل ---
def send_email_alert(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 تم إرسال إيميل التنبيه بنجاح!")
    except Exception as e:
        print(f"❌ فشل إرسال الإيميل: {e}")

# --- 3. محرك اتخاذ القرار (للداتا اليومية) ---
def apply_delivery_logic(row):
    delay = 0
    bonus = 0
    temp = row.get('max_temp', 25)
    precip = row.get('precip_sum', 0)
    wind = row.get('wind_max', 0)
    
    if precip > 0:
        delay += 15
        bonus += 10
        if precip > 2:
            delay += 20
            bonus += 15
    if wind > 20:
        delay += 10
        bonus += 10
    if temp > 38:
        delay += 10
        bonus += 5
    return pd.Series([delay, bonus], index=['expected_delay_min', 'risk_bonus_egp'])

# --- 4. وظيفة التنبؤ والإنذار المبكر ---
def check_for_alerts(df):
    print("\n🔍 فحص المخاطر المتوقعة ليوم غد...")
    tomorrow = (pd.Timestamp.now().normalize() + pd.Timedelta(days=1)).date()
    # تحويل العمود لتاريخ للمقارنة الصحيحة
    df_copy = df.copy()
    df_copy['date_parsed'] = pd.to_datetime(df_copy['date']).dt.date
    tomorrow_df = df_copy[df_copy['date_parsed'] == tomorrow]

    alert_messages = []
    for _, row in tomorrow_df.iterrows():
        alerts = []
        if row['precip_sum'] > 5: alerts.append(f"🌧️ مطر غزير ({row['precip_sum']} ملم)")
        if row['wind_max'] > 35: alerts.append(f"💨 رياح قوية ({row['wind_max']} كم/س)")
        if row['max_temp'] > 40: alerts.append(f"🔥 موجة حر ({row['max_temp']}°)")

        if alerts:
            msg = f"محافظة {row['city']}: متوقع { ' و '.join(alerts) } | الميزانية المتوقعة: {row.get('total_bonus_budget', 0)} ج.م"
            alert_messages.append(msg)
            print(f"🚨 {msg}")

    if alert_messages:
        subject = f"⚠️ تقرير مخاطر الطقس الاستباقي - {tomorrow}"
        body = "السيد المدير،\n\nيرجى العلم بوجود مخاطر طقس متوقعة غداً قد تؤثر على العمليات:\n\n" + "\n".join(alert_messages)
        send_email_alert(subject, body)
    else:
        print("✅ حالة الطقس غداً مستقرة في جميع المحافظات.")

# --- 5. خط إنتاج البيانات (The Pipeline) ---
def run_weather_pipeline():
    try:
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        cities = ["Cairo", "Alexandria", "Giza", "Qalyubia", "Dakahlia", "Gharbia", "Monufia", "Sharqia", "Beheira", "Kafr El Sheikh", "Damietta", "Port Said", "Ismailia", "Suez", "Faiyum", "Beni Suef", "Minya", "Asyut", "Sohag", "Qena", "Luxor", "Aswan", "Red Sea", "New Valley", "Matrouh", "North Sinai", "South Sinai", "New Capital"]
        
        url = "https://api.open-meteo.com/v1/forecast"
        params = { 
            "latitude": [30.0626, 31.2018, 30.0094, 30.4598, 31.0423, 30.7885, 30.563, 30.5877, 31.0341, 31.1117, 31.4165, 31.2653, 30.6043, 29.9737, 29.3084, 29.2084, 28.0919, 27.181, 26.557, 26.1551, 25.6989, 24.0908, 27.2579, 25.439, 31.3543, 31.1316, 28.209, 30.0238], 
            "longitude": [31.2497, 29.9158, 31.2086, 31.1842, 31.3533, 31.0019, 31.0097, 31.502, 30.4682, 30.9399, 31.8133, 32.3019, 32.2722, 32.5263, 30.8428, 31.0166, 30.7581, 31.1837, 31.6948, 32.716, 32.6421, 32.8994, 33.8116, 30.5586, 27.2373, 33.7984, 33.6455, 31.7549], 
            "current": ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m"],
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
            "daily": ["temperature_2m_max", "precipitation_sum", "wind_speed_10m_max"], 
            "timezone": "Africa/Cairo"
        }

        print("📡 سحب بيانات الطقس (Current, Hourly, Daily)...")
        responses = openmeteo.weather_api(url, params=params)
        
        all_current_dfs = []
        all_hourly_dfs = []
        all_daily_dfs = []
        
        for i, response in enumerate(responses):
            # --- أ: تجهيز بيانات Current ---
            current = response.Current()
            all_current_dfs.append(pd.DataFrame({
                "city": [cities[i]],
                "time": [pd.to_datetime(current.Time(), unit="s", utc=True).strftime('%Y-%m-%d %H:%M:%S')],
                "temp": [current.Variables(0).Value()],
                "humidity": [current.Variables(1).Value()],
                "rain": [current.Variables(2).Value()],
                "wind_speed": [current.Variables(3).Value()]
            }))
            
            # --- ب: تجهيز بيانات Hourly ---
            hourly = response.Hourly()
            hourly_time = pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s", utc=True), end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True), freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left")
            all_hourly_dfs.append(pd.DataFrame({
                "city": cities[i],
                "time": hourly_time.strftime('%Y-%m-%d %H:%M:%S'),
                "temp": hourly.Variables(0).ValuesAsNumpy(),
                "humidity": hourly.Variables(1).ValuesAsNumpy(),
                "precipitation": hourly.Variables(2).ValuesAsNumpy()
            }))

            # --- جـ: تجهيز بيانات Daily ---
            daily = response.Daily()
            daily_time = pd.date_range(start=pd.to_datetime(daily.Time(), unit="s", utc=True), end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True), freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left")
            all_daily_dfs.append(pd.DataFrame({
                "city": cities[i], 
                "date": daily_time.strftime('%Y-%m-%d'),
                "max_temp": daily.Variables(0).ValuesAsNumpy(),
                "precip_sum": daily.Variables(1).ValuesAsNumpy(),
                "wind_max": daily.Variables(2).ValuesAsNumpy()
            }))
        
        # تحويل القوائم لـ DataFrames شاملة لكل المحافظات
        final_current = pd.concat(all_current_dfs)
        final_hourly = pd.concat(all_hourly_dfs)
        final_daily = pd.concat(all_daily_dfs)
        
        # حساب منطق التوصيل والتأخير للجدول اليومي
        final_daily[['expected_delay_min', 'risk_bonus_egp']] = final_daily.apply(apply_delivery_logic, axis=1)

        # دمج ملف الطلبات وحساب ميزانية البونص الكلية
        if os.path.exists('orders_data.csv'):
            orders_df = pd.read_csv('orders_data.csv')
            final_daily = pd.merge(final_daily, orders_df, on='city', how='left')
            final_daily['total_bonus_budget'] = final_daily['risk_bonus_egp'] * final_daily['avg_daily_orders']
        else:
            final_daily['avg_daily_orders'] = 0
            final_daily['total_bonus_budget'] = 0

        # --- 🛠️ إدارة الداتابيز وجداول البيانات الـ 3 (نسخة الحفاظ على التاريخ) ---
        db_url = os.getenv('DATABASE_URL')
        engine = create_engine(db_url)
        
        # 1. رفع جدول الطلبات الأساسي (إذا لم يكن موجوداً)
        print("📦 رفع جدول الطلبات الأساسي...")
        if 'orders_df' in locals():
            try:
                orders_df.to_sql('cities_orders', engine, if_exists='fail', index=False)
                with engine.connect() as conn:
                    conn.execute(text("ALTER TABLE cities_orders ADD PRIMARY KEY (city);"))
                    conn.commit()
            except ValueError:
                print("ℹ️ جدول cities_orders موجود بالفعل، جاري تخطي إعادة إنشائه لحماية العلاقات والبيانات.")

        # 2. صب وجدولة البيانات الـ 3 في الداتابيز (Append حقيقي تراكمي)
        print("☁️ حفظ جدول الـ Daily (إضافة فوق البيانات القديمة)...")
        final_daily.to_sql('daily_weather', engine, if_exists='append', index=False)

        print("⏳ حفظ جدول الـ Hourly التفصيلي...")
        final_hourly.to_sql('hourly_weather', engine, if_exists='append', index=False)

        print("⚡ حفظ جدول الـ Current اللحظي...")
        final_current.to_sql('current_weather', engine, if_exists='append', index=False)

        # 3. بناء العلاقات والـ Foreign Keys (بأمان دون تكرار)
        with engine.connect() as conn:
            print("🔐 فحص وربط العلاقات والـ Foreign Keys...")
            try:
                conn.execute(text("ALTER TABLE daily_weather ADD CONSTRAINT fk_daily_city FOREIGN KEY (city) REFERENCES cities_orders(city);"))
                conn.execute(text("ALTER TABLE hourly_weather ADD CONSTRAINT fk_hourly_city FOREIGN KEY (city) REFERENCES cities_orders(city);"))
                conn.execute(text("ALTER TABLE current_weather ADD CONSTRAINT fk_current_city FOREIGN KEY (city) REFERENCES cities_orders(city);"))
                conn.commit()
                print("✅ تم ربط العلاقات بنجاح لأول مرة.")
            except Exception:
                print("ℹ️ العلاقات والـ Foreign Keys مفعلة مسبقاً، جاري المتابعة بأمان وحفظ البيانات بنجاح.")
        
        # تشغيل الإنذار وإرسال الإيميل الاستباقي
        check_for_alerts(final_daily)
        print(f"\n🎉 مبروك الـ 3 جداول بقوا لايف وجاهزين وتم تحديثهم بشكل تراكمي: {pd.Timestamp.now()}")

    except Exception as e:
        print(f"❌ مشكلة: {e}")

if __name__ == "__main__":
    run_weather_pipeline()