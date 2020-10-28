import string
import tkinter as tk
from tkinter import messagebox
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure
import basic


class Gui():
    def __init__(self, root):
        self.root = root
        tk.Label(leftFrame, text="Choose city:").grid(row=0, column=0, padx=10, pady=2)
        btncity = tk.Entry(leftFrame)
        btncity.grid(row=0,column=1,padx=3,pady=2)
        search = tk.Button(leftFrame, text ="Search",command= lambda: self.searchCity(btncity))
        search.grid(row=0,column=3,padx=3,pady=2)


    def check_input(self,city,all_countries):
        if len(city) == 0:
            messagebox.showinfo("Empty input", "Please Type the country name")
            return False
        citylower = city.lower()
        if not (citylower in all_countries):
            messagebox.showinfo("Wrong input", "Sorry there is no such country")
            return False
        return True




    def searchCity(self,btncity):
        city = btncity.get()
        api = basic.Retriever()
        all_countries =basic.Retriever.get_allcountries(api)
        if not self.check_input(city,all_countries):
            return
        city = city.capitalize()
        information = basic.Retriever.dict_country(api,city)
        self.printInfo(information)
        fivedays = tk.Button(leftFrame, text ="5 days",command= lambda: self.draw_graph(city,5))
        fivedays.grid(row=5,column=0,padx=3,pady=2)
        tendays = tk.Button(leftFrame, text ="10 days",command= lambda: self.draw_graph(city,10))
        tendays.grid(row=5,column=1,padx=3,pady=2)
        twendays = tk.Button(leftFrame, text ="20 days",command= lambda: self.draw_graph(city,20))
        twendays.grid(row=5,column=2,padx=3,pady=2)

    def printInfo(self,information):
        tk.Label(leftFrame, text="Country: %s " %(information['Country'])).grid(row=1, column=1, padx=10, pady=2)
        tk.Label(leftFrame, text="Date: %s " %(information['Date'])).grid(row=2, column=1, padx=10, pady=2)
        tk.Label(leftFrame, text="TotalConfirmed: %s " %(information['TotalConfirmed'])).grid(row=3, column=1, padx=10, pady=2)
        tk.Label(leftFrame, text="TotalDeaths: %s " %(information['TotalDeaths'])).grid(row=4, column=1, padx=10, pady=2)
        x = (information['TotalConfirmed']) - (information['TotalRecovered'])
        tk.Label(leftFrame, text="Active Cases: %s " %x).grid(row=4, column=1, padx=10, pady=2)

    def draw_graph(self,country,lastdays):
        api = basic.Retriever()
        dates,cases = basic.Retriever.get_sinceDayone(api,country)
        lastdays = -1 * lastdays
        dates = dates[lastdays:]
        cases = cases[lastdays:]
        plt.figure(figsize=(1,1))
        data = { 'Dates': dates,'Cases': cases}
        df = DataFrame(data, columns=['Dates','Cases'])
        figure = plt.Figure(figsize=(6,6), dpi=70)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, root)
        chart_type.get_tk_widget().grid(row=6,column=0,padx=0,pady=0)
        df = df[['Dates','Cases']].groupby('Dates').sum()
        df.plot(kind='line', legend=True, ax=ax)
        ax.set_title('Cases in the last %s days in %s' %(-lastdays,country))




if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Covid19 Info")
    root.geometry("500x600")
    leftFrame = tk.Frame(root, width=500, height = 600)
    leftFrame.grid(row=0, column=0, padx=0, pady=0)
    #rightframe = tk.Frame(root, width=800, height = 600)
    #rightframe.grid(row=1, column=1, padx=0, pady=0)
    gui = Gui(root)
    root.mainloop()
