from termuxgui import Connection, Activity, LinearLayout, TextView
import time
import glob

print("TienVu")
def get_ram():
    mem = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":", 1)
            mem[key] = int(value.strip().split()[0])

    available = mem["MemAvailable"] / 1024
    total = mem["MemTotal"] / 1024
    return available, total


def get_temp():
    temps = []

    for path in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
        try:
            with open(path) as f:
                temp = int(f.read().strip()) / 1000
                if 0 < temp < 100:
                    temps.append(temp)
        except:
            pass

    return max(temps) if temps else None


with Connection() as conn:
    activity = Activity(conn)

    layout = LinearLayout(activity, vertical=True)

    ram_text = TextView(activity, "RAM: đang đọc...", layout)
    temp_text = TextView(activity, "Nhiệt: đang đọc...", layout)

    print("GUI đang chạy")

    while True:
        ram_free, ram_total = get_ram()
        temp = get_temp()

        ram_text.settext(
            f"RAM trống: {ram_free:.0f} MB / {ram_total:.0f} MB"
        )

        if temp:
            temp_text.settext(f"Nhiệt độ: {temp:.1f}°C")
        else:
            temp_text.settext("Nhiệt độ: không đọc được")

        time.sleep(2)
