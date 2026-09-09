from flask import Flask, render_template
import folium
from folium import plugins

app = Flask(__name__)

# ข้อมูลสถานที่ท่องเที่ยว One Day Trip ในจังหวัดเชียงใหม่ (Cozy Minimalist Trip)
locations = [
    {
        "id": 1,
        "name": "อุทยานแห่งชาติออบขาน",
        "type": "อุทยานธรรมชาติ",
        "coords": [18.72530528909277, 98.82260284622211],
        "description": "หุบเขาและหน้าผาหินปูนอันงดงาม เกิดจากสายน้ำกัดเซาะมาเป็นเวลาหลายล้านปี บรรยากาศร่มรื่น เหมาะกับการพักผ่อนหย่อนใจใน,สไตล์ธรรมชาติที่เงียบสงบ",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQul9ozefSyIAqNJ_frhN_v81d78cxLTLaeLmfS99Qvvg&s=10",
        "google_maps": "https://www.google.com/maps/search/?api=1&query=18.72530528909277,98.82260284622211"
    },
    {
        "id": 2,
        "name": "อุทยานแห่งชาติขุนขาน",
        "type": "อุทยาน / ธรรมชาติ",
        "coords": [18.857965459410543, 98.62423990583265],
        "description": "สัมผัสความดิบชื้นของผืนป่าและสายหมอกยามเช้า ท่ามกลางหุบเขาที่สลับซับซ้อน อากาศเย็นสบายตลอดปี เหมาะสำหรับคนรักความสงบและธรรมชาติแท้จริง",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXjlazw1IyzLKIrs_7p8PM8XaMe_ZaU82-l5o46Yx_ZA&s=10",
        "google_maps": "https://www.google.com/maps/search/?api=1&query=18.857965459410543,98.62423990583265"
    },
    {
        "id": 3,
        "name": "นกน้อย ลานกางเต็นท์",
        "type": "จุดกางเต็นท์ / ท่องเที่ยว",
        "coords": [18.89564894179074, 98.68157480226415],
        "description": "จุดชมวิวยอดฮิตสำหรับสายแคมป์ปิ้ง ตื่นมาพบกับวิวทิวทัศน์ขุนเขาและทะเลหมอกแบบ 360 องศา บรรยากาศอบอุ่นยามคั่งคืนใต้แสงดาว",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_mPUFTyhK0GatHvniUjsT-mR1p_w5oBjn3bXn1v5jag&s",
        "google_maps": "https://www.google.com/maps/search/?api=1&query=18.89564894179074,98.68157480226415"
    },
    {
        "id": 4,
        "name": "บ้านปางยาง",
        "type": "หมู่บ้านวัฒนธรรม",
        "coords": [18.817778490730497, 98.82936645386482],
        "description": "หมู่บ้านชุมชนกลางหุบเขา เรียนรู้วิถีชีวิตที่เรียบง่าย สัมผัสความอบอุ่นและเป็นกันเองของคนในท้องถิ่นท่ามกลางธรรมชาติอันบริสุทธิ์",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTziJNVQyXP7TNE9B6HgRYFYuYagLfdo3H7WnPtOWB_A&s=10",
        "google_maps": "https://www.google.com/maps/search/?api=1&query=18.817778490730497,98.82936645386482"
    },
    {
        "id": 5,
        "name": "สวนดอยหมอกเชียงใหม่",
        "type": "จุดชมวิว / ที่ท่องเที่ยว",
        "coords": [18.80398827320955, 98.84816776437376],
        "description": "จุดพักผ่อนหย่อนใจที่มองเห็นวิวทิวเขาสลับซับซ้อนเคล้าสายหมอกบางๆ เหมาะกับการจิบกาแฟอุ่นๆ พร้อมดื่มด่ำกับบรรยากาศสุดโคซี่",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxVSjsq0PiHBRRm40eaU_XzaV-9AtGF9D0bYdEZf4sGg&s=10",
        "google_maps": "https://www.google.com/maps/search/?api=1&query=18.80398827320955,98.84816776437376"
    }
]

@app.route('/')
def index():
    # สร้างแผนที่ Folium โดยใช้พิกัดกึ่งกลางระหว่างสถานที่ทั้งหมดในเชียงใหม่
    center_lat = sum([loc["coords"][0] for loc in locations]) / len(locations)
    center_lon = sum([loc["coords"][1] for loc in locations]) / len(locations)
    
    trip_map = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=11, 
        tiles='CartoDB positron' # สไตล์แผนที่แนว Minimal สะอาดตา
    )
    
    # เก็บรายชื่อพิกัดเพื่อทำเส้นทางเชื่อมโยง (Polyline)
    route_coords = []

    for loc in locations:
        route_coords.append(loc["coords"])
        
        # ปักหมุดพร้อม Popup สไตล์มินิมอล
        popup_html = f"""
        <div style="font-family: 'Prompt', sans-serif; width: 200px; padding: 5px;">
            <h4 style="margin: 0 0 5px 0; color: #4A403A; font-size: 14px;">{loc['name']}</h4>
            <p style="margin: 0; color: #7B6E65; font-size: 12px;">{loc['type']}</p>
        </div>
        """
        
        folium.Marker(
            location=loc["coords"],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=loc["name"],
            icon=folium.Icon(color="orange", icon="leaf", prefix="fa")
        ).add_to(trip_map)

    # วาดเส้นทางเชื่อมโยงจุดท่องเที่ยวทั้งหมด (Route Line)
    folium.PolyLine(
        route_coords,
        color="#D4A373",
        weight=3,
        opacity=0.8,
        dash_array='5, 5'
    ).add_to(trip_map)

    # แปลงแผนที่เป็น HTML string เพื่อนำไปแสดงผลในหน้าเว็บ
    map_html = trip_map._repr_html_()
    
    # รวมลิงก์สำหรับปุ่ม Explore Route รวมภาพรวมจุดหมายปลายทางทั้งหมดบน Google Maps
    # (ใช้พิกัดจุดแรกหรือพิกัดกลางในการสร้าง Query รวม)
    master_google_maps_url = f"https://www.google.com/maps/dir/?api=1&destination={locations[-1]['coords'][0]},{locations[-1]['coords'][1]}"

    return render_template('index.html', locations=locations, map_html=map_html, master_maps=master_google_maps_url)

if __name__ == '__main__':
    app.run(debug=True)