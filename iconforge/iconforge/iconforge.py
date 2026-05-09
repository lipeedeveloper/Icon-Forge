#!/usr/bin/env python3
"""
IconForge — Google Material Icons downloader by category.
Author: Emanuel Felipe (Lipe Developer)
License: Apache 2.0
"""

import os
import sys
import json
import time
import shutil
import zipfile
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ──────────────────────────────────────────────────────────────────────────────
# SVG base URL: material-icons.github.io CDN
# ──────────────────────────────────────────────────────────────────────────────
CDN_BASE = "https://material-icons.github.io/material-icons/svg/{name}/{variant}.svg"

VARIANTS = ["baseline", "outline", "round", "sharp", "twotone"]

# ──────────────────────────────────────────────────────────────────────────────
# ICON CATALOG  (category → list of icon names)
# ──────────────────────────────────────────────────────────────────────────────
CATALOG: dict[str, list[str]] = {
    "action": [
        "accessibility","accessibility_new","account_balance","account_balance_wallet",
        "account_box","account_circle","add_shopping_cart","alarm","alarm_add","alarm_off",
        "alarm_on","all_inbox","all_out","android","announcement","aspect_ratio","assessment",
        "assignment","assignment_ind","assignment_late","assignment_return","assignment_returned",
        "assignment_turned_in","auto_fix_high","backup","book","bookmark","bookmark_border",
        "bug_report","build","build_circle","cached","calendar_today","camera_enhance",
        "card_giftcard","card_membership","card_travel","change_history","check_circle",
        "check_circle_outline","chrome_reader_mode","class","code","commute","compare_arrows",
        "contact_support","copyright","credit_card","dashboard","date_range","delete",
        "delete_forever","delete_outline","description","dns","done","done_all","done_outline",
        "donut_large","donut_small","eco","eject","event","event_seat","exit_to_app",
        "explore","explore_off","extension","face","fact_check","favorite","favorite_border",
        "feedback","filter_alt","find_in_page","find_replace","fingerprint","flight_land",
        "flight_takeoff","flip_to_back","flip_to_front","gavel","get_app","grade","group_work",
        "help","help_outline","highlight_alt","highlight_off","history","home","hourglass_empty",
        "hourglass_full","http","https","important_devices","info","input","label",
        "label_important","label_off","language","launch","leaderboard","list","lock",
        "lock_open","login","logout","loyalty","manage_search","markunread_mailbox","maximize",
        "minimize","note_add","offline_bolt","offline_pin","opacity","open_in_browser",
        "open_in_new","open_with","pageview","pan_tool","payment","pending","pending_actions",
        "perm_camera_mic","perm_contact_calendar","perm_data_setting","perm_identity",
        "perm_media","perm_phone_msg","perm_scan_wifi","pets","picture_in_picture",
        "picture_in_picture_alt","play_for_work","polymer","power_settings_new","preview",
        "print","privacy_tip","query_builder","question_answer","queue","record_voice_over",
        "redeem","remove_shopping_cart","reorder","report_problem","restore","restore_page",
        "room","rowing","schedule","search","send","settings","settings_applications",
        "settings_backup_restore","settings_bluetooth","settings_brightness","settings_cell",
        "settings_ethernet","settings_phone","settings_power","settings_voice","shop",
        "shop_two","shopping_basket","shopping_cart","source","speaker_notes","spellcheck",
        "stars","store","subject","subtitles","supervised_user_circle","swap_horiz","swap_vert",
        "system_update_alt","tab","table_view","theaters","thumb_down","thumb_up",
        "thumbs_up_down","timeline","toc","today","toll","touch_app","tour","track_changes",
        "translate","trending_down","trending_flat","trending_up","turned_in","turned_in_not",
        "update","upgrade","verified","verified_user","view_agenda","view_array","view_carousel",
        "view_column","view_day","view_headline","view_list","view_module","view_quilt",
        "view_stream","view_week","visibility","visibility_off","watch_later","work",
        "work_off","work_outline","youtube_searched_for","zoom_in","zoom_out",
    ],
    "alert": [
        "add_alert","error","error_outline","notification_important","warning","warning_amber",
    ],
    "av": [
        "4k","add_to_queue","airplay","album","art_track","av_timer","closed_caption",
        "closed_caption_disabled","closed_caption_off","equalizer","explicit","fast_forward",
        "fast_rewind","featured_play_list","featured_video","fiber_dvr","fiber_manual_record",
        "fiber_new","fiber_pin","fiber_smart_record","forward_10","forward_30","forward_5",
        "games","hd","hearing","hearing_disabled","high_quality","library_add",
        "library_add_check","library_books","library_music","loop","mic","mic_none","mic_off",
        "missed_video_call","movie","movie_creation","movie_filter","music_video","new_releases",
        "not_interested","note","pause","pause_circle_filled","pause_circle_outline",
        "play_arrow","play_circle_filled","play_circle_outline","play_disabled","queue_music",
        "queue_play_next","radio","recent_actors","remove_from_queue","repeat","repeat_on",
        "repeat_one","replay","replay_10","replay_30","replay_5","sd","shuffle","shuffle_on",
        "skip_next","skip_previous","slow_motion_video","snooze","sort_by_alpha","speed","stop",
        "stop_circle","subscriptions","surround_sound","video_call","video_label",
        "video_library","video_settings","videocam","videocam_off","videogame_asset",
        "volume_down","volume_mute","volume_off","volume_up","web","web_asset",
    ],
    "communication": [
        "alternate_email","business","call","call_end","call_made","call_merge","call_missed",
        "call_missed_outgoing","call_received","call_split","cancel_presentation","cell_wifi",
        "chat","chat_bubble","chat_bubble_outline","clear_all","comment","contact_mail",
        "contact_page","contact_phone","contacts","desktop_access_disabled","dialer_sip",
        "dialpad","document_scanner","domain_disabled","domain_verification","duo","email",
        "forum","forward_to_inbox","import_contacts","import_export","live_help",
        "location_off","location_on","mail_outline","mark_chat_read","mark_chat_unread",
        "mark_email_read","mark_email_unread","message","mobile_screen_share","nat","no_sim",
        "pause_presentation","phone","phone_disabled","phone_enabled","phonelink_erase",
        "phonelink_lock","phonelink_ring","phonelink_setup","portable_wifi_off",
        "present_to_all","print_disabled","qr_code","qr_code_2","qr_code_scanner","read_more",
        "rss_feed","screen_share","sip","stop_screen_share","stay_current_landscape",
        "stay_current_portrait","swap_calls","textsms","unsubscribe","voicemail","vpn_key",
        "wifi_calling","wifi_lock","wifi_tethering","wifi_tethering_off",
    ],
    "content": [
        "add","add_box","add_circle","add_circle_outline","add_link","archive","backspace",
        "ballot","block","bolt","calculate","clear","content_copy","content_cut",
        "content_paste","content_paste_go","content_paste_off","content_paste_search","create",
        "delete_sweep","drafts","dynamic_feed","filter_list","flag","font_download",
        "font_download_off","forward","gesture","how_to_reg","how_to_vote","inbox","insights",
        "inventory","inventory_2","link","link_off","low_priority","mail","markunread",
        "move_to_inbox","next_week","outlined_flag","push_pin","redo","remove","remove_circle",
        "remove_circle_outline","reply","reply_all","report","report_off","save","save_all",
        "save_alt","select_all","send","shield","square_foot","stream","tag","text_format",
        "unarchive","undo","waves","weekend","where_to_vote",
    ],
    "device": [
        "access_alarm","access_alarms","access_time","add_alarm","add_to_home_screen",
        "airplane_ticket","airplanemode_active","airplanemode_inactive","battery_alert",
        "battery_charging_full","battery_full","battery_saver","battery_std","battery_unknown",
        "bluetooth","bluetooth_connected","bluetooth_disabled","bluetooth_searching",
        "brightness_auto","brightness_high","brightness_low","brightness_medium","devices",
        "dvr","gps_fixed","gps_not_fixed","gps_off","graphic_eq","grid_off","grid_on",
        "location_disabled","location_searching","media_bluetooth_off","media_bluetooth_on",
        "mobile_friendly","mobile_off","mobiledata_off","mode_night","mode_standby",
        "monitor_heart","monitor_weight","nearby_error","nearby_off","network_cell",
        "network_wifi","nfc","nightlight","note_alt","notifications","notifications_active",
        "notifications_none","notifications_off","notifications_paused","password","pattern",
        "phone_android","phone_iphone","phonelink","phonelink_off","price_change","price_check",
        "remember_me","reset_tv","restart_alt","screen_lock_landscape","screen_lock_portrait",
        "screen_lock_rotation","screen_rotation","security_update","security_update_good",
        "sell","send_to_mobile","share","shortcut","signal_cellular_0_bar",
        "signal_cellular_4_bar","signal_cellular_alt","signal_cellular_nodata",
        "signal_cellular_null","signal_cellular_off","signal_wifi_0_bar","signal_wifi_4_bar",
        "signal_wifi_4_bar_lock","signal_wifi_bad","signal_wifi_off","sim_card",
        "sim_card_alert","sim_card_download","sms","sms_failed","splitscreen","storage","task",
        "thermostat","timer","timer_off","usb","usb_off","wallpaper","widgets","wifi",
        "wifi_find","wifi_off","wifi_password",
    ],
    "editor": [
        "add_chart","add_comment","align_horizontal_center","align_horizontal_left",
        "align_horizontal_right","align_vertical_bottom","align_vertical_center",
        "align_vertical_top","area_chart","attach_file","attach_money","bar_chart",
        "border_all","border_bottom","border_clear","border_color","border_horizontal",
        "border_inner","border_left","border_outer","border_right","border_style","border_top",
        "border_vertical","bubble_chart","candlestick_chart","check","checklist",
        "checklist_rtl","color_lens","drag_handle","edit","edit_attributes","edit_note",
        "edit_road","emoji_flags","emoji_food_beverage","emoji_nature","emoji_objects",
        "emoji_people","emoji_symbols","emoji_transportation","event_note","format_align_center",
        "format_align_justify","format_align_left","format_align_right","format_bold",
        "format_clear","format_color_fill","format_color_reset","format_color_text",
        "format_indent_decrease","format_indent_increase","format_italic","format_line_spacing",
        "format_list_bulleted","format_list_numbered","format_list_numbered_rtl","format_paint",
        "format_quote","format_shapes","format_size","format_strikethrough",
        "format_textdirection_l_to_r","format_textdirection_r_to_l","format_underlined",
        "functions","height","highlight","horizontal_distribute","horizontal_rule","html",
        "insert_chart","insert_chart_outlined","insert_comment","insert_drive_file",
        "insert_emoticon","insert_invitation","insert_link","insert_photo","linear_scale",
        "list","merge_type","mode","mode_comment","mode_edit","monetization_on","money_off",
        "multiline_chart","notes","numbers","pie_chart","pie_chart_outline","post_add",
        "publish","query_stats","redo","score","short_text","show_chart","space_bar",
        "stacked_line_chart","strikethrough_s","subscript","summarize","superscript",
        "table_chart","table_rows","text_decrease","text_fields","text_increase","title","toc",
        "undo","unfold_less","unfold_more","vertical_align_bottom","vertical_align_center",
        "vertical_align_top","vertical_distribute","wrap_text",
    ],
    "file": [
        "attach_email","audio_file","cloud","cloud_circle","cloud_done","cloud_download",
        "cloud_off","cloud_queue","cloud_sync","cloud_upload","create_new_folder","difference",
        "drive_file_move_outline","drive_file_rename_outline","drive_folder_upload","feed",
        "file_copy","file_download","file_download_done","file_download_off","file_open",
        "file_present","file_upload","folder","folder_copy","folder_delete","folder_off",
        "folder_open","folder_shared","folder_special","folder_zip","home_storage","note",
        "note_add","request_quote","rule_folder","snippet_folder","task","topic","upload_file",
        "video_file","workspaces",
    ],
    "hardware": [
        "browser_not_supported","cast","cast_connected","cast_for_education","computer",
        "desktop_mac","desktop_windows","developer_board","developer_board_off","device_hub",
        "device_thermostat","device_unknown","devices_other","dock","earbuds","earbuds_battery",
        "fax","gamepad","headphones","headphones_battery","headset","headset_mic","headset_off",
        "keyboard","keyboard_alt","keyboard_arrow_down","keyboard_arrow_left",
        "keyboard_arrow_right","keyboard_arrow_up","keyboard_backspace","keyboard_capslock",
        "keyboard_command_key","keyboard_control_key","keyboard_double_arrow_down",
        "keyboard_double_arrow_left","keyboard_double_arrow_right","keyboard_double_arrow_up",
        "keyboard_hide","keyboard_return","keyboard_tab","keyboard_voice","laptop",
        "laptop_chromebook","laptop_mac","laptop_windows","memory","monitor","mouse",
        "network_check","phone_android","phone_iphone","phonelink","phonelink_off",
        "point_of_sale","power","power_input","router","scanner","security","sim_card",
        "smart_display","smart_screen","smartphone","speaker","speaker_group","tablet",
        "tablet_android","tablet_mac","tv","tv_off","videogame_asset","watch",
    ],
    "home": [
        "ac_unit","air","bathroom","bed","bedroom_baby","bedroom_child","bedroom_parent",
        "blender","breakfast_dining","brunch_dining","carpenter","chair","chair_alt","chalet",
        "checkroom","cleaning_services","coffee","coffee_maker","countertops","dining",
        "door_back","door_front","door_sliding","doorbell","dry","dry_cleaning",
        "electrical_services","elevator","escalator","fence","fire_extinguisher","fireplace",
        "fitness_center","food_bank","foundation","garage","grass","handyman","hardware",
        "hot_tub","house","hvac","iron","kitchen","living","microwave","mop","night_shelter",
        "nights_stay","no_food","outlet","pool","roofing","room_preferences","room_service",
        "sensor_door","sensor_window","shower","soap","sofa","solar_power","spa","stairs",
        "storefront","tub","umbrella","villa","wash","water_damage","water_drop","window","yard",
    ],
    "image": [
        "add_a_photo","add_photo_alternate","add_to_photos","adjust","animation","assistant",
        "assistant_photo","auto_fix_high","auto_fix_normal","auto_fix_off","blur_circular",
        "blur_linear","blur_off","blur_on","brightness_1","brightness_2","brightness_3",
        "brightness_4","brightness_5","brightness_6","brightness_7","broken_image","brush",
        "burst_mode","camera","camera_alt","camera_front","camera_rear","camera_roll",
        "center_focus_strong","center_focus_weak","circle","collections",
        "collections_bookmark","color_lens","colorize","compare","contrast","control_point",
        "control_point_duplicate","crop","crop_16_9","crop_3_2","crop_5_4","crop_7_5",
        "crop_free","crop_landscape","crop_original","crop_portrait","crop_rotate","crop_square",
        "dehaze","details","edit","exposure","exposure_minus_1","exposure_minus_2",
        "exposure_plus_1","exposure_plus_2","exposure_zero","filter","filter_1","filter_2",
        "filter_3","filter_4","filter_5","filter_6","filter_7","filter_8","filter_9",
        "filter_b_and_w","filter_center_focus","filter_drama","filter_frames","filter_hdr",
        "filter_none","filter_tilt_shift","filter_vintage","flare","flash_auto","flash_off",
        "flash_on","flip","flip_camera_android","flip_camera_ios","gradient","grain","hdr_off",
        "hdr_on","hdr_strong","hdr_weak","healing","hide_image","image","image_aspect_ratio",
        "image_not_supported","image_search","landscape","leak_add","leak_remove","lens",
        "linked_camera","looks","looks_3","looks_4","looks_5","looks_6","looks_one","looks_two",
        "loupe","monochrome_photos","mountain","movie_creation","movie_filter","nature",
        "nature_people","navigate_before","navigate_next","panorama","panorama_fish_eye",
        "panorama_horizontal","panorama_photosphere","panorama_vertical","panorama_wide_angle",
        "photo","photo_album","photo_camera","photo_camera_back","photo_camera_front",
        "photo_filter","photo_library","photo_size_select_actual","photo_size_select_large",
        "photo_size_select_small","picture_as_pdf","portrait","remove_red_eye",
        "rotate_90_degrees_ccw","rotate_left","rotate_right","shutter_speed","slide_show",
        "straighten","style","switch_camera","switch_video","tag_faces","timelapse","timer",
        "timer_3","timer_off","tonality","transform","tune","wb_auto","wb_cloudy",
        "wb_incandescent","wb_shade","wb_sunny","wb_twilight",
    ],
    "maps": [
        "add_business","add_location","add_location_alt","add_road","agriculture","atm",
        "attractions","bakery_dining","beenhere","bike_scooter","breakfast_dining",
        "brunch_dining","bus_alert","car_rental","car_repair","castle","category",
        "cleaning_services","compass_calibration","delivery_dining","departure_board",
        "dinner_dining","directions","directions_bike","directions_boat","directions_bus",
        "directions_car","directions_ferry","directions_off","directions_railway",
        "directions_run","directions_subway","directions_transit","directions_walk","do_not_step",
        "do_not_touch","downhill_skiing","dry","electric_bike","electric_car","electric_moped",
        "electric_scooter","ev_station","fastfood","festival","flight","forest","fort",
        "gas_station","hail","hardware","home","hotel","icecream","kayaking","kebab_dining",
        "kitesurfing","layers","layers_clear","local_activity","local_airport","local_atm",
        "local_bar","local_cafe","local_car_wash","local_convenience_store","local_dining",
        "local_drink","local_fire_department","local_florist","local_gas_station",
        "local_grocery_store","local_hospital","local_hotel","local_laundry_service",
        "local_library","local_mall","local_movies","local_offer","local_parking",
        "local_pharmacy","local_phone","local_pizza","local_play","local_police",
        "local_post_office","local_printshop","local_see","local_shipping","local_taxi",
        "location_city","location_on","location_pin","lunch_dining","map","maps_ugc",
        "medical_services","menu_book","merge","minor_crash","miscellaneous_services","money",
        "moped","mosque","moving","museum","my_location","navigation","near_me","nightlife",
        "nordic_walking","not_listed_location","park","paragliding","pedal_bike","person_pin",
        "person_pin_circle","pest_control","pin_drop","place","ramen_dining","ramp_left",
        "ramp_right","restaurant","restaurant_menu","route","run_circle","sailing","set_meal",
        "skateboarding","sledding","snowboarding","snowmobile","snowshoeing","social_distance",
        "spa","stadium","store","straight","streetview","subway","synagogue","tapas","terrain",
        "traffic","train","tram","transfer_within_a_station","transit_enterexit","trip_origin",
        "turn_left","turn_right","turn_sharp_left","turn_sharp_right","two_wheeler","umbrella",
        "volunteer_activism","water","wine_bar","wrong_location","zoom_in_map","zoom_out_map",
    ],
    "navigation": [
        "apps","arrow_back","arrow_back_ios","arrow_back_ios_new","arrow_downward",
        "arrow_drop_down","arrow_drop_down_circle","arrow_drop_up","arrow_forward",
        "arrow_forward_ios","arrow_left","arrow_right","arrow_upward","cancel","check",
        "chevron_left","chevron_right","close","double_arrow","east","expand_less","expand_more",
        "first_page","fullscreen","fullscreen_exit","last_page","legend_toggle","menu",
        "menu_open","more_horiz","more_vert","north","north_east","north_west","refresh",
        "south","south_east","south_west","subdirectory_arrow_left","subdirectory_arrow_right",
        "switch_left","switch_right","unfold_less","unfold_more","west",
    ],
    "notification": [
        "adb","bluetooth_audio","confirmation_num","disc_full","do_disturb","do_disturb_alt",
        "do_disturb_off","do_disturb_on","do_not_disturb","do_not_disturb_alt",
        "do_not_disturb_off","do_not_disturb_on","drive_eta","enhanced_encryption",
        "event_available","event_busy","event_note","folder_special","live_tv","mms","more",
        "network_check","network_locked","no_encryption","ondemand_video","personal_video",
        "phone_bluetooth_speaker","phone_call_end","phone_forwarded","phone_in_talk",
        "phone_locked","phone_missed","phone_paused","power","power_off","priority_high",
        "running_with_errors","sd_card","sd_card_alert","sim_card_alert","sms","sms_failed",
        "support_agent","sync","sync_disabled","sync_lock","sync_problem","system_update",
        "tap_and_play","time_to_leave","unsubscribe","vibration","voice_chat","vpn_lock","wc",
        "wifi","wifi_calling_3",
    ],
    "places": [
        "airport_shuttle","all_inclusive","apartment","baby_changing_station","backpack",
        "bathtub","beach_access","bento","business_center","cabin","carpenter","casino",
        "child_care","child_friendly","corporate_fare","cottage","countertops","crib","deck",
        "domain","dry","elevator","escalator","family_restroom","fire_extinguisher",
        "fitness_center","food_bank","free_breakfast","gite","golf_course","grass",
        "holiday_village","hot_tub","hotel","house","houseboat","hvac","iron","kitchen","lock",
        "luggage","meeting_room","microwave","no_cell","no_drinks","no_flash","no_food",
        "no_meeting_room","no_photography","other_houses","pool","rice_bowl","roofing","room",
        "room_preferences","room_service","rv_hookup","smoke_free","smoking_rooms","soap","spa",
        "stairs","storefront","stroller","tapas","tub","umbrella","villa","wash","water_damage",
        "wheelchair_pickup",
    ],
    "search": [
        "document_scanner","find_in_page","find_replace","manage_search","saved_search",
        "search","search_off","youtube_searched_for",
    ],
    "social": [
        "back_hand","cake","connect_without_contact","coronavirus","cruelty_free","domain",
        "domain_add","elderly","emoji_emotions","emoji_events","emoji_flags",
        "emoji_food_beverage","emoji_nature","emoji_objects","emoji_people","emoji_symbols",
        "emoji_transportation","engineering","family_restroom","female","fence","follow_the_signs",
        "front_hand","group","group_add","group_off","groups","hail","handshake",
        "health_and_safety","hiking","king_bed","kitesurfing","male","man","masks","military_tech",
        "mood","mood_bad","nordic_walking","other_houses","outdoor_grill","pages","paragliding",
        "party_mode","people","people_alt","people_outline","person","person_add",
        "person_add_alt","person_off","person_outline","person_pin","person_remove",
        "person_search","personal_injury","poll","psychology","public","public_off",
        "real_estate_agent","recommend","recycling","reduce_capacity","reviews","safety_check",
        "sailing","school","self_improvement","sentiment_dissatisfied","sentiment_neutral",
        "sentiment_satisfied","sentiment_very_dissatisfied","sentiment_very_satisfied","share",
        "sick","single_bed","skateboarding","sledding","snowboarding","snowshoeing",
        "social_distance","sports","sports_bar","sports_baseball","sports_basketball",
        "sports_cricket","sports_esports","sports_football","sports_golf","sports_handball",
        "sports_hockey","sports_kabaddi","sports_mma","sports_motorsports","sports_rugby",
        "sports_soccer","sports_swimming","sports_tennis","sports_volleyball","star",
        "star_border","star_half","star_outline","support_agent","surfing","switch_account",
        "tag_faces","theater_comedy","thumb_down","thumb_up","thumbs_up_down","transgender",
        "travel_explore","volunteer_activism","waving_hand","whatshot","woman","workspaces",
    ],
    "toggle": [
        "check_box","check_box_outline_blank","indeterminate_check_box","radio_button_checked",
        "radio_button_unchecked","star","star_border","star_half","star_outline",
        "toggle_off","toggle_on",
    ],
    "transportation": [
        "agriculture","airport_shuttle","bike_scooter","bus_alert","car_crash","car_rental",
        "car_repair","commute","departure_board","directions_bike","directions_boat",
        "directions_bus","directions_car","directions_ferry","directions_railway",
        "directions_run","directions_subway","directions_transit","directions_walk",
        "electric_bike","electric_car","electric_moped","electric_scooter","ev_station",
        "flight","flight_class","flight_land","flight_takeoff","local_airport","local_shipping",
        "local_taxi","moped","motorcycle","multiple_stop","no_crash","no_transfer",
        "pedal_bike","sailing","subway","train","tram","transit_enterexit","trip_origin",
        "two_wheeler",
    ],
}

# ──────────────────────────────────────────────────────────────────────────────
# ANSI colours (fallback gracefully on Windows without colorama)
# ──────────────────────────────────────────────────────────────────────────────
try:
    import colorama
    colorama.init()
    _COLOR = True
except ImportError:
    _COLOR = False

def _c(code: str, text: str) -> str:
    if not _COLOR and sys.platform == "win32":
        return text
    return f"\033[{code}m{text}\033[0m"

def cyan(t):   return _c("96", t)
def green(t):  return _c("92", t)
def yellow(t): return _c("93", t)
def red(t):    return _c("91", t)
def bold(t):   return _c("1",  t)
def dim(t):    return _c("2",  t)
def magenta(t):return _c("95", t)

# ──────────────────────────────────────────────────────────────────────────────
# BANNER
# ──────────────────────────────────────────────────────────────────────────────
BANNER = r"""
██╗ ██████╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██║██╔════╝██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
██║██║     ██║   ██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║  ███╗█████╗
██║██║     ██║   ██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
██║╚██████╗╚██████╔╝██║ ╚████║██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
"""

def print_banner():
    print(cyan(BANNER))
    print(bold("  Google Material Icons Downloader"))
    print(dim("  by Emanuel Felipe (Lipe Developer)"))
    print(dim("  Apache License 2.0\n"))
    print(dim("  Source: https://material-icons.github.io\n"))


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def total_icons() -> int:
    return sum(len(v) for v in CATALOG.values())


def format_size(nbytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} GB"


def progress_bar(done: int, total: int, width: int = 30) -> str:
    filled = int(width * done / max(total, 1))
    bar = "█" * filled + "░" * (width - filled)
    pct = int(100 * done / max(total, 1))
    return f"[{cyan(bar)}] {bold(str(pct).rjust(3))}%  {dim(f'{done}/{total}')}"


def download_svg(name: str, variant: str, dest: Path) -> tuple[bool, str]:
    url = CDN_BASE.format(name=name, variant=variant)
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "IconForge/1.0 (https://github.com/lipedev/iconforge)"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                return False, f"HTTP {resp.status}"
            data = resp.read()
            if b"<svg" not in data:
                return False, "not SVG"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return True, ""
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, str(e.reason)
    except Exception as e:
        return False, str(e)


# ──────────────────────────────────────────────────────────────────────────────
# INTERACTIVE MENU
# ──────────────────────────────────────────────────────────────────────────────
def show_menu() -> tuple[list[str], list[str], str]:
    cats = list(CATALOG.keys())

    print(bold("  ╔══ CATEGORIES ═══════════════════════════╗"))
    cols = 2
    items = [f"  {yellow(str(i+1).rjust(2))}. {c.capitalize():<22}({len(CATALOG[c])} icons)"
             for i, c in enumerate(cats)]
    items.append(f"  {yellow(str(len(cats)+1).rjust(2))}. {bold('ALL CATEGORIES'):<22}({total_icons()} icons)")

    per_col = -(-len(items) // cols)
    for row in range(per_col):
        left  = items[row] if row < len(items) else ""
        right = items[row + per_col] if row + per_col < len(items) else ""
        print(f"{left:<55}{right}")
    print(bold("  ╚══════════════════════════════════════════╝\n"))

    while True:
        raw = input(f"  {cyan('▶')} Choose categories {dim('(e.g. 1,3,5 or 20 for ALL)')}:  ").strip()
        if not raw:
            continue
        chosen_cats: list[str] = []
        try:
            nums = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            print(red("  ✖  Enter numbers separated by commas.\n"))
            continue
        valid = True
        all_idx = len(cats) + 1
        for n in nums:
            if n == all_idx:
                chosen_cats = list(cats)
                break
            if 1 <= n <= len(cats):
                c = cats[n - 1]
                if c not in chosen_cats:
                    chosen_cats.append(c)
            else:
                print(red(f"  ✖  '{n}' is out of range.\n"))
                valid = False
                break
        if valid and chosen_cats:
            break

    print()
    print(bold("  ╔══ VARIANTS ══════════════════════════════╗"))
    for i, v in enumerate(VARIANTS, 1):
        print(f"  {yellow(str(i).rjust(2))}. {v}")
    print(f"  {yellow(str(len(VARIANTS)+1).rjust(2))}. {bold('ALL VARIANTS')}")
    print(bold("  ╚══════════════════════════════════════════╝\n"))

    while True:
        raw = input(f"  {cyan('▶')} Choose variants {dim('(e.g. 1 or 1,2 or 6 for ALL)')}:  ").strip()
        if not raw:
            continue
        chosen_vars: list[str] = []
        try:
            nums = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            print(red("  ✖  Enter numbers separated by commas.\n"))
            continue
        valid = True
        all_idx = len(VARIANTS) + 1
        for n in nums:
            if n == all_idx:
                chosen_vars = list(VARIANTS)
                break
            if 1 <= n <= len(VARIANTS):
                v = VARIANTS[n - 1]
                if v not in chosen_vars:
                    chosen_vars.append(v)
            else:
                print(red(f"  ✖  '{n}' is out of range.\n"))
                valid = False
                break
        if valid and chosen_vars:
            break

    print()
    dest = input(f"  {cyan('▶')} Output folder {dim('[default: ./icons]')}:  ").strip()
    if not dest:
        dest = "icons"
    return chosen_cats, chosen_vars, dest


# ──────────────────────────────────────────────────────────────────────────────
# DOWNLOAD ENGINE
# ──────────────────────────────────────────────────────────────────────────────
def build_tasks(categories: list[str], variants: list[str]) -> list[tuple[str, str, str]]:
    tasks = []
    for cat in categories:
        for name in CATALOG.get(cat, []):
            for var in variants:
                tasks.append((cat, name, var))
    return tasks


def run_downloads(tasks: list[tuple[str, str, str]], out_root: str,
                  workers: int = 8, delay: float = 0.0):
    root = Path(out_root)
    root.mkdir(parents=True, exist_ok=True)

    total = len(tasks)
    done = 0
    ok = 0
    fail = 0
    failed_list: list[str] = []

    print(f"\n  {bold('Downloading')} {cyan(str(total))} files → {yellow(str(root))}\n")

    def job(t):
        cat, name, var = t
        dest = root / cat / name / f"{var}.svg"
        if dest.exists():
            return True, ""
        if delay:
            time.sleep(delay)
        return download_svg(name, var, dest)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(job, t): t for t in tasks}
        for fut in as_completed(futures):
            cat, name, var = futures[fut]
            success, err = fut.result()
            done += 1
            if success:
                ok += 1
            else:
                fail += 1
                failed_list.append(f"{cat}/{name}/{var}: {err}")

            bar = progress_bar(done, total)
            label = green("✔") if success else red("✖")
            print(f"\r  {label}  {bar}  {dim(name):<35}", end="", flush=True)

    print(f"\n\n  {green('✔')} {bold(str(ok))} downloaded   "
          f"{red('✖') if fail else dim('✖')} {bold(str(fail))} failed\n")

    if failed_list:
        log = root / "_failed.log"
        log.write_text("\n".join(failed_list))
        print(f"  {yellow('!')} Failed list saved → {log}\n")

    return ok, fail, root


def zip_output(root: Path, categories: list[str]):
    archive = root.parent / f"iconforge_{'-'.join(categories)}.zip"
    print(f"  {cyan('→')} Creating archive {bold(archive.name)} …", end="", flush=True)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in root.rglob("*.svg"):
            zf.write(f, f.relative_to(root.parent))
    size = format_size(archive.stat().st_size)
    print(f"\r  {green('✔')} Archive ready  {bold(archive.name)}  ({size})\n")
    return archive


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────
def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="iconforge",
        description="IconForge — Download Google Material Icons by category",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python iconforge.py
  python iconforge.py --categories action navigation --variants baseline outline
  python iconforge.py --categories all --variants baseline --output ./my-icons --zip
  python iconforge.py --list
        """,
    )
    p.add_argument("--categories", "-c", nargs="+",
                   help=f"Categories to download (or 'all'). Available: {', '.join(CATALOG)}")
    p.add_argument("--variants", "-v", nargs="+", default=["baseline"],
                   help=f"Icon variants (default: baseline). Available: {', '.join(VARIANTS)}")
    p.add_argument("--output", "-o", default="icons",
                   help="Output directory (default: ./icons)")
    p.add_argument("--workers", "-w", type=int, default=8,
                   help="Parallel download threads (default: 8)")
    p.add_argument("--zip", "-z", action="store_true",
                   help="Create a .zip archive after download")
    p.add_argument("--list", "-l", action="store_true",
                   help="List all categories and exit")
    p.add_argument("--no-banner", action="store_true",
                   help="Suppress the ASCII banner")
    return p


def main():
    parser = build_argparser()
    args = parser.parse_args()

    if not args.no_banner:
        print_banner()

    # --list
    if args.list:
        print(bold("  Available categories:\n"))
        for cat, icons in CATALOG.items():
            print(f"  {cyan(cat.ljust(18))} {dim(str(len(icons)).rjust(4))} icons")
        print(f"\n  {bold('Total:')} {cyan(str(total_icons()))} icons across {len(CATALOG)} categories\n")
        print(f"  Available variants: {', '.join(yellow(v) for v in VARIANTS)}\n")
        return

    # interactive or flag-driven
    if args.categories:
        if "all" in args.categories:
            cats = list(CATALOG.keys())
        else:
            cats = []
            for c in args.categories:
                if c in CATALOG:
                    cats.append(c)
                else:
                    print(red(f"  ✖  Unknown category '{c}'. Use --list to see options."))
                    sys.exit(1)

        variants = []
        for v in args.variants:
            if v in VARIANTS:
                variants.append(v)
            else:
                print(red(f"  ✖  Unknown variant '{v}'. Available: {', '.join(VARIANTS)}"))
                sys.exit(1)
        dest = args.output
    else:
        cats, variants, dest = show_menu()

    # summary
    tasks = build_tasks(cats, variants)
    print(f"\n  {bold('Plan:')}")
    print(f"  {dim('Categories :')} {', '.join(cyan(c) for c in cats)}")
    print(f"  {dim('Variants   :')} {', '.join(yellow(v) for v in variants)}")
    print(f"  {dim('Total files:')} {bold(str(len(tasks)))}")
    print(f"  {dim('Output     :')} {yellow(dest)}\n")

    confirm = input(f"  {cyan('▶')} Proceed? {dim('[Y/n]')}:  ").strip().lower()
    if confirm in ("n", "no"):
        print(dim("  Aborted.\n"))
        return

    ok, fail, root = run_downloads(tasks, dest, workers=args.workers)

    if (args.zip or (not args.categories and
            input(f"  {cyan('▶')} Create .zip archive? {dim('[y/N]')}:  ").strip().lower() in ("y", "yes"))):
        zip_output(root, cats)

    print(f"  {green('Done!')} Icons saved to {bold(str(root))}\n")
    print(f"  {dim('Folder structure:')}")
    print(f"  {yellow(dest)}/")
    print(f"    ├── {dim('<category>')}/")
    print(f"    │     └── {dim('<icon_name>')}/")
    print(f"    │           └── {dim('<variant>.svg')}\n")
    print(dim("  by Emanuel Felipe (Lipe Developer)\n"))


if __name__ == "__main__":
    main()
