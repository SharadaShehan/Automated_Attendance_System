from components.MainComponent import UIApp
import os


if __name__ == "__main__":
    bin_folder = 'bin'
    if not os.path.exists(bin_folder):
        os.makedirs(bin_folder)
    app = UIApp()
    app.mainloop()
