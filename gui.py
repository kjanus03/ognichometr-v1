import PySimpleGUIWeb as sg
from Pogoda import daty, policz_punkty


def main():
    wynik = 0
    t1 = ''
    layout = [[sg.Text("Witaj w ognichometrze!", size=(30, 2), font=("Helvetica", 14))],
              [sg.Text('Wybierz dzien: ', size=(30, 4), font=("Helvetica", 14)),
               sg.Combo((daty[0], daty[1], daty[2], daty[3], daty[4]), enable_events=True, key='combo',
                        font=("Helvetica", 14))],
              [sg.Text(f"Punkty dla wybranej daty: {wynik}/1000 pkt", size=(34, 2), key='-OUTPUT-', font=("Helvetica", 16))],
              [sg.Text(f"Dane: {t1}", size=(50, 7), key='-OUTPUT2-', font=("Helvetica", 14))],
              [sg.Button("Policz punkty", font=("Helvetica", 14)), sg.Exit(font=("Helvetica", 14))]]
    sg.theme('dark grey 9')
    window = sg.Window(title="Ognichometr", layout=layout, web_multiple_instance=True, disable_close=False)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Policz punkty':
            combo = values['combo']  # use the combo key
            wynik = policz_punkty(combo)[0]
            t1 = policz_punkty(combo)[1]
            window['-OUTPUT-'].update(f"Punkty dla wybranej daty: {wynik}/1000 pkt")
            window['-OUTPUT2-'].update(f"Dane: {t1}")

    window.close()


main()
