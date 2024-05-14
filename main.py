from imports import *

ctk.set_appearance_mode("dark")


def get_films():
    cinema_url = "https://liniakino.com/showtimes/cherry/"
    try:
        driver.get(cinema_url)
        showtime_list = driver.find_element(By.CLASS_NAME, "showtimes").find_element(By.CLASS_NAME, "showtimes-list").find_elements(By.CLASS_NAME, "showtime-movie")
        with open('movies.csv', "w", newline='', encoding='utf-8') as file:
            header = ['movie_title', 'movie_url', 'movie_session1', 'movie_session2', 'movie_session3']
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            for showtime_movie_data in showtime_list:
                showtime_movie_url = showtime_movie_data.find_element(By.CLASS_NAME, "poster").find_element(By.TAG_NAME, "a").get_attribute("href")
                showtime_movie_title = showtime_movie_data.find_element(By.TAG_NAME, "h1").find_element(By.TAG_NAME, "a").text
                showtime_movie_session_list = []
                showtime_time_list = showtime_movie_data.find_elements(By.CSS_SELECTOR, "[class*='day-block']")
                showtime_time_day_times = showtime_time_list[0].find_element(By.CLASS_NAME, "showtime-theater").find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
                for day_time in showtime_time_day_times:
                    exact_time = day_time.find_element(By.TAG_NAME, "a").text
                    showtime_movie_session_list.append(exact_time)
                try:
                    showtime_movie_session1 = showtime_movie_session_list[0]
                except IndexError:
                    showtime_movie_session1 = ""

                try:
                    showtime_movie_session2 = showtime_movie_session_list[1]
                except IndexError:
                    showtime_movie_session2 = ""

                try:
                    showtime_movie_session3 = showtime_movie_session_list[2]
                except IndexError:
                    showtime_movie_session3 = ""

                writer.writerow({'movie_title': showtime_movie_title,
                                'movie_url': showtime_movie_url,
                                'movie_session1': showtime_movie_session1,
                                'movie_session2': showtime_movie_session2,
                                'movie_session3': showtime_movie_session3})
    finally:
        driver.close()
        driver.quit()


def run_app():
    root = ctk.CTk()
    root.title("Розклад фільмів")
    root.iconbitmap('root_icon.ico')
    root.geometry("1500x600")
    root.resizable(False, False)

    menu = CTkTitleMenu(master=root)
    menu.add_cascade("Відвідати офіційний сайт", postcommand=lambda: webbrowser.open("https://liniakino.com/showtimes/cherry/"))
    menu.add_cascade("Про нас", postcommand=lambda: webbrowser.open("https://github.com/Vladislavus1"))

    label_text = ctk.CTkLabel(master=root, text="Розклад фільмів на сьогодні", font=('System', 24), fg_color='black', corner_radius=15)
    label_text.place(relx=0.5, rely=0.075, anchor=ctk.CENTER)
    try:
        get_films()

        success_label = ctk.CTkLabel(master=root, text_color='white', fg_color='dark green', text=f'Усі фільми успішно записані у файл "movies.csv"', corner_radius=15, font=('System', 24))
        success_label.place(relx=0.5, rely=0.925, anchor=ctk.CENTER)

        values = []

        with open('movies.csv', encoding='utf-8') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                values.append(row)

        values = values[1:]
        values.insert(0, ["Назва фільму", "Посиланя на фільм", "Сеанс №1", "Сеанс №2", "Сеанс №3"])

        table = CTkTable(master=root, row=len(values), column=5, values=values, header_color="black", hover_color="gray", color_phase='horizontal')
        table.pack(fill="both", padx=30, pady=70)

        def hide_label(event):
            success_label.place_forget()

        success_label.bind("<Button-1>", hide_label)
    except Exception as e:
        print(e)
        label_text = ctk.CTkLabel(master=root, text="Сталася помилка під час збору інформації про наявні кіно-сесії.\nБудь ласка спробуйте ще раз пізніше.", font=('System', 26), corner_radius=15, fg_color="red")
        label_text.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    root.mainloop()


if __name__ == "__main__":
    run_app()
