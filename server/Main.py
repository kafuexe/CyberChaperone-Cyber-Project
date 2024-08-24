from UserInterface import App

if __name__ == "__main__":
    try:
        app = App()

        app.mainloop()
    except Exception as e:
        print(e)
