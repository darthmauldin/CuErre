import PySimpleGUI as sg
import qrcode

sg.theme('DarkAmber')

themes = {
    'Dark Amber': 'DarkAmber',
    'Blackity Black Black': 'Black',
    'Majority Red': 'DarkRed1'
}

hidden_status = {
    "Yes": True,
    "No": False
}


def create_window():
    wifi_tab = [
        [sg.T("SSID (Name of wifi network)")],
        [sg.In(key='-SSID-')],
        [sg.T("Is your network hidden?")],
        [sg.Combo(
            ("Yes", "No"),
            key='-H-'
        )],
        [sg.T("Wifi Password")],
        [sg.In(key='-PW-')]
    ]

    webpage_tab = [
        [sg.T("Enter website url")],
        [sg.In(key='-URL-')]
    ]

    layout = [
        [sg.Titlebar("Seder QR Coder")],
        [sg.T("Change Theme"),
         sg.Combo(
             ['Dark Amber', 'Blackity Black Black', 'Majority Red'],
             key='-TH-',
             enable_events=True)
         ],
        [sg.TabGroup([
            [sg.Tab('Wifi QR', wifi_tab), sg.Tab('Website QR', webpage_tab)]
        ])],
        [sg.Text("Choose save location folder")],
        [sg.In(key='-DIR-'), sg.FolderBrowse()],
        [sg.T("Enter a file name")],
        [sg.In(key='-F-')],
        [sg.B("Generate QR Code"), sg.Exit()]
    ]

    return sg.Window(
        "Seder CuErre",
        layout,
        enable_close_attempted_event=True,
        grab_anywhere=True,
        element_padding=12,
        icon=sg.DEFAULT_BASE64_ICON
    )


def success_popup():
    return sg.popup(
        "You made a Cu Erre code!",
        auto_close=True,
        auto_close_duration=1,
        keep_on_top=True
    )


def try_again_popup():
    return sg.popup(
        "Make sure all fields are filled",
        keep_on_top=True,
        no_titlebar=True,
        relative_location=(200, -200),
        background_color="black",
        text_color="white",
        button_color=("black", "white")
    )


def generate(vals):
    data = ''
    folder = vals['-DIR-']
    fname = vals['-F-']
    ssid = vals['-SSID-']
    url = vals['-URL-']
    hidden = hidden_status.get(vals['-H-'])
    if ssid:
        pw = vals['-PW-']
        auth_type = "WPA"
        data = f"WIFI:S:{ssid};T:{auth_type};P:{pw};H:{hidden};;"
        print(data)
    elif url:
        data = url
    qr_img = qrcode.make(data)
    qr_img.save(f'{folder}/{fname}.png')


def main():
    win = create_window()
    while True:
        event, values = win.read()
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no(
            'Do you really want to exit?',
            keep_on_top=True
        ) == 'Yes':
            break
        choice = values['-TH-']

        if event == '-TH-':
            win.close()
            del win
            sg.theme(themes.get(choice))
            win = create_window()
        if event == 'Generate QR Code':
            try:
                generate(values)
                success_popup()
            except:
                try_again_popup()
            win.close()
            del win
            sg.theme(themes.get(choice))
            win = create_window()


if __name__ == '__main__':
    main()
