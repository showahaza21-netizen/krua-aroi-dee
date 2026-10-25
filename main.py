import flet as ft

def main(page: ft.Page):
    page.title = "ร้านครัวอร่อยดี"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F4F7F5"
    page.padding = 20
    page.window.width = 1200
    page.window.height = 850
    page.window.min_width = 850
    page.window.min_height = 600

    GREEN = "#087F5B"
    DARK = "#18352D"
    MUTED = "#687A73"

    # 1. รายการอาหารทั้งหมด (เพิ่มเมนูแนะนำเครปพริกเผาหมูหยองไส้กรอก)
    foods = [
        {
            "id": 1,
            "name": "เคบับ (เลือกเนื้อสัตว์และตัวเลือกเสริม)",
            "price": 60,
            "category": "เคบับ",
            "emoji": "🌯",
            "image": "assets/kabab.jpg",
            "has_options": True,
            "type": "kebab"
        },
        {
            "id": 2,
            "name": "เครปญี่ปุ่น (เลือกแป้ง ไส้ และซอส)",
            "price": 40,
            "category": "เครปญี่ปุ่น",
            "emoji": "🥞",
            "image": "assets/เครป.jpg",
            "has_options": True,
            "type": "crepe"
        },
        {
            "id": 5,
            "name": "เครปพริกเผาหมูหยองไส้กรอก",
            "price": 45,
            "category": "เครปญี่ปุ่น",
            "emoji": "🔥",
            "image": "assets/เครป.jpg",
            "has_options": False
        },
        {
            "id": 3,
            "name": "ขนมโตเกียว (เลือกไส้และขนาด เล็ก/ใหญ่)",
            "price": 12,
            "category": "โตเกียว",
            "emoji": "🍢",
            "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500",
            "has_options": True,
            "type": "tokyo"
        },
    ]

    cart = {}
    search_query = ""
    selected_category = "ทั้งหมด"

    cart_items_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    total_price_text = ft.Text("0 บาท", size=20, weight=ft.FontWeight.BOLD, color=GREEN)

    def update_cart_ui():
        cart_items_column.controls.clear()
        total_price = 0

        if not cart:
            cart_items_column.controls.append(
                ft.Container(
                    padding=20,
                    content=ft.Text("ยังไม่มีสินค้าในตะกร้า", color=MUTED, italic=True)
                )
            )
        else:
            for cart_key, item in cart.items():
                item_total = item["price"] * item["quantity"]
                total_price += item_total

                row = ft.Row([
                    ft.Text(f"{item['name']}\n{item['details']}", expand=True, size=11, weight=ft.FontWeight.BOLD, color=DARK),
                    ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_size=16, icon_color="#E03131", on_click=lambda e, k=cart_key: decrease_cart_item(k)),
                    ft.Text(f"{item['quantity']}", size=12, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.ADD_CIRCLE_OUTLINE, icon_size=16, icon_color=GREEN, on_click=lambda e, k=cart_key: increase_cart_item(k)),
                    ft.Text(f"{item_total} ฿", size=12, weight=ft.FontWeight.BOLD, color=DARK),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

                cart_items_column.controls.append(row)

        total_price_text.value = f"{total_price} บาท"
        page.update()

    def add_to_cart_custom(item_name, base_price, details):
        cart_key = f"{item_name}_{details}"
        if cart_key in cart:
            cart[cart_key]["quantity"] += 1
        else:
            cart[cart_key] = {
                "name": item_name,
                "price": base_price,
                "quantity": 1,
                "details": details
            }
        update_cart_ui()

    def increase_cart_item(cart_key):
        if cart_key in cart:
            cart[cart_key]["quantity"] += 1
            update_cart_ui()

    def decrease_cart_item(cart_key):
        if cart_key in cart:
            cart[cart_key]["quantity"] -= 1
            if cart[cart_key]["quantity"] <= 0:
                del cart[cart_key]
            update_cart_ui()

    # --- ฟังก์ชันเปิดหน้าต่างเลือกเคบับ ---
    def open_kebab_modal(food):
        meat_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="ไก่", label="ไก่ (60฿)"),
                ft.Radio(value="ไส้กรอก", label="ไส้กรอก (60฿)"),
                ft.Radio(value="ปูอัด", label="ปูอัด (60฿)"),
                ft.Radio(value="แฮม", label="แฮม (60฿)"),
                ft.Radio(value="เบค่อน", label="เบค่อน (60฿)"),
            ]),
            value="ไก่"
        )
        no_veg_checkbox = ft.Checkbox(label="ไม่ใส่ผัก (+10฿)", value=False)
        cheese_dropdown = ft.Dropdown(
            label="เพิ่มชีส (เลเวลละ 20฿)",
            value="0",
            options=[
                ft.dropdown.Option("0", "ไม่เพิ่มชีส"),
                ft.dropdown.Option("1", "ชีส 1 เลเวล (+20฿)"),
                ft.dropdown.Option("2", "ชีส 2 เลเวล (+40฿)"),
                ft.dropdown.Option("3", "ชีส 3 เลเวล (+60฿)"),
            ],
            width=250
        )

        def close_modal(e):
            dlg.open = False
            page.update()

        def confirm_modal(e):
            base_price = 60
            selected_meat = meat_radio.value
            
            options_desc = []
            if no_veg_checkbox.value:
                base_price += 10
                options_desc.append("ไม่ใส่ผัก (+10฿)")

            cheese_level = int(cheese_dropdown.value)
            if cheese_level > 0:
                base_price += (cheese_level * 20)
                options_desc.append(f"เพิ่มชีส {cheese_level} เลเวล (+{cheese_level * 20}฿)")

            details = f"เนื้อ: {selected_meat} | {', '.join(options_desc) if options_desc else 'ปกติ'}"
            add_to_cart_custom("เคบับ", base_price, details)
            dlg.open = False
            page.update()

        modal_content = ft.Container(
            width=450, height=400, padding=10,
            content=ft.Column([
                ft.Text("🍗 เลือกเนื้อสัตว์ (ราคา 60 บาท):", weight=ft.FontWeight.BOLD, color=GREEN),
                meat_radio,
                ft.Divider(),
                ft.Text("🧀 ตัวเลือกเสริม:", weight=ft.FontWeight.BOLD, color=GREEN),
                no_veg_checkbox,
                ft.Container(height=10),
                cheese_dropdown
            ], scroll=ft.ScrollMode.AUTO)
        )

        dlg = ft.AlertDialog(title=ft.Text("📝 สั่งทำเมนู: เคบับ", size=18, weight=ft.FontWeight.BOLD, color=DARK), content=modal_content, actions=[ft.TextButton("ยกเลิก", on_click=close_modal), ft.Button(content="ยืนยันเพิ่มลงตะกร้า", color=ft.Colors.WHITE, bgcolor=GREEN, on_click=confirm_modal)])
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # --- ฟังก์ชันเปิดหน้าต่างเลือกเครป ---
    def open_crepe_modal(food):
        batter_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="แป้งนม", label="แป้งนม (+20฿)"),
                ft.Radio(value="แป้งชาโคล", label="แป้งชาโคล (+20฿)"),
                ft.Radio(value="แป้งโนริสาหร่าย", label="แป้งโนริสาหร่าย (+20฿)"),
            ]),
            value="แป้งนม"
        )
        jams = {
            "แยมช็อกโกแลต": ft.Checkbox(label="แยมช็อกโกแลต (+5฿)", value=False),
            "แยมวนิลา": ft.Checkbox(label="แยมวนิลา (+5฿)", value=False),
            "แยมใบเตย": ft.Checkbox(label="แยมใบเตย (+5฿)", value=False),
            "แยมสตอเบอร์รี่": ft.Checkbox(label="แยมสตอเบอร์รี่ (+5฿)", value=False),
            "แยมบลูเบอร์รี่": ft.Checkbox(label="แยมบลูเบอร์รี่ (+5฿)", value=False),
        }
        savory_items = ["พริกเผา", "ซอสพิซซ่า", "ไส้กรอก", "ปูอัด", "แฮม", "หมูหยอง", "หมูสับ", "ไข่ไก่", "สาหร่ายเส้น", "ไข่กุ้ง", "ยำสาหร่าย", "ชีส"]
        savory_controls = {}
        for item in savory_items:
            savory_controls[item] = ft.RadioGroup(content=ft.Row([ft.Radio(value="ไม่ใส่", label="ไม่ใส่"), ft.Radio(value="ธรรมดา", label="ธรรมดา"), ft.Radio(value="พิเศษ", label="พิเศษ")]), value="ไม่ใส่")

        sweet_items = ["โอวัลตินครันชี่", "บราวนี่", "นูเทล่า", "เนยถั่ว", "ช็อกโกแลตเฟอร์เช่", "ฝอยทอง", "เม็ดมะม่วง", "กล้วยหอม", "โอวัลตินเฟลก", "โอริโอ้บด", "ลูกเกด", "เยลลี่", "ซีเรียล", "คอนเฟลก", "เม็ดช็อกโกแลต", "เม็ดสายรุ้ง", "มาชเมลโล่"]
        sweet_controls = {}
        for item in sweet_items:
            sweet_controls[item] = ft.RadioGroup(content=ft.Row([ft.Radio(value="ไม่ใส่", label="ไม่ใส่"), ft.Radio(value="ธรรมดา", label="ธรรมดา"), ft.Radio(value="พิเศษ", label="พิเศษ")]), value="ไม่ใส่")

        free_sauces = {
            "ซอสช็อกโกแลต": ft.Checkbox(label="ช็อกโกแลต", value=False),
            "ซอสสตอเบอร์รี่": ft.Checkbox(label="สตอเบอร์รี่", value=False),
            "นมข้น": ft.Checkbox(label="นมข้น", value=False),
            "ซอสชีส": ft.Checkbox(label="ซอสชีส", value=False),
            "ซอสพริก": ft.Checkbox(label="พริก", value=False),
            "ซอสมะเขือเทศ": ft.Checkbox(label="มะเขือเทศ", value=False),
            "มายองเนส": ft.Checkbox(label="มายองเนส", value=False),
            "พริกไทย": ft.Checkbox(label="พริกไทย", value=False),
            "แม็กกี้": ft.Checkbox(label="แม็กกี้", value=False),
        }

        def close_modal(e):
            dlg.open = False
            page.update()

        def confirm_modal(e):
            extra_price = 20
            selected_batter = batter_radio.value
            chosen_jams = [j_name for j_name, chk in jams.items() if chk.value]
            extra_price += len(chosen_jams) * 5

            chosen_savory = []
            for name, rg in savory_controls.items():
                val = rg.value
                if val != "ไม่ใส่":
                    chosen_savory.append(f"{name}({val})")
                    if name in ["พริกเผา", "ซอสพิซซ่า"]: extra_price += 5
                    elif name in ["ไส้กรอก", "ปูอัด"]: extra_price += 5 if val == "ธรรมดา" else 10
                    elif name in ["แฮม", "หมูหยอง", "หมูสับ", "ไข่ไก่", "สาหร่ายเส้น"]: extra_price += 10 if val == "ธรรมดา" else 15
                    elif name in ["ไข่กุ้ง", "ยำสาหร่าย", "ชีส"]: extra_price += 15 if val == "ธรรมดา" else 30

            chosen_sweet = []
            for name, rg in sweet_controls.items():
                val = rg.value
                if val != "ไม่ใส่":
                    chosen_sweet.append(f"{name}({val})")
                    if name in ["โอวัลตินครันชี่"]: extra_price += 20 if val == "ธรรมดา" else 30
                    elif name in ["บราวนี่", "นูเทล่า"]: extra_price += 15 if val == "ธรรมดา" else (30 if name=="บราวนี่" else 20)
                    elif name in ["เนยถั่ว", "ช็อกโกแลตเฟอร์เช่", "ฝอยทอง", "เม็ดมะม่วง", "กล้วยหอม", "โอวัลตินเฟลก", "โอริโอ้บด"]: extra_price += 10 if val == "ธรรมดา" else (20 if "เฟลก" in name or "โอริโอ้" in name or "ช็อกโกแลตเฟอร์เช่" in name else 15)
                    elif name in ["ลูกเกด", "เยลลี่", "ซีเรียล", "คอนเฟลก", "เม็ดช็อกโกแลต", "เม็ดสายรุ้ง", "มาชเมลโล่"]: extra_price += 5 if val == "ธรรมดา" else 10

            chosen_sauces = [s_name for s_name, chk in free_sauces.items() if chk.value]
            details = f"[{selected_batter}] | แยม: {', '.join(chosen_jams) if chosen_jams else '-'} | คาว: {', '.join(chosen_savory) if chosen_savory else '-'} | หวาน: {', '.join(chosen_sweet) if chosen_sweet else '-'} | ซอส: {', '.join(chosen_sauces) if chosen_sauces else '-'}"
            add_to_cart_custom(food["name"], extra_price, details)
            dlg.open = False
            page.update()

        modal_content = ft.Container(
            width=580, height=500, padding=10,
            content=ft.Column([
                ft.Text("🥞 เลือกแป้งเครป:", weight=ft.FontWeight.BOLD, color=GREEN),
                batter_radio, ft.Divider(),
                ft.Text("🍓 เลือกไส้แยม (+5฿):", weight=ft.FontWeight.BOLD, color=GREEN),
                ft.Column(list(jams.values())), ft.Divider(),
                ft.Text("🥓 เลือกไส้คาว:", weight=ft.FontWeight.BOLD, color=GREEN),
                ft.Column([ft.Row([ft.Text(item, width=130, weight=ft.FontWeight.W_500), savory_controls[item]], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) for item in savory_items]),
                ft.Divider(),
                ft.Text("🍫 เลือกไส้หวาน:", weight=ft.FontWeight.BOLD, color=GREEN),
                ft.Column([ft.Row([ft.Text(item, width=130, weight=ft.FontWeight.W_500), sweet_controls[item]], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) for item in sweet_items]),
                ft.Divider(),
                ft.Text("🧴 เลือกซอสฟรี:", weight=ft.FontWeight.BOLD, color=GREEN),
                ft.Column(list(free_sauces.values())),
            ], scroll=ft.ScrollMode.AUTO)
        )

        dlg = ft.AlertDialog(title=ft.Text(f"📝 สั่งทำเมนู: {food['name']}", size=18, weight=ft.FontWeight.BOLD, color=DARK), content=modal_content, actions=[ft.TextButton("ยกเลิก", on_click=close_modal), ft.Button(content="ยืนยันเพิ่มลงตะกร้า", color=ft.Colors.WHITE, bgcolor=GREEN, on_click=confirm_modal)])
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # --- ฟังก์ชันเปิดหน้าต่างเลือกขนมโตเกียว ---
    def open_tokyo_modal(food):
        tokyo_items = {
            "คัสตาร์ดครีม": {"small": 12, "large": 20},
            "คัสตาร์ด+ฝอยทอง": {"small": 15, "large": 20},
            "คัสตาร์ด+เยลลี่": {"small": 15, "large": 25},
            "นูเทล่า": {"small": 15, "large": 30},
            "นูเทล่า+เยลลี่": {"small": 15, "large": 30},
            "นูเทล่า+กล้วย": {"small": 15, "large": 35},
            "นูเทล่า+ฝอยทอง": {"small": 15, "large": 35},
            "นูเทล่า+บราวนี่": {"small": 20, "large": 40},
            "นูเทล่า+กล้วย+ฝอยทอง": {"small": 20, "large": 40},
            "นูเทล่า+เม็ดมะม่วง": {"small": 20, "large": 40},
            "เนยถั่ว": {"small": 12, "large": 20},
            "เนยถั่ว+ฝอยทอง": {"small": 15, "large": 30},
            "เนยถั่ว+กล้วย": {"small": 15, "large": 30},
            "เนยถั่ว+เยลลี่": {"small": 15, "large": 30},
            "เนยถั่ว+เม็ดมะม่วง": {"small": 15, "large": 30},
            "ไข่+หมูสับ": {"small": 12, "large": 20},
            "ไข่+ปูอัด": {"small": 12, "large": 20},
            "ไข่+แฮม": {"small": 15, "large": 30},
            "ปูอัด+หมูสับ": {"small": 12, "large": 20},
            "ไส้กรอก+หมูสับ": {"small": 15, "large": 30},
            "แฮม+หมูสับ": {"small": 15, "large": 30},
            "ไข่+ไส้กรอก+หมูสับ": {"small": 15, "large": 30},
            "ไข่+ปูอัด+หมูสับ": {"small": 15, "large": 30},
            "ไข่+แฮม+หมูสับ": {"small": 15, "large": 30},
            "พิซซ่า+ปูอัด": {"small": 15, "large": 30},
            "พิซซ่า+แฮม": {"small": 15, "large": 30},
            "พิซซ่า+ไส้กรอก": {"small": 15, "large": 30},
            "พิซซ่า+ไข่": {"small": 12, "large": 20},
            "พิซซ่า+ปูอัด+ชีส": {"small": 20, "large": 40},
            "พิซซ่า+แฮม+ชีส": {"small": 20, "large": 40},
            "พิซซ่า+ไส้กรอก+ชีส": {"small": 20, "large": 40},
            "พิซซ่า+ไข่+ชีส": {"small": 20, "large": 40},
            "พริกเผา+ไส้กรอก": {"small": 12, "large": 25},
            "พริกเผา+ปูอัด": {"small": 12, "large": 25},
            "พริกเผา+ไข่": {"small": 12, "large": 30},
            "พริกเผา+แฮม": {"small": 12, "large": 30},
            "พริกเผา+หมูหยอง": {"small": 15, "large": 30},
            "พริกเผา+หมูหยอง+ไส้กรอก": {"small": 20, "large": 30},
            "พริกเผา+หมูหยอง+ปูอัด": {"small": 20, "large": 30},
            "พริกเผา+หมูหยอง+แฮม": {"small": 20, "large": 30},
            "พริกเผา+ไข่+หมูหยอง": {"small": 20, "large": 35},
            "พริกเผา+ไข่+ไส้กรอก": {"small": 20, "large": 35},
            "พริกเผา+ไข่+ปูอัด": {"small": 20, "large": 35},
            "พริกเผา+ไข่+แฮม": {"small": 20, "large": 35},
            "แฮม+ชีส": {"small": 15, "large": 35},
            "ไส้กรอก+ชีส": {"small": 15, "large": 35},
            "ปูอัด+ชีส": {"small": 15, "large": 35},
            "ไข่+ไส้กรอก+ชีส": {"small": 20, "large": 40},
            "ไข่+ปูอัด+ชีส": {"small": 20, "large": 40},
            "ไข่+แฮม+ชีส": {"small": 20, "large": 40},
        }

        tokyo_controls = {}
        for name, prices in tokyo_items.items():
            tokyo_controls[name] = ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="ไม่สั่ง", label="ไม่สั่ง"),
                    ft.Radio(value="เล็ก", label=f"เล็ก ({prices['small']}฿)"),
                    ft.Radio(value="ใหญ่", label=f"ใหญ่ ({prices['large']}฿)"),
                ], spacing=10),
                value="ไม่สั่ง"
            )

        def close_modal(e):
            dlg.open = False
            page.update()

        def confirm_modal(e):
            selected_items = []
            total_tokyo_price = 0

            for name, rg in tokyo_controls.items():
                val = rg.value
                if val != "ไม่สั่ง":
                    price = tokyo_items[name]["small"] if val == "เล็ก" else tokyo_items[name]["large"]
                    selected_items.append(f"{name} ({val} - {price}฿)")
                    total_tokyo_price += price

            if not selected_items:
                page.snack_bar = ft.SnackBar(ft.Text("กรุณาเลือกไส้ขนมโตเกียวอย่างน้อย 1 ไส้"))
                page.snack_bar.open = True
                page.update()
                return

            details = f"ไส้: {', '.join(selected_items)}"
            add_to_cart_custom(food["name"], total_tokyo_price, details)
            dlg.open = False
            page.update()

        modal_content = ft.Container(
            width=620, height=500, padding=10,
            content=ft.Column([
                ft.Text("🍢 เลือกไส้ขนมโตเกียวและขนาด (เล็ก / ใหญ่):", weight=ft.FontWeight.BOLD, color=GREEN),
                ft.Divider(),
                ft.Column([
                    ft.Row([
                        ft.Text(name, width=180, weight=ft.FontWeight.W_500, size=13),
                        tokyo_controls[name]
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    for name in tokyo_items.keys()
                ], spacing=10)
            ], scroll=ft.ScrollMode.AUTO)
        )

        dlg = ft.AlertDialog(title=ft.Text(f"📝 สั่งทำเมนู: {food['name']}", size=18, weight=ft.FontWeight.BOLD, color=DARK), content=modal_content, actions=[ft.TextButton("ยกเลิก", on_click=close_modal), ft.Button(content="ยืนยันเพิ่มลงตะกร้า", color=ft.Colors.WHITE, bgcolor=GREEN, on_click=confirm_modal)])
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def handle_food_click(food):
        if food.get("has_options"):
            if food.get("type") == "kebab":
                open_kebab_modal(food)
            elif food.get("type") == "crepe":
                open_crepe_modal(food)
            elif food.get("type") == "tokyo":
                open_tokyo_modal(food)
        else:
            add_to_cart_custom(food["name"], food["price"], "ปกติ")

    # --- ส่วน UI รายการอาหาร ---
    food_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=240,
        child_aspect_ratio=0.72,
        spacing=15,
        run_spacing=15,
    )

    def update_food_list():
        food_grid.controls.clear()
        for food in foods:
            matches_search = search_query.lower() in food["name"].lower()
            matches_category = (selected_category == "ทั้งหมด" or food["category"] == selected_category)

            if matches_search and matches_category:
                card_content = ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Image(
                                src=food["image"],
                                width=200,
                                height=110,
                                fit="cover",
                                border_radius=8,
                            ),
                            ft.Row([
                                ft.Text(food["emoji"], size=16),
                                ft.Text(food["name"], weight=ft.FontWeight.BOLD, color=DARK, size=12),
                            ], alignment=ft.MainAxisAlignment.START),
                            ft.Text(f"ราคาเริ่มต้น: {food['price']} บาท", color=MUTED, size=11),
                            ft.Container(height=5),
                            ft.Button(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.ADD_SHOPPING_CART, size=16, color=ft.Colors.WHITE),
                                    ft.Text("เลือก/สั่งซื้อ", color=ft.Colors.WHITE, size=12)
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                bgcolor=GREEN,
                                on_click=lambda e, f=food: handle_food_click(f)
                            )
                        ], spacing=4)
                    )
                )
                food_grid.controls.append(card_content)
        page.update()

    def on_search_change(e):
        nonlocal search_query
        search_query = e.control.value
        update_food_list()

    def filter_category(category):
        nonlocal selected_category
        selected_category = category
        update_food_list()

    search_field = ft.TextField(
        label="ค้นหาเมนูอาหาร...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=on_search_change,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        height=48,
    )

    categories = ["ทั้งหมด", "เคบับ", "เครปญี่ปุ่น", "โตเกียว"]
    category_buttons = ft.Row(
        [
            ft.Button(
                content=cat,
                color=ft.Colors.WHITE if cat == selected_category else DARK,
                bgcolor=GREEN if cat == selected_category else ft.Colors.WHITE,
                on_click=lambda e, c=cat: filter_category(c),
            ) for cat in categories
        ],
        spacing=8,
    )

    left_side = ft.Column([
        ft.Text("🍽️ ร้านครัวอร่อยดี", size=24, weight=ft.FontWeight.BOLD, color=DARK),
        search_field,
        category_buttons,
        ft.Divider(),
        food_grid
    ], expand=True)

    right_side = ft.Container(
        width=340,
        padding=15,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.SHOPPING_BAG, color=DARK),
                ft.Text("ตะกร้าสินค้า", size=18, weight=ft.FontWeight.BOLD, color=DARK),
            ]),
            ft.Divider(),
            cart_items_column,
            ft.Divider(),
            ft.Row([
                ft.Text("ราคารวมทั้งหมด:", size=14, weight=ft.FontWeight.BOLD, color=DARK),
                total_price_text,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=10),
            ft.Button(
                content="ชำระเงิน / ยืนยันออเดอร์",
                color=ft.Colors.WHITE,
                bgcolor=GREEN,
                width=300,
                on_click=lambda e: print("สั่งซื้อสำเร็จ!")
            )
        ])
    )

    update_food_list()
    update_cart_ui()

    page.add(
        ft.Row([left_side, right_side], expand=True, spacing=20)
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8501, host="0.0.0.0")