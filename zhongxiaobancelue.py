
# def initialize(context):
#     # set_order_cost(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5),type='stock')
#     set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003,
#                             min_commission=5), type='stock')
#     # 每笔交易时的手续费是, 买入时万分之三，卖出时万分之三加千分之一印花税close_tax, 每笔交易最低扣5块钱

#     set_option('use_real_price',True)
#     #开启动态复权模式

#     g.buy_stock_count = 3

# 小盘股策略

def initialize(context):
    set_order_cost(OrderCost(close_tax=0.001 ,open_commission=0.0003 ,close_commission=0.0003,
                             min_commission=5) ,type='stock')
    # 股票类每笔交易时的手续费是：买入时open_commission佣金万分之三，卖出时close_commission佣金万分之三加千分之一印花税（close_tax）, 每笔交易佣金最低扣5块钱
    set_option('use_real_price' ,True)
    set_benchmark('000300.XSHG')

    g.buy_stock_list = 3
    g. index ='399005.XSHE'

    run_daily(buy_stock ,time='14:59')

def buy_stock(context):

    # 选择前50个小市值股票 q= query(valuation.code, valuation.circulating_market_cap).order_by(valuation.circulating_market_cap.asc()).filter(
        valuation.circulating_market_cap<100) . limit(100)

    result = get_fundamentals(q)

    stock_list = stock_filtration(list(result['code']), context)  # 获得股票列表

    # 购买股票
    # 1、先把不在列表的股票卖掉
    current_positions = context.portfolio.positions
    current_data = get_current_data()
    if len(current_positions) > 0:
        for stock in context.portfolio.positions.keys():
            if stock not in stock_list:

                if current_data[stock].last_price < current_data[stock].high_limit:
                    order_target_value(stock,0)

    # 小于目标仓位，剩下的钱就继续买股票
    # 考虑一下中小本指数在30日均线上才买进
    IPO_index = attribute_history(g.index,40, '1d', [ 'close'])
    thirty_mean = IPO_index['close'][-30:].mean()
    # print(current_data[g.index].last_price,11111111)
    if current_data[g.index].last_price > thirty_mean:
        if len(current_positions) < g.buy_stock_list:
            cash = context.portfolio.available_cash/(g. buy_stock_list-len( current_positions))
            # print(1)
            for stock in stock_list:

                if stock not in context.portfolio.positions.keys():
                    # if context.portfolio.positions[stock].total_amount ==0:
                    order_target_value(stock,cash)



                    # print(stock_list)

def \


stock_filtration(stock_list, context):
    # 过滤那些ST或者要退市，涨停跌停的股票，上市不足一年的股票

    limit_list=[]
    days_list=[]
    current_data = get_current_data()
    # 过滤ST或者退市的
    stock_filter = [stock for stock in stock_list if not
                    current_data[stock].paused and not current_data[stock].is_st and '退' not in current_data[stock]
                        .name]
    # 过滤涨跌停的
    for stock in stock_filter:
        if current_data[stock].low_limit < current_data[stock].last_price < current_data[stock].high_limit:
            limit_list.append(stock)
    # 上市不足一年的股票
    for stock in limit_list:
        days_public = (context.current_dt.date() - get_security_info(stock).start_date).days
        if days_public < 365:
            days_list.append(stock)



    return [i for i in days_list if i[0:3] == '002']  # 必须是中小板









