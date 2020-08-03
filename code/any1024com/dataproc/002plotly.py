# coding=utf-8
import pathlib
import numpy as np
import pandas as pd
import plotly.express as px


def main():
    '''
    生成树状图
    '''
    df = px.data.gapminder().query("year == 2007")
    fig = px.treemap(df, path=['continent', 'country'], values='pop',
                     color='lifeExp', hover_data=['iso_alpha'],
                     color_continuous_scale='RdBu',
                     color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop']))
    fig.show()


def gen_report(file_path):
    comps = ['腾讯', '阿里', '百度', '京东', '美团', '小米', '字节跳动', '滴滴']
    df_dict = pd.read_excel(file_path, comps)
    for k, v in df_dict.items():
        v['投资主体'] = k
    # domain_set = set().union(* [set(df['行业']) for df in df_dict.values()])
    # df_all = pd.concat(df_dict.values())
    df_all = pd.concat(df_dict)
    df_all['海外'] = df_all['海外'].where(df_all['海外'].notnull(), '国内')
    fig = px.treemap(df_all, path=['行业', '投资主体', '日期', '公司简称'])
    fig.show()


def gen_report_all(file_path):
    df = pd.read_excel(file_path)
    # 转时间序列
    df['日期'] = pd.to_datetime(df['日期'])
    df = df.set_index('日期').to_period('A')
    df['日期'] = df.index
    # print(df)
    fig = px.treemap(df, path=['行业', '投资主体', '日期', '公司简称'])
    fig.write_html(str(file_path.parent.joinpath('all.html')))
    fig.write_image(str(file_path.parent.joinpath('all.png')), scale=20)
    fig.show()


if __name__ == "__main__":
    path = pathlib.Path(
        '~/dev/python/python1024/data/dataproc/2020internet').expanduser()
    file_path = path.joinpath('investments.xlsx')
    # gen_report(file_path)
    gen_report_all(path.joinpath('all.xlsx'))
