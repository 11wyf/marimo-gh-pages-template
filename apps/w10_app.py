import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import marimo as mo
    # mo.notebook_location() 能自动获取当前环境下的正确路径
    data_path = mo.notebook_location() / "public" / "market_returns.csv"
    df=pd.read_csv(data_path,parse_dates=['date']) #指定 date 列转为 pandas 时间格式
    df.head()
    return (df,)


@app.cell
def _():
    import marimo as mo
    # 调用 marimo 的用户界面（UI）库，创建一个滑块。
    # 定义这个滑块控件，范围是 2 到 60 个月，默认值是 20
    window_slider = mo.ui.slider(start=2, stop=60, value=20, label="滑动窗口 (月): ")

    # 显示这个滑块（在 marimo 中，最后一行只写变量名就会显示控件）
    window_slider

    # 创建资产选择下拉菜单
    asset_selector=mo.ui.dropdown(
        options=["asset_a", "asset_b", "asset_c"],
        value="asset_a",
        label='选择资产'
    )
    asset_selector,window_slider
    return asset_selector, window_slider


@app.cell
def _(asset_selector, df, window_slider):
    # 计算选中的资产的滚动波动率
    vol_series = df.set_index('date')[asset_selector.value].rolling(window=window_slider.value).std()


    return (vol_series,)


@app.cell
def _(asset_selector, vol_series, window_slider):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 4))
    # 画折线图：X轴是时间（索引），Y轴是波动率
    ax.plot(vol_series.index, vol_series, color='blue', label=f"{asset_selector.value} Rolling Volatility")

    ax.set_title(f"{asset_selector.value} Rolling Volatility (Window={window_slider.value})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    ax.legend()

    # 为了美观，自动调整日期标签的角度
    fig.autofmt_xdate()
    fig,window_slider,asset_selector
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
