import string
import random
import pathlib
import numpy as np
import pandas as pd
from scipy import stats

path = pathlib.Path(
    '~/dev/python/python1024/data/dataproc/006analysis/case').expanduser()
shop_path = path.joinpath('店铺基本数据.xlsx')

# 产品列表
product_list = [f'产品{c}' for c in string.ascii_uppercase]
# 产品价格/成本列表
product_price_list = np.random.randint(12, 31, len(product_list))
product_dict = dict(zip(product_list, product_price_list))
# 付款方式
pay_p = [0.5,   0.2,    0.1,    0.06,  0.1, 0.03, 0.01]
pay_list = ['微信', '支付宝', '银行卡', '饿了么', '美团', 'POS', '现金']
# 就餐形式
dining_p = [0.4,  0.2,  0.4]
dining_list = ['堂食', '打包', '外卖']
# 折扣率
discount_p = [0.4, 0.1, 0.1, 0.2, 0.1, 0.05, 0.05]
discount_list = [1,   0.9, 0.8, 0.7, 0.6, 0.5,  0.4]
# 订单备注
comment_p = [0.7, 0.05, 0.05, 0.03, 0.02, 0.01,
             0.02, 0.02, 0.03, 0.03, 0.02, 0.02]  # 概率分布
comment_list = ['', '少糖', '加糖', '少冰', '去冰',
                '加冰', '加奶', '无奶', '少珍珠', '多珍珠', '去柠檬', '加柠檬']
# 订单明细，主要是单品，有部分2品、3品、4品、5品，分布概率
productn_p = [0.8, 0.1, 0.06, 0.02, 0.02]


def init_shops(n_shop=100):
    """
    初始化基础数据
    :param n_shop: 默认初始化100个门店
    :return : df_shop, DataFrame
    """
    shop_list = [f'SP{i:04d}' for i in range(n_shop)]
    # 每个门店有[800~15000)个用户
    shop_user_size = np.random.randint(800, 15000, n_shop)
    # 门店x的用户范围：shop_user_list[x-1] ~ shop_user_list[x]，初始值0
    shop_user_list = shop_user_size.cumsum()
    # 各门店用户ID起点，用户默认从小到大编号
    shop_user_start = np.insert(shop_user_list[:-1], 0, 0)
    # 各门店产品清单，每个门店[5,26)个产品
    shop_product_list = [np.sort(np.random.choice(
        product_list, np.random.randint(5, 26))) for i in range(n_shop)]
    # 门店成立时间
    shop_start_dates = np.random.choice(pd.period_range(
        '2015-01-01', '2018-12-31', freq='M'), size=n_shop)
    # 生成门店基本数据表
    df_shop = pd.DataFrame({'门店ID': shop_list,
                            '成立时间': shop_start_dates,
                            '用户规模': shop_user_size,
                            '用户起点ID': shop_user_start,
                            '产品': shop_product_list})
    return df_shop


def init_orders(shop):
    """
    开始生成订单
    shop: Series
    :return (df_order, df_order_x), DataFrame
    """
    df_order_all = []
    df_order_x_all = []
    # 门店所有用户
    user_list = np.arange(shop['用户起点ID'], shop['用户起点ID']+shop['用户规模'])
    for day in pd.date_range(shop['成立时间'].to_timestamp('D', 'start'), '2020-06-30', freq='D'):
        # 每天随机生成96~1440个订单，随机分布在其用户群中
        # TODO: 老用户在部分门店需要按某个比例淘汰，概率分布更准确
        # freq从40S到600S随机
        time_freq = np.random.randint(40, 601)
        # 营业时间从上午6点到晚上10点
        ot_list = pd.date_range(start=day+pd.Timedelta('6H'),
                                end=day+pd.Timedelta('22H'),
                                freq=f'{time_freq}S')
        # 当天订单ID列表
        n_order = ot_list.size  # 当天订单量
        order_id_list = ot_list.to_series().apply(
            lambda x: f'{shop["门店ID"]}X{x.timestamp():.0f}')
        order_id_list.index = np.arange(n_order)
        # 用户二项概率分布
        user_p = stats.binom.pmf(np.arange(user_list.size), n_order, p=0.5)
        order_user = np.random.choice(user_list, p=user_p, size=n_order)
        # 计算每个订单有多少个产品
        order_product_nlist = np.random.choice(
            np.arange(1, 6), p=productn_p, size=n_order)
        # 生成当日订单明细表
        x_order_prod = np.random.choice(
            shop['产品'], size=order_product_nlist.sum())
        x_orderid = order_id_list.loc[order_id_list.index.repeat(
            order_product_nlist)]
        x_order_prodn = np.random.choice(
            [1, 2, 3], size=order_product_nlist.sum())
        df_order_x = pd.DataFrame({'订单ID': x_orderid,
                                   '产品': x_order_prod,
                                   '数量': x_order_prodn})
        df_order_x['单价'] = pd.Series(x_order_prod).map(
            lambda x: product_dict[x])
        # Bug: product_dict[x['产品']]不一定能获取到正确单价?
        # df_order_x['原价'] = df_order_x.apply(
        #     lambda x: x['数量'] * product_dict[x['产品']], axis=1)
        df_order_x['原价'] = df_order_x['数量']*df_order_x['单价']
        # 生成当日订单
        df_order = pd.DataFrame({'门店ID': [shop['门店ID']]*n_order,
                                 '订单ID': order_id_list,
                                 '用户ID': pd.Series(order_user).map(lambda x: f'U{x:08d}'),
                                 '订单日期': ot_list,
                                 '折扣': np.random.choice(discount_list, size=n_order, p=discount_p),
                                 '付款方式': np.random.choice(pay_list, size=n_order, p=pay_p),
                                 '就餐形式': np.random.choice(dining_list, size=n_order, p=dining_p),
                                 '订单备注': np.random.choice(comment_list, size=n_order, p=comment_p)},
                                index=np.arange(n_order))
        # 更新订单，原价、实付
        df_order = df_order.merge(df_order_x.groupby('订单ID')[
                                  '原价'].sum(), on='订单ID')
        df_order['实付'] = df_order['原价'] * df_order['折扣']
        df_order_all.append(df_order)
        df_order_x_all.append(df_order_x)

    df_all = pd.concat(df_order_all, ignore_index=True)
    df_all_x = pd.concat(df_order_x_all, ignore_index=True)
    return df_all, df_all_x


if __name__ == "__main__":
    df_shop = init_shops()
    # 导出数据保存生成的门店基本信息
    df_shop.to_excel(shop_path)
    for idx, shop in df_shop.iterrows():
        if idx <= 34:
            continue
        print(f'Gen for index {idx}...')
        order, order_x = init_orders(shop)
        order_path = path.joinpath(f'{shop["门店ID"]}.xlsx')
        orderx_path = path.joinpath(f'{shop["门店ID"]}_X.xlsx')
        order.to_excel(order_path)
        order_x.to_excel(orderx_path)
