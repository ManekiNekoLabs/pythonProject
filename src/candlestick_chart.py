import sys
import json
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QPen, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QChart, QChartView, QDateTimeAxis, QValueAxis


def load_data():
    with open('btc_historical_data.json', 'r') as f:
        data = json.load(f)
    return data


def main():
    app = QApplication(sys.argv)

    # Load data from JSON file
    data = load_data()

    # Create candlestick series and add data to it
    series = QCandlestickSeries()
    for d in data:
        dt = QDateTime.fromString(d['time'], 'yyyy-MM-dd HH:mm:ss')
        candlestick_set = QCandlestickSet(d['open'], d['high'], d['low'], d['close'], dt.toMSecsSinceEpoch())
        series.append(candlestick_set)

    # Create chart and add candlestick series to it
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Bitcoin Candlestick Chart")
    chart.setAnimationOptions(QChart.SeriesAnimations)

    # Customize chart axes
    axis_x = QDateTimeAxis()
    axis_x.setTickCount(10)
    axis_x.setFormat("MM/dd/yyyy")

    # set x-axis on the chart
    chart.setAxisX(axis_x)

    # create y-axis for price values
    axis_y = QValueAxis()
    axis_y.setLabelFormat("$%.2f")
    axis_y.setTickCount(10)
    axis_y.setTitleText("Price (USD)")
    # set y-axis on the chart
    chart.setAxisY(axis_y)

    # Create chart view and set the chart on it
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)

    # Create main window and set chart view as central widget
    window = QMainWindow()
    window.setCentralWidget(chart_view)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
