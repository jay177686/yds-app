import flet as ft
from datetime import datetime

# 数据存储
overtime_list = []

def main(page: ft.Page):
    page.title = "加班统计"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 400
    page.window_height = 700

    # ========== 输入区域 ==========
    name_input = ft.TextField(
        label="员工姓名",
        width=200,
        autofocus=True
    )
    
    hours_input = ft.TextField(
        label="加班时长(小时)",
        width=150,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    date_input = ft.TextField(
        label="日期",
        value=datetime.now().strftime("%Y-%m-%d"),
        width=150
    )
    
    # ========== 统计显示 ==========
    total_count = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600)
    total_hours = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600)
    
    # ========== 记录列表 ==========
    records_view = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=400)
    
    # ========== 刷新界面 ==========
    def refresh_view():
        # 更新统计
        total_count.value = str(len(overtime_list))
        total_hours.value = f"{sum(r['hours'] for r in overtime_list):.1f}"
        
        # 更新列表
        records_view.controls.clear()
        if not overtime_list:
            records_view.controls.append(
                ft.Text("暂无记录", size=16, color=ft.Colors.GREY_500, italic=True)
            )
        else:
            for r in reversed(overtime_list):
                records_view.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.icons.PERSON, color=ft.Colors.BLUE_600, size=20),
                                    ft.Text(r['name'], weight=ft.FontWeight.BOLD, size=16),
                                    ft.Container(expand=True),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_size=20,
                                        icon_color=ft.Colors.RED_400,
                                        on_click=lambda e, rid=r['id']: delete_record(rid)
                                    ),
                                ]),
                                ft.Row([
                                    ft.Text(f"📅 {r['date']}", size=12, color=ft.Colors.GREY_600),
                                    ft.Text(f"⏱ {r['hours']}小时", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                                ], spacing=20),
                            ]),
                            padding=15,
                        )
                    )
                )
        page.update()
    
    # ========== 添加记录 ==========
    def add_record(e):
        name = name_input.value
        if not name:
            name_input.error_text = "请输入姓名"
            page.update()
            return
        name_input.error_text = None
        
        try:
            hours = float(hours_input.value) if hours_input.value else 0
            if hours <= 0:
                raise ValueError
        except ValueError:
            hours_input.error_text = "请输入有效时长"
            page.update()
            return
        hours_input.error_text = None
        
        overtime_list.append({
            "id": len(overtime_list) + 1,
            "name": name,
            "hours": hours,
            "date": date_input.value,
        })
        
        name_input.value = ""
        hours_input.value = ""
        date_input.value = datetime.now().strftime("%Y-%m-%d")
        
        refresh_view()
        
        page.snack_bar = ft.SnackBar(content=ft.Text("✅ 添加成功"), bgcolor=ft.Colors.GREEN_600)
        page.snack_bar.open = True
        page.update()
    
    # ========== 删除记录 ==========
    def delete_record(rid):
        global overtime_list
        overtime_list = [r for r in overtime_list if r['id'] != rid]
        refresh_view()
        page.snack_bar = ft.SnackBar(content=ft.Text("🗑 已删除"), bgcolor=ft.Colors.ORANGE_600)
        page.snack_bar.open = True
        page.update()
    
    # ========== 清空所有 ==========
    def clear_all(e):
        global overtime_list
        overtime_list.clear()
        refresh_view()
        page.snack_bar = ft.SnackBar(content=ft.Text("清空所有记录"), bgcolor=ft.Colors.RED_600)
        page.snack_bar.open = True
        page.update()
    
    # ========== 布局 ==========
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("📊 员工加班统计", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                
                # 统计卡片
                ft.Row([
                    ft.Container(
                        content=ft.Column([ft.Text("总次数", size=14, color=ft.Colors.GREY_600), total_count], spacing=0),
                        expand=True,
                        padding=15,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Column([ft.Text("总时长", size=14, color=ft.Colors.GREY_600), total_hours], spacing=0),
                        expand=True,
                        padding=15,
                        bgcolor=ft.Colors.GREEN_50,
                        border_radius=10,
                        alignment=ft.alignment.center
                    ),
                ], spacing=15),
                
                # 添加记录卡片
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("➕ 添加记录", size=16, weight=ft.FontWeight.BOLD),
                            name_input,
                            ft.Row([hours_input, date_input], spacing=10),
                            ft.ElevatedButton("添加", icon="add", on_click=add_record, expand=True),
                        ], spacing=15),
                        padding=20,
                    )
                ),
                
                # 记录列表
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("📋 记录列表", size=16, weight=ft.FontWeight.BOLD),
                                ft.TextButton("清空所有", on_click=clear_all, icon=ft.icons.DELETE, style=ft.ButtonStyle(color=ft.Colors.RED_400)),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            records_view,
                        ], spacing=15),
                        padding=20,
                    )
                ),
            ], spacing=20),
            padding=10,
        )
    )
    
    refresh_view()

ft.app(target=main)
